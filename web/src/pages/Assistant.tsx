import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Check, ExternalLink, Landmark, ListChecks, Mail, MessageCircle, Mic, Phone, RotateCcw, Send, Share2, ShieldCheck, Square, Undo2, Users } from "lucide-react";
import { useEffect, useReducer, useRef, useState, type FormEvent, type ReactNode, type Ref } from "react";
import { Link, useSearchParams } from "react-router";
import CopyButton from "../components/CopyButton";
import EvidenceChecklist from "../components/EvidenceChecklist";
import { LANGS, useI18n } from "../i18n/I18n";
import { Conversation, type Case } from "../lib/conversation";
import { CATEGORIES } from "../lib/data";

const KEYS = ["amount", "datetime", "payment_mode", "txn_id", "scammer_contact", "bank", "scam_type"];
const IST = { timeZone: "Asia/Kolkata" } as const;
const fmt = (c: Case, k: string, v: any) => k === "amount" ? "₹" + Number(v).toLocaleString("en-IN")
  : k === "datetime" && c.fraud_ts != null ? new Date(c.fraud_ts * 1000).toLocaleString("en-IN",
      { ...IST, day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }) + " (" + v + ")"
  : String(v);

export default function Assistant() {
  const { lang, setLang, t, tl } = useI18n();
  const [params] = useSearchParams();
  const cat = CATEGORIES.findIndex(c => c.id === params.get("category"));
  const [, force] = useReducer(x => x + 1, 0);
  const make = () => new Conversation(lang, force, cat >= 0 ? CATEGORIES[cat].seed : {});
  const conv = useRef<Conversation | null>(null);
  if (!conv.current) conv.current = make();
  const c = conv.current;
  const [text, setText] = useState("");
  const [hud, setHud] = useState(false);
  const log = useRef<HTMLDivElement>(null), plan = useRef<HTMLElement>(null);

  useEffect(() => () => conv.current?.destroy(), []);
  useEffect(() => { conv.current?.setLang(lang); }, [lang]);
  useEffect(() => { log.current?.scrollTo({ top: log.current.scrollHeight, behavior: "smooth" }); }, [c.msgs.length, c.busy]);
  useEffect(() => { if (c.result) plan.current?.scrollIntoView({ behavior: "smooth", block: "start" }); }, [c.result]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === "`" && !(e.target instanceof HTMLInputElement)) setHud(h => !h); };
    addEventListener("keydown", k); return () => removeEventListener("keydown", k);
  }, []);

  const submit = (e: FormEvent) => { e.preventDefault(); c.sendText(text); setText(""); };
  const restart = () => { c.destroy(); conv.current = make(); setText(""); force(); };
  const label = (["idle", "listening", "hearing", "speaking", "working"] as const).find(k => k === c.label);
  const filled = KEYS.filter(k => c.caseData[k] != null).length;
  const fields = tl("fields");

  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-10 md:px-8 md:pt-14">
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div>
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .6 }}>
            <h1 className="text-[clamp(2.2rem,5vw,3.75rem)] font-extrabold leading-[1.03] tracking-[-.035em]">{t("a_h")}</h1>
            <p className="mt-4 max-w-2xl text-[17px] leading-relaxed text-stone">{t("a_p")}</p>
          </motion.div>

          <div className="mt-6 flex flex-wrap items-center gap-2" role="group" aria-label={t("a_lang")}>
            {LANGS.map(l => (
              <button key={l.code} onClick={() => setLang(l.code)} aria-pressed={lang === l.code}
                className={`rounded-full border px-4 py-2 text-[15px] transition ${lang === l.code ? "border-ink bg-ink text-ivory" : "border-line hover:border-ink/30"}`}>
                {l.native}
              </button>
            ))}
            {cat >= 0 && <span className="ml-1 rounded-full bg-mint px-3.5 py-2 text-[14px] font-medium text-forest">{t("a_topic")}: {tl("cat_t")[cat]}</span>}
          </div>

          <section className="card mt-6 overflow-hidden">
            <div ref={log} className="flex h-[21vh] min-h-[130px] flex-col md:h-[min(52vh,520px)] gap-3 overflow-y-auto p-5 md:p-6" aria-live="polite">
              <AnimatePresence initial={false}>
                {c.msgs.map((m, k) => (
                  <motion.div key={k} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .25 }}
                    className={`max-w-[85%] whitespace-pre-wrap break-words rounded-[20px] px-4 py-3 text-[16px] leading-relaxed ${
                      m.role === "you" ? "self-end rounded-br-md bg-forest text-ivory"
                      : m.role === "err" ? "self-start bg-[#f6e3df] text-alert" : "self-start rounded-bl-md bg-cream"}`}>
                    {m.key ? t(m.key) : m.text}
                  </motion.div>
                ))}
              </AnimatePresence>
              {c.busy && <div className="flex gap-1 self-start px-4 py-3" aria-label={t("working")}>
                {[0, 1, 2].map(k => <motion.span key={k} className="size-2 rounded-full bg-stone" animate={{ opacity: [.25, 1, .25] }} transition={{ duration: 1, repeat: Infinity, delay: k * .15 }} />)}
              </div>}
            </div>

            {c.msgs.length === 1 && (
              <div className="flex gap-2 overflow-x-auto border-t border-line px-5 py-3 md:flex-wrap md:px-6 md:py-4">
                {tl("prompts").map(p => (
                  <button key={p} onClick={() => c.sendText(p)} className="shrink-0 whitespace-nowrap rounded-full border border-line bg-ivory px-3.5 py-2 text-[14px] hover:border-forest hover:text-forest md:shrink md:whitespace-normal md:text-left">{p}</button>
                ))}
              </div>
            )}

            <form onSubmit={submit} className="flex items-center gap-2 border-t border-line bg-cream/60 p-3 md:p-4">
              <button type="button" onClick={() => c.toggleMic()} disabled={c.busy}
                aria-label={c.live ? t("stop") : t("idle")} title={c.live ? t("stop") : t("idle")}
                className={`relative grid size-14 shrink-0 place-items-center rounded-full text-ivory transition disabled:opacity-40 ${c.live ? "bg-alert" : "bg-ink hover:bg-black"}`}>
                {c.live && <motion.span className="absolute inset-0 rounded-full bg-alert" animate={{ scale: [1, 1.35], opacity: [.45, 0] }} transition={{ duration: 1.4, repeat: Infinity }} />}
                {c.live ? <Square className="relative size-5 fill-current" /> : <Mic className="size-6" />}
              </button>
              <label className="sr-only" htmlFor="say">{t("input_ph")}</label>
              <input id="say" value={text} onChange={e => setText(e.target.value)} maxLength={500} autoComplete="off" placeholder={t("input_ph")}
                className="min-w-0 flex-1 rounded-full border border-line bg-ivory px-5 py-4 text-[17px] placeholder:text-stone/70 focus:border-forest focus:outline-none" />
              <button className="btn-green size-14 shrink-0 !p-0 sm:w-auto sm:!px-5" disabled={!text.trim() || c.busy} aria-label={t("send")}>
                <Send className="size-5" /><span className="hidden sm:inline">{t("send")}</span>
              </button>
            </form>
            <div className="flex items-center justify-between gap-3 px-5 pb-3 pt-1 md:px-6">
              <p className="text-[13px] text-stone" aria-live="polite">{label ? t(label) : c.label}</p>
              {c.canUndo && <button type="button" onClick={() => c.undo()} className="inline-flex items-center gap-1.5 text-[13px] font-medium text-stone hover:text-ink">
                <Undo2 className="size-3.5" />{t("undo")}</button>}
            </div>
          </section>
        </div>

        <aside className="grid content-start gap-4 lg:sticky lg:top-24 lg:self-start">
          <a href="tel:1930" className="flex items-center gap-3 rounded-[24px] bg-alert p-4 text-ivory hover:bg-[#a3413a]">
            <span className="grid size-11 place-items-center rounded-full bg-ivory/15"><Phone className="size-5" /></span>
            <span className="font-semibold">{t("call_short")}</span>
          </a>
          <div className="card p-5">
            <div className="flex items-center justify-between">
              <h2 className="text-[16px] font-bold">{t("case_h")}</h2>
              <span className="text-[14px] text-stone">{filled}/{KEYS.length}</span>
            </div>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-cream">
              <motion.div className="h-full rounded-full bg-forest" initial={{ width: 0 }} animate={{ width: `${100 * filled / KEYS.length}%` }} />
            </div>
            <Since ts={c.caseData.fraud_ts} />
            <ul className="mt-3">
              {KEYS.map((k, i) => {
                const v = c.caseData[k], ok = v != null, unk = v === "not known";
                return (
                  <li key={k} className="flex gap-3 border-t border-line py-3 first:border-0">
                    <span className={`mt-0.5 grid size-5 shrink-0 place-items-center rounded-full border ${ok ? "border-forest bg-forest text-ivory" : "border-ink/20"}`}>
                      {ok && <Check className="size-3" strokeWidth={3} />}
                    </span>
                    <div className="min-w-0">
                      <p className="text-[13px] text-stone">{fields[i]}</p>
                      <p className={`break-words text-[15px] ${ok && !unk ? "font-semibold" : "text-stone"}`}>
                        {!ok ? "—" : unk ? t("unknown") : fmt(c.caseData, k, v)}
                        {c.caseData.confirming === k ? <em className="ml-2 text-[12px] not-italic text-gold">{t("confirming")}</em>
                          : c.caseData.meta?.[k]?.confirmed ? <em className="ml-2 text-[12px] not-italic text-forest">{t("confirmed")}</em> : null}
                      </p>
                    </div>
                  </li>
                );
              })}
            </ul>
            <button onClick={restart} className="btn-line btn-sm mt-3"><RotateCcw className="size-3.5" />{t("start_over")}</button>
          </div>
          <p className="flex gap-2.5 px-1 text-[13px] leading-relaxed text-stone"><ShieldCheck className="mt-0.5 size-4 shrink-0 text-forest" />{t("a_never")}</p>
        </aside>
      </div>

      {c.result && <Plan ref={plan} c={c} cat={cat} />}
      {hud && c.timings && (
        <pre className="fixed bottom-3 right-3 z-50 rounded-xl bg-black/85 p-3 font-mono text-[12px] text-[#9fe8c8]">
          {"ms after end of speech\n" + Object.entries(c.timings).map(([k, v]) => k.padEnd(17) + String(v).padStart(6)).join("\n")}
        </pre>
      )}
    </div>
  );
}

function Since({ ts }: { ts?: number }) {
  // The golden hour made visible: how long ago the money went.
  const { lang } = useI18n();
  const [now, setNow] = useState(Date.now());
  useEffect(() => { const id = setInterval(() => setNow(Date.now()), 30000); return () => clearInterval(id); }, []);
  if (ts == null) return null;
  const m = Math.max(0, Math.floor((now / 1000 - ts) / 60)), rtf = new Intl.RelativeTimeFormat(lang, { numeric: "auto" });
  const ago = m < 60 ? rtf.format(-m, "minute") : m < 1440 ? rtf.format(-Math.floor(m / 60), "hour") : rtf.format(-Math.floor(m / 1440), "day");
  return <p className={`mt-3 inline-flex rounded-full px-3 py-1 text-[13px] font-semibold ${m < 1440 ? "bg-[#f6e3df] text-alert" : "bg-cream text-stone"}`}>⏱ {ago}</p>;
}

const Card = ({ n, h, children, tone = "" }: { n: number; h: string; children: ReactNode; tone?: string }) => (
  <motion.section className={`rounded-[24px] border border-line p-6 ${tone}`} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: n * .08 }}>
    <p className="font-display text-[13px] font-bold tracking-[.14em] text-gold">0{n}</p>
    <h3 className="mt-1 text-[20px] font-bold">{h}</h3>
    <div className="mt-4">{children}</div>
  </motion.section>
);

function Plan({ ref, c, cat }: { ref: Ref<HTMLElement>; c: Conversation; cat: number }) {
  const { t, tl } = useI18n();
  const r = c.result!, cs = c.caseData, fields = tl("fields");
  const card = KEYS.map((k, i) => fields[i] + ": " + (cs[k] == null ? "—" : cs[k] === "not known" ? t("unknown") : fmt(cs, k, cs[k]))).join("\n");
  const [subj, ...body] = r.bank_email.split("\n");
  const mail = "mailto:?subject=" + encodeURIComponent(subj.replace(/^Subject:\s*/, "")) + "&body=" + encodeURIComponent(body.join("\n").trim());
  const when = cs.fraud_ts != null ? new Date(cs.fraud_ts * 1000) : null;
  const part = (o: Intl.DateTimeFormatOptions) => when ? when.toLocaleString("en-CA", { ...IST, ...o }) : "";
  const known = (v: any) => v != null && v !== "not known";
  const prefill = { amount: cs.amount ? String(cs.amount) : "", bank: known(cs.bank) ? cs.bank : "",
    utr: known(cs.txn_id) ? cs.txn_id : "", date: part({ year: "numeric", month: "2-digit", day: "2-digit" }),
    time: part({ hour: "2-digit", minute: "2-digit", hour12: false }), category: cat >= 0 ? CATEGORIES[cat].id : "",
    description: [known(cs.scam_type) && `It was a ${cs.scam_type} scam.`, known(cs.scammer_contact) && `The fraudster used ${cs.scammer_contact}.`,
      known(cs.payment_mode) && `The money was sent via ${cs.payment_mode}.`].filter(Boolean).join(" ") };
  // For a family member helping from elsewhere: the case, the steps, and where to call. Sent only when the user taps.
  const share = [t("share_title"), r.verdict, card, t("share_do") + "\n" + r.checklist.map((s, k) => `${k + 1}. ${s}`).join("\n"),
    "1930 · https://cybercrime.gov.in", location.origin].join("\n\n");
  const nativeShare = () => navigator.share?.({ title: t("share_title"), text: share }).catch(() => { /* closed the sheet */ });

  return (
    <section ref={ref} className="mt-16 scroll-mt-24">
      <h2 className="text-[clamp(2rem,4vw,3rem)] font-extrabold tracking-[-.03em]">{t("r_h")}</h2>
      <div className="mt-8 grid grid-cols-1 items-start gap-4 lg:grid-cols-2">
        <Card n={1} h={t("r1")}>
          <p className="text-[18px] font-semibold leading-snug">{r.verdict}</p>
          <pre className="mt-4 whitespace-pre-wrap rounded-2xl bg-cream p-4 font-sans text-[14px] leading-relaxed">{card}</pre>
          <div className="mt-3"><CopyButton text={card} label={t("read_call")} /></div>
        </Card>
        <Card n={2} h={t("r2")} tone="bg-[#fbf3f1] border-alert/20">
          <ol className="grid gap-3">
            {r.checklist.map((s, k) => (
              <li key={k} className="flex gap-3 text-[16px] leading-relaxed">
                <span className={`grid size-7 shrink-0 place-items-center rounded-full text-[13px] font-bold ${k === 0 ? "bg-alert text-ivory" : "bg-ivory"}`}>{k + 1}</span>{s}
              </li>
            ))}
          </ol>
          <a href="tel:1930" className="btn-red mt-5"><Phone className="size-4" />{t("em_call")}</a>
          <p className="mt-4 text-[12px] leading-relaxed text-stone">{t("plan_src")}</p>
        </Card>
        <Card n={3} h={t("r3")}>
          <ul className="grid gap-3 text-[15px]">
            <li><a href="tel:1930" className="flex items-center gap-3 rounded-2xl bg-cream p-3 hover:bg-sand/60"><Phone className="size-5 shrink-0 text-alert" />{t("c_1930")}</a></li>
            <li className="flex items-center gap-3 rounded-2xl bg-cream p-3"><Landmark className="size-5 shrink-0 text-forest" />{t("c_bank")}</li>
            <li><a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 rounded-2xl bg-cream p-3 hover:bg-sand/60"><ExternalLink className="size-5 shrink-0" />{t("c_portal")}</a></li>
          </ul>
        </Card>
        <Card n={4} h={t("r4")}><EvidenceChecklist compact /></Card>
        <div className="lg:col-span-2">
          <Card n={5} h={t("r5")}>
            <p className="text-[15px] text-stone">{t("r5_p")}</p>
            <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
              {([[t("complaint_h"), r.complaint], [t("email_h"), r.bank_email]] as const).map(([h, body]) => (
                <div key={h} className="rounded-2xl bg-cream p-4">
                  <div className="flex items-center justify-between gap-3"><h4 className="text-[15px] font-semibold">{h}</h4><CopyButton text={body} /></div>
                  <pre lang="en" className="mt-3 max-h-64 overflow-auto whitespace-pre-wrap font-sans text-[14px] leading-relaxed">{body}</pre>
                </div>
              ))}
            </div>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link to="/complaint-generator" state={{ prefill }} className="btn-green">{t("open_gen")}<ArrowRight className="size-4" /></Link>
              <a href={mail} className="btn-line"><Mail className="size-4" />{t("open_mail")}</a>
              <Link to="/track" state={{ prefill: { fraudDate: prefill.date, bank: prefill.bank } }} className="btn-line"><ListChecks className="size-4" />{t("track_link")}</Link>
            </div>
          </Card>
        </div>
      </div>
      <motion.div className="mt-4 flex flex-col gap-4 rounded-[24px] bg-mint p-6 md:flex-row md:items-center" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .5 }}>
        <span className="grid size-12 shrink-0 place-items-center rounded-full bg-forest text-ivory"><Users className="size-5" /></span>
        <div className="mr-auto">
          <h3 className="text-[18px] font-bold">{t("share_h")}</h3>
          <p className="mt-1 max-w-xl text-[15px] text-forest">{t("share_p")}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {"share" in navigator && <button onClick={nativeShare} className="btn-green"><Share2 className="size-4" />{t("share_btn")}</button>}
          <a href={"https://wa.me/?text=" + encodeURIComponent(share)} target="_blank" rel="noopener noreferrer" className="btn-line"><MessageCircle className="size-4" />WhatsApp</a>
          <CopyButton text={share} />
        </div>
      </motion.div>
    </section>
  );
}
