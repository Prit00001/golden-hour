"""Gnani Prisma STT + Timbre TTS (REST)."""
import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.llm import env

BASE = "https://api.vachana.ai"

# Retry connect failures / 429 / 5xx a few times; POST is safe to retry here (no side effects).
http = requests.Session()
http.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, allowed_methods=None,
                                                     status_forcelist=[429, 500, 502, 503, 504])))

# Context hints so bank names, apps and IDs come out right.
KEYTERMS = ["UPI", "UTR", "KYC", "OTP", "SBI", "HDFC", "ICICI", "Axis", "PNB", "Kotak", "Bank of Baroda",
            "Canara", "PhonePe", "Google Pay", "Paytm", "CBI", "1930", "cybercrime", "डिजिटल अरेस्ट"]
TOPIC = "A cyber fraud victim describes money taken from their bank account: amount, bank, UPI, UTR number, time."


def _key():
    return env()["GNANI_API_KEY"]


def stt(audio: bytes, filename: str = "audio.wav", previous_text: str = "") -> dict:
    """<=30 s audio -> {'transcript', 'detected_language_code', ...}"""
    data = {"model": "prisma-v3.0", "language_code": "indic-auto", "format": "transcribe",
            "keyterms": json.dumps(KEYTERMS, ensure_ascii=False), "topic": TOPIC}
    if previous_text.strip():
        data["previous_text"] = previous_text[-600:]
    r = http.post(f"{BASE}/stt/v3", headers={"X-API-Key-ID": _key()},
                      files={"audio_file": (filename, audio)}, data=data, timeout=(10, 60))
    r.raise_for_status()
    return r.json()


def tts(text: str, lang: str = "hi") -> bytes:
    """Text -> 16 kHz mono wav bytes."""
    r = http.post(
        f"{BASE}/api/v1/tts/inference",
        headers={"X-API-Key-ID": _key()},
        json={"text": text, "model": "timbre-v3.0", "voice": "Shivani",
              "language": "en-IN" if lang == "en" else "hi-IN",
              "audio_config": {"sample_rate": 16000, "num_channels": 1, "sample_width": 2,
                               "encoding": "linear_pcm", "container": "wav"}},
        timeout=(10, 60),
    )
    r.raise_for_status()
    return r.content
