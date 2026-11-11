# Golden Hour

A voice assistant for victims of UPI and bank fraud in India. It talks to the caller in Hindi, Hinglish, English, Kannada, Tamil, Telugu, Bengali or Marathi, asks for the details the 1930 helpline and the bank need (amount, payment mode, bank, time, UTR), then gives the next steps, a ready-to-paste complaint and an email to the bank.

Built on Gnani's Prisma streaming speech-to-text and Timbre text-to-speech. Synthetic data only. Nothing is stored after a call ends.

## Run locally

```bash
pip install fastapi requests python-multipart uvicorn websockets
cp .env.example .env        # then put your GNANI_API_KEY in .env
python3 -m uvicorn app.server:app --port 8000
```

Open http://localhost:8000 in Chrome and tap the mic. Press the backtick key (`` ` ``) for the latency panel.

Tests: `python3 test_flow.py && python3 test_stream.py` (offline), `python3 smoke_call.py` (live call; needs the server running and costs a few rupees of Gnani credit).

## Evaluation

[`eval/REPORT.md`](eval/REPORT.md) has the full numbers. In short:
- **Field accuracy:** 98.2% on 34 synthetic cases in 7 languages, and 92.8% under 5 dB babble or a telephone band.
- **Latency:** 36 live turns on the deployed app, first reply audio p50 1.12 s and p90 1.22 s, all under 1.5 s.
- **Usage:** about 52 s of STT and 1,100 TTS characters per call.

```bash
python3 -m eval.run                 # accuracy under noise (Gnani credits; cached in eval/cache/)
python3 -m eval.latency wss://golden-hour-bigo.onrender.com/ws/call 2
python3 -m eval.test_eval           # offline check of the eval maths
```

## Deploy (Render, free)

The live call needs a long-lived WebSocket, which serverless hosts such as Vercel don't keep open. Render runs the Docker image instead.

1. Push this repo to GitHub.
2. In Render, choose **New → Blueprint** and pick the repo. It reads `render.yaml`.
3. When asked, paste `GNANI_API_KEY`. It is stored as a Render secret, not in git.

Every push to `main` then redeploys. The free plan sleeps after 15 minutes idle, and the first request after that takes about a minute, so open the URL once before a demo.

Any Docker host works the same way:

```bash
docker build -t golden-hour .
docker run -p 8000:8000 -e GNANI_API_KEY=... golden-hour
```

The container listens on `$PORT` (default 8000).
