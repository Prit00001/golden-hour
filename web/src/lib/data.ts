import { Fingerprint, Landmark, Link2, Phone, QrCode, ShieldCheck, ShoppingBag, TrendingUp, FileText, ListChecks, type LucideIcon } from "lucide-react";

// Order matches cat_t / cat_p in the strings. `seed` pre-fills the case where a category settles a field.
export const CATEGORIES: { id: string; icon: LucideIcon; tint: string; seed?: Record<string, string> }[] = [
  { id: "upi", icon: QrCode, tint: "bg-[#efe3cc]", seed: { payment_mode: "UPI" } },
  { id: "banking", icon: Landmark, tint: "bg-mint" },
  { id: "phishing", icon: Link2, tint: "bg-[#f3dcd6]" },
  { id: "investment", icon: TrendingUp, tint: "bg-[#e6e1d4]" },
  { id: "shopping", icon: ShoppingBag, tint: "bg-[#e9e4f0]" },
  { id: "identity", icon: Fingerprint, tint: "bg-[#dde6ea]" },
];

export const REVIEWED = "13 November 2026";  // the date every article and step was last checked against its sources
export type Article = { slug: string; icon: LucideIcon; tint: string; title: string; desc: string; minutes: number;
  sources: { label: string; url: string }[];
  body: { h: string; p?: string; list?: string[] }[] };

// English only for now (the page says so in other languages). Facts kept to what official sources state.
export const RESOURCES: Article[] = [
  { slug: "after-upi-fraud", icon: QrCode, tint: "bg-[#efe3cc]", minutes: 3,
    sources: [{ label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }, { label: "RBI circular: Limiting liability of customers in unauthorised electronic banking transactions (6 July 2017)", url: "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11040" }],
    title: "What to do immediately after UPI fraud",
    desc: "The first hour decides a lot. Here is the order to do things in.",
    body: [
      { h: "1. Call 1930 now", p: "1930 is the National Cyber Crime Helpline. When you report quickly, it can ask the banks that received your money to put it on hold while it is still in their accounts. Every minute counts, so do this first." },
      { h: "2. Call your bank's official helpline", p: "Use the number on the back of your card, in your passbook or on the bank's official website — never a number from a search ad or a message. Ask them to block UPI and cards on the account, and write down the complaint reference number they give you." },
      { h: "3. File a complaint on cybercrime.gov.in", p: "Choose \"Report Financial Fraud\". Keep the acknowledgement number; you will need it for the bank and for any follow-up." },
      { h: "4. Save your evidence", list: ["UTR / transaction ID from the bank SMS or UPI app", "Screenshots of the payment and the conversation", "The scammer's phone number, UPI ID and any links they sent"] },
      { h: "Good to know", p: "If money left your account without your approval, RBI rules limit your liability when you report it to your bank quickly — within three working days for zero liability in many cases. If you were tricked into approving the payment yourself, report it just as fast: the police complaint is how that money is traced." },
      { h: "Watch out", p: "Anyone who calls promising to recover your money for a fee is another scammer. Real recovery only happens through 1930, the police and your bank, and none of them charge you." },
    ] },
  { slug: "report-banking-fraud", icon: Landmark, tint: "bg-mint", minutes: 3,
    sources: [{ label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }, { label: "RBI Complaint Management System (Integrated Ombudsman)", url: "https://cms.rbi.org.in" }, { label: "RBI circular: Limiting liability of customers in unauthorised electronic banking transactions (6 July 2017)", url: "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11040" }],
    title: "How to report online banking fraud",
    desc: "Block, report, and put it in writing so there is a record.",
    body: [
      { h: "Stop further loss", list: ["Call the bank's official helpline and block net banking, cards and UPI", "From a device you trust, change your net banking password and UPI PIN", "Log out of all sessions in your banking app if it offers that"] },
      { h: "Report it", list: ["Call 1930 and file on cybercrime.gov.in", "Send a written complaint to your bank (the bank email generator here can draft it)", "Keep every reference and acknowledgement number"] },
      { h: "If the bank doesn't resolve it", p: "If your bank doesn't reply within 30 days, or you aren't satisfied with the reply, you can complain to the RBI Ombudsman at cms.rbi.org.in. Attach your bank complaint and its reference number." },
    ] },
  { slug: "spot-phishing-links", icon: Link2, tint: "bg-[#f3dcd6]", minutes: 2,
    sources: [{ label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }, { label: "Sanchar Saathi, Department of Telecommunications (Chakshu)", url: "https://sancharsaathi.gov.in" }],
    title: "How to identify phishing links",
    desc: "Fake links look real. A few checks catch most of them.",
    body: [
      { h: "Check before you tap", list: ["Read the web address carefully: sbi.co.in is not sbi-kyc-update.in", "A padlock (https) only means the connection is encrypted, not that the site is genuine", "Be wary of shortened links (bit.ly and similar) in messages about money"] },
      { h: "Red flags in the message", list: ["Urgency: \"your account will be blocked today\"", "KYC, electricity bill or parcel messages asking you to click and pay", "Requests for OTP, PIN, CVV or passwords — banks never ask for these"] },
      { h: "If you already clicked", p: "Don't enter anything else. If you typed a password or card details, change the password and call your bank to block the card straight away. If money moved, call 1930." },
    ] },
  { slug: "fake-customer-care", icon: Phone, tint: "bg-[#e6e1d4]", minutes: 2,
    sources: [{ label: "Sanchar Saathi, Department of Telecommunications (Chakshu)", url: "https://sancharsaathi.gov.in" }, { label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }],
    title: "How to recognise fake customer care numbers",
    desc: "Scammers buy search ads and post fake helpline numbers.",
    body: [
      { h: "Where real numbers are", list: ["The back of your debit or credit card", "The official app or website you type in yourself", "Your passbook or bank statement"] },
      { h: "Signs it's a scam", list: ["They ask you to install a screen-sharing app such as AnyDesk or TeamViewer", "They ask you to enter your UPI PIN to \"receive\" a refund — a UPI PIN is only ever used to send money", "They ask for an OTP, or for a small \"verification\" payment"] },
      { h: "Report the number", p: "You can report suspected fraud calls and messages on the government's Sanchar Saathi portal (sancharsaathi.gov.in, under Chakshu)." },
    ] },
  { slug: "preserve-evidence", icon: ListChecks, tint: "bg-[#dde6ea]", minutes: 2,
    sources: [{ label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }],
    title: "How to preserve digital evidence",
    desc: "What to keep, and how, so your complaint holds up.",
    body: [
      { h: "Keep everything", list: ["Bank SMS and emails about the transaction", "Screenshots that show the date and time", "Chats, call logs and emails with the scammer — don't delete them", "The scammer's phone numbers, UPI IDs, websites and app names"] },
      { h: "Keep it safe", list: ["Put copies in one folder, and on a second device or in cloud storage", "Note down the timeline while you still remember it", "Don't open suspicious links again to take screenshots"] },
      { h: "Never share", p: "Evidence never includes your passwords, OTPs, PINs or CVV. No official will ask for them." },
    ] },
  { slug: "follow-up-complaint", icon: FileText, tint: "bg-[#e9e4f0]", minutes: 2,
    sources: [{ label: "National Cyber Crime Reporting Portal (I4C, MHA)", url: "https://cybercrime.gov.in" }, { label: "RBI Complaint Management System (Integrated Ombudsman)", url: "https://cms.rbi.org.in" }],
    title: "How to follow up on a cybercrime complaint",
    desc: "After you file: tracking, your bank and what to expect.",
    body: [
      { h: "Track it", p: "Use your acknowledgement number to check the status on cybercrime.gov.in. Your local cyber police station may contact you for details or a statement." },
      { h: "Keep your bank in the loop", p: "Share the cybercrime acknowledgement number with your bank and ask them to add it to your complaint. Ask for updates in writing." },
      { h: "Keep a log", list: ["Every call: date, who you spoke to, what they said", "Every reference number", "Copies of everything you send"] },
      { h: "Stay safe", p: "Scammers often target victims a second time, pretending to be police or \"recovery agents\". Officials won't ask you to pay to recover money." },
    ] },
];
export const SHIELD = ShieldCheck;
