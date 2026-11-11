"""Rule-based field extraction (default; no third-party LLM).

Expects Prisma `format=transcribe` output: numbers as digits, English words in Latin script.
ponytail: keyword lists cover common banks/scams only; extend lists, or set EXTRACTOR=groq|gemini.
"""
import re

BANKS = {
    "SBI": ["sbi", "state bank", "एसबीआई", "स्टेट बैंक"],
    "HDFC Bank": ["hdfc", "एचडीएफसी"],
    "ICICI Bank": ["icici", "आईसीआईसीआई"],
    "Axis Bank": ["axis", "एक्सिस"],
    "Punjab National Bank": ["pnb", "punjab national", "पंजाब नेशनल", "पीएनबी"],
    "Bank of Baroda": ["baroda", "बड़ौदा", "बरोडा"],
    "Kotak Mahindra Bank": ["kotak", "कोटक"],
    "Canara Bank": ["canara", "केनरा"],
    "Union Bank of India": ["union bank", "यूनियन बैंक"],
    "Bank of India": ["bank of india", "बैंक ऑफ इंडिया"],
    "Indian Bank": ["indian bank", "इंडियन बैंक"],
    "Yes Bank": ["yes bank", "यस बैंक"],
    "IndusInd Bank": ["indusind", "इंडसइंड"],
    "IDFC First Bank": ["idfc", "आईडीएफसी"],
    "Airtel Payments Bank": ["airtel payment", "एयरटेल पेमेंट"],
    "India Post Payments Bank": ["india post", "पोस्ट ऑफिस", "डाकघर"],
}

PAYMENT = {
    "UPI": ["upi", "यूपीआई", "gpay", "google pay", "गूगल पे", "phonepe", "phone pe", "फोनपे", "फ़ोनपे",
            "paytm", "पेटीएम", "bhim", "भीम", "qr", "क्यूआर", "स्कैन"],
    "card": ["card", "कार्ड", "debit", "credit", "डेबिट", "क्रेडिट", "atm", "एटीएम"],
    "net banking": ["net banking", "netbanking", "नेट बैंकिंग", "internet banking", "इंटरनेट बैंकिंग"],
    "wallet": ["wallet", "वॉलेट"],
}

SCAMS = {
    "digital arrest": ["cbi", "सीबीआई", "police", "पुलिस", "arrest", "गिरफ्तार", "अरेस्ट", "ed", "customs", "कस्टम"],
    "courier/parcel scam": ["parcel", "पार्सल", "courier", "कूरियर", "fedex", "drugs", "ड्रग"],
    "fake KYC update": ["kyc", "k yc", "के yc", "केवाईसी", "केवाई सी"],  # Prisma sometimes splits KYC
    "OTP fraud": ["otp", "ओटीपी"],
    "refund scam": ["refund", "रिफंड", "cashback", "कैशबैक"],
    "job/task scam": ["job", "नौकरी", "task", "टास्क", "work from home", "वर्क फ्रॉम होम"],
    "investment scam": ["investment", "इन्वेस्ट", "trading", "ट्रेडिंग", "share", "शेयर", "crypto", "क्रिप्टो"],
    "lottery scam": ["lottery", "लॉटरी", "इनाम", "prize"],
    "electricity bill scam": ["electricity", "बिजली", "bill", "बिल"],
}

WHEN = r"(आज|कल|परसों|अभी|today|yesterday|aaj|kal|abhi|subah|सुबह|दोपहर|शाम|रात|morning|evening|night)"
WHEN_SPAN = re.compile(
    WHEN + r"(?:(?:\s+\S+){0,3}?\s*\d{1,2}(?::\d{2})?\s*(?:बजे|baje|am|pm|a\.m\.|p\.m\.))?"
    r"|\d{1,2}(?::\d{2})?\s*(?:बजे|baje|am|pm)"
    r"|\d+\s*(?:मिनट|घंटे|minute|minutes|hour|hours|ghante)\s*(?:पहले|pehle|ago)",
    re.I,
)
MULT = {"हज़ार": 1000, "हजार": 1000, "hazar": 1000, "hazaar": 1000, "thousand": 1000, "k": 1000,
        "लाख": 100000, "lakh": 100000, "lac": 100000, "करोड़": 10**7, "crore": 10**7}
AMOUNT = re.compile(r"(₹|rs\.?|inr)?\s*(\d[\d,]*(?:\.\d+)?)\s*((?:" + "|".join(MULT) + r")(?![a-z]))?\s*"
                    r"(रुपये|रुपए|रूपये|rupees|rupaye|rs)?", re.I)


def _has(low, key):
    # Latin keys match whole words only ("ed" must not hit "charged"); Devanagari keys match as substrings.
    if key.isascii():
        return re.search(r"(?<![a-z])" + re.escape(key) + r"(?![a-z])", low) is not None
    return key in low


def find_all(text, table):
    """Every entry mentioned, in table order ("SBI nahi, HDFC" -> both, so a correction can pick the new one)."""
    low = text.lower()
    return [name for name, keys in table.items() if any(_has(low, k) for k in keys)]


def _find(text, table):
    return (find_all(text, table) or [None])[0]


def _join_spaced_digits(text):
    # "4 1 2 3 4 5 6 7 8 9 0 1" or "41234 5678901" -> one run, so spoken IDs survive
    return re.sub(r"(?<=\d)[\s-]+(?=\d)", "", text)


def extract(transcript: str) -> dict:
    t = transcript or ""
    joined = _join_spaced_digits(t)
    utr = re.search(r"(?<!\d)\d{12}(?!\d)", joined)
    phone = re.search(r"(?<!\d)(?:\+?91)?([6-9]\d{9})(?!\d)", joined)
    upi = re.search(r"[\w.\-]{2,}@[a-z]{2,}", t, re.I)

    amount = None
    for m in AMOUNT.finditer(t):
        cur, num, mult, word = m.groups()
        raw = num.replace(",", "")
        if len(raw.split(".")[0]) > 8:  # phone/UTR, not money
            continue
        if cur or mult or word:
            amount = int(float(raw) * MULT.get((mult or "").lower(), 1))
            break

    when = WHEN_SPAN.search(t)
    devanagari = len(re.findall(r"[ऀ-ॿ]", t))
    return {
        "amount": amount,
        "datetime": when.group(0).strip() if when else None,
        "payment_mode": _find(t, PAYMENT),
        "txn_id": utr.group(0) if utr else None,
        "scammer_contact": upi.group(0) if upi else (phone.group(1) if phone else None),
        "bank": _find(t, BANKS),
        "scam_type": _find(t, SCAMS),
        "language": "hi" if devanagari > len(t) * 0.2 else "en",
    }
