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

# Matched as whole words/phrases (a Devanagari "ना" must not hit "नाम"). hi/en/Hinglish, kn, ta, te, bn, mr.
YES = ["haan", "haa", "han", "ha", "ji", "sahi", "correct", "right", "yes", "yeah", "yep", "theek", "thik",
       "bilkul", "हाँ", "हां", "हा", "जी", "सही", "ठीक", "बिल्कुल",
       "ಹೌದು", "ಹೂಂ", "ಸರಿ", "ஆமாம்", "ஆம்", "சரி", "అవును", "ఔను", "సరే", "హా", "হ্যাঁ", "হ্যা", "হাঁ", "ঠিক",
       "हो", "होय", "बरोबर"]
NO = ["nahi", "nahin", "nhi", "na", "no", "galat", "wrong", "incorrect", "नहीं", "नही", "ना", "गलत", "ग़लत",
      "ಇಲ್ಲ", "ತಪ್ಪು", "இல்லை", "தவறு", "కాదు", "లేదు", "తప్పు", "না", "নয়", "ভুল", "नाही", "चूक"]
CORRECTION = NO + ["actually", "asal", "sorry", "matlab", "असल", "मतलब", "सॉरी"]
DONT_KNOW = ["pata nahi", "pata nahin", "nahi pata", "नहीं पता", "पता नहीं", "don't know", "dont know",
             "not sure", "no idea", "yaad nahi", "याद नहीं", "skip", "ಗೊತ್ತಿಲ್ಲ", "தெரியாது", "தெரியவில்லை",
             "తెలియదు", "జ్ఞాపకం లేదు", "জানি না", "জানিনা", "মনে নেই", "माहीत नाही", "माहित नाही", "आठवत नाही"]
# Free-text answers are kept as said when the rules can't name them ("मेरे गाँव के बैंक में" is still a bank).
FREE_TEXT = {"bank", "payment_mode", "scam_type", "datetime"}

# Spoken at call start: who we are, the disclaimer, then the first question. "hi" lists the languages (auto mode).
GREETING = {
    "hi": "नमस्ते, मैं गोल्डन ऑवर हूँ। यह सरकारी सेवा नहीं है और पैसे वापस नहीं दिला सकती, पर मैं आपको जल्दी से "
          "1930 और आपके बैंक तक पहुँचने में मदद करूँगी। आप हिंदी, English, कन्नड़, तमिल, तेलुगु, बांग्ला या मराठी "
          "में बोल सकते हैं। बताइए, क्या हुआ?",
    "en": "Hello, I'm Golden Hour. I'm not a government service and can't recover money, but I'll help you reach "
          "1930 and your bank quickly. Tell me, what happened?",
    "kn": "ನಮಸ್ಕಾರ, ನಾನು ಗೋಲ್ಡನ್ ಅವರ್. ಇದು ಸರ್ಕಾರಿ ಸೇವೆ ಅಲ್ಲ, ಹಣವನ್ನು ವಾಪಸ್ ಕೊಡಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ, ಆದರೆ 1930 ಮತ್ತು "
          "ನಿಮ್ಮ ಬ್ಯಾಂಕನ್ನು ಬೇಗ ತಲುಪಲು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ಹೇಳಿ, ಏನಾಯಿತು?",
    "ta": "வணக்கம், நான் கோல்டன் ஹவர். இது அரசு சேவை அல்ல, பணத்தை மீட்டுத் தர முடியாது, ஆனால் 1930-ஐயும் உங்கள் "
          "வங்கியையும் விரைவாக அணுக உதவுவேன். சொல்லுங்கள், என்ன நடந்தது?",
    "te": "నమస్కారం, నేను గోల్డెన్ అవర్. ఇది ప్రభుత్వ సేవ కాదు, డబ్బును తిరిగి ఇప్పించలేను, కానీ 1930 మరియు మీ "
          "బ్యాంకును త్వరగా చేరడానికి సహాయం చేస్తాను. చెప్పండి, ఏం జరిగింది?",
    "bn": "নমস্কার, আমি গোল্ডেন আওয়ার। এটা সরকারি পরিষেবা নয়, টাকা ফেরত দিতে পারব না, কিন্তু 1930 আর আপনার "
          "ব্যাঙ্কের কাছে তাড়াতাড়ি পৌঁছাতে সাহায্য করব। বলুন, কী হয়েছে?",
    "mr": "नमस्कार, मी गोल्डन अवर. ही सरकारी सेवा नाही आणि पैसे परत मिळवून देऊ शकत नाही, पण 1930 आणि तुमच्या "
          "बँकेपर्यंत लवकर पोहोचायला मदत करेन. सांगा, काय झाले?",
}

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
    "kn": {
        "amount": "ಎಷ್ಟು ಹಣ ಹೋಗಿದೆ?",
        "payment_mode": "ಹಣ ಹೇಗೆ ಹೋಯಿತು — UPI, ಕಾರ್ಡ್ ಅಥವಾ ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್?",
        "bank": "ನಿಮ್ಮ ಖಾತೆ ಯಾವ ಬ್ಯಾಂಕಿನಲ್ಲಿದೆ?",
        "datetime": "ಇದು ಯಾವಾಗ ಆಯಿತು? ಸುಮಾರು ಸಮಯ ಹೇಳಿ.",
        "scammer_contact": "ವಂಚಕರು ಯಾವ ನಂಬರ್‌ನಿಂದ ಕರೆ ಮಾಡಿದರು, ಅಥವಾ ಯಾವ UPI ID ಗೆ ಹಣ ಹೋಯಿತು? ಗೊತ್ತಿಲ್ಲದಿದ್ದರೆ 'ಗೊತ್ತಿಲ್ಲ' ಎಂದು ಹೇಳಿ.",
        "scam_type": "ಅವರು ಏನು ಹೇಳಿ ಹಣ ತೆಗೆದುಕೊಂಡರು — KYC ಅಪ್‌ಡೇಟ್, ಪೊಲೀಸ್ ಅಥವಾ CBI, ಪಾರ್ಸೆಲ್, ಕೆಲಸ, ಅಥವಾ ಬೇರೆ ಏನಾದರೂ?",
        "txn_id": "ಬ್ಯಾಂಕ್ SMS ನಲ್ಲಿ ಹನ್ನೆರಡು ಅಂಕಿಯ UTR ಅಥವಾ ಟ್ರಾನ್ಸಾಕ್ಷನ್ ನಂಬರ್ ಇರುತ್ತದೆ, ದಯವಿಟ್ಟು ಓದಿ ಹೇಳಿ.",
    },
    "ta": {
        "amount": "எவ்வளவு பணம் போனது?",
        "payment_mode": "பணம் எப்படி போனது — UPI, கார்டு, அல்லது நெட் பேங்கிங்?",
        "bank": "உங்கள் கணக்கு எந்த வங்கியில் உள்ளது?",
        "datetime": "இது எப்போது நடந்தது? தோராயமான நேரத்தைச் சொல்லுங்கள்.",
        "scammer_contact": "மோசடி செய்தவர் எந்த எண்ணிலிருந்து அழைத்தார், அல்லது எந்த UPI ID-க்கு பணம் போனது? தெரியாவிட்டால் 'தெரியாது' என்று சொல்லுங்கள்.",
        "scam_type": "அவர்கள் என்ன சொல்லி பணம் வாங்கினார்கள் — KYC அப்டேட், போலீஸ் அல்லது CBI, பார்சல், வேலை, அல்லது வேறு ஏதாவது?",
        "txn_id": "வங்கி SMS-இல் பன்னிரண்டு இலக்க UTR அல்லது பரிவர்த்தனை எண் இருக்கும், தயவுசெய்து படித்துச் சொல்லுங்கள்.",
    },
    "te": {
        "amount": "ఎంత డబ్బు పోయింది?",
        "payment_mode": "డబ్బు ఎలా పోయింది — UPI, కార్డు, లేదా నెట్ బ్యాంకింగ్?",
        "bank": "మీ ఖాతా ఏ బ్యాంకులో ఉంది?",
        "datetime": "ఇది ఎప్పుడు జరిగింది? సుమారు సమయం చెప్పండి.",
        "scammer_contact": "మోసగాడు ఏ నంబర్ నుండి కాల్ చేశాడు, లేదా ఏ UPI ID కి డబ్బు వెళ్ళింది? తెలియకపోతే 'తెలియదు' అని చెప్పండి.",
        "scam_type": "వాళ్ళు ఏం చెప్పి డబ్బు తీసుకున్నారు — KYC అప్‌డేట్, పోలీస్ లేదా CBI, పార్సెల్, ఉద్యోగం, లేదా ఇంకేదైనా?",
        "txn_id": "బ్యాంకు SMS లో పన్నెండు అంకెల UTR లేదా ట్రాన్సాక్షన్ నంబర్ ఉంటుంది, దయచేసి చదివి చెప్పండి.",
    },
    "bn": {
        "amount": "কত টাকা কেটে নিয়েছে?",
        "payment_mode": "টাকা কীভাবে গেছে — UPI, কার্ড, না নেট ব্যাঙ্কিং?",
        "bank": "আপনার অ্যাকাউন্ট কোন ব্যাঙ্কে?",
        "datetime": "এটা কখন হয়েছে? মোটামুটি সময়টা বলুন।",
        "scammer_contact": "প্রতারক কোন নম্বর থেকে ফোন করেছিল, বা কোন UPI ID-তে টাকা গেছে? না জানলে 'জানি না' বলুন।",
        "scam_type": "ওরা কী বলে টাকা নিয়েছে — KYC আপডেট, পুলিশ বা CBI, পার্সেল, চাকরি, নাকি অন্য কিছু?",
        "txn_id": "ব্যাঙ্কের SMS-এ বারো সংখ্যার UTR বা ট্রানজ্যাকশন নম্বর থাকবে, দয়া করে পড়ে শোনান।",
    },
    "mr": {
        "amount": "किती पैसे गेले?",
        "payment_mode": "पैसे कसे गेले — UPI, कार्ड, की नेट बँकिंग?",
        "bank": "तुमचे खाते कोणत्या बँकेत आहे?",
        "datetime": "हे कधी झाले? अंदाजे वेळ सांगा.",
        "scammer_contact": "फसवणूक करणाऱ्याने कोणत्या नंबरवरून कॉल केला, किंवा कोणत्या UPI ID वर पैसे गेले? माहीत नसेल तर 'माहीत नाही' म्हणा.",
        "scam_type": "त्यांनी काय सांगून पैसे घेतले — KYC अपडेट, पोलीस किंवा CBI, पार्सल, नोकरी, की आणखी काही?",
        "txn_id": "बँकेच्या SMS मध्ये बारा अंकी UTR किंवा ट्रान्झॅक्शन नंबर असेल, कृपया वाचून सांगा.",
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
    "kn": [
        "ಗಾಬರಿಯಾಗಬೇಡಿ. ಮೊದಲು ಈಗಲೇ 1930 ಗೆ ಕರೆ ಮಾಡಿ, ಇದು ಸರ್ಕಾರದ ಸೈಬರ್ ವಂಚನೆ ಸಹಾಯವಾಣಿ.",
        "ನಂತರ ನಿಮ್ಮ ಬ್ಯಾಂಕಿನ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ, ಖಾತೆ ಮತ್ತು ಕಾರ್ಡ್ ಅನ್ನು ತಕ್ಷಣ ಫ್ರೀಜ್ ಮಾಡಿಸಿ.",
        "ಆಮೇಲೆ cybercrime.gov.in ನಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ. ದೂರಿನ ಪೂರ್ಣ ಕರಡು ಪರದೆಯ ಮೇಲೆ ಸಿದ್ಧವಿದೆ.",
        "ಯಾರಿಗೂ OTP ಅಥವಾ PIN ಹೇಳಬೇಡಿ. ಹಣ ವಾಪಸ್ ಕೊಡಿಸುತ್ತೇವೆ ಎಂದು ಶುಲ್ಕ ಕೇಳುವವರೂ ವಂಚಕರೇ.",
    ],
    "ta": [
        "பதற வேண்டாம். முதலில் இப்போதே 1930-க்கு அழையுங்கள், இது அரசின் சைபர் மோசடி உதவி எண்.",
        "பிறகு உங்கள் வங்கியின் உதவி எண்ணை அழைத்து, கணக்கையும் கார்டையும் உடனே முடக்கச் சொல்லுங்கள்.",
        "அதன் பிறகு cybercrime.gov.in-இல் புகார் பதிவு செய்யுங்கள். புகாரின் முழு வரைவு திரையில் தயாராக உள்ளது.",
        "யாரிடமும் OTP அல்லது PIN சொல்லாதீர்கள். பணத்தை மீட்டுத் தருவதாகக் கட்டணம் கேட்பவரும் மோசடிக்காரரே.",
    ],
    "te": [
        "కంగారు పడకండి. ముందు ఇప్పుడే 1930 కి కాల్ చేయండి, ఇది ప్రభుత్వ సైబర్ మోసాల హెల్ప్‌లైన్.",
        "తర్వాత మీ బ్యాంకు హెల్ప్‌లైన్‌కు కాల్ చేసి, ఖాతా మరియు కార్డును వెంటనే ఫ్రీజ్ చేయించండి.",
        "ఆ తర్వాత cybercrime.gov.in లో ఫిర్యాదు నమోదు చేయండి. ఫిర్యాదు పూర్తి డ్రాఫ్ట్ స్క్రీన్‌పై సిద్ధంగా ఉంది.",
        "ఎవరికీ OTP లేదా PIN చెప్పకండి. డబ్బు తిరిగి ఇప్పిస్తామని ఫీజు అడిగేవాళ్ళు కూడా మోసగాళ్ళే.",
    ],
    "bn": [
        "ভয় পাবেন না। প্রথমে এখনই 1930-এ ফোন করুন, এটা সরকারি সাইবার প্রতারণা হেল্পলাইন।",
        "তারপর আপনার ব্যাঙ্কের হেল্পলাইনে ফোন করে অ্যাকাউন্ট আর কার্ড এখনই ফ্রিজ করান।",
        "তারপর cybercrime.gov.in-এ অভিযোগ দায়ের করুন। অভিযোগের পুরো খসড়া স্ক্রিনে তৈরি আছে।",
        "কাউকে OTP বা PIN বলবেন না। টাকা ফেরত দেওয়ার নামে কেউ ফি চাইলে সেটাও প্রতারণা।",
    ],
    "mr": [
        "घाबरू नका. सर्वात आधी आत्ताच 1930 वर कॉल करा, ही सरकारी सायबर फसवणूक हेल्पलाइन आहे.",
        "मग तुमच्या बँकेच्या हेल्पलाइनवर कॉल करून खाते आणि कार्ड लगेच फ्रीज करायला सांगा.",
        "त्यानंतर cybercrime.gov.in वर तक्रार नोंदवा. तक्रारीचा पूर्ण मसुदा स्क्रीनवर तयार आहे.",
        "कोणालाही OTP किंवा PIN सांगू नका. पैसे परत मिळवून देण्यासाठी फी मागणारेही फसवणूक करणारेच आहेत.",
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
    "kn": {
        "readback": "ನಾನು {name} ಹೀಗೆ ಬರೆದುಕೊಂಡಿದ್ದೇನೆ: {value}. ಇದು ಸರಿಯೇ? ಹೌದು ಅಥವಾ ಇಲ್ಲ ಎಂದು ಹೇಳಿ.",
        "txn_id": "UTR", "scammer_contact": "ವಂಚಕರ ನಂಬರ್",
        "urgent": "ಇದು ಈಗಷ್ಟೇ ಆಗಿದೆ, ಆದ್ದರಿಂದ ಪ್ರತಿ ನಿಮಿಷವೂ ಮುಖ್ಯ. ಇನ್ನೆರಡು ಮೂರು ಪ್ರಶ್ನೆಗಳು, ನಂತರ ತಕ್ಷಣ 1930 ಗೆ ಕರೆ ಮಾಡಿ.",
        "recent": "ಇದು {age} ಹಿಂದೆ ಆಗಿದೆ, ಆದ್ದರಿಂದ ಹಣವನ್ನು ತಡೆಹಿಡಿಯುವ ಸಾಧ್ಯತೆ ಇನ್ನೂ ಇದೆ.",
        "unknown_time": "ಇದು ಕಳೆದ ಇಪ್ಪತ್ತನಾಲ್ಕು ಗಂಟೆಗಳಲ್ಲಿ ಆಗಿದ್ದರೆ, ಹಣವನ್ನು ತಡೆಹಿಡಿಯುವ ಸಾಧ್ಯತೆ ಇನ್ನೂ ಇದೆ.",
        "old": "ಒಂದು ದಿನಕ್ಕಿಂತ ಹೆಚ್ಚು ಆಗಿದೆ, ಆದರೂ 1930 ಗೆ ಕರೆ ಮಾಡಿ ಮತ್ತು ಆನ್‌ಲೈನ್ ದೂರು ದಾಖಲಿಸಿ — ಬ್ಯಾಂಕಿಗೆ ದೂರಿನ ಸಂಖ್ಯೆ ಬೇಕಾಗುತ್ತದೆ.",
        "min": "{n} ನಿಮಿಷ", "hr": "{n} ಗಂಟೆ",
    },
    "ta": {
        "readback": "நான் {name} இப்படி குறித்துக்கொண்டேன்: {value}. இது சரியா? ஆமாம் அல்லது இல்லை என்று சொல்லுங்கள்.",
        "txn_id": "UTR", "scammer_contact": "மோசடிக்காரரின் எண்",
        "urgent": "இது இப்போதுதான் நடந்தது, அதனால் ஒவ்வொரு நிமிடமும் முக்கியம். இன்னும் இரண்டு மூன்று கேள்விகள், பிறகு உடனே 1930-க்கு அழையுங்கள்.",
        "recent": "இது {age} முன்பு நடந்தது, அதனால் பணத்தை நிறுத்தி வைக்க இன்னும் வாய்ப்பு உள்ளது.",
        "unknown_time": "இது கடந்த இருபத்து நான்கு மணி நேரத்தில் நடந்திருந்தால், பணத்தை நிறுத்தி வைக்க இன்னும் வாய்ப்பு உள்ளது.",
        "old": "ஒரு நாளுக்கு மேல் ஆகிவிட்டது, இருந்தாலும் 1930-க்கு அழைத்து ஆன்லைனில் புகார் செய்யுங்கள் — வங்கிக்கு புகார் எண் தேவைப்படும்.",
        "min": "{n} நிமிடம்", "hr": "{n} மணி நேரம்",
    },
    "te": {
        "readback": "నేను {name} ఇలా రాసుకున్నాను: {value}. ఇది సరైనదేనా? అవును లేదా కాదు అని చెప్పండి.",
        "txn_id": "UTR", "scammer_contact": "మోసగాడి నంబర్",
        "urgent": "ఇది ఇప్పుడే జరిగింది, కాబట్టి ప్రతి నిమిషం ముఖ్యం. ఇంకా రెండు మూడు ప్రశ్నలు, తర్వాత వెంటనే 1930 కి కాల్ చేయండి.",
        "recent": "ఇది {age} క్రితం జరిగింది, కాబట్టి డబ్బును ఆపే అవకాశం ఇంకా ఉంది.",
        "unknown_time": "ఇది గత ఇరవై నాలుగు గంటల్లో జరిగితే, డబ్బును ఆపే అవకాశం ఇంకా ఉంది.",
        "old": "ఒక రోజు కంటే ఎక్కువ అయింది, అయినా 1930 కి కాల్ చేసి ఆన్‌లైన్‌లో ఫిర్యాదు చేయండి — బ్యాంకుకు ఫిర్యాదు నంబర్ అవసరం.",
        "min": "{n} నిమిషాల", "hr": "{n} గంటల",
    },
    "bn": {
        "readback": "আমি {name} লিখে রেখেছি: {value}। এটা কি ঠিক? হ্যাঁ বা না বলুন।",
        "txn_id": "UTR", "scammer_contact": "প্রতারকের নম্বর",
        "urgent": "এটা এইমাত্র হয়েছে, তাই প্রতিটা মিনিট গুরুত্বপূর্ণ। আর দু-তিনটে প্রশ্ন, তারপর সঙ্গে সঙ্গে 1930-এ ফোন করুন।",
        "recent": "এটা {age} আগে হয়েছে, তাই টাকা আটকানোর সম্ভাবনা এখনও আছে।",
        "unknown_time": "এটা গত চব্বিশ ঘণ্টার মধ্যে হয়ে থাকলে, টাকা আটকানোর সম্ভাবনা এখনও আছে।",
        "old": "এক দিনের বেশি হয়ে গেছে, তবুও 1930-এ ফোন করুন আর অনলাইনে অভিযোগ করুন — ব্যাঙ্কের অভিযোগ নম্বর লাগবে।",
        "min": "{n} মিনিট", "hr": "{n} ঘণ্টা",
    },
    "mr": {
        "readback": "मी {name} असा लिहून घेतला: {value}. हे बरोबर आहे का? हो किंवा नाही म्हणा.",
        "txn_id": "UTR", "scammer_contact": "फसवणूक करणाऱ्याचा नंबर",
        "urgent": "हे आत्ताच झाले आहे, त्यामुळे प्रत्येक मिनिट महत्त्वाचा आहे. आणखी दोन-तीन प्रश्न, मग लगेच 1930 वर कॉल करा.",
        "recent": "हे {age} आधी झाले आहे, त्यामुळे पैसे थांबवण्याची अजूनही शक्यता आहे.",
        "unknown_time": "हे गेल्या चोवीस तासांत झाले असेल, तर पैसे थांबवण्याची अजूनही शक्यता आहे.",
        "old": "एक दिवसापेक्षा जास्त झाले आहे, तरीही 1930 वर कॉल करा आणि ऑनलाइन तक्रार करा — बँकेला तक्रार क्रमांक लागेल.",
        "min": "{n} मिनिटे", "hr": "{n} तास",
    },
}
RECENT_H = 24  # 1930 can still ask banks to hold money that hasn't left the mule accounts

IST = timezone(timedelta(hours=5, minutes=30))  # India has no DST


def new_case() -> dict:
    return {f: None for f in FIELDS}


def lang(case: dict) -> str:
    """Reply language: the caller's, if we have it; Hindi until we know; English for languages we don't."""
    lg = (case.get("language") or "hi").split("-")[0].lower()
    return lg if lg in QUESTIONS else "en"


def _says(text: str, words) -> bool:
    # Indic letters and marks (Devanagari..Kannada, plus ZWJ/ZWNJ), but not the danda "।" / "॥", which is punctuation.
    toks = " " + " ".join(re.findall(r"[a-z0-9'\u0900-\u0963\u0966-\u0cff\u200c\u200d]+", (text or "").lower())) + " "
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
    t, cur = rules.normalize(text).lower(), datetime.fromtimestamp(now, IST)
    ago = re.search(r"(\d+)\s*(" + rules.MINUTE + "|" + rules.HOUR + ")", t)
    if ago and re.search(rules.AGO, t):
        n = int(ago.group(1)) * (1 if re.match(rules.MINUTE, ago.group(2)) else 60)
        return int(now - n * 60)
    clock = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(" + rules.CLOCK + ")", t)
    if not clock:
        return int(now) if re.search(rules.NOW, t) else None
    h, m, unit = int(clock.group(1)) % 24, int(clock.group(2) or 0), clock.group(3)
    days = 2 if re.search(rules.DAY_BEFORE, t) else 1 if re.search(rules.YESTERDAY, t) else 0
    if unit.startswith("p") and h < 12:
        h += 12
    elif not unit.startswith("a") and h < 12:
        if re.search(rules.LATER, t) or (re.search(rules.NIGHT, t) and h >= 6):
            h += 12
        elif not re.search(rules.MORNING + "|" + rules.NIGHT, t):
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


def advance(case: dict, history: str, said: str, now: Optional[float] = None, lang_hint: Optional[str] = None):
    """One conversation turn. Returns (payload for the browser, text to speak).

    Besides the field values, the case carries: meta {field: {confirmed, source_text}}, confirming (the ID
    just read back), fraud_ts (epoch s, for the countdown) and urged (urgency said once)."""
    now = time.time() if now is None else now
    case = {**new_case(), **case}
    meta = {**(case.get("meta") or {})}
    confirming, case["confirming"] = case.get("confirming"), None
    got = extract(said)
    hint = (lang_hint or "").split("-")[0].lower()
    if hint in QUESTIONS and not rules.hinglish(said):  # STT's language beats script guessing (hi vs mr)
        got["language"] = hint
    heard, said = said, rules.normalize(said)  # spoken digits as digits, so the merge guard sees the UTR said
    fixing = _says(said, CORRECTION)
    # The first turn answers no question, so a phone number there must not become the amount.
    asked = None if confirming or not history.strip() else next((f for f in ASK_ORDER if case.get(f) is None), None)
    if asked == "amount" and got["amount"] is None:
        got["amount"] = bare_amount(said)
    if asked in SKIPPABLE and got.get(asked) is None and _says(said, DONT_KNOW):
        got[asked] = NOT_KNOWN
    elif asked in FREE_TEXT and got.get(asked) is None and said.strip():
        got[asked] = said.strip()[:80]  # their own words are fine for the complaint

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
    out = {"transcript": heard, "case": case, "question": question}
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
