"""Pick the extractor. EXTRACTOR=rules (default, Gnani + own code only) | groq | gemini | custom.

Third-party LLMs only fill fields the rules missed; rules output always wins.
"""
from app import llm, rules


def extract(transcript: str) -> dict:
    out = rules.extract(transcript)
    provider = llm.env().get("EXTRACTOR", "rules")
    if provider != "rules" and any(v is None for v in out.values()):
        try:
            for k, v in llm.extract(transcript, provider).items():
                if out.get(k) is None:
                    out[k] = v
        except Exception as e:  # LLM is optional; never break the flow
            print(f"[extract] {provider} failed: {e}")
    return out
