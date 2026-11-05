"""Phase 1 smoke test: Gnani TTS -> wav -> Gnani STT round trip.

Run: python3 smoke_test.py
Needs GNANI_API_KEY in .env (same folder).
"""
import os
import time
from pathlib import Path

import requests

BASE = "https://api.vachana.ai"
HERE = Path(__file__).parent

# Synthetic victim line; numbers written as words per TTS docs.
TEXT = "मेरे खाते से चालीस हज़ार रुपये कट गए, एक कॉल आया था कि मेरा KYC expire हो गया है."


def load_key():
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("GNANI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"')
    return os.environ["GNANI_API_KEY"]


def tts(key, text, out):
    t = time.time()
    r = requests.post(
        f"{BASE}/api/v1/tts/inference",
        headers={"X-API-Key-ID": key},
        json={
            "text": text,
            "model": "timbre-v3.0",
            "voice": "Shivani",
            "language": "hi-IN",
            "audio_config": {"sample_rate": 16000, "num_channels": 1, "sample_width": 2,
                             "encoding": "linear_pcm", "container": "wav"},
        },
        timeout=60,
    )
    if r.status_code != 200:
        raise SystemExit(f"TTS failed {r.status_code}: {r.text[:300]}")
    out.write_bytes(r.content)
    return time.time() - t


def stt(key, wav):
    t = time.time()
    with open(wav, "rb") as f:
        r = requests.post(
            f"{BASE}/stt/v3",
            headers={"X-API-Key-ID": key},
            files={"audio_file": (wav.name, f, "audio/wav")},
            data={"model": "prisma-v3.0", "language_code": "indic-auto"},
            timeout=60,
        )
    if r.status_code != 200:
        raise SystemExit(f"STT failed {r.status_code}: {r.text[:300]}")
    return r.json(), time.time() - t


if __name__ == "__main__":
    key = load_key()
    wav = HERE / "smoke.wav"
    tts_s = tts(key, TEXT, wav)
    print(f"TTS ok: {wav.name} ({wav.stat().st_size} bytes) in {tts_s:.2f}s")
    res, stt_s = stt(key, wav)
    print(f"STT ok in {stt_s:.2f}s, detected={res.get('detected_language_code')}")
    print("IN :", TEXT)
    print("OUT:", res.get("transcript"))
    print("Now check credits used on app.gnani.ai and note them in SDLC_PLAN.md")
