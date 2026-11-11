"""Live check of WS /ws/call: stream synthetic victim speech in real time and print per-turn latency.

Start the server first (python3 -m uvicorn app.server:app), then: python3 smoke_call.py [ws-url] [hi|kn|ta]
Costs a few rupees of Gnani credits (TTS clips to fake the caller + live STT/TTS).
"""
import asyncio
import io
import json
import sys
import time
import wave

import websockets

from app.gnani import tts

FRAME, PACE = 1024, 0.032  # 512 samples at 16 kHz, sent in real time like a mic
SAYS = {"kn": ["ನನ್ನ ಎಸ್‌ಬಿಐ ಖಾತೆಯಿಂದ ನಲವತ್ತು ಸಾವಿರ ರೂಪಾಯಿ ಹೋಯಿತು, ಯುಪಿಐ ಮೂಲಕ.",
               "ಇಂದು ಮಧ್ಯಾಹ್ನ ಎರಡು ಗಂಟೆಗೆ.", "ಗೊತ್ತಿಲ್ಲ.", "ಪೊಲೀಸ್ ಎಂದು ಹೇಳಿದರು.",
               "ಯುಟಿಆರ್ ನಾಲ್ಕು ಒಂದು ಎರಡು ಮೂರು ನಾಲ್ಕು ಐದು ಆರು ಏಳು ಎಂಟು ಒಂಬತ್ತು ಸೊನ್ನೆ ಒಂದು.", "ಹೌದು."],
        "ta": ["என் எஸ்பிஐ கணக்கில் இருந்து நாற்பதாயிரம் ரூபாய் போனது, யுபிஐ மூலம்.",
               "இன்று மதியம் இரண்டு மணிக்கு.", "தெரியாது.", "போலீஸ் என்று சொன்னார்கள்.",
               "யுடிஆர் நான்கு ஒன்று இரண்டு மூன்று நான்கு ஐந்து ஆறு ஏழு எட்டு ஒன்பது பூஜ்ஜியம் ஒன்று.", "ஆமாம்."],
        "hi": ["मेरे एसबीआई खाते से चालीस हज़ार रुपये कट गए, यूपीआई से गए।", "आज दोपहर दो बजे।", "पता नहीं।",
               "बोला बिजली का बिल बकाया है।", "यूटीआर है चार एक दो तीन चार पाँच छह सात आठ नौ शून्य एक।",
               "हाँ, सही है।"]}


def pcm(text, lang):
    w = wave.open(io.BytesIO(tts(text, lang)))
    return w.readframes(w.getnframes())


async def call(url, lang, log=print):
    """One full call. Returns greeting/turn latencies (ms) and usage: seconds streamed to STT, characters spoken."""
    clips = [pcm(t, lang) for t in SAYS[lang]]
    out = {"lang": lang, "first_audio_ms": [], "tts_chars": 0, "turns_answered": 0}
    url += "" if lang == "hi" else "?lang=" + lang  # like picking the language on the page; Hindi stays auto
    t0 = time.monotonic()
    async with websockets.connect(url, max_size=None) as ws:
        done = asyncio.Event()

        async def recv():
            audio = 0
            async for m in ws:
                if isinstance(m, bytes):
                    audio += len(m)
                    continue
                j = json.loads(m)
                if j["type"] == "turn":
                    out["turns_answered"] += 1
                    log(f"\nheard : {j['transcript']}\nreply : {j['question'] or j.get('verdict', '') + ' + checklist'}")
                elif j["type"] == "timings":
                    log(f"audio : {audio / 32000:.1f} s of reply speech\nms    : {j['ms']}")
                    out["first_audio_ms"].append(j["ms"].get("first_audio_sent"))
                    out["tts_chars"] += j.get("chars", 0)
                    audio = 0
                    done.set()
                elif j["type"] == "error":
                    log("error : " + j["message"])

        receiver = asyncio.create_task(recv())
        await ws.send(json.dumps({"type": "init", "case": {}, "history": ""}))  # like the page: starts the greeting
        while not done.is_set():  # let the greeting finish, as a caller would
            await ws.send(bytes(FRAME)); await asyncio.sleep(PACE)
        out["greeting_ms"] = out["first_audio_ms"].pop()
        log(f"greeting first audio: {out['greeting_ms']} ms after the call opened")
        for clip in clips:
            done.clear()
            for i in range(0, len(clip), FRAME):
                await ws.send(clip[i:i + FRAME].ljust(FRAME, b"\0"))
                await asyncio.sleep(PACE)
            for _ in range(int(20 / PACE)):  # keep the line live (silence) until the reply finishes, max 20 s
                if done.is_set():
                    break
                await ws.send(bytes(FRAME))
                await asyncio.sleep(PACE)
        receiver.cancel()
    out["stt_seconds"] = round(time.monotonic() - t0, 1)  # the mic streams for the whole call
    return out


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "ws://127.0.0.1:8000/ws/call"
    r = asyncio.run(call(url, sys.argv[2] if len(sys.argv) > 2 else "hi"))
    print(f"\nfirst audio after end of speech (ms): {r['first_audio_ms']}   target < 1500")
