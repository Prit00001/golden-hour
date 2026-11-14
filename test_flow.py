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

# Eval-found fixes: regional number words, "টাকা" is not a clock, the time phrase with a number wins.
assert extract("Axis Bank నుండి అరవై వేలు రూపాయలు పంపాను")["amount"] == 60000
assert at(fraud_time(extract("ಇಂದು ಮಧ್ಯಾಹ್ನ ಎರಡು ಗಂಟೆಗೆ")["datetime"], NOW)) == "11 14:00"
assert at(fraud_time(extract("நேற்று இரவு ஒன்பது மணிக்கு ஓடிபி சொன்னேன்")["datetime"], NOW)) == "10 21:00"
assert at(fraud_time(extract("UPI দিয়ে 20,000 টাকা কেটে নিয়েছে আজ দুপুর 3টায়")["datetime"], NOW)) == "11 15:00"
assert at(fraud_time(extract("12000 रुपये कट गए अभी 20 minute पहले")["datetime"], NOW)) == "11 14:40"
r = extract("ನಾನು ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್ ಮೂಲಕ ಕಳುಹಿಸಿದೆ, ಪುಲೀಸ್ ಎಂದು ಹೇಳಿದರು")
assert r["payment_mode"] == "net banking" and r["scam_type"] == "digital arrest"
print("eval fixes ok")

from app.flow import LINES, clean_case  # noqa: E402
# A day word with no clock time saves the real date (NOW is Wed 11 Nov), not just "parso".
for said, date, old in [("parso hua tha", "09 Nov 2026", True), ("परसों हुआ", "09 Nov 2026", True),
                        ("kal hua", "10 Nov 2026", False), ("aaj subah", "11 Nov 2026", False),
                        ("3 din pehle hua", "08 Nov 2026", True)]:
    c = {"language": "hi", "amount": 5000, "payment_mode": "UPI", "bank": "SBI", "scammer_contact": "not known",
         "scam_type": "other", "txn_id": "not known"}
    out, _ = advance(c, "x", said, now=NOW)
    cs = out["case"]
    assert cs["datetime"].startswith(date) and cs["fraud_ts"] is None and cs["fraud_day"], (said, cs["datetime"])
    assert (out["verdict"] == LINES["hi"]["old"]) == old, said
    assert date in out["complaint"]
assert clean_case({"fraud_day": 1.5})["fraud_day"] is None and clean_case(cs)["fraud_day"] == cs["fraud_day"]
assert at(fraud_time("2 din pehle 3 baje", NOW)) == "09 15:00"
print("day words ok")

# "40,000 kat gaye" is the amount even without ₹ or "rupaye"; a time or a phone number next to it is not.
assert extract("Abhi 20 minute pehle UPI se 40,000 kat gaye")["amount"] == 40000
assert extract("50000 भेजे थे")["amount"] == 50000
assert extract("9876543210 se call aaya, 2 baje gaye")["amount"] is None
print("debit verbs ok")

# Numbers Prisma writes as words: Hindi 13-99 and Kannada fused tens ("ಇಪ್ಪತ್ತೈದು" = 25), and hundreds.
assert extract("मेरे पच्चीस हज़ार रुपये कट गए")["amount"] == 25000
assert extract("सत्तासी हज़ार रुपये")["amount"] == 87000 and extract("पंद्रह हज़ार रुपये")["amount"] == 15000
assert extract("ನಾನು ಇಪ್ಪತ್ತೈದು ಸಾವಿರ ರೂಪಾಯಿ ಕಳುಹಿಸಿದೆ")["amount"] == 25000
assert extract("ತೊಂಬತ್ತೊಂಬತ್ತು ಸಾವಿರ ರೂಪಾಯಿ")["amount"] == 99000 and extract("ಇಪ್ಪತ್ತಮೂರು ಸಾವಿರ ರೂಪಾಯಿ")["amount"] == 23000
assert extract("ಹದಿನೈದು ಸಾವಿರ ರೂಪಾಯಿ")["amount"] == 15000 and extract("पाँच सौ रुपये कट गए")["amount"] == 500

# NEFT/RTGS UTRs start with the bank's IFSC code; a plain 12-digit UPI UTR and a phone still work as before.
assert extract("UTR SBIN412345678901")["txn_id"] == "SBIN412345678901"
assert extract("UTR है SBIN 4123 4567 8901")["txn_id"] == "SBIN412345678901"
assert extract("sbin412345678901")["txn_id"] == "SBIN412345678901"
assert extract("RTGS UTR SBINR52024111500123456")["txn_id"] == "SBINR52024111500123456"
assert extract("mera UTR 412345678901 hai")["txn_id"] == "412345678901"
assert extract("HDFC se 40,000 kat gaye, 9876543210 se call aaya")["txn_id"] is None
assert spoken_id("SBIN412345678901") == "S B I N, 4 1 2 3, 4 5 6 7, 8 9 0 1"

# A UTR or phone read in groups arrives in two pieces over the live call: hold the first, say "go on", join them.
def call(lines, lg, seed={"payment_mode": "UPI"}):
    c, h, outs = dict(seed), "", []
    for s in lines:
        o, _ = advance(c, h, s, now=NOW, lang_hint=lg)
        c, h = o["case"], h + " " + s
        outs.append(o)
    return outs, c
outs, c = call(["30 ನಿಮಿಷ ಹಿಂದೆ ಪೊಲೀಸ್ ಎಂದು ಹೇಳಿ ಹೆದರಿಸಿದರು, ನಾನು ಇಪ್ಪತ್ತೈದು ಸಾವಿರ ರೂಪಾಯಿ ಕಳುಹಿಸಿದೆ.", "Canara Bank",
                "9123456780 ಈ ನಂಬರ್ ಇಂದ ಕರೆ ಬಂತು.", "ಹೌದು.", "UTR 5234", "5, 6, 7, 8, 9, 0, 1, 2.", "ಹೌದು."], "kn")
assert outs[4].get("partial") and outs[4]["question"] == "ಹೂಂ, ಮುಂದೆ ಹೇಳಿ." and c["partial"] is None
assert c["amount"] == 25000 and c["txn_id"] == "523456789012" and "verdict" in outs[-1]
outs, c = call(["Abhi 20 minute pehle KYC update ke naam pe 40,000 kat gaye, SBI account se", "98765 se",
                "43210 se call aaya", "haan", "UTR SBIN 4123", "4567 8901", "haan"], "hi")
assert outs[1].get("partial") and outs[4].get("partial") and "verdict" in outs[-1]
assert c["scammer_contact"] == "9876543210" and c["txn_id"] == "SBIN412345678901"
# Not holding: "don't know", a whole UTR, or a piece that isn't digits.
outs, c = call(["Abhi 40,000 kat gaye SBI se", "9876543210", "haan", "aaj subah", "KYC", "pata nahi"], "hi")
assert c["txn_id"] == "not known" and not any(o.get("partial") for o in outs)
# The browser holds the case between turns, so the held piece is checked like the rest.
assert clean_case({"partial": "UTR 5234"})["partial"] == "UTR 5234"
assert clean_case({"partial": "1" * 12})["partial"] is None and clean_case({"partial": 5})["partial"] is None
print("voice numbers ok")

# One recorded clip with a pause inside comes back from REST STT as "UTR 52345678. 9012".
outs, c = call(["Abhi 40,000 kat gaye SBI se", "9876543210", "haan", "aaj subah", "KYC", "UTR 52345678. 9012"], "hi")
assert c["txn_id"] == "523456789012" and not outs[-1].get("partial")
# A lower-case word before the digits is not a bank code.
outs, c = call(["Abhi 40,000 kat gaye SBI se", "9876543210", "haan", "aaj subah", "KYC", "mera 52345678. 9012"], "hi")
assert c["txn_id"] == "523456789012"
print("one-piece UTR ok")

# "SBIN" said aloud: STT writes "SBI N" (SBI is one of its keyterms).
assert extract("UTR है, SBI N412345678901।")["txn_id"] == "SBIN412345678901"
assert extract("UTR SBI N 412345678901.")["txn_id"] == "SBIN412345678901"
outs, c = call(["Abhi 40,000 kat gaye SBI se", "9876543210", "haan", "aaj subah", "KYC", "UTR SBI N 4123", "4567 8901"], "hi")
assert outs[-2].get("partial") and c["txn_id"] == "SBIN412345678901"
assert extract("SBI se 40,000 kat gaye")["txn_id"] is None and extract("SBI account 412345678901")["txn_id"] == "412345678901"
print("spoken bank code ok")
