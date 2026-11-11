"""Offline check for eval/run.py helpers (no API calls). Run: python3 -m eval.test_eval"""
import numpy as np

from eval.run import mix, phone_band, pink, same, wer

rng = np.random.default_rng(0)
speech = rng.standard_normal(16000) * 0.1
noisy = mix(speech, pink(8000, seed=1), 5)  # noise shorter than speech: tiled
snr = 10 * np.log10(np.mean(speech ** 2) / np.mean((noisy - speech) ** 2))
assert abs(snr - 5) < 0.01, snr
tone = lambda hz: np.sin(2 * np.pi * hz * np.arange(16000) / 16000)
assert np.abs(phone_band(tone(1000))).max() > 0.9 and np.abs(phone_band(tone(6000))).max() < 0.01

assert wer("UTR नंबर है 4 1 2 3 4 5 6 7 8 9 0 1।", "UTR नंबर है 412345678901") == 0  # digits joined, danda dropped
assert wer("मेरे 40,000 रुपये कट गए", "मेरे 40000 रुपये गए") == 0.2  # one deletion in five words
assert same("scammer_contact", "9876543210", "98765 43210") and not same("bank", "SBI", None)
assert same("scammer_contact", "lucky.winner@ybl", "Lucky.Winner@ybl")
print("eval ok")
