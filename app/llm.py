"""Optional third-party LLM extraction via OpenAI-compatible chat endpoints.

.env: EXTRACTOR=groq|gemini|custom, LLM_API_KEY, optional LLM_MODEL / LLM_BASE_URL overrides.
"""
import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent

PRESETS = {
    "groq": ("https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash"),
}

PROMPT = """You extract facts from a cyber-fraud victim's speech (Hindi, English or Hinglish).
Return ONLY a JSON object with these keys; use null when the speaker did not say it. Never guess.
- amount: integer rupees (convert words like "चालीस हज़ार" to 40000)
- datetime: when it happened, as said (e.g. "today 3 pm", "kal shaam")
- payment_mode: one of "UPI", "card", "net banking", "wallet", "other"
- txn_id: UTR / transaction ID exactly as spoken, digits only if numeric
- scammer_contact: phone number or UPI ID of the fraudster, exactly as spoken
- bank: bank name in English (e.g. "SBI", "HDFC Bank")
- scam_type: short English label, e.g. "fake KYC update", "digital arrest", "OTP fraud", "refund scam", "job scam"
- language: "hi" if the speaker mainly uses Hindi/Hinglish, else "en"

Speech: \"\"\"{transcript}\"\"\""""


def env():
    cfg = dict(os.environ)
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                cfg.setdefault(k.strip(), v.strip().strip('"'))
    return cfg


def extract(transcript: str, provider: str) -> dict:
    cfg = env()
    base, model = PRESETS.get(provider, ("", ""))
    base = cfg.get("LLM_BASE_URL") or base
    model = cfg.get("LLM_MODEL") or model
    r = requests.post(
        base.rstrip("/") + "/chat/completions",
        headers={"Authorization": f"Bearer {cfg.get('LLM_API_KEY', '')}"},
        json={
            "model": model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": PROMPT.format(transcript=transcript)}],
        },
        timeout=30,
    )
    r.raise_for_status()
    return json.loads(r.json()["choices"][0]["message"]["content"])
