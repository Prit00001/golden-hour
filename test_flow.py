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
