"""Latency and usage over full live calls (greeting + 6 turns each), per language.

Run from the repo root:  python3 -m eval.latency URL [runs-per-language]
  e.g. python3 -m eval.latency wss://golden-hour-bigo.onrender.com/ws/call 2
Writes results.json "latency" (keyed by host) and "usage" (needs a server that reports spoken characters).
Gnani publishes no prices, so cost is shown as usage per call, priced at Sarvam's public rates as a benchmark.
"""
import asyncio
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import numpy as np

from smoke_call import call

RESULTS = Path(__file__).parent / "results.json"
# Benchmark only (Sarvam public price list, see research notes): STT ₹30/hour, TTS ₹15-30 per 10K characters.
STT_PER_HOUR, TTS_PER_10K = 30, (15, 30)


def pct(xs):
    return {"p50": int(np.percentile(xs, 50)), "p90": int(np.percentile(xs, 90)), "max": int(max(xs)),
            "under_1500ms": round(float(np.mean([x < 1500 for x in xs])), 3), "n": len(xs)}


async def main(url, runs):
    calls = []
    for lang in ("hi", "kn", "ta"):
        for r in range(runs):
            res = await call(url, lang, log=lambda *_: None)
            print(f"{lang} run {r + 1}: greeting {res['greeting_ms']} ms, turns {res['first_audio_ms']}")
            calls.append(res)
    turns = [ms for c in calls for ms in c["first_audio_ms"] if ms is not None]
    lat = {"turns": pct(turns), "greeting": pct([c["greeting_ms"] for c in calls]),
           "by_language": {lg: pct([ms for c in calls if c["lang"] == lg for ms in c["first_audio_ms"] if ms])
                           for lg in ("hi", "kn", "ta")},
           "unanswered_turns": sum(6 - c["turns_answered"] for c in calls), "calls": calls}
    results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    results.setdefault("latency", {})[urlparse(url).hostname] = lat
    if all(c["tts_chars"] for c in calls):
        stt_s = float(np.mean([c["stt_seconds"] for c in calls]))
        chars = float(np.mean([c["tts_chars"] for c in calls]))
        stt_inr = stt_s / 3600 * STT_PER_HOUR
        results["usage"] = {"per_call": {"stt_seconds": round(stt_s, 1), "tts_chars": round(chars)},
                            "benchmark_inr_per_call": [round(stt_inr + chars / 1e4 * p, 2) for p in TTS_PER_10K],
                            "note": "Gnani pricing is not public; INR uses Sarvam's public rates as a benchmark."}
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in lat.items() if k != "calls"}, indent=1), results.get("usage"))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1))
