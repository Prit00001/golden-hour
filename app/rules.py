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
    "UPI": ["upi", "यूपीआई", "ಯುಪಿಐ", "யுபிஐ", "యూపీఐ", "ইউপিআই", "gpay", "google pay", "गूगल पे", "phonepe", "phone pe", "फोनपे", "फ़ोनपे",
            "paytm", "पेटीएम", "bhim", "भीम", "qr", "क्यूआर", "स्कैन"],
    "card": ["card", "कार्ड", "ಕಾರ್ಡ", "கார்ட", "కార్డ", "কার্ড", "debit", "credit", "डेबिट", "क्रेडिट", "atm", "एटीएम"],
    "net banking": ["net banking", "netbanking", "नेट बैंकिंग", "internet banking", "इंटरनेट बैंकिंग", "नेट बँकिंग",
                    "ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್", "நெட் பேங்கிங்", "నెట్ బ్యాంకింగ్", "নেট ব্যাঙ্কিং"],
    "wallet": ["wallet", "वॉलेट"],
}

SCAMS = {
    "digital arrest": ["cbi", "सीबीआई", "police", "पुलिस", "arrest", "गिरफ्तार", "अरेस्ट", "ed", "customs", "कस्टम",
                       "ಪೊಲೀಸ್", "ಪುಲೀಸ್", "போலீஸ்", "పోలీస్", "পুলিশ", "पोलीस"],
    "courier/parcel scam": ["parcel", "पार्सल", "courier", "कूरियर", "fedex", "drugs", "ड्रग",
                            "ಪಾರ್ಸೆಲ್", "பார்சல்", "పార్సెల్", "পার্সেল"],
    "fake KYC update": ["kyc", "k yc", "के yc", "केवाईसी", "केवाई सी"],  # Prisma sometimes splits KYC
    "OTP fraud": ["otp", "ओटीपी", "ಒಟಿಪಿ", "ஓடிபி", "ఓటీపీ", "ওটিপি"],
    "refund scam": ["refund", "रिफंड", "cashback", "कैशबैक"],
    "job/task scam": ["job", "नौकरी", "task", "टास्क", "work from home", "वर्क फ्रॉम होम",
                        "ಕೆಲಸ", "வேலை", "ఉద్యోగ", "চাকরি", "नोकरी"],
    "investment scam": ["investment", "इन्वेस्ट", "trading", "ट्रेडिंग", "share", "शेयर", "crypto", "क्रिप्टो"],
    "lottery scam": ["lottery", "लॉटरी", "इनाम", "prize"],
    "electricity bill scam": ["electricity", "बिजली", "bill", "बिल"],
}

# Time words in hi/en/Hinglish and kn, ta, te, bn, mr (shared with flow.fraud_time).
TODAY = "आज|aaj|today|ಇಂದು|இன்று|ఈ రోజు|ఈరోజు|আজ"
YESTERDAY = "कल|kal|yesterday|ನಿನ್ನೆ|நேற்று|నిన్న|গতকাল|কাল|काल"
DAY_BEFORE = "परसों|parso|parson|ಮೊನ್ನೆ|நேற்று முன்தினம்|మొన్న|পরশু|परवा"
NOW = "अभी|abhi|just now|ಈಗ|இப்போது|ఇప్పుడే|এইমাত্র|आत्ता"
MORNING = "सुबह|subah|morning|ಬೆಳಿಗ್ಗೆ|ಬೆಳಗ್ಗೆ|காலை|ఉదయం|সকাল|सकाळी"
LATER = ("दोपहर|dopahar|afternoon|शाम|shaam|sham|evening|ಮಧ್ಯಾಹ್ನ|ಸಂಜೆ|மதியம்|மாலை|మధ్యాహ్నం|సాయంత్రం|"
         "দুপুর|বিকেল|সন্ধ্যা|दुपारी|संध्याकाळी")
NIGHT = "रात|raat|night|ರಾತ್ರಿ|இரவு|రాత్రి|রাত|रात्री"
CLOCK = r"बजे|baje|am|pm|a\.m\.|p\.m\.|ಗಂಟೆಗೆ|ಗಂಟೆ|மணிக்கு|மணி|గంటలకు|గంటకు|টায়|টায়|টা(?!কা)|वाजता"
MINUTE = "मिनट|min|minute|ನಿಮಿಷ|நிமிட|నిమిష|মিনিট|मिनिट"
HOUR = "घंटे|घंटा|ghante|ghanta|hour|ಗಂಟೆ|மணி நேர|மணிநேர|గంట|ঘণ্টা|तास"
DAY = "दिन|din|day|ದಿನ|நாள்|நாட்கள|రోజు|রোজ|দিন|दिवस"
AGO = "पहले|pehle|pahle|ago|ಹಿಂದೆ|முன்பு|முன்|క్రితం|আগে|पूर्वी|आधी"

WHEN = "(" + "|".join([TODAY, YESTERDAY, DAY_BEFORE, NOW, MORNING, LATER, NIGHT]) + ")"
WHEN_SPAN = re.compile(
    WHEN + r"(?:(?:\s+\S+){0,3}?\s*\d{1,2}(?::\d{2})?\s*(?:" + CLOCK + "))?"
    r"|(?<![\d,])\d{1,2}(?::\d{2})?\s*(?:" + CLOCK + ")"
    r"|\d+\s*(?:" + MINUTE + "|" + HOUR + "|" + DAY + r")\S*\s*(?:" + AGO + ")",
    re.I,
)
MULT = {"हज़ार": 1000, "हजार": 1000, "hazar": 1000, "hazaar": 1000, "thousand": 1000, "k": 1000,
        "लाख": 100000, "lakh": 100000, "lac": 100000, "करोड़": 10**7, "crore": 10**7,
        "ಸಾವಿರ": 1000, "ಲಕ್ಷ": 100000, "ஆயிரம்": 1000, "லட்சம்": 100000, "వేలు": 1000, "వేల": 1000,
        "లక్ష": 100000, "হাজার": 1000, "লাখ": 100000}
RUPEES = r"रुपये|रुपए|रूपये|rupees|rupaye|rs|ರೂಪಾಯಿ\S*|ரூபாய்\S*|రూపాయ\S*|টাকা\S*|रुपय\S*"
# "40,000 kat gaye": no ₹ or rupee word, but a debit verb right after the number says it's money.
DEBITED = re.compile(r"(?<![\d,])(\d[\d,]*)\s*(?:कट|kat|cut|debit|deduct|निकल|nikal|चले|chale|गए|गये|gaye|gay|भेजे|bheje|sent|transfer|paid)",
                     re.I)
AMOUNT = re.compile(r"(₹|rs\.?|inr)?\s*(\d[\d,]*(?:\.\d+)?)\s*((?:" + "|".join(MULT) + r")(?![a-z]))?\s*"
                    r"(" + RUPEES + ")?", re.I)

# Script -> language. Marathi shares Devanagari with Hindi, so it is told apart by common words.
SCRIPTS = {"hi": "\u0900-\u097f", "bn": "\u0980-\u09ff", "ta": "\u0b80-\u0bff", "te": "\u0c00-\u0c7f",
           "kn": "\u0c80-\u0cff"}
MARATHI = ["आहे", "माझ्या", "माझे", "माझा", "झाले", "झाला", "गेले", "नाही", "होते", "तुम्ही"]
HINGLISH = ["hai", "se", "ka", "ki", "ke", "mera", "meri", "mere", "gaye", "gaya", "kat", "paise", "rupaye",
            "nahi", "haan", "kal", "aaj", "baje", "tha", "thi", "kya", "aur", "bola", "mujhe", "hua", "pata"]

# Spoken numbers STT may leave as words (and typed Hinglish). "do" (2) only for Hinglish, never English text.
NUM_WORDS = {"शून्य": 0, "ज़ीरो": 0, "जीरो": 0, "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पाँच": 5, "पांच": 5,
             "छह": 6, "छः": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "बीस": 20, "तीस": 30, "चालीस": 40,
             "पचास": 50, "साठ": 60, "सत्तर": 70, "अस्सी": 80, "नब्बे": 90, "ग्यारह": 11, "बारह": 12,
             # Prisma writes small numbers as words in regional languages ("ಎರಡು ಗಂಟೆಗೆ", "అరవై వేలు")
             "ಸೊನ್ನೆ": 0, "ಒಂದು": 1, "ಎರಡು": 2, "ಮೂರು": 3, "ನಾಲ್ಕು": 4, "ಐದು": 5, "ಆರು": 6, "ಏಳು": 7, "ಎಂಟು": 8,
             "ಒಂಬತ್ತು": 9, "ಹತ್ತು": 10, "ಹನ್ನೊಂದು": 11, "ಹನ್ನೆರಡು": 12, "ಇಪ್ಪತ್ತು": 20, "ಮೂವತ್ತು": 30,
             "ನಲವತ್ತು": 40, "ಐವತ್ತು": 50, "ಅರವತ್ತು": 60, "ಎಪ್ಪತ್ತು": 70, "ಎಂಬತ್ತು": 80, "ತೊಂಬತ್ತು": 90,
             "பூஜ்ஜியம்": 0, "ஒன்று": 1, "இரண்டு": 2, "மூன்று": 3, "நான்கு": 4, "ஐந்து": 5, "ஆறு": 6, "ஏழு": 7,
             "எட்டு": 8, "ஒன்பது": 9, "பத்து": 10, "பதினொன்று": 11, "பன்னிரண்டு": 12, "இருபது": 20, "முப்பது": 30,
             "நாற்பது": 40, "ஐம்பது": 50, "அறுபது": 60, "எழுபது": 70, "எண்பது": 80, "தொண்ணூறு": 90,
             "సున్నా": 0, "ఒకటి": 1, "రెండు": 2, "మూడు": 3, "నాలుగు": 4, "ఐదు": 5, "ఆరు": 6, "ఏడు": 7, "ఎనిమిది": 8,
             "తొమ్మిది": 9, "పది": 10, "పదకొండు": 11, "పన్నెండు": 12, "ఇరవై": 20, "ముప్పై": 30, "నలభై": 40,
             "యాభై": 50, "అరవై": 60, "డెబ్బై": 70, "ఎనభై": 80, "తొంభై": 90,
             # Bengali নয় (9) is left out: it also means "not", which the read-back needs
             "শূন্য": 0, "এক": 1, "দুই": 2, "তিন": 3, "চার": 4, "পাঁচ": 5, "ছয়": 6, "সাত": 7, "আট": 8, "দশ": 10,
             "এগারো": 11, "বারো": 12, "কুড়ি": 20, "তিরিশ": 30, "চল্লিশ": 40, "পঞ্চাশ": 50, "ষাট": 60, "সত্তর": 70,
             "আশি": 80, "নব্বই": 90,
             "दोन": 2, "पाच": 5, "सहा": 6, "नऊ": 9, "दहा": 10, "अकरा": 11, "बारा": 12, "वीस": 20, "चाळीस": 40,
             "पन्नास": 50, "ऐंशी": 80, "नव्वद": 90}
ROMAN_NUMS = {"shunya": 0, "zero": 0, "ek": 1, "do": 2, "teen": 3, "char": 4, "chaar": 4, "paanch": 5,
              "panch": 5, "chhe": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10, "bees": 20, "tees": 30,
              "chalis": 40, "chaalis": 40, "pachas": 50, "pachaas": 50}
INDIC_DIGITS = str.maketrans("०१२३४५६७८९০১২৩৪৫৬৭৮৯௦௧௨௩௪௫௬௭௮௯౦౧౨౩౪౫౬౭౮౯೦೧೨೩೪೫೬೭೮೯", "0123456789" * 5)


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


def hinglish(text):
    """Romanized Hindi ("SBI se 40,000 kat gaye"), not English."""
    low = text.lower()
    return sum(_has(low, w) for w in HINGLISH) >= 2


def language(text):
    t = text or ""
    counts = {lg: len(re.findall("[" + r + "]", t)) for lg, r in SCRIPTS.items()}
    lg, n = max(counts.items(), key=lambda kv: kv[1])
    if n > len(t) * 0.2:
        return "mr" if lg == "hi" and any(w in t for w in MARATHI) else lg
    return "hi" if hinglish(t) else "en"


def normalize(text):
    """Native digits -> 0-9 and spoken number words -> digits, so "चार एक दो" reads as 412."""
    t = (text or "").translate(INDIC_DIGITS)
    words = {**NUM_WORDS, **(ROMAN_NUMS if hinglish(t) else {})}
    pat = r"(?<![\w\u0900-\u0dff])(" + "|".join(sorted(words, key=len, reverse=True)) + r")(?![\w\u0900-\u0dff])"
    return re.sub(pat, lambda m: str(words[m.group(1).lower()]), t, flags=re.I)


def _join_spaced_digits(text):
    # "4 1 2 3 4 5 6 7 8 9 0 1" or "41234 5678901" -> one run, so spoken IDs survive
    return re.sub(r"(?<=\d)[\s-]+(?=\d)", "", text)


def extract(transcript: str) -> dict:
    t = normalize(transcript)
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
    if amount is None:
        amount = next((int(n) for n in (m.group(1).replace(",", "") for m in DEBITED.finditer(t)) if 0 < len(n) <= 8), None)

    spans = [m.group(0) for m in WHEN_SPAN.finditer(t)]
    when = next((w for w in spans if re.search(r"\d", w)), spans[0] if spans else None)
    return {
        "amount": amount,
        "datetime": when.strip() if when else None,
        "payment_mode": _find(t, PAYMENT),
        "txn_id": utr.group(0) if utr else None,
        "scammer_contact": upi.group(0) if upi else (phone.group(1) if phone else None),
        "bank": _find(t, BANKS),
        "scam_type": _find(t, SCAMS),
        "language": language(t),
    }
