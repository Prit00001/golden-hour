"""Speech accuracy under noise: Timbre TTS -> noise -> Prisma STT -> rules extraction, on eval/cases.py.

Run from the repo root:  python3 -m eval.run            (first run: 34 TTS + ~210 STT calls, a few minutes)
                         python3 -m eval.run --rescore  (no API calls: re-score cached transcripts after a fix)
Audio and transcripts are cached in eval/cache/. Writes the "accuracy" part of eval/results.json and prints
the tables used in eval/REPORT.md. Regional languages use STT locked to the language (what the page's
language picker does) plus one auto-detect run on clean audio for comparison.
"""
import io
import json
import re
import sys
import wave
from datetime import datetime
from pathlib import Path

import numpy as np  # eval only; not a runtime dependency

from app import gnani, rules
from app.flow import IST, QUESTIONS, fraud_time
from eval.cases import CASES

HERE = Path(__file__).parent
CACHE = HERE / "cache"
NOW = datetime(2026, 11, 11, 15, 0, tzinfo=IST).timestamp()
RATE = 16000
CONDITIONS = ["clean", "babble 15dB", "babble 5dB", "pink 15dB", "pink 5dB", "phone band"]
FIELDS = ["amount", "bank", "payment_mode", "txn_id", "scammer_contact", "scam_type", "time"]


def pcm(wav_bytes):
    w = wave.open(io.BytesIO(wav_bytes))
    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def to_wav(x):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    return buf.getvalue()


def fit(x, n):
    return np.tile(x, n // len(x) + 1)[:n]


def mix(speech, noise, snr_db):
    """Add noise so that 10*log10(P_speech / P_noise) == snr_db."""
    noise = fit(noise, len(speech))
    gain = np.sqrt(np.mean(speech ** 2) / (np.mean(noise ** 2) * 10 ** (snr_db / 10)))
    return speech + gain * noise


def pink(n, seed):
    spec = np.fft.rfft(np.random.default_rng(seed).standard_normal(n))
    spec /= np.sqrt(np.maximum(np.arange(len(spec)), 1))  # 1/f power: hiss + rumble, like a street or fan
    return np.fft.irfft(spec, n)


def phone_band(x):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / RATE)
    spec[(f < 300) | (f > 3400)] = 0  # narrowband telephone channel
    return np.fft.irfft(spec, len(x))


def degrade(i, clips, cond):
    x = clips[i]
    if cond == "clean":
        return x
    if cond == "phone band":
        return phone_band(x)
    kind, snr = cond.split()
    if kind == "babble":  # three other speakers talking at once
        noise = sum(fit(clips[(i + k) % len(clips)], len(x)) for k in (1, 2, 3))
    else:
        noise = pink(len(x), seed=i)
    return mix(x, noise, int(snr[:-2]))


def words(text):
    """WER tokens: digits normalised and joined (Prisma writes 4123 4567 8901 as 412345678901), no punctuation."""
    t = rules._join_spaced_digits(rules.normalize(text).lower()).replace(",", "")
    return re.sub(r"[.?!।॥—\-:;\"'()]", " ", t).split()


def wer(ref, hyp):
    r, h = words(ref), words(hyp)
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        prev, d[0] = d[0], i
        for j, hw in enumerate(h, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (rw != hw))
    return d[len(h)] / max(len(r), 1)


def predict(transcript, code):
    got = rules.extract(transcript)
    ts = fraud_time(got["datetime"], NOW) if got["datetime"] else None
    got["time"] = datetime.fromtimestamp(ts, IST).strftime("%d %H:%M") if ts is not None else None
    hint = (code or "").split("-")[0].lower()
    got["language"] = hint if hint in QUESTIONS and not rules.hinglish(transcript) else got["language"]
    return got


def same(field, want, got):
    if got is None:
        return False
    if field == "scammer_contact":
        return re.sub(r"\D", "", str(got)) == re.sub(r"\D", "", str(want)) if want[0].isdigit() \
            else str(got).lower() == want.lower()
    return got == want


def load(name, default):
    p = CACHE / name
    return json.loads(p.read_text()) if p.exists() else default


def main(rescore=False):
    CACHE.mkdir(exist_ok=True)
    clips = []
    for i, (lang, text, _) in enumerate(CASES):
        p = CACHE / f"tts_{i}.wav"
        if not p.exists():
            assert not rescore, f"missing {p}: run without --rescore first"
            p.write_bytes(gnani.tts(text, lang))
        clips.append(pcm(p.read_bytes()))

    stt = load("stt.json", {})
    runs = []  # (case index, condition, mode)
    for i, (lang, _, _) in enumerate(CASES):
        mode = "auto" if lang in ("hi", "en") else "locked"
        runs += [(i, c, mode) for c in CONDITIONS]
        if mode == "locked":
            runs.append((i, "clean", "auto"))
    for n, (i, cond, mode) in enumerate(runs):
        key = f"{i}|{cond}|{mode}"
        if key in stt:
            continue
        assert not rescore, f"missing transcript {key}: run without --rescore first"
        lang = CASES[i][0]
        res = gnani.stt(to_wav(degrade(i, clips, cond)), "case.wav", lang="" if mode == "auto" else lang)
        stt[key] = {"text": res["transcript"], "code": res.get("detected_language_code")}
        (CACHE / "stt.json").write_text(json.dumps(stt, ensure_ascii=False, indent=1))
        print(f"\r{n + 1}/{len(runs)} transcribed", end="", flush=True)
    print()

    rows = []
    for i, cond, mode in runs:
        lang, text, want = CASES[i]
        heard = stt[f"{i}|{cond}|{mode}"]
        got = predict(heard["text"], heard["code"])
        rows.append({"case": i, "lang": lang, "condition": cond, "mode": mode, "heard": heard["text"],
                     "detected": heard["code"], "wer": round(wer(text, heard["text"]), 3),
                     "fields": {f: same(f, v, got.get(f)) for f, v in want.items()},
                     "got": {f: got.get(f) for f in want}, "language_ok": got["language"] == lang})

    def summary(rs):
        checks = [(f, ok) for r in rs for f, ok in r["fields"].items()]
        per = {f: [ok for g, ok in checks if g == f] for f in FIELDS}
        return {"n": len(rs), "wer": round(float(np.mean([r["wer"] for r in rs])), 3),
                "field_accuracy": round(sum(ok for _, ok in checks) / len(checks), 3),
                "case_all_correct": round(float(np.mean([all(r["fields"].values()) for r in rs])), 3),
                "language_id": round(float(np.mean([r["language_ok"] for r in rs])), 3),
                "per_field": {f: round(sum(v) / len(v), 3) for f, v in per.items() if v}}

    product = [r for r in rows if r["mode"] == ("auto" if r["lang"] in ("hi", "en") else "locked")]
    acc = {
        "cases": len(CASES), "stt_calls": len(runs), "now": "2026-11-11 15:00 IST",
        "by_condition": {c: summary([r for r in product if r["condition"] == c]) for c in CONDITIONS},
        "by_language_clean": {lg: summary([r for r in product if r["lang"] == lg and r["condition"] == "clean"])
                              for lg in dict.fromkeys(c[0] for c in CASES)},
        "regional_auto_vs_locked_clean": {
            m: summary([r for r in rows if r["lang"] not in ("hi", "en") and r["condition"] == "clean"
                        and r["mode"] == m]) for m in ("auto", "locked")},
        "clean_failures": [{**{k: r[k] for k in ("case", "lang", "heard", "got")},
                            "missed": [f for f, ok in r["fields"].items() if not ok]}
                           for r in product if r["condition"] == "clean" and not all(r["fields"].values())],
        "rows": rows,
    }
    results = load("../results.json", {})
    results["accuracy"] = acc
    (HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))

    print("| Condition | WER | Field accuracy | Cases fully right |\n|---|---|---|---|")
    for c, s in acc["by_condition"].items():
        print(f"| {c} | {s['wer']:.1%} | {s['field_accuracy']:.1%} | {s['case_all_correct']:.1%} |")
    print("\n| Language (clean) | Cases | WER | Field accuracy |\n|---|---|---|---|")
    for lg, s in acc["by_language_clean"].items():
        print(f"| {lg} | {s['n']} | {s['wer']:.1%} | {s['field_accuracy']:.1%} |")
    print("\n| Regional STT (clean) | WER | Field accuracy | Language ID |\n|---|---|---|---|")
    for m, s in acc["regional_auto_vs_locked_clean"].items():
        print(f"| {m} | {s['wer']:.1%} | {s['field_accuracy']:.1%} | {s['language_id']:.1%} |")
    print("\nPer field (clean):", acc["by_condition"]["clean"]["per_field"])
    print("\nClean failures:")
    for f in acc["clean_failures"]:
        print(f"  #{f['case']} {f['lang']} missed {f['missed']}: heard {f['heard']!r} -> {f['got']}")


if __name__ == "__main__":
    main(rescore="--rescore" in sys.argv)
