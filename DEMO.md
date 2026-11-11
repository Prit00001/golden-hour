# 2-minute demo script

For the submission video. Total 2:00. Record the screen with your voice, using the live site.

## Before you record

- [ ] Open https://golden-hour-bigo.onrender.com about a minute early (the free server sleeps after 15 idle minutes).
- [ ] Use Chrome and allow the microphone. **Wear headphones**, so the bot doesn't hear itself and barge-in only triggers on your voice.
- [ ] Use a dark-mode or clean browser window, zoom at 110%, and close other tabs.
- [ ] Do one full rehearsal call, then reload the page (a fresh page means a fresh case).
- [ ] Every number below is made up. Don't use real account or phone numbers.
- [ ] Backup: if the mic misbehaves, type the same lines in the box. The flow is identical.

## Script

| Time | On screen | You say (narration in *italics*, lines to the bot in quotes) | The bot does |
|---|---|---|---|
| 0:00–0:12 | Home page, red "Call 1930" bar | *"When money is stolen over UPI, India's 1930 helpline can ask banks to hold it, but only in the first hours. Most victims lose that hour panicking. Golden Hour is a voice helpline for that hour."* | — |
| 0:12–0:20 | Tap the 🎤 | *(stay quiet)* | Greets you and says it's not a government service and can't recover money. |
| 0:20–0:30 | Watch "Your case" fill in | "मेरे SBI खाते से 40,000 रुपये कट गए, UPI से।" | Amount, bank and payment mode tick ✓ at once. Asks when. |
| 0:30–0:40 | The ⏱ countdown appears in the red bar | "30 मिनट पहले।" | Says every minute counts, then asks for the scammer's number. |
| 0:40–0:47 | **Barge-in:** speak over it mid-sentence | "पता नहीं।" | Stops talking straight away, marks "not known", asks what they said. |
| 0:47–0:53 | — | "बोला KYC अपडेट करना है।" | Scam type ✓. Asks for the UTR. |
| 0:53–1:10 | Point at "confirming…" | "UTR है 4123 4567 8902।" then, after the read-back: "नहीं, 4123 4567 8901।" then: "हाँ।" | Reads it back digit by digit, takes the correction, reads it back again, then marks it ✓ confirmed. |
| 1:10–1:25 | Scroll to the results | *"It ends with a verdict, the official steps, a card to read out on the 1930 call, the complaint for cybercrime.gov.in, and a pre-filled email to the bank."* | Speaks the verdict ("…पैसा रोके जाने का अभी भी मौका है") and the steps. |
| 1:25–1:40 | **Reload the page** (fresh case), tap **ಕನ್ನಡ**, tap 🎤 | "ನನ್ನ SBI ಖಾತೆಯಿಂದ 40,000 ರೂಪಾಯಿ ಹೋಯಿತು." *"Eight languages: Hindi, English, Kannada, Tamil, Telugu, Bengali, Marathi and Hinglish."* | Greets in Kannada, fills amount and bank, and asks the next question in Kannada. |
| 1:40–1:52 | Press the backtick key to show the latency panel, then show the README numbers | *"About 1.1 seconds from when you stop speaking to its reply. 98% of details captured correctly on clean speech, 93% in heavy noise, across seven languages."* | — |
| 1:52–2:00 | Back to the home page | *"Built on Gnani Prisma and Timbre, no LLM, nothing stored. Next step: a phone line in front of 1930 itself."* | — |

## If you're running long

- Cut the Kannada beat to just tapping ಕನ್ನಡ and showing the greeting (saves about 10 s).
- Skip the wrong-UTR correction: say the right UTR, then "हाँ" (saves about 8 s).
- Speed up the bot's long checklist 1.5× in the edit, but keep the verdict line at normal speed.

## For the written submission

Declare the Gnani models used:
- **Prisma v3**: streaming STT for the live call, REST STT for the fallback.
- **Timbre v3**: SSE streaming TTS with the Shivani voice, REST TTS for the fallback.

No other model is used by default.

Links to include:
- Live app: https://golden-hour-bigo.onrender.com
- Code: https://github.com/Prit00001/golden-hour
- Numbers: `eval/REPORT.md`
