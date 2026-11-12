// The conversation with the server, ported unchanged from the old single-page front end:
// live call over WS /ws/call (streaming STT/TTS with barge-in), else tap-to-record or typed lines over POST /turn.
// The browser holds the case between turns; the server treats it as untrusted (flow.clean_case).

export type Msg = { role: "bot" | "you" | "err"; text?: string; key?: "greet" | "ready" | "e_net" | "e_mic" | "e_drop" };
export type Result = { verdict: string; checklist: string[]; complaint: string; bank_email: string };
export type Case = Record<string, any>;
type Call = { ws: WebSocket; ctx: AudioContext; stream: MediaStream; playEnd: number; srcs: Set<AudioBufferSourceNode>;
  drop: boolean; held: ArrayBuffer[]; loud: number };
type Rec = { stream: MediaStream; ctx: AudioContext; node: ScriptProcessorNode; chunks: Float32Array[]; tick: number; timer: number };

// The AudioWorklet downsamples the mic to 16 kHz and posts 512-sample (1,024-byte) frames.
const WORKLET = `registerProcessor("down16k", class extends AudioWorkletProcessor {
  constructor() { super(); this.step = sampleRate / 16000; this.pos = 0; this.acc = 0; this.n = 0; this.out = new Int16Array(512); this.i = 0; }
  process([input]) {
    for (const s of input[0] || []) {
      this.acc += s; this.n++;
      if (++this.pos >= this.step) {  // average each window: a cheap low-pass before decimating
        this.pos -= this.step;
        this.out[this.i++] = Math.max(-1, Math.min(1, this.acc / this.n)) * 0x7fff; this.acc = 0; this.n = 0;
        if (this.i === 512) { this.port.postMessage(this.out.buffer, [this.out.buffer]); this.out = new Int16Array(512); this.i = 0; }
      }
    }
    return true;
  }
});`;
// Barge-in: BARGE_FRAMES loud frames in a row while the agent talks = the caller is talking over it.
const BARGE_RMS = 0.03, BARGE_FRAMES = 6, HOLD = 10;  // ponytail: fixed energy gate (echo-cancelled mic); tune on real phones

export class Conversation {
  msgs: Msg[] = [{ role: "bot", key: "greet" }];
  caseData: Case;
  history = "";
  label = "idle";          // a strings key ("idle", "listening"…) or literal text such as the recording timer
  live = false;            // live call or recording in progress
  busy = false;
  result: Result | null = null;
  timings: Record<string, number> | null = null;
  private past: { caseData: Case; history: string; msgs: Msg[]; result: Result | null }[] = [];  // one per answered turn
  private call: Call | null = null;
  private rec: Rec | null = null;
  private noLive = false;
  private lang: string;
  private onChange: () => void;

  constructor(lang: string, onChange: () => void, seed: Case = {}) {
    this.lang = lang; this.onChange = onChange;
    this.caseData = { language: lang, ...seed };
  }
  private emit() { this.onChange(); }
  // Hindi and English go to auto-detect, which handles Hinglish; a regional choice locks STT to it
  // (in the eval, auto-detect identified only 65% of regional statements, against 100% when locked).
  private callLang() { return ["hi", "en"].includes(this.lang) ? "" : this.lang; }
  private say(m: Msg) { this.msgs = [...this.msgs, m]; this.emit(); }

  setLang(lang: string) {
    this.lang = lang; this.caseData = { ...this.caseData, language: lang };
    if (this.call) this.endCall();  // the speech model is chosen when the call connects; tap the mic again
    this.emit();
  }

  get canUndo() { return this.past.length > 0 && !this.busy; }
  // "Go back one step": restore the case as it was before the last answer. A live call is hung up, because the
  // server holds its own copy of the case; the next mic tap sends the restored one in its init message.
  undo() {
    const prev = this.past.pop();
    if (!prev || this.busy) return;
    if (this.call) this.endCall();
    Object.assign(this, prev);
    this.emit();
  }

  private show(j: any) {
    this.past.push({ caseData: this.caseData, history: this.history, msgs: this.msgs, result: this.result });
    this.caseData = j.case; this.history += " " + j.transcript;
    this.msgs = [...this.msgs, { role: "you", text: j.transcript }, ...(j.question ? [{ role: "bot" as const, text: j.question }] : [])];
    if (j.checklist) {
      this.msgs.push({ role: "bot", key: "ready" });
      this.result = { verdict: j.verdict || "", checklist: j.checklist, complaint: j.complaint, bank_email: j.bank_email };
    }
    this.emit();
  }

  // Fallback: one recorded clip or typed line per POST /turn.
  private async send(fd: FormData) {
    fd.append("case", JSON.stringify(this.caseData)); fd.append("history", this.history); fd.append("lang", this.callLang());
    this.busy = true; this.label = "working"; this.emit();
    try {
      const r = await fetch("/turn", { method: "POST", body: fd });
      const j = await r.json();
      this.busy = false; this.label = "idle";
      if (!r.ok) return this.say({ role: "err", text: String(j.detail) });
      this.show(j);
      if (j.audio) new Audio("data:audio/wav;base64," + j.audio).play().catch(() => {});
    } catch {
      this.busy = false; this.label = "idle"; this.say({ role: "err", key: "e_net" });
    }
  }

  sendText(text: string) {
    const v = text.trim();
    if (!v || this.busy) return;
    if (this.call) { this.stopPlayback(this.call); this.call.ws.send(JSON.stringify({ type: "text", text: v })); return; }
    const fd = new FormData(); fd.append("text", v); this.send(fd);
  }

  async toggleMic() {
    if (this.call) return this.endCall();
    if (this.rec) return this.stopRec();
    if (!this.noLive) {
      try { return await this.startCall(); }
      catch (e: any) { if (e?.name === "NotAllowedError") return this.say({ role: "err", key: "e_mic" }); this.noLive = true; }  // fall back to tap-to-record
    }
    this.startRec().catch(() => this.say({ role: "err", key: "e_mic" }));
  }

  private async startCall() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
    const lock = this.callLang();
    const ws = new WebSocket((location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws/call" + (lock ? "?lang=" + lock : ""));
    ws.binaryType = "arraybuffer";
    try {
      await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = ws.onclose = fail; setTimeout(fail, 3000); });
      const ctx = new AudioContext();
      await ctx.audioWorklet.addModule(URL.createObjectURL(new Blob([WORKLET], { type: "text/javascript" })));
      const node = new AudioWorkletNode(ctx, "down16k"), silence = new ArrayBuffer(1024);
      const c: Call = { ws, ctx, stream, playEnd: 0, srcs: new Set(), drop: false, held: [], loud: 0 };
      ctx.createMediaStreamSource(stream).connect(node); node.connect(ctx.destination);  // node outputs silence; keeps it pulled
      node.port.onmessage = e => { if (ws.readyState === 1) ws.send(this.gate(c, e.data) ? e.data : silence); };
      ws.onmessage = e => typeof e.data === "string" ? this.onMsg(JSON.parse(e.data)) : this.play(e.data);
      ws.onclose = () => { if (this.call === c) { this.endCall(); this.say({ role: "err", key: "e_drop" }); } };
      ws.send(JSON.stringify({ type: "init", case: this.caseData, history: this.history }));
      this.call = c;
    } catch {
      stream.getTracks().forEach(t => t.stop()); ws.close();
      throw new Error("live call unavailable");
    }
    this.live = true; this.setState("listening");
  }

  endCall() {
    const c = this.call;
    if (!c) return;
    this.call = null;
    c.stream.getTracks().forEach(t => t.stop()); c.ctx.close(); if (c.ws.readyState < 2) c.ws.close();
    this.live = false; this.label = "idle"; this.emit();
  }

  private setState(s: string) {
    if (!this.call) return;
    const left = this.call.playEnd - this.call.ctx.currentTime;
    if (s === "listening" && left > 0) { setTimeout(() => this.setState(s), left * 1000); return; }  // still playing the reply
    this.label = s; this.emit();
  }

  private onMsg(j: any) {
    if (j.type === "turn") { if (this.call) this.call.drop = false; this.show(j); }
    else if (j.type === "state") this.setState(j.state);
    else if (j.type === "timings") { this.timings = j.ms; this.emit(); }
    else if (j.type === "error") { this.say({ role: "err", text: String(j.message) }); if (j.fallback) this.noLive = true; }
  }

  // While the agent talks, STT gets silence (so it never transcribes its own voice) and each mic frame is checked
  // for loudness. On barge-in: stop playback, cancel the reply, and send STT the held frames so the first word isn't lost.
  private gate(c: Call, buf: ArrayBuffer) {
    if (c.ctx.currentTime >= c.playEnd + 0.3) { c.loud = 0; c.held = []; return true; }  // not speaking: pass through
    const pcm = new Int16Array(buf);
    const rms = Math.sqrt(pcm.reduce((a, v) => a + v * v, 0) / pcm.length) / 0x8000;
    c.held.push(buf); if (c.held.length > HOLD) c.held.shift();
    c.loud = rms > BARGE_RMS ? c.loud + 1 : 0;
    if (c.loud < BARGE_FRAMES) return false;
    this.stopPlayback(c);
    c.ws.send(JSON.stringify({ type: "barge_in" }));
    c.held.slice(0, -1).forEach(b => c.ws.send(b)); c.held = []; c.loud = 0;
    this.setState("hearing");
    return true;
  }
  private stopPlayback(c: Call) {
    c.srcs.forEach(s => { try { s.stop(); } catch { /* already ended */ } }); c.srcs.clear();
    c.playEnd = 0; c.drop = true;  // drop audio still in flight from the cancelled reply, until the next turn
  }
  private play(buf: ArrayBuffer) {
    const c = this.call;
    if (!c || c.drop) return;
    const f = Float32Array.from(new Int16Array(buf), v => v / 0x8000);
    const b = c.ctx.createBuffer(1, f.length, 16000); b.copyToChannel(f, 0);
    const src = c.ctx.createBufferSource(); src.buffer = b; src.connect(c.ctx.destination);
    const at = Math.max(c.ctx.currentTime + 0.05, c.playEnd);  // queue right after the previous chunk: no gaps
    src.start(at); c.playEnd = at + b.duration;
    c.srcs.add(src); src.onended = () => c.srcs.delete(src);
  }

  // Tap-to-record: 16 kHz mono WAV (Prisma REST takes <=30 s; we stop at 25 s).
  private async startRec() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const ctx = new AudioContext(), src = ctx.createMediaStreamSource(stream);
    const node = ctx.createScriptProcessor(4096, 1, 1), chunks: Float32Array[] = [];
    node.onaudioprocess = e => chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
    src.connect(node); node.connect(ctx.destination);
    const t0 = Date.now();
    const tick = window.setInterval(() => { this.label = "⏺ " + Math.round((Date.now() - t0) / 1000) + "s"; this.emit(); }, 250);
    this.rec = { stream, ctx, node, chunks, tick, timer: window.setTimeout(() => this.stopRec(), 25000) };
    this.live = true; this.emit();
  }
  private stopRec(send = true) {
    const r = this.rec;
    if (!r) return;
    this.rec = null; clearTimeout(r.timer); clearInterval(r.tick);
    r.node.disconnect(); r.stream.getTracks().forEach(t => t.stop()); r.ctx.close();
    this.live = false; this.label = "idle"; this.emit();
    if (send) { const fd = new FormData(); fd.append("audio", toWav(r.chunks, r.ctx.sampleRate), "speech.wav"); this.send(fd); }
  }

  destroy() { this.endCall(); this.stopRec(false); }
}

function toWav(chunks: Float32Array[], rate: number) {
  const all = new Float32Array(chunks.reduce((n, c) => n + c.length, 0)); let o = 0;
  for (const c of chunks) { all.set(c, o); o += c.length; }
  const step = rate / 16000, n = Math.floor(all.length / step), buf = new DataView(new ArrayBuffer(44 + n * 2));
  const str = (p: number, s: string) => [...s].forEach((ch, i) => buf.setUint8(p + i, ch.charCodeAt(0)));
  str(0, "RIFF"); buf.setUint32(4, 36 + n * 2, true); str(8, "WAVEfmt "); buf.setUint32(16, 16, true);
  buf.setUint16(20, 1, true); buf.setUint16(22, 1, true); buf.setUint32(24, 16000, true); buf.setUint32(28, 32000, true);
  buf.setUint16(32, 2, true); buf.setUint16(34, 16, true); str(36, "data"); buf.setUint32(40, n * 2, true);
  for (let i = 0; i < n; i++) { const s = Math.max(-1, Math.min(1, all[Math.floor(i * step)])); buf.setInt16(44 + i * 2, s * 0x7fff, true); }
  return new Blob([buf], { type: "audio/wav" });
}
