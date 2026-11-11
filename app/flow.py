"""Case state, follow-up questions, hard-coded recovery steps and complaint templates.

The official steps are hard-coded and must never be generated; an LLM may only help extract fields.
"""
import re
from typing import Optional

from app import rules
from app.extract import extract

FIELDS = ["amount", "datetime", "payment_mode", "txn_id", "scammer_contact", "bank", "scam_type", "language"]

# Asked in this order; txn_id last because victims often need to open their bank SMS for it.
ASK_ORDER = ["amount", "payment_mode", "bank", "datetime", "txn_id"]

QUESTIONS = {
    "hi": {
        "amount": "कितने रुपये कटे हैं?",
        "payment_mode": "पैसे कैसे गए — UPI से, कार्ड से या नेट बैंकिंग से?",
        "bank": "आपका खाता किस बैंक में है?",
        "datetime": "यह कब हुआ? लगभग समय बताइए।",
        "txn_id": "बैंक के SMS में बारह अंकों का UTR या ट्रांज़ैक्शन नंबर होगा, कृपया पढ़कर बताइए।",
    },
    "en": {
        "amount": "How much money was taken?",
        "payment_mode": "How did the money go — UPI, card, or net banking?",
        "bank": "Which bank is your account with?",
        "datetime": "When did this happen? Tell me the approximate time.",
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


def new_case() -> dict:
    return {f: None for f in FIELDS}


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def merge(case: dict, extracted: dict, transcript: str) -> dict:
    """Fill empty fields from LLM output. IDs/contacts are kept only if their digits appear
    in what the user actually said, so the LLM cannot invent them."""
    said = _digits(transcript)
    out = dict(case)
    for f in FIELDS:
        v = extracted.get(f)
        if v in (None, "", "null") or out.get(f) is not None:
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
    lang = "hi" if case.get("language") in (None, "hi", "hi-IN") else "en"
    for f in ASK_ORDER:
        if case.get(f) is None:
            return QUESTIONS[lang][f]
    return None


def bare_amount(said: str) -> Optional[str]:
    """A bare "40,000" answering "how much?" has no ₹/rupee word for the rules to anchor on."""
    nums = [n for n in re.findall(r"\d[\d,]*", rules._join_spaced_digits(said))
            if len(n.replace(",", "")) <= 8]  # skip phone/UTR
    return nums[0] if nums else None


def advance(case: dict, history: str, said: str):
    """One conversation turn. Returns (payload for the browser, text to speak)."""
    case = {**new_case(), **case}
    # The first turn answers no question, so a phone number there must not become the amount.
    asked = next((f for f in ASK_ORDER if case.get(f) is None), None) if history.strip() else None
    got = extract(said)
    if asked == "amount" and got["amount"] is None:
        got["amount"] = bare_amount(said)
    case = merge(case, got, said)
    question = next_question(case)
    out = {"transcript": said, "case": case, "question": question}
    if question:
        return out, question
    out["checklist"] = checklist(case)
    out.update(complaint(case))
    return out, " ".join(out["checklist"])


def checklist(case: dict) -> list:
    return CHECKLIST["en" if case.get("language") in ("en", "en-IN") else "hi"]


def complaint(case: dict) -> dict:
    v = {f: case.get(f) or "[not provided]" for f in FIELDS}
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
