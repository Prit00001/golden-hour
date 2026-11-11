"""Offline check for app/stream.py (Gnani TTS stubbed, no network). Run: python3 test_stream.py"""
import asyncio
import time

from app import gnani, stream

assert stream.sentences("घबराइए मत। अभी 1930 पर कॉल कीजिए? Then call your bank.") == \
    ["घबराइए मत।", "अभी 1930 पर कॉल कीजिए?", "Then call your bank."]


class FakeWS:
    def __init__(self):
        self.sent = []

    async def send_json(self, m):
        self.sent.append(m)

    async def send_bytes(self, b):
        self.sent.append(b)


def fake_tts(text, lang="hi"):
    yield text.encode()[:3]  # odd length: must be carried over, never sent as half a sample
    yield text.encode()[3:]


def endless_tts(text, lang="hi"):
    while True:
        time.sleep(0.01)
        yield b"\0\0"


async def main():
    ws = FakeWS()
    call = stream.Call(ws)
    now = time.monotonic()
    gnani.tts_stream = fake_tts
    call.start("SBI se 40,000 rupaye gaye UPI se", {"speech_end": now, "stt_done": now})
    await call.reply
    kinds = [m["type"] if isinstance(m, dict) else "audio" for m in ws.sent]
    assert kinds[:2] == ["turn", "state"] and kinds[-2:] == ["timings", "state"], kinds
    assert ws.sent[0]["case"]["amount"] == 40000 and ws.sent[0]["question"].startswith("यह कब")  # Hinglish in, Hindi out
    chunks = [m for m in ws.sent if isinstance(m, bytes)]
    want = "यह कब हुआ?लगभग समय बताइए।".encode()
    assert b"".join(chunks) == want[:len(want) // 2 * 2]  # a trailing odd byte is never sent as half a sample
    assert all(len(c) % 2 == 0 for c in chunks)
    assert set(ws.sent[-2]["ms"]) >= {"stt_done", "extract_done", "first_tts_byte", "first_audio_sent"}

    # A newer utterance cancels the reply mid-speech: no more audio after that.
    gnani.tts_stream = endless_tts
    call.start("aaj 2 baje", {"speech_end": now, "stt_done": now})
    await asyncio.sleep(0.1)
    call.start("UTR 4123 4567 8901", {"speech_end": now, "stt_done": now})
    old = len(ws.sent)
    await asyncio.sleep(0.1)
    call.reply.cancel()
    await asyncio.sleep(0.1)
    n = len(ws.sent)
    await asyncio.sleep(0.2)
    assert len(ws.sent) == n and n > old, "cancelled replies must stop sending"
    assert call.case["datetime"] and call.case["txn_id"] == "412345678901"

    # Barge-in: the caller talks over the agent, so the reply stops and nothing more is sent.
    call.start("SBI", {"speech_end": now, "stt_done": now})
    await asyncio.sleep(0.1)
    call.barge_in()
    await asyncio.sleep(0.05)
    n = len(ws.sent)
    await asyncio.sleep(0.2)
    assert call.reply.cancelled() and len(ws.sent) == n, "barge-in must stop the reply"
    call.barge_in()  # no reply playing: harmless

    # Call start: the greeting + disclaimer is spoken (and warms the TTS connection).
    ws2 = FakeWS(); call2 = stream.Call(ws2)
    gnani.tts_stream = fake_tts
    call2.greet(); await call2.reply
    spoken = b"".join(m for m in ws2.sent if isinstance(m, bytes))
    assert "सरकारी सेवा नहीं".encode() in spoken and ws2.sent[0] == {"type": "state", "state": "speaking"}


asyncio.run(main())
print("stream ok")
