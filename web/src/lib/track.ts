// Follow-up tracker: what to do after reporting, and by when. Pure functions; the data stays in the browser.
// Deadlines follow the RBI liability circular (6 July 2017: report unauthorised electronic transactions within
// 3 working days of the bank's alert) and the RBI Integrated Ombudsman Scheme (escalate if the bank hasn't
// resolved the complaint within 30 days).

export type Track = { fraudDate: string; reportedOn: string; ackNo: string; bank: string; bankFiledOn: string; bankRef: string; done: string[] };
export const EMPTY_TRACK: Track = { fraudDate: "", reportedOn: "", ackNo: "", bank: "", bankFiledOn: "", bankRef: "", done: [] };
export type StepState = "done" | "overdue" | "today" | "upcoming" | "waiting" | "ongoing";
export type Step = { id: string; title: string; detail: string; due: Date | null; state: StepState; manual: boolean;
  link?: { label: string; href: string; external?: boolean } };

const DAY = 864e5;
const parse = (d: string) => (/^\d{4}-\d{2}-\d{2}$/.test(d) ? new Date(d + "T00:00:00") : null);
const addDays = (d: Date, n: number) => new Date(d.getTime() + n * DAY);

// ponytail: skips Saturdays and Sundays only; bank holidays vary by state, so the date is "about".
export function addWorkingDays(d: Date, n: number) {
  const x = new Date(d);
  while (n > 0) { x.setDate(x.getDate() + 1); if (x.getDay() !== 0 && x.getDay() !== 6) n--; }
  return x;
}

export function steps(t: Track, today = new Date()): Step[] {
  const fraud = parse(t.fraudDate), reported = parse(t.reportedOn), bankOn = parse(t.bankFiledOn);
  const day0 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const raw = [
    { id: "report", title: "Report to 1930 or cybercrime.gov.in", manual: false,
      detail: "As soon as possible, ideally within the first hour. Keep the acknowledgement number you are given.",
      due: fraud, done: !!reported || !!t.ackNo.trim(), link: { label: "Open cybercrime.gov.in", href: "https://cybercrime.gov.in", external: true } },
    { id: "bank", title: "Send a written complaint to your bank", manual: false,
      detail: "Within 3 working days of the bank's alert. RBI rules limit your liability for unauthorised electronic transactions reported this quickly.",
      due: fraud && addWorkingDays(fraud, 3), done: !!bankOn || !!t.bankRef.trim(), link: { label: "Draft the bank email", href: "/bank-email" } },
    { id: "status", title: "Check the status and follow up", manual: true,
      detail: "Check your complaint on cybercrime.gov.in with the acknowledgement number, and ask your bank for an update in writing.",
      due: reported && addDays(reported, 7), done: t.done.includes("status") },
    { id: "ombudsman", title: "Escalate to the RBI Ombudsman if needed", manual: true,
      detail: "If your bank hasn't resolved your complaint within 30 days, or you're unhappy with its reply, complain at cms.rbi.org.in with your bank reference number.",
      due: bankOn && addDays(bankOn, 30), done: t.done.includes("ombudsman"), link: { label: "Open cms.rbi.org.in", href: "https://cms.rbi.org.in", external: true } },
    { id: "safe", title: "Keep records, and beware of recovery scams", manual: true,
      detail: "Log every call and reference number. Anyone who asks for a fee to recover your money is another scammer; officials never charge.",
      due: null, done: t.done.includes("safe") },
  ];
  return raw.map(({ done, ...s }) => ({ ...s,
    state: (done ? "done" : s.id === "safe" ? "ongoing" : !s.due ? "waiting"
      : s.due < day0 ? "overdue" : s.due.getTime() === day0.getTime() ? "today" : "upcoming") as StepState }));
}

export function summary(t: Track, today = new Date()) {
  const fmt = (d: Date | null) => (d ? d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : "—");
  return ["Golden Hour — complaint follow-up",
    `Fraud date: ${t.fraudDate || "—"}`, `Reported to 1930 / cybercrime.gov.in: ${t.reportedOn || "—"} (ack. no. ${t.ackNo || "—"})`,
    `Bank: ${t.bank || "—"}, complaint filed ${t.bankFiledOn || "—"} (ref. ${t.bankRef || "—"})`, "",
    ...steps(t, today).map(s => `[${s.state === "done" ? "x" : " "}] ${s.title}${s.due ? ` — by ${fmt(s.due)}` : ""}`)].join("\n");
}
