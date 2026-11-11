# Golden Hour

**A voice helpline for victims of UPI and bank fraud, in eight Indian languages.**
Live: **https://golden-hour-bigo.onrender.com** (free plan: the first visit after 15 idle minutes takes about a minute to wake)

When money is stolen through UPI or a bank transfer, India's 1930 cyber-fraud helpline can ask banks to hold it, but only while it is still sitting in the fraudster's accounts. That window is the "golden hour". Victims usually spend it panicking. They don't know what to do first and can't find their UTR, so the 1930 call takes longer than it should.

Golden Hour is a voice agent the victim can talk to right away, in their own language. It:
- tells them to call 1930 now if the fraud was recent;
- collects exactly what 1930 and the bank will ask for, reading every ID back to confirm it;
- ends with a clear verdict, the official steps, a case card to read out on the 1930 call, a ready-to-paste cybercrime.gov.in complaint, and an email to the bank.

It does not file anything or promise recovery. It gets the victim to the right people faster, with the right details.

## A call, step by step

1. **The caller taps the mic** (and optionally picks a language). The agent greets them and says it is not a government service and cannot recover money.
2. **The caller explains in their own words**, for example "मेरे SBI खाते से 40,000 रुपये कट गए, UPI से।" The agent fills in amount, bank and payment mode from that one sentence.
3. **It asks only what's still missing:** when it happened, the scammer's number or UPI ID, what they said, and the UTR. "पता नहीं" (don't know) skips a question, and "नहीं, 50,000 थे" corrects a field.
4. **If the fraud was recent,** it says once that every minute counts, and a countdown ("40m ago") appears next to the Call 1930 button.
5. **It reads the UTR back digit by digit** ("4 1 2 3, 4 5 6 7, 8 9 0 1 — सही है?") and waits for a yes.
6. **It speaks a verdict and the steps.** The verdict is something like "यह 40 मिनट पहले हुआ है, इसलिए पैसा रोके जाने का अभी भी मौका है।" The page shows a **Call 1930** button, an **Email your bank** button (pre-filled), the case card and the complaint.

The caller can **talk over the agent at any time** (barge-in), or type instead of speaking.

## Gnani models used

| Model | How it's used |
|---|---|
| **Prisma v3** streaming STT (`wss://api.vachana.ai/stt/v3/stream`) | Live call. The browser mic streams 16 kHz audio and Prisma's voice activity detection ends each utterance. Bank, app and scam terms are passed as `keyterms`. The language is locked when the caller picks one. |
| **Prisma v3** REST STT | Tap-to-record fallback when the live call can't connect. |
| **Timbre v3** streaming TTS (SSE, voice Shivani) | Every reply, sentence by sentence, in the caller's language. The first audio plays while later sentences are still being made. |
| **Timbre v3** REST TTS | Fallback replies. |

No LLM is needed. Fields are pulled out with rules written for how Prisma transcribes Indian speech: digits for numbers, English terms in Latin script, and number words in regional languages. An LLM can be switched on (`EXTRACTOR=groq|gemini|custom`), but it may only fill fields the rules missed. Any ID or phone number it returns is dropped unless those digits were actually said.

## Languages

Hindi, Hinglish, English, Kannada, Tamil, Telugu, Bengali and Marathi. Every question, confirmation, verdict, checklist and greeting is in each language, spoken with Timbre.

- **Auto mode** uses Prisma's detected language, then the script. Romanized Hindi gets Hindi replies.
- **Picking a language** locks speech recognition to it. In the eval, auto-detect identified only 65% of regional-language statements, against 100% when locked.

## Numbers

The full method and caveats are in [`eval/REPORT.md`](eval/REPORT.md).

| | Result |
|---|---|
| Field accuracy, clean speech (34 synthetic cases, 7 languages) | 98.2% |
| Field accuracy under 5 dB babble, or a telephone band | 92.8% |
| First reply audio after the caller stops (36 live turns on Render) | p50 1.12 s, p90 1.22 s, all under 1.5 s |
| Usage per full call | 52 s STT and 1,136 TTS characters (≈ ₹2–4 at public market rates) |

The eval also found a real bug: regional-language number words weren't understood, so fraud times like "ಎರಡು ಗಂಟೆಗೆ" (2 o'clock) were missed. Fixing it raised clean field accuracy from 89% to 98%.

## Safety and privacy

- **Hard-coded, reviewed steps.** The checklist, verdict and complaint are fixed templates, never generated. The verdict says how urgent things are; it never promises the money back.
- **Disclaimer.** Spoken at the start of every call and shown on every screen.
- **Nothing stored.** The case lives in the open connection and the page, and is gone when the call ends. Server logs hold timings only, never transcripts.
- **Synthetic data only.** All test and eval data is made up; there is no real PII.
- **Secrets.** The API key comes from the environment (a Render secret in production), never from git.
- **Abuse limits.** There is no login, and every call spends Gnani credit, so `app/guard.py` caps live calls (3 at once and 30 an hour per visitor, 20 at once and 400 a day in total), typed turns, and the size of every input. Requests from other websites are refused. The page runs under a strict Content Security Policy (no external scripts, styles or fonts), and the container runs as a non-root user. The limits live in memory, so they reset on restart and need Redis if the app ever runs on more than one instance.

## How it works

```
Browser                                Server (FastAPI, app/)                       Gnani
mic ─AudioWorklet 16 kHz─► WS /ws/call ──── stream.py: relay audio ───────────► Prisma streaming STT
                                             ◄── transcript ────────────────────
                                             flow.advance(): rules.extract → merge
                                             (ID guard) → corrections / read-back /
                                             next question / verdict + checklist
speaker ◄─ PCM, sentence by sentence ─────── Timbre SSE, one sentence at a time ◄─ Timbre streaming TTS
barge-in: the page hears the caller over the agent → stops playback → server cancels the reply
```

| File | What it does |
|---|---|
| `app/flow.py` | The conversation: questions, corrections, read-back, urgency, verdict, checklist, complaint, all languages |
| `app/rules.py` | Field extraction: amounts, banks, payment modes, scam types, times and number words in every language |
| `app/stream.py` | The live call: STT relay, streaming TTS, barge-in, the greeting, timings |
| `app/server.py` | The page, `WS /ws/call`, `POST /turn` (the fallback), and security headers |
| `app/guard.py` | Rate limits, input size caps, and the same-origin check |
| `app/gnani.py` | Prisma and Timbre clients |
| `app/static/index.html` | The whole front end: a single page, no build step |
| `eval/` | Accuracy under noise, live latency, cost; `REPORT.md` |

## Run locally

```bash
pip install fastapi requests python-multipart uvicorn websockets
cp .env.example .env        # then put your GNANI_API_KEY in .env
python3 -m uvicorn app.server:app --port 8000
```

Open http://localhost:8000 in Chrome and tap the mic. Press the backtick key (`` ` ``) for the latency panel.

```bash
python3 test_flow.py && python3 test_stream.py && python3 test_guard.py   # offline tests
python3 smoke_call.py ws://127.0.0.1:8000/ws/call kn   # a full live call in hi | kn | ta (uses Gnani credit)
python3 -m eval.run                               # accuracy under noise (uses credit; cached in eval/cache/)
python3 -m eval.latency wss://golden-hour-bigo.onrender.com/ws/call 2
```

## Deploy

The live call needs a long-lived WebSocket, which serverless hosts such as Vercel don't keep open, so the app ships as a Docker image.

On Render (free): **New → Blueprint**, pick this repo (it reads `render.yaml`), and paste `GNANI_API_KEY` when asked. Every push to `main` redeploys.

Anywhere else:

```bash
docker build -t golden-hour .
docker run -p 8000:8000 --env-file .env golden-hour
```

## Limits and next steps

- **Untested with real voices.** All eval audio is synthetic, from one voice. Recordings from real callers come next.
- **Translations need a native check.** The Kannada, Tamil, Telugu, Bengali and Marathi strings were written by the developer and need native review.
- **Barge-in threshold.** The loudness level that counts as the caller talking is fixed. It should be tuned on real phones and speakers.
- **Telephone line.** The natural next step is a phone number, an Exotel or Twilio bridge to the same `/ws/call`, so victims without a smartphone can call in. Better still, it could sit in front of the 1930 line itself and hand the officer a finished case.
