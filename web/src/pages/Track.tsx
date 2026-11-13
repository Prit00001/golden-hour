import { motion } from "framer-motion";
import { AlertCircle, Check, Clock, ExternalLink, RotateCcw, ShieldCheck } from "lucide-react";
import { useEffect, useState, type ChangeEvent } from "react";
import { Link, useLocation } from "react-router";
import CopyButton from "../components/CopyButton";
import NotTranslated from "../components/NotTranslated";
import { EMPTY_TRACK, steps, summary, type Step, type Track as T } from "../lib/track";

const KEY = "gh-track";  // stays in this browser only; nothing is sent anywhere
const load = (): T | null => { try { const v = localStorage.getItem(KEY); return v ? { ...EMPTY_TRACK, ...JSON.parse(v) } : null; } catch { return null; } };
const fmt = (d: Date) => d.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" });

const CHIP: Record<Step["state"], [string, string]> = {
  done: ["Done", "bg-mint text-forest"], overdue: ["Overdue", "bg-[#f6e3df] text-alert"], today: ["Due today", "bg-[#fbf1dc] text-[#7a5a1f]"],
  upcoming: ["Upcoming", "bg-cream text-stone"], waiting: ["Add a date", "bg-cream text-stone"], ongoing: ["Ongoing", "bg-cream text-stone"],
};

export default function Track() {
  const { state } = useLocation() as { state?: { prefill?: Partial<T> } };
  const [t, setT] = useState<T>(() => load() ?? { ...EMPTY_TRACK, ...state?.prefill });
  useEffect(() => { try { localStorage.setItem(KEY, JSON.stringify(t)); } catch { /* not remembered */ } }, [t]);
  const set = (k: keyof T) => (e: ChangeEvent<HTMLInputElement>) => setT({ ...t, [k]: e.target.value });
  const toggle = (id: string) => setT({ ...t, done: t.done.includes(id) ? t.done.filter(x => x !== id) : [...t.done, id] });
  const reset = () => { if (confirm("Clear everything saved in the tracker?")) setT(EMPTY_TRACK); };
  const list = steps(t);
  const today = new Date().toISOString().slice(0, 10);

  const field = (k: keyof T, label: string, type = "text", hint?: string) => (
    <div>
      <label htmlFor={"t-" + k} className="text-[14px] font-semibold">{label}</label>
      {hint && <p className="text-[13px] text-stone">{hint}</p>}
      <input id={"t-" + k} type={type} value={t[k] as string} onChange={set(k)} maxLength={40} max={type === "date" ? today : undefined}
        className="field mt-1.5" autoComplete="off" />
    </div>
  );

  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-12 md:px-8 md:pt-16" lang="en">
      <NotTranslated />
      <div className="max-w-3xl">
        <p className="eyebrow">Follow-up tracker</p>
        <h1 className="mt-4 text-[clamp(2.2rem,5.5vw,4.25rem)] leading-[1.06] tracking-[-.012em]">Stay on top of your complaint.</h1>
        <p className="mt-4 text-[17px] leading-relaxed text-stone">Save your reference numbers and the dates you reported. Golden Hour shows what to do next and by when. Everything stays in this browser.</p>
      </div>

      <div className="mt-10 grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
        <div className="card self-start p-6 md:p-8">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            {field("fraudDate", "Date of the fraud", "date")}
            {field("reportedOn", "Reported to 1930 / portal on", "date")}
            <div className="sm:col-span-2">{field("ackNo", "Acknowledgement number", "text", "From 1930 or cybercrime.gov.in")}</div>
            {field("bank", "Bank")}
            {field("bankFiledOn", "Bank complaint filed on", "date")}
            <div className="sm:col-span-2">{field("bankRef", "Bank complaint reference", "text", "The number your bank gave you")}</div>
          </div>
          <p className="mt-6 flex gap-2.5 rounded-[6px] bg-[#f6e3df] px-4 py-3 text-[13px] leading-relaxed text-alert">
            <ShieldCheck className="mt-0.5 size-4 shrink-0" />Reference numbers only. Never save OTPs, PINs, passwords or card numbers here.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <CopyButton text={summary(t)} label="Copy summary" />
            <button type="button" onClick={reset} className="btn-line btn-sm"><RotateCcw className="size-3.5" />Clear</button>
          </div>
        </div>

        <ol className="relative grid gap-3">
          {list.map((s, k) => {
            const [chip, tone] = CHIP[s.state];
            return (
              <motion.li key={s.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: k * .06 }}
                className={`rounded-[8px] border p-5 ${s.state === "done" ? "border-forest/20 bg-mint/40" : s.state === "overdue" ? "border-alert/30" : "border-line"}`}>
                <div className="flex items-start gap-4">
                  <span className={`grid size-9 shrink-0 place-items-center rounded-full font-display text-[14px] font-bold ${s.state === "done" ? "bg-forest text-ivory" : "bg-cream"}`}>
                    {s.state === "done" ? <Check className="size-4" strokeWidth={3} /> : k + 1}
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="mr-auto font-sans text-[17px] font-semibold leading-snug">{s.title}</h2>
                      <span className={`inline-flex items-center gap-1 rounded-[4px] px-2 py-1 text-[12px] font-medium ${tone}`}>
                        {s.state === "overdue" ? <AlertCircle className="size-3.5" /> : s.state !== "done" && <Clock className="size-3.5" />}
                        {chip}{s.due && s.state !== "done" && s.state !== "waiting" ? ` · ${fmt(s.due)}` : ""}
                      </span>
                    </div>
                    <p className="mt-1.5 text-[15px] leading-relaxed text-stone">{s.detail}</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {s.link && (s.link.external
                        ? <a href={s.link.href} target="_blank" rel="noopener noreferrer" className="btn-line btn-sm">{s.link.label}<ExternalLink className="size-3.5" /></a>
                        : <Link to={s.link.href} className="btn-line btn-sm">{s.link.label}</Link>)}
                      {s.manual && <button type="button" onClick={() => toggle(s.id)} aria-pressed={s.state === "done"} className="btn-line btn-sm">
                        <Check className="size-3.5" />{s.state === "done" ? "Mark as not done" : "Mark as done"}</button>}
                    </div>
                    {s.state === "waiting" && <p className="mt-2 text-[13px] text-stone">Add the {s.id === "status" ? "date you reported" : s.id === "ombudsman" ? "date you filed with the bank" : "date of the fraud"} to see when this is due.</p>}
                  </div>
                </div>
              </motion.li>
            );
          })}
        </ol>
      </div>
      <p className="mt-8 text-[13px] text-stone">Deadlines follow the RBI's 2017 circular on customer liability (3 working days, weekends skipped; check bank holidays) and the RBI Integrated Ombudsman Scheme (30 days). Always follow what your bank and the police tell you.</p>
    </div>
  );
}
