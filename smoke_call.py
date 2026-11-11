"""Live check of WS /ws/call: stream synthetic victim speech in real time and print per-turn latency.

Start the server first (python3 -m uvicorn app.server:app), then: python3 smoke_call.py [ws-url]
Costs a few rupees of Gnani credits (3 TTS clips to fake the caller + live STT/TTS).
"""
import asyncio
import io
import json
import sys
import wave

import websockets

from app.gnani import tts

URL = sys.argv[1] if len(sys.argv) > 1 else "ws://127.0.0.1:8000/ws/call"
SAYS = ["मेरे एसबीआई खाते से चालीस हज़ार रुपये कट गए, यूपीआई से गए।",
        "आज दोपहर दो बजे।",
        "यूटीआर है चार एक दो तीन चार पाँच छह सात आठ नौ शून्य एक।"]
FRAME, PACE = 1024, 0.032  # 512 samples at 16 kHz, sent in real time like a mic


def pcm(text):
    w = wave.open(io.BytesIO(tts(text, "hi")))
    return w.readframes(w.getnframes())


async def main():
    clips = [pcm(t) for t in SAYS]
    firsts = []
    async with websockets.connect(URL, max_size=None) as ws:
        done = asyncio.Event()

        async def recv():
            audio = 0
            async for m in ws:
                if isinstance(m, bytes):
                    audio += len(m)
                    continue
                j = json.loads(m)
                if j["type"] == "turn":
                    print(f"\nheard : {j['transcript']}\nreply : {j['question'] or 'checklist + complaint'}")
                elif j["type"] == "timings":
                    print(f"audio : {audio / 32000:.1f} s of reply speech\nms    : {j['ms']}")
                    firsts.append(j["ms"].get("first_audio_sent"))
                    audio = 0
                    done.set()
                elif j["type"] == "error":
                    print("error :", j["message"])

        receiver = asyncio.create_task(recv())
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
