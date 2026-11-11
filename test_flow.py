"""Self-check for app/flow.py (no network). Run: python3 test_flow.py"""
from app.flow import complaint, merge, new_case, next_question

said = "mera 40000 kat gaya UPI se, SBI account, UTR 412345678901, call aaya 9876543210 se"

# LLM output with one hallucinated UTR and one real contact
case = merge(new_case(), {"amount": "40,000", "payment_mode": "UPI", "bank": "SBI",
                          "txn_id": "999999999999", "scammer_contact": "98765 43210",
                          "language": "hi"}, said)
assert case["amount"] == 40000
assert case["txn_id"] is None, "invented UTR must be dropped"
assert case["scammer_contact"] == "98765 43210"
assert next_question(case).startswith("यह कब"), "datetime is next missing field"

# second turn fills the rest; existing fields are not overwritten
case = merge(case, {"datetime": "aaj 3 baje", "txn_id": "412345678901", "bank": "HDFC"},
             said + " aaj 3 baje")
assert case["bank"] == "SBI"
assert case["txn_id"] == "412345678901"
assert next_question(case).startswith("उन्होंने"), "scam type is the only field left"
case["scam_type"] = "fake KYC update"
assert next_question(case) is None

c = complaint(case)
assert "Rs. 40,000" in c["complaint"] and "412345678901" in c["bank_email"]
print("flow ok")

# rules extractor on Prisma `transcribe`-style output
from app.rules import extract

r = extract("आज शाम 4 बजे KYC के नाम पर कॉल आया, मेरे SBI खाते से PhonePe से ₹40,000 कट गए। "
            "UTR 4123 4567 8901 है, नंबर 98765 43210 से कॉल था")
assert r["amount"] == 40000, r
assert r["bank"] == "SBI" and r["payment_mode"] == "UPI" and r["scam_type"] == "fake KYC update"
assert r["txn_id"] == "412345678901" and r["scammer_contact"] == "9876543210"
assert r["datetime"].startswith("आज") and r["language"] == "hi"

r = extract("Someone from CBI called yesterday, I paid 2 lakh by net banking from HDFC to fraud.pay@ybl")
assert r["amount"] == 200000 and r["bank"] == "HDFC Bank" and r["payment_mode"] == "net banking"
assert r["scam_type"] == "digital arrest" and r["scammer_contact"] == "fraud.pay@ybl" and r["language"] == "en"
r = extract("My ICICI credit card was charged 15,000 rupees yesterday night after I shared an OTP.")
assert r["scam_type"] == "OTP fraud", r  # "charged" must not match the ED keyword
assert extract("आज दोपहर 2 बजे")["datetime"] == "आज दोपहर 2 बजे"
assert extract("SBI se 40,000 rupaye kat gaye")["amount"] == 40000  # "k" multiplier must not hit "kat"
assert extract("50k gaye")["amount"] == 50000
print("rules ok")

# one conversation turn (shared by /turn and /ws/call)
from app.flow import advance, bare_amount

assert bare_amount("40,000 tha") == "40,000" and bare_amount("98765 43210") is None
out, speak = advance({}, "", "98765 43210 se call aaya")
assert out["case"]["amount"] is None and speak == out["question"]  # first turn: a phone number is not the amount
assert out["case"]["confirming"] == "scammer_contact"  # the number is read back first
out, _ = advance(out["case"], "98765 43210 se call aaya", "haan")
out, _ = advance(out["case"], "98765 43210 se call aaya haan", "40,000")
assert out["case"]["amount"] == 40000  # bare number answering "how much?"
print("advance ok")

# Step 3: corrections, ID read-back, "don't know", urgency, timestamp, verdict.
from datetime import datetime
from app.flow import IST, fraud_time, spoken_id

NOW = datetime(2026, 11, 11, 15, 0, tzinfo=IST).timestamp()  # Wed 3 pm IST
at = lambda ts: datetime.fromtimestamp(ts, IST).strftime("%d %H:%M")
assert at(fraud_time("आज दोपहर 2 बजे", NOW)) == "11 14:00"
assert at(fraud_time("2 बजे", NOW)) == "11 14:00"           # bare hour: latest past 2:00/14:00
assert at(fraud_time("kal raat 11 baje", NOW)) == "10 23:00"
assert at(fraud_time("subah 10 baje", NOW)) == "11 10:00"
assert at(fraud_time("raat 2 baje", NOW)) == "11 02:00"
assert at(fraud_time("40 मिनट पहले", NOW)) == "11 14:20"
assert at(fraud_time("4 pm", NOW)) == "10 16:00"            # can't be in the future: yesterday
assert fraud_time("kal", NOW) is None
assert spoken_id("412345678901") == "4 1 2 3, 4 5 6 7, 8 9 0 1" and spoken_id("9876543210") == "9 8 7 6 5, 4 3 2 1 0"

def turn(case, hist, said):
    out, speak = advance(case, hist, said, now=NOW)
    return out["case"], hist + " " + said, out, speak

c, h, out, speak = turn({}, "", "SBI से 40,000 रुपये गए UPI से, आज दोपहर 2 बजे")
assert c["fraud_ts"] == NOW - 3600 and c["urged"] and speak.startswith("यह अभी हाल ही में हुआ है")
assert c["meta"]["amount"] == {"confirmed": False, "source_text": "SBI से 40,000 रुपये गए UPI से, आज दोपहर 2 बजे"}
c, h, out, speak = turn(c, h, "नहीं, 50,000 थे, और बैंक HDFC था, SBI नहीं")   # corrections overwrite
assert c["amount"] == 50000 and c["bank"] == "HDFC Bank", c
assert not speak.startswith("यह अभी"), "urgency is said once"
c, h, out, _ = turn(c, h, "पता नहीं।")                                          # scammer contact skipped
assert c["scammer_contact"] == "not known" and out["question"].startswith("उन्होंने")
c, h, out, _ = turn(c, h, "बोला बिजली का बिल बकाया है")
assert c["scam_type"] == "electricity bill scam"
c, h, out, speak = turn(c, h, "UTR 4123 4567 8902")                             # read back, not finished
assert c["confirming"] == "txn_id" and "4 1 2 3, 4 5 6 7, 8 9 0 2" in speak and "checklist" not in out
c, h, out, speak = turn(c, h, "नहीं, 4123 4567 8901")                           # wrong: corrected, read back again
assert c["txn_id"] == "412345678901" and c["confirming"] == "txn_id" and "8 9 0 1" in speak
c, h, out, speak = turn(c, h, "हाँ, सही है।")                                  # confirmed: done, with verdict
assert c["meta"]["txn_id"]["confirmed"] and c["confirming"] is None
assert out["verdict"] == "यह 1 घंटे पहले हुआ है, इसलिए पैसा रोके जाने का अभी भी मौका है।" and speak.startswith(out["verdict"])
assert "Rs. 50,000" in out["complaint"] and "HDFC Bank" in out["bank_email"]
assert "On 11 Nov 2026, 02:00 PM IST," in out["complaint"], out["complaint"]

c2, h2, _, _ = turn({**c, "txn_id": None, "confirming": None}, h, "UTR 412345678901")
c2, h2, out, _ = turn(c2, h2, "गलत है")                                      # "no" alone: ask for it again
assert c2["txn_id"] is None and out["question"].startswith("बैंक के SMS")
c3, _, out, _ = turn({**c, "fraud_ts": NOW - 3 * 86400}, h, "हाँ")
assert out["verdict"].startswith("इसे एक दिन से ज़्यादा")
print("step3 ok")

# Step 4: languages, Hinglish, spoken numbers.
from app.rules import language, normalize

assert language("ನನ್ನ ಖಾತೆಯಿಂದ 40,000 ರೂಪಾಯಿ ಹೋಯಿತು") == "kn" and language("என் கணக்கில் இருந்து பணம் போனது") == "ta"
assert language("నా ఖాతా నుండి డబ్బు పోయింది") == "te" and language("আমার অ্যাকাউন্ট থেকে টাকা কেটে নিয়েছে") == "bn"
assert language("माझ्या खात्यातून पैसे गेले आहेत") == "mr" and language("मेरे खाते से पैसे कट गए") == "hi"
assert language("SBI se 40,000 kat gaye") == "hi" and language("My SBI account was debited") == "en"
assert normalize("UTR चार एक दो तीन, नौ बजे") == "UTR 4 1 2 3, 9 बजे"
assert normalize("do baje paise gaye") == "2 baje paise gaye" and normalize("I do not know") == "I do not know"
assert normalize("৪০,০০০ টাকা") == "40,000 টাকা"
assert extract("पचास हज़ार रुपये गए")["amount"] == 50000
assert extract("ನಿನ್ನೆ ರಾತ್ರಿ 11 ಗಂಟೆಗೆ 40,000 ರೂಪಾಯಿ ಹೋಯಿತು")["amount"] == 40000
assert at(fraud_time("ನಿನ್ನೆ ರಾತ್ರಿ 11 ಗಂಟೆಗೆ", NOW)) == "10 23:00"
assert at(fraud_time("இன்று மதியம் 2 மணிக்கு", NOW)) == "11 14:00"
assert at(fraud_time("40 நிமிடங்களுக்கு முன்பு", NOW)) == "11 14:20"
assert at(fraud_time("আজ দুপুর ২টায়", NOW)) == "11 14:00" and at(fraud_time("आज दुपारी 2 वाजता", NOW)) == "11 14:00"

# Hinglish in -> Hindi out; STT's language code wins over script (Marathi in Devanagari).
out, _ = advance({}, "", "SBI se 40,000 rupaye kat gaye UPI se", now=NOW)
assert out["case"]["language"] == "hi" and out["question"].startswith("यह कब")
out, _ = advance({}, "", "SBI मधून 40,000 रुपये गेले UPI ने", now=NOW, lang_hint="mr-IN")
assert out["case"]["language"] == "mr" and out["question"] == "हे कधी झाले? अंदाजे वेळ सांगा."
out, _ = advance({}, "", "My money is gone", now=NOW, lang_hint="ml-IN")
assert out["question"].startswith("How much"), "languages we don't speak get English"

# A whole Kannada call: free-text bank, "don't know", read-back confirmed with ಹೌದು, Kannada verdict.
c, h = {}, ""
for said, hint in [("ನನ್ನ ಖಾತೆಯಿಂದ UPI ಮೂಲಕ 40,000 ರೂಪಾಯಿ ಹೋಯಿತು", "kn-IN"), ("ಗ್ರಾಮೀಣ ಬ್ಯಾಂಕ್", "kn-IN"),
                   ("ಇಂದು ಮಧ್ಯಾಹ್ನ 2 ಗಂಟೆಗೆ", "kn-IN"), ("ಗೊತ್ತಿಲ್ಲ", "kn-IN"), ("ಪೊಲೀಸ್ ಎಂದು ಹೇಳಿದರು", "kn-IN"),
                   ("UTR 412345678901", "kn-IN"), ("ಹೌದು", "kn-IN")]:
    out, speak = advance(c, h, said, now=NOW, lang_hint=hint)
    c, h = out["case"], h + " " + said
assert c["language"] == "kn" and c["bank"] == "ಗ್ರಾಮೀಣ ಬ್ಯಾಂಕ್" and c["scammer_contact"] == "not known"
assert c["scam_type"] == "digital arrest" and c["meta"]["txn_id"]["confirmed"] and c["fraud_ts"] == NOW - 3600
assert out["verdict"] == "ಇದು 1 ಗಂಟೆ ಹಿಂದೆ ಆಗಿದೆ, ಆದ್ದರಿಂದ ಹಣವನ್ನು ತಡೆಹಿಡಿಯುವ ಸಾಧ್ಯತೆ ಇನ್ನೂ ಇದೆ."
assert out["checklist"][0].startswith("ಗಾಬರಿಯಾಗಬೇಡಿ") and "Rs. 40,000" in out["complaint"]

# Tamil: read-back rejected with இல்லை, then re-read.
c, _ = advance({}, "", "என் SBI கணக்கில் இருந்து UPI மூலம் 40,000 ரூபாய் போனது, UTR 412345678901", now=NOW, lang_hint="ta-IN")
c = c["case"]
assert c["confirming"] == "txn_id"
out, speak = advance(c, "x", "இல்லை, 412345678902", now=NOW, lang_hint="ta-IN")
assert out["case"]["txn_id"] == "412345678902" and speak.startswith("நான் UTR இப்படி குறித்துக்கொண்டேன்: 4 1 2 3")
print("languages ok")
