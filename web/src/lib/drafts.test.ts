// Run: node --experimental-strip-types src/lib/drafts.test.ts
import assert from "node:assert/strict";
import { bankEmailDraft, complaintDraft, EMPTY, followUpEmail, incidentSummary, validate } from "./drafts.ts";

const ok = { ...EMPTY, name: "Asha Verma", phone: "98765 43210", email: "", bank: "State Bank of India", accountType: "Savings account",
  date: "2026-11-12", time: "14:05", category: "UPI Fraud", amount: "40,000", utr: "412345678901",
  description: "A caller said my KYC had expired and sent a link. I paid through it.", branch: "" };
const now = new Date("2026-11-12T18:00:00");

assert.deepEqual(validate(ok, now), {});
const bad = validate({ ...EMPTY, phone: "12345", date: "2027-01-01", amount: "-5", utr: "41@3" }, now);
for (const k of ["name", "phone", "bank", "accountType", "date", "category", "amount", "utr", "description"]) assert.ok(k in bad, k);
// secrets are refused wherever they're typed
assert.ok(validate({ ...ok, description: "He asked for the OTP and I told him 482913, then money went." }, now).description);
assert.ok(validate({ ...ok, description: "Card 4111 1111 1111 1111 was charged twice by the fake shop." }, now).description);
assert.ok(!validate({ ...ok, description: "He asked for my OTP but I did not share it. Money still went." }, now).description);

const c = complaintDraft(ok, now), m = bankEmailDraft(ok);
assert.ok(c.includes("Rs. 40,000") && c.includes("412345678901") && c.includes("12 November 2026, 14:05") && c.includes("Asha Verma"));
assert.ok(c.includes("(UPI Fraud)") && m.includes("the result of UPI Fraud"), "acronyms keep their case");
assert.ok(m.includes("Subject: Fraudulent transaction of Rs. 40,000 on 12 November 2026") && m.includes("XXXX"));
assert.ok(!/@\w+\.(com|in)/.test(m), "never invents a bank email address");
assert.ok(bankEmailDraft({ ...ok, utr: "" }).includes("UTR: not available"));
const sum = incidentSummary(ok), fu = followUpEmail(ok);
assert.ok(sum.includes("Amount lost: Rs. 40,000") && sum.includes("UPI Fraud") && sum.includes("Asha Verma"));
assert.ok(fu.includes("Follow-up on my complaint") && fu.includes("[add your bank complaint reference]") && fu.includes("RBI Ombudsman"));
assert.ok(!/@\w+\.(com|in)/.test(fu), "never invents a bank email address");
console.log("drafts ok");
