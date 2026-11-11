"""Live check of WS /ws/call: stream synthetic victim speech in real time and print per-turn latency.

Start the server first (python3 -m uvicorn app.server:app), then: python3 smoke_call.py [ws-url] [hi|kn|ta]
Costs a few rupees of Gnani credits (TTS clips to fake the caller + live STT/TTS).
"""
import asyncio
import io
import json
import sys
import wave

import websockets

from app.gnani import tts

URL = sys.argv[1] if len(sys.argv) > 1 else "ws://127.0.0.1:8000/ws/call"
LANG = sys.argv[2] if len(sys.argv) > 2 else "hi"
SAYS = {"kn": ["ನನ್ನ ಎಸ್‌ಬಿಐ ಖಾತೆಯಿಂದ ನಲವತ್ತು ಸಾವಿರ ರೂಪಾಯಿ ಹೋಯಿತು, ಯುಪಿಐ ಮೂಲಕ.",
               "ಇಂದು ಮಧ್ಯಾಹ್ನ ಎರಡು ಗಂಟೆಗೆ.", "ಗೊತ್ತಿಲ್ಲ.", "ಪೊಲೀಸ್ ಎಂದು ಹೇಳಿದರು.",
               "ಯುಟಿಆರ್ ನಾಲ್ಕು ಒಂದು ಎರಡು ಮೂರು ನಾಲ್ಕು ಐದು ಆರು ಏಳು ಎಂಟು ಒಂಬತ್ತು ಸೊನ್ನೆ ಒಂದು.", "ಹೌದು."],
        "ta": ["என் எஸ்பிஐ கணக்கில் இருந்து நாற்பதாயிரம் ரூபாய் போனது, யுபிஐ மூலம்.",
               "இன்று மதியம் இரண்டு மணிக்கு.", "தெரியாது.", "போலீஸ் என்று சொன்னார்கள்.",
               "யுடிஆர் நான்கு ஒன்று இரண்டு மூன்று நான்கு ஐந்து ஆறு ஏழு எட்டு ஒன்பது பூஜ்ஜியம் ஒன்று.", "ஆமாம்."],
        "hi": ["मेरे एसबीआई खाते से चालीस हज़ार रुपये कट गए, यूपीआई से गए।",
        "आज दोपहर दो बजे।",
        "पता नहीं।",
        "बोला बिजली का बिल बकाया है।",
        "यूटीआर है चार एक दो तीन चार पाँच छह सात आठ नौ शून्य एक।",
        "हाँ, सही है।"]}[LANG]
FRAME, PACE = 1024, 0.032  # 512 samples at 16 kHz, sent in real time like a mic


def pcm(text):
    w = wave.open(io.BytesIO(tts(text, LANG)))
    return w.readframes(w.getnframes())


async def main():
    clips = [pcm(t) for t in SAYS]
    firsts = []
    url = URL + ("" if LANG == "hi" else "?lang=" + LANG)  # like picking the language on the page; Hindi stays auto
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
                    print(f"\nheard : {j['transcript']}\nreply : {j['question'] or j.get('verdict', '') + ' + checklist'}\ncase  : { {k: v for k, v in j['case'].items() if v is not None and k != 'meta'} }")
                elif j["type"] == "timings":
                    print(f"audio : {audio / 32000:.1f} s of reply speech\nms    : {j['ms']}")
                    firsts.append(j["ms"].get("first_audio_sent"))
                    audio = 0
                    done.set()
                elif j["type"] == "error":
                    print("error :", j["message"])

        receiver = asyncio.create_task(recv())
        await ws.send(json.dumps({"type": "init", "case": {}, "history": ""}))  # like the page: starts the greeting
        while not done.is_set():  # let the greeting finish, as a caller would
            await ws.send(bytes(FRAME)); await asyncio.sleep(PACE)
        print(f"greeting first audio: {firsts.pop()} ms after the call opened")
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
    print(f"\nfirst audio after end of speech (ms): {firsts}   target < 1500")


asyncio.run(main())
