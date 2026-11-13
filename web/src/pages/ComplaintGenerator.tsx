import { AnimatePresence, motion } from "framer-motion";
import { Download, FileText, Mail, PencilLine, Printer, RotateCcw, ShieldAlert, Sparkles, TriangleAlert } from "lucide-react";
import { useRef, useState, type ChangeEvent, type FormEvent, type ReactNode } from "react";
import { Link, useLocation } from "react-router";
import CopyButton from "../components/CopyButton";
import NotTranslated from "../components/NotTranslated";
import en from "../i18n/en";
import { CATEGORIES } from "../lib/data";
import { bankEmailDraft, complaintDraft, EMPTY, validate, type Form } from "../lib/drafts";

const ACCOUNT_TYPES = ["Savings account", "Current account", "Credit card", "Debit card", "UPI / wallet", "Other"];
type Tab = "complaint" | "bank";

function download(name: string, blob: Blob) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
async function docx(name: string, text: string) {
  const { Document, Packer, Paragraph, TextRun } = await import("docx");  // loaded only when someone asks for a .docx
  const doc = new Document({ sections: [{ children: text.split("\n").map((line, k) =>
    new Paragraph({ children: [new TextRun({ text: line, bold: k === 0 || /^\d\. [A-Z ]+/.test(line) || line.startsWith("Subject:"), font: "Calibri", size: 22 })] })) }] });
  download(name, await Packer.toBlob(doc));
}

export default function ComplaintGenerator({ mode }: { mode: Tab }) {
  const { state } = useLocation() as { state?: { prefill?: Partial<Form> & { category?: string } } };
  const pre = state?.prefill;
  const catTitle = (id?: string) => en.cat_t[CATEGORIES.findIndex(c => c.id === id)] || "";
  const [f, setF] = useState<Form>({ ...EMPTY, ...pre, category: catTitle(pre?.category) });
  const [errors, setErrors] = useState<Partial<Record<keyof Form, string>>>({});
  const [drafts, setDrafts] = useState<Record<Tab, string> | null>(null);
  const [tab, setTab] = useState<Tab>(mode);
  const [editing, setEditing] = useState(false);
  const out = useRef<HTMLDivElement>(null);
  const tabs: Tab[] = mode === "bank" ? ["bank"] : ["complaint", "bank"];

  const set = (k: keyof Form) => (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setF({ ...f, [k]: e.target.value }); if (errors[k]) setErrors({ ...errors, [k]: undefined });
  };
  const generate = (e: FormEvent) => {
    e.preventDefault();
    const errs = validate(f);
    setErrors(errs);
    if (Object.keys(errs).length) { document.getElementById("f-" + Object.keys(errs)[0])?.focus(); return; }
    setDrafts({ complaint: complaintDraft(f), bank: bankEmailDraft(f) }); setEditing(false);
    setTimeout(() => out.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  };
  const reset = () => { setF(EMPTY); setErrors({}); setDrafts(null); setEditing(false); window.scrollTo({ top: 0, behavior: "smooth" }); };
  const field = (k: keyof Form, label: string, input: ReactNode, hint?: string) => (
    <div className={k === "description" ? "sm:col-span-2" : ""}>
      <label htmlFor={"f-" + k} className="text-[14px] font-semibold">{label}</label>
      {hint && <p className="text-[13px] text-stone">{hint}</p>}
      <div className="mt-1.5">{input}</div>
      {errors[k] && <p id={"e-" + k} className="mt-1.5 text-[13px] font-medium text-alert">{errors[k]}</p>}
    </div>
  );
  const attrs = (k: keyof Form) => ({ id: "f-" + k, value: f[k], onChange: set(k), "aria-invalid": !!errors[k],
    "aria-describedby": errors[k] ? "e-" + k : undefined, className: `field ${errors[k] ? "!border-alert" : ""}` });
  const text = drafts?.[tab] ?? "";
  const fileBase = tab === "bank" ? "bank-email" : "cybercrime-complaint";

  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-12 md:px-8 md:pt-16" lang="en">
      <NotTranslated />
      <div className="max-w-3xl">
        <p className="eyebrow">{mode === "bank" ? "Bank email generator" : "Complaint generator"}</p>
        <h1 className="mt-4 text-[clamp(2.2rem,5.5vw,4.25rem)] leading-[1.06] tracking-[-.012em]">
          {mode === "bank" ? "Speak to your bank with confidence." : "Your complaint, professionally prepared."}
        </h1>
        <p className="mt-4 text-[17px] leading-relaxed text-stone">
          {mode === "bank" ? "Turn what happened into a clear, formal email your bank can act on — with the transaction reference, your requests and an evidence list."
            : "Preparing a complaint can be confusing. Let Golden Hour organize your information into a clear, structured draft."}
        </p>
        {mode === "bank" ? <Link to="/complaint-generator" className="mt-3 inline-block text-[15px] font-semibold text-forest underline-offset-4 hover:underline">Need the cybercrime complaint too? Use the complaint generator →</Link>
          : <Link to="/bank-email" className="mt-3 inline-block text-[15px] font-semibold text-forest underline-offset-4 hover:underline">Only need the bank email? →</Link>}
      </div>

      <div className="mt-10 grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]">
        <form onSubmit={generate} noValidate className="card p-6 md:p-8">
          <p className="mb-6 flex gap-2.5 rounded-[6px] bg-[#f6e3df] px-4 py-3 text-[14px] leading-relaxed text-alert">
            <ShieldAlert className="mt-0.5 size-4 shrink-0" />Never enter your OTP, ATM PIN, UPI PIN, net banking password, CVV or full card number. This form never asks for them.
          </p>
          <div className="grid gap-5 sm:grid-cols-2">
            {field("name", "Full name", <input {...attrs("name")} autoComplete="name" maxLength={80} />)}
            {field("phone", "Mobile number", <input {...attrs("phone")} type="tel" autoComplete="tel" inputMode="tel" maxLength={16} placeholder="98765 43210" />)}
            {field("email", "Email (optional)", <input {...attrs("email")} type="email" autoComplete="email" maxLength={120} />)}
            {field("bank", "Bank name", <input {...attrs("bank")} maxLength={80} placeholder="e.g. State Bank of India" />)}
            {field("accountType", "Account type", <select {...attrs("accountType")}><option value="">Choose…</option>{ACCOUNT_TYPES.map(a => <option key={a}>{a}</option>)}</select>)}
            {field("category", "Type of fraud", <select {...attrs("category")}><option value="">Choose…</option>{en.cat_t.map(c => <option key={c}>{c}</option>)}</select>)}
            {field("date", "Date of incident", <input {...attrs("date")} type="date" max={new Date().toISOString().slice(0, 10)} />)}
            {field("time", "Time (optional)", <input {...attrs("time")} type="time" />)}
            {field("amount", "Amount lost (₹)", <input {...attrs("amount")} inputMode="numeric" maxLength={14} placeholder="40,000" />)}
            {field("utr", "Transaction ID / UTR (optional)", <input {...attrs("utr")} maxLength={30} placeholder="12-digit number from the bank SMS" />)}
            {field("branch", "Bank branch or contact (optional)", <input {...attrs("branch")} maxLength={120} />)}
            <div className="hidden sm:block" />
            {field("description", "What happened", <textarea {...attrs("description")} rows={6} maxLength={2000}
              placeholder="In your own words: who contacted you, what they said, what you did, and what happened to the money." />,
              "Plain words are fine. Include phone numbers, UPI IDs or links the fraudster used.")}
          </div>
          <div className="mt-7 flex flex-wrap gap-3">
            <button className="btn-green"><Sparkles className="size-4" />Generate Draft</button>
            <button type="button" onClick={reset} className="btn-line"><RotateCcw className="size-4" />Start Again</button>
          </div>
          {Object.keys(errors).some(k => errors[k as keyof Form]) && <p className="mt-3 text-[14px] font-medium text-alert" role="alert">Please fix the highlighted fields.</p>}
        </form>

        <div ref={out} className="scroll-mt-24 lg:sticky lg:top-24 lg:self-start">
          <AnimatePresence mode="wait">
            {!drafts ? (
              <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="grid min-h-[420px] place-items-center rounded-[8px] border border-dashed border-ink/15 bg-cream/50 p-8 text-center">
                <div>
                  <FileText className="mx-auto size-10 text-gold" strokeWidth={1.5} />
                  <p className="mt-4 font-display text-[20px] font-bold">Your draft appears here</p>
                  <p className="mx-auto mt-2 max-w-xs text-[15px] text-stone">Fill in the form and press Generate Draft. Everything stays in your browser.</p>
                </div>
              </motion.div>
            ) : (
              <motion.div key="out" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="card overflow-hidden">
                {tabs.length > 1 && (
                  <div className="flex border-b border-line" role="tablist">
                    {tabs.map(k => (
                      <button key={k} role="tab" aria-selected={tab === k} onClick={() => { setTab(k); setEditing(false); }}
                        className={`flex-1 px-4 py-3.5 text-[14px] font-semibold transition ${tab === k ? "bg-ivory text-ink shadow-[inset_0_-2px_0_#315C47]" : "bg-cream/60 text-stone hover:text-ink"}`}>
                        {k === "complaint" ? "Cybercrime complaint" : "Bank email"}
                      </button>
                    ))}
                  </div>
                )}
                <div className="p-5">
                  <p className="flex gap-2 rounded-[6px] bg-[#fbf1dc] px-3.5 py-2.5 text-[13px] leading-relaxed text-[#7a5a1f]">
                    <TriangleAlert className="mt-0.5 size-4 shrink-0" />Check every detail and correct anything wrong before you send or submit it. Golden Hour doesn't send or file anything.
                  </p>
                  {editing ? (
                    <textarea aria-label="Edit draft" value={text} onChange={e => setDrafts({ ...drafts, [tab]: e.target.value })}
                      className="field mt-4 h-[460px] font-mono text-[13px] leading-relaxed" />
                  ) : (
                    <pre className="print-area mt-4 max-h-[460px] overflow-auto whitespace-pre-wrap rounded-[6px] border border-line bg-white p-4 font-sans text-[14px] leading-relaxed">{text}</pre>
                  )}
                  <div className="mt-4 flex flex-wrap gap-2">
                    <button onClick={() => setEditing(e => !e)} className="btn-line btn-sm"><PencilLine className="size-3.5" />{editing ? "Done editing" : "Edit Draft"}</button>
                    <CopyButton text={text} label={tab === "bank" ? "Copy Email" : "Copy Text"} />
                    <button onClick={() => { setEditing(false); setTimeout(() => window.print(), 50); }} className="btn-line btn-sm"><Printer className="size-3.5" />Download as PDF</button>
                    <button onClick={() => docx(fileBase + ".docx", text)} className="btn-line btn-sm"><Download className="size-3.5" />Download as DOCX</button>
                    {tab === "bank" && <button onClick={() => download("bank-email.txt", new Blob([text], { type: "text/plain" }))} className="btn-line btn-sm"><Mail className="size-3.5" />Download Email</button>}
                  </div>
                  <p className="mt-3 text-[12px] text-stone">"Download as PDF" opens your browser's print dialog — choose "Save as PDF".</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
