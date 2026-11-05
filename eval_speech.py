"""End-to-end check on synthetic speech: Timbre TTS -> Prisma STT -> extract -> compare.

Run: python3 eval_speech.py   (costs ~₹5 of Gnani credits)
Numbers are written as spoken words, the way a victim would say them.
"""
from app.extract import extract
from app.gnani import stt, tts

CASES = [
    ("मेरे एसबीआई खाते से चालीस हज़ार रुपये कट गए, आज शाम चार बजे केवाईसी अपडेट के नाम पर कॉल आया था, फोनपे से पैसे गए।",
     {"amount": 40000, "bank": "SBI", "payment_mode": "UPI", "scam_type": "fake KYC update"}),
    ("कल एक आदमी ने खुद को सीबीआई ऑफिसर बताया और डिजिटल अरेस्ट की धमकी दी, मैंने नेट बैंकिंग से दो लाख रुपये भेज दिए, एचडीएफसी बैंक से।",
     {"amount": 200000, "bank": "HDFC Bank", "payment_mode": "net banking", "scam_type": "digital arrest"}),
    ("यूटीआर नंबर है चार एक दो तीन चार पाँच छह सात आठ नौ शून्य एक।",
     {"txn_id": "412345678901"}),
    ("मुझे नौ आठ सात छह पाँच चार तीन दो एक शून्य नंबर से कॉल आया था।",
     {"scammer_contact": "9876543210"}),
    ("My ICICI credit card was charged fifteen thousand rupees yesterday night after I shared an OTP.",
     {"amount": 15000, "bank": "ICICI Bank", "payment_mode": "card", "scam_type": "OTP fraud"}),
    ("पार्सल में ड्रग्स मिलने की बात कहकर डराया, मैंने गूगल पे से पच्चीस हज़ार रुपये दे दिए, पंजाब नेशनल बैंक का खाता है।",
     {"amount": 25000, "bank": "Punjab National Bank", "payment_mode": "UPI", "scam_type": "courier/parcel scam"}),
]

hit = total = 0
for text, expected in CASES:
    lang = "en" if text.isascii() else "hi"
    res = stt(tts(text, lang), "case.wav")
    got = extract(res["transcript"])
    print(f"\nSTT: {res['transcript']}  [{res.get('detected_language_code')}]")
    for k, want in expected.items():
        ok = str(got.get(k)) == str(want)
        hit += ok
        total += 1
        print(f"  {'✓' if ok else '✗'} {k}: got={got.get(k)!r} want={want!r}")
print(f"\nfield accuracy: {hit}/{total} = {hit / total:.0%}")
