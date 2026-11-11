# Golden Hour evaluation

What was measured, on 12 Nov 2026, with the code in this commit. Raw numbers are in [`results.json`](results.json); per-case transcripts are under `accuracy.rows`.

| | Result |
|---|---|
| Field accuracy, clean speech (34 cases, 7 languages) | **98.2%** |
| Field accuracy, 5 dB babble / telephone band | **92.8% / 92.8%** |
| First reply audio after the caller stops (36 live turns on Render) | **p50 1.12 s, p90 1.22 s, max 1.30 s**, all under 1.5 s |
| Greeting starts after the call opens | p50 0.45 s |
| Usage per call (greeting + 6 turns) | 52 s STT, 1,136 TTS characters, ≈ ₹2–4 at public market rates |

## 1. Accuracy under noise

**Method.** [`cases.py`](cases.py) has 34 synthetic victim statements: 12 Hindi, 5 English, 5 Kannada, 5 Tamil, 3 Telugu, 2 Bengali, 2 Marathi. Each lists the fields a correct system should pull out: amount, bank, payment mode, UTR, scammer number or UPI ID, scam type, and fraud time.

Each case goes through:
1. Timbre TTS.
2. One of six conditions: clean; babble (three other speakers) at 15 and 5 dB SNR; pink noise at 15 and 5 dB; or a 300–3400 Hz telephone band.
3. Prisma STT. Hindi and English use auto-detect. Regional languages are locked to their language, which is what the page's language picker does.
4. The same rules extractor the app uses.

That makes 221 STT calls. Run it with `python3 -m eval.run` (`--rescore` re-scores cached transcripts at no cost).

| Condition | WER | Field accuracy | Cases fully right |
|---|---|---|---|
| clean | 16.3% | 98.2% | 94.1% |
| babble 15 dB | 17.1% | 97.3% | 91.2% |
| babble 5 dB | 21.2% | 92.8% | 79.4% |
| pink 15 dB | 16.4% | 97.3% | 91.2% |
| pink 5 dB | 16.2% | 96.4% | 88.2% |
| telephone band | 18.1% | 92.8% | 76.5% |

| Language (clean) | Cases | WER | Field accuracy |
|---|---|---|---|
| Hindi | 12 | 19.8% | 100% |
| English | 5 | 2.7% | 93.8% |
| Kannada | 5 | 18.3% | 92.9% |
| Tamil | 5 | 11.9% | 100% |
| Telugu | 3 | 11.4% | 100% |
| Bengali | 2 | 40.4% | 100% |
| Marathi | 2 | 19.2% | 100% |

Per field on clean speech, amount, bank, payment mode, scam type and time are all at 100%. UTR and scammer contact are at 80%. Those two errors are the remaining failures:
- Prisma misheard one UTR digit (5678**2**…).
- Prisma heard "paytm" as "payatm".

The bot reads IDs back digit by digit for the caller to confirm, so both would be caught in a real call.

**Why WER is higher than field accuracy.** Prisma writes English loanwords in Latin script ("update", "call", "account"), while the references spell them in Devanagari or Bengali script. Every one of those counts as a word error even when the meaning is identical. That is most of the Hindi and Bengali WER. Field accuracy is the number that matters for the product.

**Why the language picker exists.** Regional languages on clean audio:

| Regional STT mode | WER | Field accuracy | Language identified |
|---|---|---|---|
| auto-detect | 28.5% | 96.2% | 64.7% |
| locked to the chosen language | 17.9% | 98.1% | 100% |

Auto-detect labelled about a third of the regional statements as another language. That's how a live Kannada call drifted into Hindi before the picker was added: replies come in the language detected.

## 2. Robustness fix found by this eval

The first run scored 87.4% field accuracy on clean speech, and fraud time was right only 22% of the time. The failures had four causes, all in the extraction rules:

1. **Regional number words.** Prisma writes small numbers as words in regional languages: "ಎರಡು ಗಂಟೆಗೆ" (2 o'clock), "ஒன்பது மணிக்கு" (9 o'clock), "అరవై వేలు" (sixty thousand). `rules.normalize` only knew Hindi number words. Added 0–12 and the tens in Kannada, Tamil, Telugu, Bengali and Marathi. Bengali নয় (9) is left out because it also means "not", which the read-back depends on.
2. **"টাকা" read as a clock time.** In "20,000 টাকা" (taka), "00 টা" matched as 12 o'clock. The o'clock suffix now can't be the start of "টাকা", and a clock hour can't be the tail of a bigger number.
3. **Two time phrases in one sentence.** "अभी 20 minute पहले" kept the bare "अभी" (now). The phrase that contains a number now wins.
4. **Regional-script payment and scam words.** Added ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್, ஓடிபி, கார்டு, the spelling ಪುಲೀಸ್ and similar terms.

Same cached transcripts, old code against new:

| | Field accuracy, clean | Field accuracy, 5 dB babble | Time field, clean | Cases fully right, clean |
|---|---|---|---|---|
| before | 89.2% | 87.4% | 44.4% | 73.5% |
| after | **98.2%** | **92.8%** | **100%** | **94.1%** |

Each fix has a regression test at the end of `test_flow.py`.

I also fixed two mistakes in the eval itself. Two cases put the fraud at 4 pm when "now" is 3 pm. The parser was right to move those to yesterday, so I moved the cases to 1 pm. The "before" row above already includes that change, so the comparison only measures the code fix.

## 3. Latency on the deployed app

**Method.** `python3 -m eval.latency wss://golden-hour-bigo.onrender.com/ws/call 2` runs full calls against the live Render deployment (Singapore): 2 calls each in Hindi (auto), Kannada and Tamil (picked). Each call is the greeting plus 6 turns, with the caller's speech streamed at real-time pace.

The timer starts at the estimated end of speech. Gnani sends no end-of-speech event, so this is the transcript time minus Prisma's 600 ms silence window and its reported latency. The timer stops when the first reply audio leaves the server.

| | p50 | p90 | max | under 1.5 s |
|---|---|---|---|---|
| all turns (n = 36) | 1122 ms | 1216 ms | 1299 ms | 100% |
| Hindi | 1120 ms | 1205 ms | 1258 ms | 100% |
| Kannada | 1125 ms | 1221 ms | 1299 ms | 100% |
| Tamil | 1122 ms | 1187 ms | 1242 ms | 100% |
| greeting after the call opens (n = 6) | 448 ms | 789 ms | 1029 ms | 100% |

All 36 turns were answered.

**Where the time goes**, from the per-stage timings in the debug panel (backtick key):

| Stage | Time |
|---|---|
| Waiting for 600 ms of silence | ~600 ms |
| Prisma finalising the transcript | ~100–170 ms |
| Extraction | 1–5 ms |
| Timbre first audio byte | ~300–450 ms |

The silence wait is the biggest single cost. Lowering it would cut slow speakers off mid-sentence.

## 4. Cost per call

A full call (greeting, 6 turns, verdict and checklist) streams **52 s** of microphone audio to Prisma. The mic streams for the whole call, so that's what STT bills. It speaks **1,136 characters** through Timbre. These are averages of one Hindi, one Kannada and one Tamil call, counted by the server.

Gnani publishes no prices; the programme gives 5,000 credits with no stated conversion. At Sarvam's public rates (STT ₹30/hour, TTS ₹15–30 per 10K characters), the same usage would cost **₹2.1–3.8 per call**. That's well under the $0.07–0.19 per minute typical for commercial voice agents.

## 5. Limits

- **One voice.** All caller audio is Timbre's Shivani voice, the same voice the bot uses, so accuracy is an upper bound. Real callers have different voices, accents and microphones, and they hesitate. The next step is recordings from real speakers.
- **No held-out set.** The fixes in section 2 were made after looking at failures in these same 34 cases. They are general vocabulary and parsing fixes, not per-case hacks, but expect a fresh set to score a bit lower.
- **Simulated noise.** Babble uses the same voice. The telephone band is a filter, not a real codec or packet loss.
- **Latency excludes the network.** It doesn't include the browser↔server trip (about 50–80 ms from India to Singapore) or the 50 ms playback buffer in the page.
- **Missing cases.** 34 cases is small, and Telugu, Bengali and Marathi have only 2–3 each. There are no multi-turn correction cases here; those are covered by `test_flow.py`.
