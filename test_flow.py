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
