// Run: node --experimental-strip-types src/lib/track.test.ts
import assert from "node:assert/strict";
import { addWorkingDays, EMPTY_TRACK, steps, summary } from "./track.ts";

const d = (s: string) => new Date(s + "T00:00:00");
const ymd = (x: Date | null) => x && `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(x.getDate()).padStart(2, "0")}`;

// 3 working days skip the weekend: Thu 12 Nov 2026 -> Tue 17 Nov.
assert.equal(ymd(addWorkingDays(d("2026-11-12"), 3)), "2026-11-17");
assert.equal(ymd(addWorkingDays(d("2026-11-09"), 3)), "2026-11-12");  // Mon -> Thu

// Nothing entered: report and bank wait for the fraud date; "safe" is ongoing.
const empty = steps(EMPTY_TRACK, d("2026-11-13"));
assert.deepEqual(empty.map(s => s.state), ["waiting", "waiting", "waiting", "waiting", "ongoing"]);

// Fraud yesterday, nothing done: reporting is overdue, the bank complaint is due by Tue 17 Nov.
const t = { ...EMPTY_TRACK, fraudDate: "2026-11-12" };
let s = steps(t, d("2026-11-13"));
assert.equal(s[0].state, "overdue");
assert.equal(s[1].state, "upcoming"); assert.equal(ymd(s[1].due), "2026-11-17");

// Reported with an ack number and bank complaint filed: those are done; follow-ups get dates.
const t2 = { ...t, reportedOn: "2026-11-12", ackNo: "31511240012345", bankFiledOn: "2026-11-13", bankRef: "SBI123" };
s = steps(t2, d("2026-11-13"));
assert.deepEqual(s.map(x => x.state), ["done", "done", "upcoming", "upcoming", "ongoing"]);
assert.equal(ymd(s[2].due), "2026-11-19"); assert.equal(ymd(s[3].due), "2026-12-13");
// 30 days later the ombudsman step is due today, then overdue; ticking it marks it done.
assert.equal(steps(t2, d("2026-12-13"))[3].state, "today");
assert.equal(steps(t2, d("2026-12-20"))[3].state, "overdue");
assert.equal(steps({ ...t2, done: ["ombudsman"] }, d("2026-12-20"))[3].state, "done");
// A typed but malformed date is ignored rather than crashing.
assert.equal(steps({ ...EMPTY_TRACK, fraudDate: "12/11/2026" }, d("2026-11-13"))[0].state, "waiting");
assert.ok(summary(t2, d("2026-11-13")).includes("[x] Report to 1930"));
console.log("track ok");
