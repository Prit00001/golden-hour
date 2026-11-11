"""Synthetic victim statements (no real PII) with the fields a correct system should pull out.

`text` is what Timbre speaks and the reference for WER. Numbers are digits (Timbre says them as words; Prisma
writes them back as digits) and IDs are spaced so they are read digit by digit. `time` is the fraud time as
"DD HH:MM" when "now" is 11 Nov 2026, 3 pm IST.
"""

CASES = [
    # Hindi
    ("hi", "मेरे SBI खाते से 40,000 रुपये कट गए, आज दोपहर 1 बजे KYC अपडेट के नाम पर कॉल आया था, PhonePe से पैसे गए।",
     {"amount": 40000, "bank": "SBI", "payment_mode": "UPI", "scam_type": "fake KYC update", "time": "11 13:00"}),
    ("hi", "कल एक आदमी ने खुद को CBI ऑफिसर बताया और डिजिटल अरेस्ट की धमकी दी, मैंने नेट बैंकिंग से 2 लाख रुपये भेज दिए, HDFC बैंक से।",
     {"amount": 200000, "bank": "HDFC Bank", "payment_mode": "net banking", "scam_type": "digital arrest"}),
    ("hi", "UTR नंबर है 4 1 2 3 4 5 6 7 8 9 0 1।", {"txn_id": "412345678901"}),
    ("hi", "मुझे 9 8 7 6 5 4 3 2 1 0 नंबर से कॉल आया था।", {"scammer_contact": "9876543210"}),
    ("hi", "पार्सल में ड्रग्स मिलने की बात कहकर डराया, मैंने Google Pay से 25,000 रुपये दे दिए, पंजाब नेशनल बैंक का खाता है।",
     {"amount": 25000, "bank": "Punjab National Bank", "payment_mode": "UPI", "scam_type": "courier/parcel scam"}),
    ("hi", "बिजली का बिल बकाया है बोलकर लिंक भेजा, लिंक खोलते ही मेरे Bank of Baroda खाते से 18,500 रुपये निकल गए।",
     {"amount": 18500, "bank": "Bank of Baroda", "scam_type": "electricity bill scam"}),
    ("hi", "वर्क फ्रॉम होम टास्क के नाम पर मुझसे कुल 75,000 रुपये UPI से ले लिए, खाता केनरा बैंक में है।",
     {"amount": 75000, "bank": "Canara Bank", "payment_mode": "UPI", "scam_type": "job/task scam"}),
    ("hi", "शेयर ट्रेडिंग ऐप में इन्वेस्ट करवाया, 1 लाख 50 हज़ार रुपये चले गए, कोटक बैंक से नेट बैंकिंग से भेजे थे।",
     {"amount": 150000, "bank": "Kotak Mahindra Bank", "payment_mode": "net banking", "scam_type": "investment scam"}),
    ("hi", "किसी ने OTP मांगा और मैंने बता दिया, ICICI के डेबिट कार्ड से 12,000 रुपये कट गए, अभी 20 मिनट पहले।",
     {"amount": 12000, "bank": "ICICI Bank", "payment_mode": "card", "scam_type": "OTP fraud", "time": "11 14:40"}),
    ("hi", "रिफंड दिलाने के नाम पर QR कोड स्कैन करवाया, Paytm से 9,999 रुपये गए, एक्सिस बैंक का अकाउंट है।",
     {"amount": 9999, "bank": "Axis Bank", "payment_mode": "UPI", "scam_type": "refund scam"}),
    ("hi", "लॉटरी जीतने की बात कही और प्रोसेसिंग फीस के 5,000 रुपये मांगे, मैंने यूनियन बैंक से UPI कर दिया।",
     {"amount": 5000, "bank": "Union Bank of India", "payment_mode": "UPI", "scam_type": "lottery scam"}),
    ("hi", "ठग का UPI ID था lucky.winner@ybl, उस पर मैंने 30,000 रुपये भेजे।",
     {"scammer_contact": "lucky.winner@ybl", "amount": 30000, "payment_mode": "UPI"}),
    # English
    ("en", "Someone called pretending to be from customs, said my parcel had drugs, and I transferred 1 lakh rupees by net banking from my Yes Bank account.",
     {"amount": 100000, "bank": "Yes Bank", "payment_mode": "net banking"}),
    ("en", "My HDFC credit card was charged 15,000 rupees yesterday night after I shared an OTP.",
     {"amount": 15000, "bank": "HDFC Bank", "payment_mode": "card", "scam_type": "OTP fraud"}),
    ("en", "The UTR is 3 0 9 8 7 6 5 4 3 2 1 0.", {"txn_id": "309876543210"}),
    ("en", "I paid 45,000 rupees through Google Pay to a fake electricity board number, 9 1 2 3 4 5 6 7 8 9, from my State Bank account.",
     {"amount": 45000, "bank": "SBI", "payment_mode": "UPI", "scam_type": "electricity bill scam", "scammer_contact": "9123456789"}),
    ("en", "They took the money to the UPI ID refund.help@paytm, 8,200 rupees, this morning at 10 am.",
     {"scammer_contact": "refund.help@paytm", "amount": 8200, "time": "11 10:00"}),
    # Kannada
    ("kn", "ನನ್ನ SBI ಖಾತೆಯಿಂದ UPI ಮೂಲಕ 40,000 ರೂಪಾಯಿ ಹೋಯಿತು, ಇಂದು ಮಧ್ಯಾಹ್ನ 2 ಗಂಟೆಗೆ.",
     {"amount": 40000, "bank": "SBI", "payment_mode": "UPI", "time": "11 14:00"}),
    ("kn", "ಪೊಲೀಸ್ ಎಂದು ಹೇಳಿ ಕರೆ ಮಾಡಿದರು, ನಾನು Canara Bank ನಿಂದ ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್ ಮೂಲಕ 1,20,000 ರೂಪಾಯಿ ಕಳುಹಿಸಿದೆ.",
     {"amount": 120000, "bank": "Canara Bank", "payment_mode": "net banking", "scam_type": "digital arrest"}),
    ("kn", "UTR ಸಂಖ್ಯೆ 5 6 7 8 1 2 3 4 9 0 1 2.", {"txn_id": "567812349012"}),
    ("kn", "ಪಾರ್ಸೆಲ್ ನಲ್ಲಿ ಡ್ರಗ್ಸ್ ಇದೆ ಎಂದು ಹೆದರಿಸಿದರು, PhonePe ಮೂಲಕ 35,000 ರೂಪಾಯಿ ಕೊಟ್ಟೆ.",
     {"amount": 35000, "payment_mode": "UPI", "scam_type": "courier/parcel scam"}),
    ("kn", "9 8 4 5 0 1 2 3 4 5 ನಂಬರ್‌ನಿಂದ ಕರೆ ಬಂತು, KYC ಅಪ್‌ಡೇಟ್ ಮಾಡಬೇಕು ಎಂದರು.",
     {"scammer_contact": "9845012345", "scam_type": "fake KYC update"}),
    # Tamil
    ("ta", "என் SBI கணக்கில் இருந்து UPI மூலம் 40,000 ரூபாய் போனது, இன்று மதியம் 2 மணிக்கு.",
     {"amount": 40000, "bank": "SBI", "payment_mode": "UPI", "time": "11 14:00"}),
    ("ta", "போலீஸ் என்று சொல்லி மிரட்டினார்கள், Indian Bank கணக்கில் இருந்து 80,000 ரூபாய் நெட் பேங்கிங் மூலம் அனுப்பினேன்.",
     {"amount": 80000, "bank": "Indian Bank", "payment_mode": "net banking", "scam_type": "digital arrest"}),
    ("ta", "UTR எண் 6 7 8 9 0 1 2 3 4 5 6 7.", {"txn_id": "678901234567"}),
    ("ta", "வேலை தருவதாகச் சொல்லி Google Pay மூலம் 15,000 ரூபாய் வாங்கினார்கள்.",
     {"amount": 15000, "payment_mode": "UPI", "scam_type": "job/task scam"}),
    ("ta", "நேற்று இரவு 9 மணிக்கு OTP சொன்னேன், HDFC கார்டில் இருந்து 22,000 ரூபாய் போனது.",
     {"amount": 22000, "bank": "HDFC Bank", "payment_mode": "card", "scam_type": "OTP fraud", "time": "10 21:00"}),
    # Telugu
    ("te", "నా SBI ఖాతా నుండి UPI ద్వారా 50,000 రూపాయలు పోయాయి, ఈ రోజు ఉదయం 11 గంటలకు.",
     {"amount": 50000, "bank": "SBI", "payment_mode": "UPI", "time": "11 11:00"}),
    ("te", "పోలీస్ అని చెప్పి బెదిరించారు, Axis Bank నుండి 60,000 రూపాయలు పంపాను.",
     {"amount": 60000, "bank": "Axis Bank", "scam_type": "digital arrest"}),
    ("te", "UTR నంబర్ 7 8 9 0 1 2 3 4 5 6 7 8.", {"txn_id": "789012345678"}),
    # Bengali
    ("bn", "আমার SBI অ্যাকাউন্ট থেকে UPI দিয়ে 20,000 টাকা কেটে নিয়েছে, আজ দুপুর 3টায়।",
     {"amount": 20000, "bank": "SBI", "payment_mode": "UPI", "time": "11 15:00"}),
    ("bn", "পুলিশ সেজে ফোন করেছিল, HDFC থেকে 1 লাখ টাকা পাঠিয়েছি।",
     {"amount": 100000, "bank": "HDFC Bank", "scam_type": "digital arrest"}),
    # Marathi
    ("mr", "माझ्या SBI खात्यातून UPI ने 30,000 रुपये गेले, आज दुपारी 1 वाजता.",
     {"amount": 30000, "bank": "SBI", "payment_mode": "UPI", "time": "11 13:00"}),
    ("mr", "पोलीस असल्याचे सांगून धमकावले, बँक ऑफ इंडियातून 70,000 रुपये पाठवले.",
     {"amount": 70000, "bank": "Bank of India", "scam_type": "digital arrest"}),
]
