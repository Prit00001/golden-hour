# Golden Hour — SDLC Plan

Voice-first fraud-response assistant built on Gnani AI.
A scam victim speaks (Hindi / Hinglish / other supported languages) → the app extracts the fraud details,
speaks the official recovery steps (1930 → bank freeze → cybercrime.gov.in), and produces a
pre-filled complaint + bank email.

- **Deadline:** 10 Nov 2026, 11:59 PM IST (no extensions)
- **Demo post live:** 6 Nov evening (engagement needs time to build)
- **Model:** Iterative / time-boxed (Agile-lite). Each phase ends with a gate; anything not done by its gate is cut, not delayed.

---

## Phase 1 — Planning (31 Oct)

| Task | Done when |
|---|---|
| Register on app.gnani.ai, get API key | Key works on one STT + one TTS call |
| Measure credit burn (credits per STT minute / TTS char) | ✅ 31 Oct: 1 credit = ₹1. STT prisma-v3.0 ≈ 0.45–0.5 credits/min; TTS timbre-v3.0 ≈ 0.27 credits/100 chars. 5,000 credits ≈ 10,000 STT min or ~1.8M TTS chars — not a constraint |
| Check Evon weights at huggingface.co/gnani/gnani-evon-v3.3-30B-A3B | Decide: Evon or fallback LLM |
| Lock scope (MVP below) | Nothing new added after this |

**Risks register**

| Risk | Impact | Mitigation |
|---|---|---|
| "ChatGPT can already do this" | High | Demo must show structured extraction + exact Indian sequence + filled complaint |
| Credits run out | High | Cache test audio results; use REST only for short clips |
| Evon unavailable / rules on external LLM unclear | Medium | Keep Gnani central for speech in/out; LLM only for extraction |
| LLM invents wrong steps | High | Steps are hard-coded, LLM only fills fields |
| Looks like a govt service / "recovery agent" | High | Clear disclaimer; never promise recovery |
| Real PII in demo | Disqualification | Synthetic data only |

---

## Phase 2 — Requirements (31 Oct – 1 Nov)

**Users:** fraud victim (often elderly / low-literacy), family member helping them.

**Functional (MVP — must have)**
1. FR1: User records or streams speech describing the fraud (Prisma STT, `indic-auto` language detection).
2. FR2: Extract fields: amount, date/time, payment mode (UPI/card/netbanking), txn/UTR ID, scammer number/UPI ID, bank, scam type.
3. FR3: Ask by voice for any missing field (Timbre TTS), loop until required fields filled.
4. FR4: Speak the action checklist in the user's language: call 1930 now → call bank to freeze → file on cybercrime.gov.in.
5. FR5: Generate pre-filled complaint text (copy-ready for cybercrime.gov.in) and bank email.
6. FR6: Show "time since fraud" urgency banner.

**Nice to have (only if MVP is done by 4 Nov)**
- Speakerphone "is this call a scam?" check.
- Download complaint as PDF.

**Non-functional**
- End-to-end response < 3 s after user stops speaking.
- Works on mobile browser.
- Stores nothing server-side (privacy, DPDP Act).
- Disclaimer visible on every screen.

**Out of scope:** auto-submitting to cybercrime.gov.in (no API, CAPTCHA), real bank integration.

---

## Phase 3 — Design (1 – 2 Nov)

```
Browser (React)
  mic ──WebSocket──► FastAPI ──► Gnani Prisma STT (wss stream / REST ≤30 s)
                       │
                       ├─► LLM extraction → JSON schema (FR2)
                       ├─► Rules engine: missing fields? → next question (FR3)
                       │                 all filled?     → checklist (FR4)
                       ├─► Template → complaint + bank email (FR5)
                       └─► Gnani Timbre TTS ──► audio back to browser
```

**Core schema**
```json
{
  "amount": null, "datetime": null, "payment_mode": null,
  "txn_id": null, "scammer_contact": null, "bank": null,
  "scam_type": null, "language": null
}
```

**API**
- `WS /stream` — audio in, transcript + TTS audio out
- `POST /extract` — transcript → schema JSON
- `POST /complaint` — schema → complaint text + bank email

---

## Phase 4 — Implementation (2 – 5 Nov)

| Day | Build |
|---|---|
| 2 Nov | FastAPI skeleton, Gnani STT + TTS round-trip working |
| 3 Nov | LLM extraction + missing-field question loop |
| 4 Nov | Checklist speech, complaint/email templates, React UI |
| 5 Nov | Polish UI, disclaimer, urgency banner; code freeze 8 PM |

---

## Phase 5 — Testing (5 – 6 Nov)

**Test set:** 20 synthetic victim recordings (record yourself + friends): Hindi, Hinglish, English, 1–2 other
supported languages, some with background noise.

| Metric | Target |
|---|---|
| Field extraction accuracy (per field, vs hand-labelled) | ≥ 85% |
| Required fields completed after follow-up questions | 100% |
| Response latency | < 3 s |
| Checklist order correct | 100% (hard-coded) |
| Complaint text has no hallucinated values | 100% |

---

## Phase 6 — Deployment & Demo (6 – 7 Nov)

- Deploy (Render / Railway / HF Spaces); demo from a phone.
- **60-second video:** panicked Hinglish voice → app asks 1–2 questions → speaks steps → filled complaint on screen.
- Post on LinkedIn + X: tag Gnani AI, `#GnaniAI #GreatIndianAIInternshipChallenge`, Hindi/English captions,
  end with a question ("Has someone in your family been scammed?").
- Teaser post on 3–4 Nov.

---

## Phase 7 — Maintenance (7 – 10 Nov)

- Reply to every comment; fix bugs people report.
- Submit form with title, problem, users, Gnani models used, contributions — **by 9 Nov**, one day of buffer.
