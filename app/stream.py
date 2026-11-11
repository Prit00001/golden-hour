"""Live call over one WebSocket: browser mic -> Gnani streaming STT -> flow -> Gnani SSE TTS -> browser.

Browser -> server: binary 1,024-byte frames (512 samples of 16 kHz s16le mono = 32 ms),
  or JSON {"type": "text", "text"} for typed input, {"type": "init", "case", "history"} to resume,
  {"type": "barge_in"} when the caller talks over the agent (the browser has already stopped playback).
Server -> browser: JSON {"type": "state" | "turn" | "timings" | "error"} and binary 16 kHz s16le audio.
Gnani's server-side VAD decides when an utterance ends, so there is no local VAD.
Nothing is stored: the case lives in this connection and is gone when it closes.
"""
import asyncio
import json
import re
import threading
import time

import websockets
from fastapi import WebSocket

from app import flow, gnani
from app.llm import env

STT_URL = "wss://api.vachana.ai/stt/v3/stream"
SILENCE_MS = 600  # pause that ends an utterance; lower is snappier but cuts off slow speakers


def sentences(text: str) -> list:
    """Split a reply so sentence 1 can play while the rest are still being synthesised."""
    return [s for s in re.split(r"(?<=[।?!.])\s+", text.strip()) if s]


def _synth(parts, lang, q, loop, stop):
    """Thread: stream each sentence's PCM into an asyncio queue, in order; None marks the end.

    One request at a time: parallel requests on one key get throttled (measured: 3.7 s first byte, then 429s),
    and Timbre runs faster than real time, so sentence 2 is ready before sentence 1 finishes playing."""
    put = lambda x: loop.call_soon_threadsafe(q.put_nowait, x)  # noqa: E731
    try:
        for text in parts:
            for chunk in gnani.tts_stream(text, lang):
                if stop.is_set():
                    return
                put(chunk)
        put(None)
    except Exception as e:
        put(e)


class Call:
    def __init__(self, ws: WebSocket):
        self.ws, self.case, self.history = ws, flow.new_case(), ""
        self.reply = None  # the reply task currently speaking

    async def send(self, **msg):
        await self.ws.send_json(msg)

    def start(self, said: str, marks: dict, lang_hint=None):
        if self.reply and not self.reply.done():
            self.reply.cancel()  # a newer utterance supersedes the old reply
        self.reply = asyncio.create_task(self.respond(said, marks, lang_hint))

    def barge_in(self):
        """Caller spoke over the reply: stop synthesising and sending it. Their speech becomes the next turn."""
        if self.reply and not self.reply.done():
            self.reply.cancel()
            print("[barge_in] reply cancelled")

    def greet(self):
        """Spoken greeting + disclaimer at call start. Also opens the TTS connection, so turn 1 isn't cold."""
        lg = flow.lang(self.case)
        self.reply = asyncio.create_task(self.speak(flow.GREETING[lg], {"speech_end": time.monotonic()}, lg))

    async def respond(self, said: str, marks: dict, lang_hint=None):
        out, speak = flow.advance(self.case, self.history, said, lang_hint=lang_hint)
        self.case, self.history = out["case"], self.history + " " + said
        marks["extract_done"] = time.monotonic()
        await self.send(type="turn", **out)
        await self.speak(speak, marks, flow.lang(self.case))

    async def speak(self, text: str, marks: dict, lang: str):
        await self.send(type="state", state="speaking")
        loop, stop, q = asyncio.get_running_loop(), threading.Event(), asyncio.Queue()
        threading.Thread(target=_synth, args=(sentences(text), lang, q, loop, stop), daemon=True).start()
        try:
            odd = b""  # carry a stray byte so every frame holds whole 16-bit samples
            while (chunk := await q.get()) is not None:
                if isinstance(chunk, Exception):
                    raise chunk
                marks.setdefault("first_tts_byte", time.monotonic())
                buf = odd + chunk
                cut = len(buf) - len(buf) % 2
                chunk, odd = buf[:cut], buf[cut:]
                if chunk:
                    await self.ws.send_bytes(chunk)
                    marks.setdefault("first_audio_sent", time.monotonic())
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.send(type="error", message=f"Voice unavailable, reply is on screen ({type(e).__name__}).")
        finally:
            stop.set()
        marks["audio_done"] = time.monotonic()
        base = marks["speech_end"]
        ms = {k: round((v - base) * 1000) for k, v in marks.items() if k != "speech_end"}
        print(f"[timings] {json.dumps(ms)}")  # timings only; transcripts are never logged
        await self.send(type="timings", ms=ms)
        await self.send(type="state", state="listening")


async def run(ws: WebSocket):
    await ws.accept()
    call = Call(ws)
    # ?lang=kn locks STT and replies to the caller's chosen language: auto-detect mishears short regional replies
    # ("ஆமாம்" came back as Devanagari "आमाम"). No choice = indic-auto.
    chosen = ws.query_params.get("lang")
    chosen = chosen if chosen in flow.QUESTIONS else None
    headers = {"x-api-key-id": env().get("GNANI_API_KEY", ""),
               "language_code": f"{chosen}-IN" if chosen else "indic-auto",
               "model": "prisma-v3.0", "format": "transcribe", "x-sample-rate": "16000",
               "x-min-silence-ms": str(SILENCE_MS), "x-idle-timeout-sec": "300",
               # HTTP headers must be ASCII (websockets>=16 enforces it): \uXXXX escapes, same JSON once parsed.
               "keyterms": json.dumps(gnani.KEYTERMS), "topic": gnani.TOPIC}
    try:
        stt = await websockets.connect(STT_URL, additional_headers=headers, open_timeout=10)
    except Exception as e:
        await call.send(type="error", fallback=True, message=f"Live speech unavailable ({type(e).__name__}), "
                                                             "switching to tap-to-record.")
        await ws.close()
        return

    async def up():  # browser -> Gnani
        while True:
            m = await ws.receive()
            if m["type"] == "websocket.disconnect":
                return
            if m.get("bytes"):
                await stt.send(m["bytes"])
            elif m.get("text"):
                j = json.loads(m["text"])
                if j.get("type") == "init":
                    call.case, call.history = {**flow.new_case(), **(j.get("case") or {})}, j.get("history", "")
                    if chosen:
                        call.case["language"] = chosen
                    if not call.history.strip():
                        call.greet()
                elif j.get("type") == "barge_in":
                    call.barge_in()
                elif j.get("type") == "text" and j.get("text", "").strip():
                    now = time.monotonic()
                    call.start(j["text"].strip(), {"speech_end": now, "stt_done": now})

    async def down():  # Gnani -> browser
        async for raw in stt:
            m = json.loads(raw)
            if m["type"] == "speech_start":
                await call.send(type="state", state="hearing")
            elif m["type"] == "transcript" and m.get("text", "").strip():
                now = time.monotonic()
                # No end-of-speech event arrives, so estimate it: VAD silence wait + Gnani's reported latency.
                end = now - (SILENCE_MS + m.get("latency", 0)) / 1000
                call.start(m["text"].strip(), {"speech_end": end, "stt_done": now}, m.get("detected_language_code"))
            elif m["type"] == "error":
                await call.send(type="error", message=m.get("message", "Speech error"))

    tasks = [asyncio.create_task(up()), asyncio.create_task(down())]
    try:
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for t in tasks + ([call.reply] if call.reply else []):
            t.cancel()
        await stt.close()
