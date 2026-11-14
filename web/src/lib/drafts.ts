// Complaint and bank-email drafts from the generator form. Pure functions, run in the browser only:
// nothing typed into the form is sent to the server.

export type Form = { name: string; phone: string; email: string; bank: string; accountType: string; date: string; time: string;
  category: string; amount: string; utr: string; description: string; branch: string };
export const EMPTY: Form = { name: "", phone: "", email: "", bank: "", accountType: "", date: "", time: "", category: "",
  amount: "", utr: "", description: "", branch: "" };

// Banking secrets must never end up in a draft: an OTP/PIN/CVV/password next to digits, or a full card number.
const SECRET = /\b(otp|pin|m-?pin|upi\s*pin|cvv|password|passcode)\b\D{0,20}\d{3,}|\b(?:\d[ -]?){15,16}\b/i;

export function validate(f: Form, today = new Date()): Partial<Record<keyof Form, string>> {
  const e: Partial<Record<keyof Form, string>> = {};
  if (f.name.trim().length < 2) e.name = "Enter your full name.";
  if (!/^(\+?91[\s-]?)?[6-9]\d{9}$/.test(f.phone.replace(/[\s-]/g, ""))) e.phone = "Enter a 10-digit Indian mobile number.";
  if (f.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) e.email = "This email address doesn't look right.";
  if (!f.bank.trim()) e.bank = "Enter your bank's name.";
  if (!f.accountType) e.accountType = "Choose the account type.";
  if (!f.date) e.date = "Enter the date of the incident.";
  else if (new Date(f.date + "T00:00:00") > today) e.date = "The date can't be in the future.";
  if (!f.category) e.category = "Choose the type of fraud.";
  const amt = Number(f.amount.replace(/,/g, ""));
  if (!(amt > 0 && amt < 1e10)) e.amount = "Enter the amount lost, in rupees.";
  if (f.utr && !/^[A-Za-z0-9]{6,30}$/.test(f.utr.trim())) e.utr = "Use only letters and digits (6–30 characters).";
  if (f.description.trim().length < 20) e.description = "Describe what happened in a few sentences (at least 20 characters).";
  for (const k of ["description", "branch", "utr", "bank", "name"] as const)
    if (SECRET.test(f[k])) e[k] = "Remove OTPs, PINs, CVVs, passwords and card numbers. They must never be shared.";
  return e;
}

const rs = (a: string) => Number(a.replace(/,/g, "")).toLocaleString("en-IN");
const long = (d: string) => new Date(d + "T00:00:00").toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
const at = (f: Form) => long(f.date) + (f.time ? `, ${f.time}` : "");
const todayStr = (now: Date) => now.toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
const EVIDENCE = ["Bank SMS or statement showing the debit", "Screenshots of the transaction",
  "Phone numbers, UPI IDs, links or chats used by the fraudster", "Any other messages or receipts about the incident"];

export function complaintDraft(f: Form, now = new Date()) {
  const amt = rs(f.amount);
  return [
    "CYBERCRIME COMPLAINT — INFORMATION DRAFT",
    "For filing at https://cybercrime.gov.in (\"Report Financial Fraud\") or reading out on the 1930 helpline. Check every detail before you submit.",
    "",
    `Subject: Complaint regarding ${f.category} — loss of Rs. ${amt}`,
    "Recipient: National Cyber Crime Reporting Portal, cybercrime.gov.in",
    "",
    "1. COMPLAINANT",
    `Name: ${f.name.trim()}`, `Phone: ${f.phone.trim()}`, `Email: ${f.email.trim() || "—"}`,
    "",
    "2. INCIDENT SUMMARY",
    `On ${at(f)}, I was the victim of financial fraud (${f.category}). Rs. ${amt} was lost from my account with ${f.bank.trim()} (${f.accountType}).`,
    "",
    "3. TRANSACTION DETAILS",
    `Bank: ${f.bank.trim()}${f.branch.trim() ? ` (${f.branch.trim()})` : ""}`, `Account type: ${f.accountType}`,
    `Amount: Rs. ${amt}`, `Transaction ID / UTR: ${f.utr.trim() || "not available"}`, `Date and time: ${at(f)}`,
    "",
    "4. TIMELINE OF EVENTS",
    `- ${at(f)}: ${f.description.trim()}`, `- ${todayStr(now)}: Complaint prepared for filing.`,
    "",
    "5. REQUESTED ACTION",
    "I request that this transaction be investigated, that the amount be put on hold in the receiving account(s) and returned to me, and that action be taken against the persons responsible.",
    "",
    "6. SUPPORTING EVIDENCE (attach copies)",
    ...EVIDENCE.map(x => "- " + x),
    "",
    "7. DECLARATION",
    "The information given above is true to the best of my knowledge.",
    "",
    f.name.trim(), todayStr(now),
  ].join("\n");
}

export function bankEmailDraft(f: Form) {
  const amt = rs(f.amount), bank = f.bank.trim();
  return [
    `To: ${bank} — Customer Care / Grievance Redressal`,
    `(Use the official email address from ${bank}'s own website or app — never one from a message or a search ad.)`,
    "",
    `Subject: Fraudulent transaction of Rs. ${amt} on ${long(f.date)} — request to block and investigate`,
    "",
    "Dear Sir/Madam,",
    "",
    `I am writing to report a fraudulent transaction on my account (${f.accountType}), the result of ${f.category}. Please treat this as urgent.`,
    "",
    "Transaction details",
    `- Account holder: ${f.name.trim()}`, "- Account number: XXXX [add the last 4 digits only]", `- Account type: ${f.accountType}`,
    ...(f.branch.trim() ? [`- Branch: ${f.branch.trim()}`] : []),
    `- Amount: Rs. ${amt}`, `- Date and time: ${at(f)}`, `- Transaction ID / UTR: ${f.utr.trim() || "not available"}`,
    "",
    "What happened",
    f.description.trim(),
    "",
    "I request you to:",
    "1. Block my account, cards and UPI immediately to prevent further loss.",
    "2. Investigate this transaction and raise a dispute with the receiving bank.",
    "3. Ask the receiving bank to put the amount on hold.",
    "4. Send me the complaint reference number in writing.",
    "",
    "I am reporting this to the National Cyber Crime Helpline (1930) and on cybercrime.gov.in, and will share the acknowledgement number with you.",
    "",
    "Evidence I can provide",
    ...EVIDENCE.map(x => "- " + x),
    "",
    "Yours faithfully,",
    f.name.trim(), f.phone.trim(), ...(f.email.trim() ? [f.email.trim()] : []),
  ].join("\n");
}

export function incidentSummary(f: Form) {
  return [
    "TRANSACTION INCIDENT SUMMARY",
    "",
    `What happened: ${f.category}`,
    `When: ${at(f)}`,
    `Amount lost: Rs. ${rs(f.amount)}`,
    `Bank and account type: ${f.bank.trim()} (${f.accountType})`,
    `Transaction ID / UTR: ${f.utr.trim() || "not available"}`,
    "",
    "In my own words:",
    f.description.trim(),
    "",
    "Reported by: " + f.name.trim() + ", " + f.phone.trim(),
  ].join("\n");
}

// Sent days after the first complaint; the reference numbers aren't on the form, so they stay as marked placeholders.
export function followUpEmail(f: Form) {
  const bank = f.bank.trim();
  return [
    `To: ${bank} — Customer Care / Grievance Redressal`,
    "",
    `Subject: Follow-up on my complaint about a fraudulent transaction of Rs. ${rs(f.amount)} on ${long(f.date)}`,
    "",
    "Dear Sir/Madam,",
    "",
    `I am following up on the complaint I made about a fraudulent transaction on my account (${f.accountType}).`,
    "",
    "- Complaint reference number: [add your bank complaint reference]",
    "- Date of my complaint: [add the date]",
    `- Amount: Rs. ${rs(f.amount)}, on ${at(f)}`,
    `- Transaction ID / UTR: ${f.utr.trim() || "not available"}`,
    "- Cybercrime acknowledgement number: [add it if you have one]",
    "",
    "Please tell me in writing the current status of my complaint, what action has been taken, and when I can expect a resolution.",
    "",
    "If the complaint is not resolved within 30 days of my original complaint, I understand I may approach the RBI Ombudsman.",
    "",
    "Yours faithfully,",
    f.name.trim(), f.phone.trim(), ...(f.email.trim() ? [f.email.trim()] : []),
  ].join("\n");
}
