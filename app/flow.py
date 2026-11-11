"""Case state, follow-up questions, hard-coded recovery steps and complaint templates.

The official steps are hard-coded and must never be generated; an LLM may only help extract fields.
"""
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from app import rules
from app.extract import extract

FIELDS = ["amount", "datetime", "payment_mode", "txn_id", "scammer_contact", "bank", "scam_type", "language"]

# Asked in this order; txn_id last because victims often need to open their bank SMS for it.
ASK_ORDER = ["amount", "payment_mode", "bank", "datetime", "scammer_contact", "scam_type", "txn_id"]
SKIPPABLE = {"datetime", "scammer_contact", "scam_type", "txn_id"}  # "pata nahi" is a valid answer
NOT_KNOWN = "not known"
READ_BACK = ["txn_id", "scammer_contact"]  # IDs are read back in digit groups and confirmed

# Matched as whole words/phrases (a Devanagari "ना" must not hit "नाम").
YES = ["haan", "haa", "han", "ha", "ji", "sahi", "correct", "right", "yes", "yeah", "yep", "theek", "thik",
       "bilkul", "हाँ", "हां", "हा", "जी", "सही", "ठीक", "बिल्कुल"]
NO = ["nahi", "nahin", "nhi", "na", "no", "galat", "wrong", "incorrect", "नहीं", "नही", "ना", "गलत", "ग़लत"]
CORRECTION = NO + ["actually", "asal", "sorry", "matlab", "असल", "मतलब", "सॉरी"]
DONT_KNOW = ["pata nahi", "pata nahin", "nahi pata", "नहीं पता", "पता नहीं", "don't know", "dont know",
             "not sure", "no idea", "yaad nahi", "याद नहीं", "skip"]

QUESTIONS = {
    "hi": {
        "amount": "कितने रुपये कटे हैं?",
        "payment_mode": "पैसे कैसे गए — UPI से, कार्ड से या नेट बैंकिंग से?",
        "bank": "आपका खाता किस बैंक में है?",
        "datetime": "यह कब हुआ? लगभग समय बताइए।",
        "scammer_contact": "ठग ने किस नंबर से कॉल किया, या किस UPI ID पर पैसे गए? पता न हो तो 'पता नहीं' कहिए।",
        "scam_type": "उन्होंने क्या कहकर पैसे लिए — KYC अपडेट, पुलिस या CBI, पार्सल, नौकरी, या कुछ और?",
        "txn_id": "बैंक के SMS में बारह अंकों का UTR या ट्रांज़ैक्शन नंबर होगा, कृपया पढ़कर बताइए।",
    },
    "en": {
        "amount": "How much money was taken?",
        "payment_mode": "How did the money go — UPI, card, or net banking?",
        "bank": "Which bank is your account with?",
        "datetime": "When did this happen? Tell me the approximate time.",
        "scammer_contact": "Which number called you, or which UPI ID got the money? Say 'don't know' if you're not sure.",
        "scam_type": "What did they say to get the money — KYC update, police or CBI, a parcel, a job, or something else?",
        "txn_id": "Your bank SMS has a 12-digit UTR or transaction number. Please read it out.",
    },
}

CHECKLIST = {
    "hi": [
        "घबराइए मत। सबसे पहले अभी 1930 पर कॉल कीजिए, यह सरकारी साइबर फ्रॉड हेल्पलाइन है।",
        "फिर अपने बैंक की हेल्पलाइन पर कॉल करके खाता और कार्ड तुरंत फ्रीज़ करवाइए।",
        "उसके बाद cybercrime.gov.in पर शिकायत दर्ज कीजिए। शिकायत का पूरा ड्राफ्ट स्क्रीन पर तैयार है।",
        "किसी को भी OTP या PIN मत बताइए। कोई पैसे वापस दिलाने के नाम पर फीस मांगे तो वह भी धोखा है।",
    ],
    "en": [
        "Stay calm. First, call 1930 right now, the government cyber-fraud helpline.",
        "Then call your bank's helpline and ask them to freeze your account and card immediately.",
        "Then file a complaint on cybercrime.gov.in. The full complaint draft is ready on screen.",
        "Never share an OTP or PIN. Anyone asking for a fee to recover your money is also a scammer.",
    ],
}

DISCLAIMER = ("This tool only guides you to official channels (1930, your bank, cybercrime.gov.in). "
              "It is not a government service and cannot recover money.")


LINES = {
    "hi": {
        "readback": "मैंने {name} नोट किया: {value}। क्या यह सही है? हाँ या नहीं बोलिए।",
        "txn_id": "UTR", "scammer_contact": "ठग का नंबर",
        "urgent": "यह अभी हाल ही में हुआ है, इसलिए हर मिनट कीमती है। बस दो-तीन बातें और, फिर तुरंत 1930 पर कॉल कीजिए।",
        "recent": "यह {age} पहले हुआ है, इसलिए पैसा रोके जाने का अभी भी मौका है।",
        "unknown_time": "अगर यह पिछले चौबीस घंटे में हुआ है, तो पैसा रोके जाने का अभी भी मौका है।",
        "old": "इसे एक दिन से ज़्यादा हो गया है, फिर भी 1930 पर कॉल और ऑनलाइन शिकायत ज़रूर कीजिए — बैंक को शिकायत नंबर चाहिए होगा।",
        "min": "{n} मिनट", "hr": "{n} घंटे",
    },
    "en": {
        "readback": "I noted the {name} as {value}. Is that right? Say yes or no.",
        "txn_id": "UTR", "scammer_contact": "scammer's number",
        "urgent": "This just happened, so every minute counts. A few quick questions, then call 1930 right away.",
        "recent": "This happened {age} ago, so there is still a chance the money can be held.",
        "unknown_time": "If this happened in the last 24 hours, there is still a chance the money can be held.",
        "old": "It has been more than a day, but still call 1930 and file online — your bank will need the complaint number.",
        "min": "{n} minutes", "hr": "{n} hours",
    },
}
RECENT_H = 24  # 1930 can still ask banks to hold money that hasn't left the mule accounts

IST = timezone(timedelta(hours=5, minutes=30))  # India has no DST


def new_case() -> dict:
    return {f: None for f in FIELDS}


def lang(case: dict) -> str:
    return "en" if case.get("language") in ("en", "en-IN") else "hi"


def _says(text: str, words) -> bool:
    # Devanagari letters and marks, but not the danda "।" / "॥" (U+0964-5), which is punctuation.
    toks = " " + " ".join(re.findall(r"[a-z0-9'\u0900-\u0963\u0966-\u097F]+", (text or "").lower())) + " "
    return any(" " + w + " " in toks for w in words)


def spoken_id(v: str) -> str:
    """Digits in groups, each digit separate, so TTS says "4 1 2 3" not "four thousand…" (UPI IDs as-is)."""
    d = _digits(v)
    if "@" in v or not d:
        return v
    size = 5 if len(d) == 10 else 4  # phone 98765 43210, UTR 4123 4567 8901
    return ", ".join(" ".join(d[i:i + size]) for i in range(0, len(d), size))


def fraud_time(text: str, now: float) -> Optional[int]:
    """Best-effort epoch seconds for "आज दोपहर 2 बजे" / "kal raat 11 baje" / "40 minute pehle". None if no clock time."""
    t, cur = (text or "").lower(), datetime.fromtimestamp(now, IST)
    ago = re.search(r"(\d+)\s*(मिनट|min|minute|minutes|घंटे|घंटा|ghante|ghanta|hour|hours)", t)
    if ago and re.search(r"पहले|pehle|pahle|ago", t):
        n = int(ago.group(1)) * (1 if ago.group(2) in ("मिनट", "min", "minute", "minutes") else 60)
        return int(now - n * 60)
    clock = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(बजे|baje|am|pm|a\.m\.|p\.m\.)", t)
    if not clock:
        return int(now) if re.search(r"अभी|abhi|just now", t) else None
    h, m, unit = int(clock.group(1)) % 24, int(clock.group(2) or 0), clock.group(3)
    days = 2 if re.search(r"परसों|parso", t) else 1 if re.search(r"कल|kal|yesterday", t) else 0
    if unit.startswith("p") and h < 12:
        h += 12
    elif not unit.startswith("a") and h < 12:
        if re.search(r"दोपहर|dopahar|afternoon|शाम|shaam|sham|evening", t) or (
                re.search(r"रात|raat|night", t) and h >= 6):
            h += 12
        elif not re.search(r"सुबह|subah|morning|रात|raat|night", t):
            # bare "2 बजे": the latest of 2:00 / 14:00 that isn't in the future
            pm = cur.replace(hour=h + 12, minute=m, second=0, microsecond=0) - timedelta(days=days)
            h += 12 if pm.timestamp() <= now else 0
    at = cur.replace(hour=h, minute=m, second=0, microsecond=0) - timedelta(days=days)
    if at.timestamp() > now + 300:  # a fraud can't be in the future: "10 बजे" said at 9 means yesterday
        at -= timedelta(days=1)
    return int(at.timestamp())


def _age(secs: float, lg: str) -> str:
    mins = max(1, int(secs // 60))
    return LINES[lg]["min"].format(n=mins) if mins < 60 else LINES[lg]["hr"].format(n=mins // 60)


def verdict(case: dict, now: float) -> str:
    """Hard-coded, like the checklist: how urgent this is, never a promise of recovery."""
    lg, ts = lang(case), case.get("fraud_ts")
    if ts is None:
        return LINES[lg]["unknown_time"]
    if now - ts > RECENT_H * 3600:
        return LINES[lg]["old"]
    return LINES[lg]["recent"].format(age=_age(now - ts, lg))


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def merge(case: dict, extracted: dict, transcript: str, overwrite=()) -> dict:
    """Fill empty fields from LLM output (and the `overwrite` fields, for corrections). IDs/contacts
    are kept only if their digits appear in what the user actually said, so the LLM cannot invent them."""
    said = _digits(transcript)
    out = dict(case)
    for f in FIELDS:
        v = extracted.get(f)
        if v in (None, "", "null") or (out.get(f) is not None and f not in overwrite):
            continue
        if f in ("txn_id", "scammer_contact") and _digits(str(v)) and _digits(str(v)) not in said:
            continue
        if f == "amount":
            try:
                v = int(float(str(v).replace(",", "")))
            except ValueError:
                continue
        out[f] = v
    return out


def next_question(case: dict) -> Optional[str]:
    for f in ASK_ORDER:
        if case.get(f) is None:
            return QUESTIONS[lang(case)][f]
    return None


def bare_amount(said: str) -> Optional[str]:
    """A bare "40,000" answering "how much?" has no ₹/rupee word for the rules to anchor on."""
    nums = [n for n in re.findall(r"\d[\d,]*", rules._join_spaced_digits(said))
            if len(n.replace(",", "")) <= 8]  # skip phone/UTR
    return nums[0] if nums else None


def advance(case: dict, history: str, said: str, now: Optional[float] = None):
    """One conversation turn. Returns (payload for the browser, text to speak).

    Besides the field values, the case carries: meta {field: {confirmed, source_text}}, confirming (the ID
    just read back), fraud_ts (epoch s, for the countdown) and urged (urgency said once)."""
    now = time.time() if now is None else now
    case = {**new_case(), **case}
    meta = {**(case.get("meta") or {})}
    confirming, case["confirming"] = case.get("confirming"), None
    got = extract(said)
    fixing = _says(said, CORRECTION)
    # The first turn answers no question, so a phone number there must not become the amount.
    asked = None if confirming or not history.strip() else next((f for f in ASK_ORDER if case.get(f) is None), None)
    if asked == "amount" and got["amount"] is None:
        got["amount"] = bare_amount(said)
    if asked in SKIPPABLE and got.get(asked) is None and _says(said, DONT_KNOW):
        got[asked] = NOT_KNOWN
    elif asked == "scam_type" and got["scam_type"] is None and said.strip():
        got["scam_type"] = said.strip()[:80]  # their own words are fine for the complaint

    overwrite = set()
    if fixing:  # "nahi, 50,000 the" / "SBI nahi, HDFC" / "actually kal raat"
        for f, table in (("bank", rules.BANKS), ("payment_mode", rules.PAYMENT), ("scam_type", rules.SCAMS)):
            other = [v for v in rules.find_all(said, table) if v != case.get(f)]
            if case.get(f) is not None and other:
                got[f] = other[0]
        if got["amount"] is None and case.get("amount") is not None and not (got["txn_id"] or got["scammer_contact"]):
            got["amount"] = bare_amount(said)
        overwrite = {f for f in FIELDS if f != "language" and got.get(f) not in (None, case.get(f))}
    if confirming:
        new = got.get(confirming)
        if new is not None and _digits(str(new)) != _digits(str(case[confirming])):
            overwrite.add(confirming)  # re-read the ID: replace and read back again
        elif _says(said, NO):
            case[confirming] = None  # wrong and no new value: ask for it again
            meta.pop(confirming, None)
        elif _says(said, YES):
            meta[confirming] = {**meta.get(confirming, {}), "confirmed": True}
        else:
            case["confirming"] = confirming  # unclear: ask again

    before = dict(case)
    case = merge(case, got, said, overwrite)
    for f in FIELDS:
        if case[f] != before[f] and f != "language":
            meta[f] = {"confirmed": False, "source_text": said}
    case["meta"] = meta
    if case["datetime"] != before["datetime"]:
        case["fraud_ts"] = fraud_time(case["datetime"], now)
    for f in READ_BACK:
        if case[f] not in (None, NOT_KNOWN) and case[f] != before[f]:
            case["confirming"] = f
            break

    lg, lead = lang(case), ""
    ts = case.get("fraud_ts")
    if ts is not None and now - ts <= RECENT_H * 3600 and not case.get("urged"):
        case["urged"], lead = True, LINES[lg]["urgent"] + " "
    if case["confirming"]:
        f = case["confirming"]
        question = LINES[lg]["readback"].format(name=LINES[lg][f], value=spoken_id(str(case[f])))
    else:
        question = next_question(case)
    out = {"transcript": said, "case": case, "question": question}
    if question:
        return out, lead + question
    out["verdict"] = verdict(case, now)
    out["checklist"] = checklist(case)
    out.update(complaint(case))
    return out, " ".join([out["verdict"]] + out["checklist"])


def checklist(case: dict) -> list:
    return CHECKLIST[lang(case)]


def complaint(case: dict) -> dict:
    v = {f: case.get(f) or "[not provided]" for f in FIELDS}
    if case.get("fraud_ts") is not None:  # officers need a clock time, not "40 मिनट पहले"
        v["datetime"] = datetime.fromtimestamp(case["fraud_ts"], IST).strftime("%d %b %Y, %I:%M %p IST")
    amt = f"Rs. {case['amount']:,}" if case.get("amount") else v["amount"]
    text = (
        f"I am reporting a financial cyber fraud. On {v['datetime']}, {amt} was debited from my "
        f"{v['bank']} account via {v['payment_mode']}. Transaction/UTR ID: {v['txn_id']}. "
        f"The fraudster contacted me from {v['scammer_contact']}. Type of fraud: {v['scam_type']}. "
        f"I did not authorise this transaction. I request that the amount be put on hold and "
        f"action be taken against the fraudster."
    )
    email = (
        f"Subject: URGENT - Fraudulent transaction, request to freeze account and hold funds\n\n"
        f"Dear {v['bank']} team,\n\n{text}\n\nPlease block my account/card immediately and "
        f"initiate a chargeback/dispute for UTR {v['txn_id']}. I have also reported this on 1930.\n\n"
        f"Regards,\n[Your name]\n[Account number]"
    )
    return {"complaint": text, "bank_email": email}
