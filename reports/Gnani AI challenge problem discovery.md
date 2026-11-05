# Choose voice-scam defence over another chatbot

The strongest evidence-backed problem for this entrant is **live detection of voice-call scams on noisy 8 kHz phone audio**. The product would listen to a suspicious call in Hindi/Hinglish (plus one more Gnani-supported language), flag scam scripts such as "digital arrest", KYC expiry or the parcel-with-drugs story within seconds, warn the user aloud through Gnani's phone-native TTS, and hand off to a "golden-hour" reporting flow (1930 helpline, account freeze, a pre-filled cybercrime.gov.in complaint). It scored **77/100** on the requested weighted matrix. It narrowly beats a post-fraud golden-hour responder (76) and a women's-helpline call-taker copilot (72), and clearly beats every Northeast-specific option (68 at best). Three facts drive the ranking. First, the harm is large and documented: Indians reportedly lost **about ₹22,845 crore to cyber fraud in 2024, up from about ₹7,465 crore in 2023** ([Scroll](https://scroll.in/latest/1084796/indians-lost-rs-22845-crore-to-cyber-fraud-in-2024-a-206-rise-from-previous-year-centre)). Second, the attack happens over voice, so speech AI is necessary rather than decorative. Third, the problem uses exactly the capabilities Gnani documents as its edge: native 8 kHz streaming STT, Hindi-English code-mix output, noise robustness, and µ-law/A-law telephony TTS. That lines the entry up with the **Noise Canceller** or **Mixed Vibes** awards and with a shareable "protect your parents" story, which matters because internship shortlisting starts with an engagement check. Northeast problems are real and severe (Assam's 2022 floods affected about 54.6 lakh people), but **Gnani's API documents no Northeast language and explicitly says Assamese is not supported**. An NE build would therefore run its core on AI4Bharat and put the "genuine use of Gnani technology" eligibility check at risk. Three caveats apply. No source breaks fraud victims down by age, language or literacy. Digital-arrest complaints specifically have *fallen* since their 2024 peak. Real-world deployment of call listening faces unresolved legal questions. The demo must use synthetic, consented recordings only, as the challenge rules require.

**Reading conventions.** **[F]** marks a fact from an official or primary document. **[E]** marks an estimate, a secondary report or a contested figure. **[H]** marks this report's hypothesis or inference. A dagger **†** marks a figure the research notes took from a search-result summary or a secondary restatement rather than a full read of the primary document; verify these before putting them on a slide. All sources were accessed on 2026-10-30 unless stated otherwise.

---

## 1. The competition rewards engagement first and Gnani-centric builds second

### Verified facts versus assumptions

The official name is **"The Great Indian AI Internship Challenge"**, with the tagline "Build Sovereign AI for India". **The brief is open**: there are no tracks and no fixed problem statement. An entry must be "a working application built on at least one Gnani AI model or API" that addresses a practical need ([Gnani landing page](https://www.gnani.ai/internship)). Entrants must be students aged 18+ enrolled at an Indian college or university, working solo or in a team of exactly two, with one entry per participant ([Gnani landing page](https://www.gnani.ai/internship); [Registration/terms](https://www.gnani.ai/great-indian-ai-internship-registration-form)). Final submissions close **10 November 2026, 11:59 PM IST, "final, no extensions"**. Today (Friday 30 October) that leaves **11 calendar days (31 Oct to 10 Nov)** of build time ([Registration/terms](https://www.gnani.ai/great-indian-ai-internship-registration-form)).

| Item | Status | Detail and source |
|---|---|---|
| Submission contents | **[F]** | Title, problem, target users, Gnani models/APIs used, each member's contribution, a written explanation, and a **public demo video posted on LinkedIn and/or X** with #GnaniAI and #GreatIndianAIInternshipChallenge, tagging Gnani AI. Posts are then nominated through a form emailed to registrants (one link per platform, post already live). "Tagging alone does not complete your entry." ([landing](https://www.gnani.ai/internship)) |
| Code repo / pitch deck | **[F] not required** | Neither appears in any source. **[H]** A public repo probably helps at the "genuine use" check and at interview. |
| Internship selection order | **[F]** | (1) engagement check (verified reactions, comments, reshares), (2) eligibility check (genuine Gnani use), (3) shortlist by strongest verified engagement, (4) individual interviews, (5) written offers ([landing](https://www.gnani.ai/internship)) |
| Engagement cutoff | **[F]** | "Only engagement recorded by the published closing cutoff counts." Purchased engagement, bots, paid promotion and engagement exchanges are prohibited ([terms](https://www.gnani.ai/great-indian-ai-internship-registration-form)) |
| Awards vs internships | **[F]** | "Awards are decided on each category's criteria, irrespective of internship selection." No team can win more than one award ([landing](https://www.gnani.ai/internship)) |
| Rewards | **[F]** | Up to **100 six-month paid internships** from 1 Jan 2027, stipend *up to* ₹1 lakh/month (a ceiling, not a standard amount), plus **ten ₹50,000 awards** ([landing](https://www.gnani.ai/internship); [FinTech BizNews, 1 Oct 2026](https://fintechbiznews.com/fintech-technology/great-indian-ai-internship-challenge-by-gnani-ai)) |
| Models named in rules | **[F]** | Prisma (STT), Timbre (TTS, beta), Evon (30B LLM). The docs also expose voice cloning `vachana-vc-v1`. The Agent Builder is **out of scope** ([terms](https://www.gnani.ai/great-indian-ai-internship-registration-form); [landing](https://www.gnani.ai/internship); [docs](https://docs.gnani.ai/api/introduction/quick-start)) |
| Credits | **[F]** | 5,000 programme credits per registration (sent to the primary registrant for teams). **The credit-to-minutes/characters conversion is not published.** |
| Data rules | **[F]** | Use synthetic data. No real phone numbers, account numbers, Aadhaar, PAN or recorded calls ([landing](https://www.gnani.ai/internship)) |
| Third-party LLMs/APIs | **Unknown** | No rule allows or bans them. **[H]** Third-party LLMs are probably fine if speech in and out visibly runs on Gnani. Swapping Gnani STT/TTS for a competitor would likely fail the genuine-use check. |
| Numeric rubric, jury | **Unknown** | The terms mention a "scoring method on the programme page", but no weights or jury were found there. |
| Start date | **[E] conflict** | Official page says 1 Oct, press says 30 Sept ([CXOToday](https://cxotoday.com/media-coverage/gnani-ai-launches-the-great-indian-ai-internship-challenge/)). Irrelevant now. |
| Partners / prior editions | **[F] none found** | No IndiaAI/MeitY co-sponsorship and no previous edition found. This appears to be the first. |

### What the ten awards reward and which problems fit

The four example ideas on the official page are a Kannada farmer helpline, a Hinglish kirana order assistant, a noise-robust call summariser and a Tamil quiz tutor. Each maps onto a technical award, which signals that Gnani values Indic languages, code-mixing and telephony noise ([landing](https://www.gnani.ai/internship)). **[H]** Ideas that clone these examples will face the most competition, so a shortlisted problem should be adjacent to them rather than identical.

| Award (₹50,000 each) | Rewards | Best-fitting candidates in this report |
|---|---|---|
| Main Character | Best regional / low-resource language build | ORF reading assessment (Kannada/Tamil/Bengali), Barak Valley flood IVR (Bengali) |
| Mixed Vibes | Best code-mixed voice experience | Scam-call shield (Hinglish), kirana catalog, golden-hour responder |
| Real Deal | Most useful real-world problem solved | Golden-hour responder, ASHA voice-to-form, PM-KISAN troubleshooter |
| Noise Canceller | Best performance on noisy telephonic audio | **Scam-call shield**, helpline copilot, placement-verification calls |
| Two-Person Army / Solo Ninja | Best team / solo project | Any; depends on registration |
| Jugaad Genius | Most creative use of Gnani models | Scam shield (keyterm biasing + 8 kHz TTS whisper), voice cloning for a family "trusted voice" warning (consent-gated) |
| Small Town, Big Build | Best Tier 2/3 entry | Possibly applicable to Imphal; **the definition (college city vs home city) is unpublished** |
| Demo Day Drop | Best **60-second** demo | Any project with a dramatic before/after; scam shield is strongest |
| Crowd Favourite | Public votes on LinkedIn/X | Relatable consumer problems (fraud, parents, floods) |

**[H] Strategic reading.** Internship shortlisting runs on verified organic engagement, so the demo post must be relatable to a general Indian LinkedIn/X audience and must go live several days before the cutoff. Awards are judged separately, so the entry should commit to *one* technical award and generate evidence for it, for example a WER and detection table at 8 kHz under noise for Noise Canceller.

### Unknowns that change scope

The binding unknowns are the credit burn rate (measure it on day 1 with a single call), whether non-rule models such as voice cloning count as "Gnani technology" (probably yes, unconfirmed), and Evon's actual availability (see the conflict in Section 5). Also unknown: whether a "misleading demo" includes simulated telephony. **[H]** Label every simulated element on screen.

---

## 2. Across fourteen domains, voice earns its place in only a handful

Household access is no longer the main barrier. MoSPI's 2025 telecom survey found that **85.5% of households have at least one smartphone** and only **9.7% have only a non-smartphone**. **70% of people aged 15+** had used the internet in the previous three months (men 76.7%, women 63.1%) **[F]** ([PIB/MoSPI, May 2025](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/may/doc2025529560001.pdf)). The live barriers are now literacy, comfort with form-heavy interfaces, and dialects that state-language services miss. The best causal evidence that language mismatch costs something comes from Kisan Call Centres, which answer in the state's official language. Farmers in districts with more non-state-language speakers adopted modern inputs less, by roughly **1.3–2.3% per standard deviation of language barrier** **[F]** ([NBER w27192](https://www.nber.org/papers/w27192)). Across the notes, voice AI is necessary under three conditions: the input is inherently speech, the user cannot read the screen, or the channel is a phone call that a capacity-constrained human answers. It is optional where text translation already works.

| Domain | Strongest documented problem | Is voice necessary? | Crowding |
|---|---|---|---|
| Financial fraud | ₹22,845 cr lost (2024)†; 36.37 lakh complaints† | **Yes**: attack is a voice call | Moderate (1930, telco spam filters not researched) |
| Women's safety | 112 calls 10.89 crore (FY23); Delhi 181 had 90,414 hoax calls of 2.41 lakh (Jul–Nov 2024) | **Yes**: inbound phone calls | Low for AI assist |
| Health | ASHA "seven different apps", double entry | Yes (hands-busy dictation) | Unknown (Khushi Baby, Wadhwani not researched) |
| Education | ~3 in 4 rural govt Std III children cannot read Std II text† | **Yes**: oral reading is speech | High (Read Along, TARA, Wadhwani) |
| Agriculture | PM-KISAN exclusions from e-KYC/bank errors; KCC language penalty | Partly | High (KCC, Farmer.Chat, Kisan e-Mitra) |
| Govt services | Status opacity, ~45% state-level grievance resolution | Partly | High (CPGRAMS 22 languages, Samadhan Didi) |
| Legal | Paralegal volunteers down 38% (2019–24) | Partly | Moderate (Tele-Law) |
| Employment | PMKVY placements ~41% reported and unverifiable (CAG) | Yes for outbound verification | Low |
| Small business | ONDC kirana catalog digitisation barrier | Partly (needs vision too) | Moderate; Gnani's own example |
| Accessibility | <50% of PwD hold UDID cards (Karnataka 46%) | Yes for blind users | Moderate |
| Disaster (NE) | Alerts one-way, text-first; 3,841 NE villages without mobile coverage | Yes for two-way IVR | Low, but Gnani lacks NE languages |
| Transport | Menu IVRs (Rail Madad 139) | Weak | Already served (Bhashini voice on RailMadad) |
| Tourism | Audio guides launched in English/Hindi first | Weak (TTS only) | Low; low harm |
| Language preservation | Transcription bottleneck for field linguists (SPPEL 117 languages documented) | Yes, but niche | Gnani irrelevant |

### Fraud and safety: harm is high and the channel is a phone call

MHA figures reported in Parliament put cyber-fraud losses at **about ₹22,845 crore in 2024 versus about ₹7,465 crore in 2023 (+206%)**. Financial-fraud complaints rose from 20.6 lakh to 36.37 lakh, and about **₹5,489 crore was saved through blocking or reversal**† ([Scroll](https://scroll.in/latest/1084796/indians-lost-rs-22845-crore-to-cyber-fraud-in-2024-a-206-rise-from-previous-year-centre); [IBTimes](https://www.ibtimes.co.in/over-22-6-lakh-cyber-crimes-registered-over-rs-22845-crore-lost-by-citizens-2024-centre-893487)). I4C data in a Supreme Court status report shows **digital-arrest complaints rising from 39,925 (2022) to a peak of 1,23,672 (2024), then falling to 58,249 (2025) and 16,377 (to June 2026)**, with ₹1,935 crore lost in 2024† ([Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/supreme-court-directs-measures-to-curb-digital-arrest-scams/print_manually)). The decline is important counter-evidence: awareness campaigns and enforcement appear to work against that one typology. The Solicitor General told the Court that elderly people are disproportionately affected ([Outlook Money](https://www.outlookmoney.com/news/digital-arrest-scams-why-senior-citizens-are-being-targeted-and-what-to-do)). **No dataset in the notes breaks victims down by age, language or literacy**, so the claim that "vernacular users are hit hardest" is unproven. Women's-safety helplines carry large voice volumes. ERSS-112 calls rose from 4.13 crore (FY21) to **10.89 crore (FY23)** **[F]** ([Rajya Sabha](https://rsdebate.nic.in/bitstream/123456789/745509/1/PQ_262_20122023_S192_p96_p97.pdf)). Delhi's 181 line logged more than 2.41 lakh calls in July–November 2024, of which **90,414 were hoax** ([Deccan Herald](https://www.deccanherald.com/india/delhi/delhi-eve-teasing-to-matrimonial-scams-woman-helpline-receives-over-2-lakh-calls-in-4-months-3302908)).

### Health, education and agriculture: big needs, crowded responses

In health, the best-evidenced pain is the frontline data burden. One ASHA "juggles seven different apps" plus WhatsApp groups and spreadsheets ([New Lines](https://newlinesmag.com/reportage/indias-digital-health-push-is-overworking-its-front-line-women/)). Digitisation has pushed workers to keep paper and digital records in parallel on their own phones and data ([Ideas for India](https://www.ideasforindia.in/topics/productivity-innovation/is-digitalisation-a-double-edged-sword-for-workers-in-indias-public-healthcare-system)). A Bihar qualitative preprint (81 participants) describes a "triple burden" of digital fatigue, duplicate reporting and inequity ([Preprints.org](https://www.preprints.org/manuscript/202507.1082/v1)). Telemedicine language friction is contested. An AIIMS Bibinagar study of 1,100 eSanjeevani consultations judged the platform linguistically inclusive ([CiteDrive](https://www.citedrive.com/en/discovery/evaluating-the-quality-of-telemedicine-consultations-in-indias-esanjeevani-ayushman-bharat-health-and-wellness-center-platform-insights-from-a-prospective-observational-study/)). In education, ASER 2024 found that only **23.4% of rural government-school Std III children can read a Std II text**† ([ASER 2024](https://asercentre.org/wp-content/uploads/2022/12/ASER-2024-National-findings.pdf); [PIB summary](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/feb/doc202524496701.pdf)). NIPUN Bharat targets oral reading fluency of 30–55 words per minute across 20 languages ([Wadhwani AI](https://wadhwaniai.org/programs/oral-reading-fluency-ai-solution)). Strong incumbents exist: Wadhwani's Vaachan Samiksha has assessed **2.5 million+ Gujarati students** ([Wadhwani AI](https://www.wadhwaniai.org/vaachan-samiksha-leveraging-ai-to-bridge-the-literacy-divide/)), and IIT Bombay has TARA ([IIT-B](https://acr.iitbombay.org/?p=47007)). In agriculture, KCC answers in all 22 languages with a reported 95% answer rate ([mKisan](https://mkisan.gov.in/Home/KCCFeature)), but a Karnataka study found **74.2% of respondents had never used it**† ([AgEcon](https://ageconsearch.umn.edu/record/367932/files/Raja4242024AJAEES114511.pdf)). PM-KISAN exclusions run into lakhs per state (Odisha 2.48 lakh and Rajasthan 2.23 lakh over Aadhaar issues†) ([Factly](https://factly.in/pm-kisan-transactions-less-than-1-failure-rate-but-wide-variation-across-states)).

### Government, legal, work and commerce: the bottleneck is often back-office

Government already ships multilingual voice front doors. CPGRAMS accepts grievances in 22 languages, and the "Samadhan Didi" voice bot files them ([PIB Aug 2026](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc202689948801.pdf)). State-level resolution of about 45% points to back-office capacity, not intake, as the constraint ([PIB Jul 2026](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jul/doc2026729936201.pdf)). Legal aid's human layer is shrinking: **paralegal volunteers fell from 69,290 to 43,050 (2019–2024)** and one clinic serves 163 villages on average ([The Wire](https://thewire.in/law/legal-aids-shrinking-footprint-38-drop-in-grassroots-volunteers-threatens-access-for-vulnerable)). The CAG found that of about 56 lakh PMKVY certifications, **about 41% were reported placed, often unverifiably, and 94.53% of beneficiary bank details were blank or zero** ([PRS CAG summary](https://prsindia.org/files/policy/policy_committee_reports/CAG_Summary-PMKVY.pdf)). Among digitally active retail MSMEs, 52–56% prefer English for technology and only 21–25% prefer Hindi ([YourStory](https://yourstory.com/smbstory/indian-retail-msme-embrace-digital-technology-paynearby)). That undercuts the assumption that kirana tools must be vernacular, at least for the already-digital segment PayNearby surveys.

### Northeast India: severe hazards, but connectivity and language support bind first

The Northeast has documented disaster severity and weak last-mile channels. The 2022 Assam floods affected about **54.6 lakh people across 32 districts** at peak, and roughly 90% of Silchar was under water† ([Dhaka Tribune](https://www.dhakatribune.com/world/south-asia/273050/assam-floods-toll-tops-100-as-5.5-million-affected); [Scroll](https://scroll.in/latest/1026826/assam-floods-toll-rises-to-108-situation-remains-critical-in-silchar-town)). NESAC's FLEWS gives revenue-circle-level flood alerts with a stated **12–36 hours of lead time** (an older ASDMA page says 7–18 h) ([NESAC](https://nesac.gov.in/scientific-programmes/disaster-management-support/); [ASDMA](https://asdma.gov.in/project_flood_warning.html)). SACHET has sent **more than 134 billion SMS alerts in 19+ languages**, and cell broadcast was tested nationally in May 2026 ([IANS](https://ianslive.in/govt-launches-cell-broadcast-alert-system-for-real-time-disaster-warnings--20260502131531)). Every channel is one-way. A DoT mandate requires feature phones to read emergency alerts aloud in Hindi and English, adding four languages a year† ([Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/emergency-alert-messages-in-cell-phones/print_manually)). **[H]** NE languages will likely come late under that mandate. The 2023 Sikkim GLOF was a sensing and institutional failure: no EWS at South Lhonak ([Down To Earth](https://www.downtoearth.org.in/natural-disasters/sikkim-floods-why-wasn-t-early-warning-system-set-up-at-glacial-lake-known-to-be-highly-vulnerable-experts-ask-92116)) and a roughly 2-hour window before the flood reached Chungthang ([Eos](https://eos.org/thelandslideblog/sikkim-glof-october-2023)). Voice would not have fixed that. Connectivity binds harder than language: **3,841 NE villages had no mobile coverage** in mid-2025 ([Sentinel Assam](https://www.sentinelassam.com/amp/story/topheadlines/3841-villages-in-northeast-remain-out-of-mobile-network-coverage)), and Manipur's 2023 mobile-internet shutdown passed 200 days ([Internet Society Pulse](https://pulse.internetsociety.org/blog/internet-shutdown-in-manipur-has-now-crossed-200-days)). About **50,000 people remained displaced in Manipur in December 2025** ([Newslaundry](https://www.newslaundry.com/amp/story/2025%2F12%2F08%2Fovercrowded-underfed-manipur-planned-to-shut-relief-camps-in-dec-but-many-still-trapped)), with documented loss of emergency and maternal care ([XCEPT](https://www.xcept-research.org/publication/unseen-and-unrecorded-the-impact-of-conflict-and-forced-displacement-on-access-to-healthcare-for-women-and-children-in-manipur/)). On the language side, Assamese (15.3 M first-language speakers), Bodo (1.48 M) and Manipuri (1.76 M)† are scheduled languages covered by AI4Bharat's IndicConformer ([Wikipedia/Census compilation](https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers_in_India); [IndicConformer](https://github.com/AI4Bharat/IndicConformerASR)). Khasi, Garo, Mizo, Kokborok and Nagamese depend on small efforts such as MWire Labs' Lemka ([Morung Express](https://morungexpress.com/mwire-labs-launches-voice-ai-system-lemka-for-six-ne-languages)). **No per-language WER for any NE language** was found from any provider.

---

## 3. Twenty-five problems pass the evidence bar, and only ten are not chatbots

The inventory spans detection, data capture, assessment, outbound verification, extraction, call-taker assistance, on-device TTS and transcription as well as conversational agents. Ratings use H/M/L. "Gnani fit" means how much of the core value depends on capabilities Gnani documents.

| # | Problem | Type | Impact | Difficulty | Data | 11-day MVP | Gnani fit |
|---|---|---|---|---|---|---|---|
| P1 | Assam flood alert-to-action two-way IVR | Two-way IVR | H | H | L | M–L | L (Assamese unsupported); M for Barak Valley Bengali variant |
| P2 | Feature-phone CAP alert readout in NE languages | On-device TTS | M | H | L | L | None |
| P3 | Landslide community voice reporting (Mizo/Meitei) | Voice reporting | M | H | L | L | None |
| P4 | Manipur relief-camp IVR helpdesk | IVR | M | M | L | M | None for Meitei/Kuki-Chin |
| P5 | Post-fraud golden-hour responder | Guided agent + extraction | H | L | M | H | H |
| P6 | Live scam-call shield | Real-time detection | H | M | L–M | M–H | **Very H** |
| P7 | Voice complaint filing to bank/RBI ombudsman | Extraction | M | L | M | H | M–H |
| P8 | PM-KISAN payment-status troubleshooter | Diagnostic agent | M–H | M | M | M | H |
| P9 | KCC dialect first-line triage + escalation transcript | Agent + handoff | M | M | M | M | M–H |
| P10 | ASHA voice-to-structured-record | Dictation → forms | M–H | M | M | M–H | M–H |
| P11 | eSanjeevani pre-consult symptom capture | Extraction | M | M | L | M | M |
| P12 | Tele-MANAS counsellor transcription/callback | Assist | L–M | M | L | L | M |
| P13 | Legal first-contact + Section 12 aid screening | RAG agent | M | L | H | H | M |
| P14 | ORF assessment with miscue diagnostics | Speech scoring | H | H | L–M | M–L | M |
| P15 | Voice navigation of UDID/benefits for blind & elderly | Agent | M | M | M | M | M |
| P16 | Live Indian-language captions for deaf users | Captioning | M | M | M | M | L (no partials/timestamps) |
| P17 | Voice job profiles for low-literacy workers | Extraction | M | L | M | H | M |
| P18 | Outbound placement-verification calls (skilling) | Outbound survey | M | L | M | H | H |
| P19 | Kirana voice catalog → ONDC listing | Code-mix extraction | M | M | M | H | H |
| P20 | Hands-busy udhaar ledger by voice | Extraction | L | L | M | H | M |
| P21 | Women's-helpline call-taker copilot (LID, severity, auto-fill) | Call-taker assist | H | M | L | M | **Very H** |
| P22 | Natural-language routing for transit IVRs | Routing | L | L | L | H | M |
| P23 | Regional-language heritage audio guides | TTS | L | L | M | H | L–M |
| P24 | Field-linguist transcription for endangered languages | ASR adaptation | L–M | H | L | L | None |
| P25 | Elderly "call before you pay" second-opinion line | Agent | M | L | L | H | H |

### Disaster and Northeast problems (P1–P4)

**P1. Assam flood alert-to-action, two-way voice/IVR.** *Users:* rural riverine households in Lakhimpur, Dhemaji, Barpeta, Nagaon and Cachar/Barak Valley; DDMA staff. *Description:* convert official FLEWS/SACHET text alerts into spoken, place-specific action instructions (where to move, which embankment, nearest camp) and let residents report rising water or trapped people by voice. *Evidence:* 54.6 lakh affected in 2022† and 11–16 lakh in early July 2024 ([Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fassam%2Fassam-flood-situation-worsens-eight-dead-over-16-lakh-hit-3091792)). FLEWS lead time of 12–36 h is enough to act on. *Alternatives:* FLEWS → ASDMA → SACHET SMS, cell broadcast, Google flood alerts and SOS ([Deccan Herald](https://www.deccanherald.com/business/technology/assam-floods-google-brings-sos-crisis-alerts-help-details-on-maps-search-apps-1122092.html)). *Gap:* all channels are one-way and text-first; coverage of Assamese dialects, Bodo and Mising is uncertain. *Intervention:* CAP-to-voice bulletin generator plus inbound IVR that converts speech to a structured incident on a DDMA map. *Gnani applicability:* **low for Assamese/Bodo** (Prisma v3 explicitly excludes Assamese). **Medium** for a Barak Valley variant in Bengali, which Gnani supports, though Sylheti-dialect accuracy is untested. *Impact:* high if ASDMA adopts. *Difficulty:* high. *Data:* FLEWS feeds are not confirmed public; ASDMA bulletins are PDFs. *MVP:* feasible only as a simulated feed. *Risks:* official authority is essential for trust; dialect WER is unknown; much of the core might run on AI4Bharat, which threatens the genuine-use check.

**P2. Feature-phone readout of CAP alerts in NE languages.** *Users:* feature-phone owners (9.7% of households nationally are feature-phone-only, higher in rural areas). *Evidence:* the DoT readout mandate (Hindi/English plus four languages a year†) and manufacturers' memory constraints ([Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/emergency-alert-messages-in-cell-phones/print_manually)). *Gap:* small on-device TTS for Bodo, Meitei, Khasi and Mizo. *Gnani:* none, since Gnani has no open weights and no NE TTS. *MVP:* infeasible in 11 days, and it needs OEM partnership. *Risks:* entirely outside Gnani's stack.

**P3. Landslide community reporting in hill states.** *Users:* Mizoram, Manipur and Sikkim hill villages. *Evidence:* 29 died in Aizawl landslides during Cyclone Remal despite a state-level warning that was not slope-specific ([News On AIR](https://www.newsonair.gov.in/death-toll-in-multiple-landslides-in-mizorams-aizawl-district-climbed-to-29-after-two-more-bodies-recovered)). *Gap:* no slope-level forecast exists to relay, and no voice reporting channel for cracks or seepage. *Gnani:* none for Mizo/Meitei. *Risks:* the upstream sensing problem dominates. This problem fits the entrant's disaster-monitoring background, but not Gnani.

**P4. Manipur relief-camp voice helpdesk.** *Users:* about 50,000 displaced people (Dec 2025) speaking Meitei and Kuki-Chin languages. *Evidence:* XCEPT on lost maternal and emergency care; repeated mobile-data shutdowns. *Intervention:* IVR (voice calls generally survive data shutdowns, **[H]** unverified) for health-camp schedules, entitlements and grievances. *Gnani:* none for the camp languages. *Risks:* ethnic polarisation makes language choice and data handling politically dangerous; a one-side-only system would be distrusted.

### Fraud and finance problems (P5–P8)

**P5. Post-fraud golden-hour responder.** *Users:* fraud victims and their family members, especially older and low-literacy users. *Description:* a voice agent in the victim's language that, minutes after a fraud, walks them through calling 1930, freezing the account and filing on cybercrime.gov.in, and turns their spoken narrative into a structured complaint draft. *Evidence:* ₹5,489 crore saved by blocking or reversal† shows that speed pays. 36.37 lakh complaints in 2024†. The RBI Ombudsman received 13.34 lakh complaints in 2024–25, **66% through the online portal** **[F]** ([RBI](https://website.rbi.org.in/web/rbi/-/publications/annual-report-of-ombudsman-scheme-2024-25)). *Alternatives:* 1930 helpline, cybercrime.gov.in, bank helplines, I4C advisories ([Udayavani](https://udayavani.com/?p=1715424)). *Gap:* **[H]** no guided, multilingual, spoken step-through that also produces the complaint text. No data on 1930 wait times was found, so the gap is not proven. *Gnani:* high (phone-native STT/TTS, code-mix). *Impact:* high if it shortens time-to-report. *Difficulty:* low. *Data:* public advisories and complaint categories; synthetic narratives. *MVP:* highly feasible. *Risks:* cannot file on the user's behalf (no API); wrong instructions could delay reporting.

**P6. Live scam-call shield.** *Users:* elderly and low-digital-literacy phone users and their adult children; potentially banks and telcos. *Description:* listen (with consent) to an ongoing call, transcribe 8 kHz audio in Hindi/Hinglish or a regional language in real time, detect scam-script markers (fake CBI/police, "digital arrest", parcel with drugs, KYC expiry, refund/OTP requests), and speak a warning to the user while the call is live. *Evidence:* ₹22,845 crore lost in 2024†; digital-arrest complaints peaked at 1,23,672 in 2024†; the Solicitor General's statement on elderly victims. *Alternatives:* I4C advisories, the 1930 helpline, and telco AI spam flagging (Airtel/Jio, 2024–25, **not researched in the notes**), which **[H]** appears to work on caller numbers rather than call content. *Gap:* **[H]** no content-level, multilingual, in-call warning was found. *Gnani:* **very high**, the best match to Gnani's telephony training, 8 kHz streaming, code-mix modes and µ-law TTS. *Impact:* high per prevented loss; deployment is hard. *Difficulty:* medium. *Data:* no public Indic scam-call corpus was found; synthetic scripts must be written from advisories. *MVP:* feasible with simulated call capture. *Risks:* legality of call capture (interception, DPDP Act), false positives, coercion that defeats warnings, and a shrinking digital-arrest typology.

**P7. Voice complaint filing to bank or RBI ombudsman.** *Users:* bank customers who cannot use the portal. *Evidence:* the RBI ombudsman figures above. *Gap:* intake for non-portal users. *Gnani:* medium-high. *Risks:* **[H]** the bottleneck may be resolution, not intake; the step is narrow.

**P8. PM-KISAN payment-status troubleshooter.** *Users:* farmers whose instalments stopped; CSC operators. *Evidence:* states mark farmers ineligible for incomplete e-KYC ([Rajya Sabha](https://rsdebate.nic.in/bitstream/123456789/753867/1/PQ_266_29112024_U506_p927_p928.pdf)); Kerala had 2.4 lakh invalid bank accounts ([Onmanorama](https://onmanorama.com/news/kerala/2023/09/21/over-two-lakh-farmers-denied-payment-pm-kisan-samman-nidhi-invalid-bank-account.html)); CAG Nagaland rejected 71,196 of 3,44,983 applications ([Morung Express](https://morungexpress.com/in-nagaland-even-dead-govt-employees-getting-pm-kisan-scheme-benefit-cag)); CAG found ₹50.48 crore untransferred in one state ([CAG](https://cag.gov.in/uploads/download_audit_report/2023/Chapter-4_CAR-2_2020-21_ENG_Report-No.1-of-2023-0641d9dc8d9ae45.18448201.pdf)). *Alternatives:* PM-KISAN portal, the government's Kisan e-Mitra voice chatbot (outcomes unresearched), CSCs. *Gap:* explaining *which* document or seeding step to fix, in dialect. *Gnani:* high (Kannada and other supported languages; the official example is a Kannada farmer helpline). *MVP:* feasible on synthetic beneficiary records only. *Risks:* no portal API; direct overlap with Kisan e-Mitra.

### Health problems (P9–P12)

**P9. KCC dialect first-line triage with escalation transcript.** *Users:* farmers who speak non-state-standard languages. *Evidence:* the NBER language penalty; an IIMA evaluation (2017, dated) found more than 50% of farmers reported voice-quality problems or call drops ([IIMA](https://www.iima.ac.in/sites/default/files/2022-12/Agro-Economic%20Policy%20Briefs%20%28Issue%201%2C%20Sept.%202017%29%20-%20Final8cc0.pdf)). *Gap:* 24x7 first answer plus a human handoff carrying the transcript. *Gnani:* medium-high, but dialects such as Bhojpuri or tribal varieties are not in Gnani's list. *Risks:* hallucinated agronomy such as pesticide doses; a crowded field.

**P10. ASHA voice-to-structured-record.** *Users:* ASHAs, ANMs, Anganwadi workers. *Description:* the worker speaks a home-visit summary in dialect and code-mixed medical terms; the system fills the fields that several apps need and reads them back for confirmation. *Evidence:* "seven different apps"; duplicated paper and digital records; a Bihar "triple burden" preprint; an older Gujarat study timing a 20–30-field form at about 12 minutes ([SEWA Rural/NMJI](https://sewarural.org/sewa/wp-content/uploads/2020/10/NatlMedJIndia.pdf)). *Alternatives:* government apps (RCH, ANMOL, state apps); Khushi Baby, ARMMAN and Wadhwani AI (not researched). *Gap:* one dictation feeding many forms. *Gnani:* medium-high (v3.0 `keyterms` for medical vocabulary, code-mix output); not telephony. *MVP:* feasible with synthetic visits. *Risks:* no write access to government apps; health-data sensitivity; mis-extraction of vitals.

**P11. eSanjeevani pre-consult symptom capture.** *Evidence:* an IIMB note on dialect difficulty describing ailments ([IIMB](https://www.iimb.ac.in/sites/default/files/2022-02/Challenges-telemedicine.pdf)) versus the AIIMS Bibinagar counter-evidence and a scoping review ranking access above language ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11414145)). *Gnani:* medium. *Risks:* clinical liability; unproven need.

**P12. Tele-MANAS counsellor support.** *Evidence:* 20 languages, 53 cells; 24,25,885 calls from December 2022 to July 2025 (RTI) ([Digital Health News](https://www.digitalhealthnews.com/tele-manas-helpline-handles-over-24-lakh-calls-since-2022-launch-rti-reveals)); call-count figures conflict across reports. *Gap:* unproven, since no unanswered-call data exists. *Risks:* AI must not counsel; extreme sensitivity. Rejected for the shortlist.

### Legal, education and accessibility problems (P13–P16)

**P13. Legal first-contact and Section 12 free-aid screening.** *Users:* rural citizens with wage, domestic-violence, land or consumer issues. *Evidence:* PLVs down 38%; ₹6 per-capita legal-aid spend; Tele-Law in 2.5 lakh gram panchayats through CSC facilitators ([Rajya Sabha](https://rsdebate.nic.in/bitstream/123456789/746019/1/PQ_262_21122023_U2184_p308_p314.pdf)). *Gap:* first-level information and eligibility screening, then a Tele-Law or DLSA booking. *Gnani:* medium. *Data:* bare acts and NALSA schemes are public, which makes it RAG-friendly. *Risks:* an older NLU Delhi study shows that 60% of aware women still preferred private lawyers ([Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/quality-of-free-legal-aid)), so trust, not information, may bind. Liability risk is high.

**P14. ORF assessment with miscue diagnostics.** *Users:* primary teachers and FLN supervisors. *Evidence:* ASER 2024†; NIPUN wpm targets; PARAKH shows state-school and SC/ST gaps ([Careers360](https://news.careers360.com/parakh-rashtriya-sarvekshan-result-2024-state-govt-schools-sc-st-far-behind-class-3-6-9-maths-science-language-evs-exam-survey)). *Alternatives:* Read Along (Google-commissioned evaluation showed larger native-language gains ([Sattva](https://www.sattva.co.in/wp-content/uploads/2020/09/Sattva_Google_Read-Along-IA-Report.pdf))), TARA (English/Hindi), Vaachan Samiksha (Gujarati), LearnBharat (claims 15 languages, live status unclear). *Gap:* miscue-level diagnosis in Kannada, Tamil, Telugu, Bengali and similar languages, with noisy classrooms and a link to remediation. *Gnani:* medium. Speech is the input and v3.0 `verbatim` mode helps, but Gnani is trained on adult telephony audio, so child read speech is a risk. *MVP:* risky, because miscue alignment depends on verbatim ASR accuracy that is unmeasured. *Risks:* child-audio ethics; incumbents.

**P15. Voice navigation of UDID and benefit applications for blind and elderly users.** *Evidence:* UDID cards reached 1,09,55,968 by July 2024 ([Rajya Sabha](https://rsdebate.nic.in/bitstream/123456789/750939/1/PQ_265_07082024_U1902_p520_p520.pdf)) against 2.68 crore PwD (Census 2011); Karnataka coverage was 46% ([Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fcag-flags-slow-implementation-of-unique-id-for-persons-with-disabilities-project-in-karnataka-3118516)). *Gap:* form-heavy Swavlamban process. *Gnani:* medium. *Risks:* **[H]** the bottleneck may be medical-board capacity, not information.

**P16. Live captions for deaf and hard-of-hearing users.** *Evidence:* fewer than 300 certified ISL interpreters per ISLRTC ([ISLRTC](https://islrtc.nic.in/?p=6487)). *Gnani:* low, because the streaming API returns only final segments with no partial results and no word timestamps ([Gnani docs](https://docs.gnani.ai/api/STT/stt-websocket.md)), which makes captions laggy. *Risks:* limited written literacy among many deaf users reduces caption value.

### Work, commerce, safety and other problems (P17–P25)

**P17. Voice job profiles for low-literacy workers.** *Evidence:* e-Shram had 30.68 crore registrations, 53.68% of them women ([Outlook Money](https://www.outlookmoney.com/news/eshram-portal-has-over-3068-crore-registration-with-more-than-half-from-women)). Apna named trust as its core issue ([ThePrint](https://theprint.in/economy/apna-linkedin-for-poor-indian-workers-who-dont-know-english-gets-8-million-investment/493134/)). *Gnani:* medium. *Risks:* doesn't fix job supply; incumbent vernacular apps.

**P18. Outbound placement-verification calls for skilling schemes.** *Users:* NSDC and state skill missions, auditors, training partners. *Description:* automated outbound calls in the trainee's language that confirm employment status, employer and wage, and log structured, auditable results instead of self-reported placement. *Evidence:* CAG found about 41% reported placed, placements often unverifiable, and 94.53% of bank details blank or zero ([Moneylife](https://moneylife.in/article/94-percentage-bank-details-missing-underage-candidates-certified-placements-unverifiable-in-pm-kaushal-vikas-yojana-cag/79358.html)). *Alternatives:* manual call centres and self-reports. *Gnani:* high (outbound telephony, 8 kHz µ-law TTS, short noisy answers in 10 languages, which is Gnani's core enterprise pattern). *MVP:* highly feasible. *Risks:* the buyer is government; phone numbers may be wrong (bank-data quality suggests contact data is poor too); a low-glamour, less viral demo.

**P19. Kirana voice catalog to ONDC listings.** *Evidence:* ONDC's FY25–26 target of 10,000+ kiranas and its named entry barriers ([ONDC](https://ondc.org/public/assets/newsletters/ondc-fy25-26-in-focus.pdf)); catalog digitisation of hundreds of barcode-less SKUs (individual write-up ([dev.to](https://dev.to/isaqureshi/dukaan-digital-teaching-an-ai-to-read-a-kirana-shop-so-small-stores-can-compete-on-ondc-2p0i))). *Gnani:* high for Hinglish brand/unit/price extraction. *Risks:* English preference among digital retailers; the idea sits close to Gnani's own "Hinglish kirana" example, so many entrants will build it.

**P20. Hands-busy udhaar ledger.** *Gnani:* medium. *Risks:* **[H]** UPI auto-records many transactions, and Khatabook-class apps exist. Low priority.

**P21. Women's-helpline call-taker copilot.** *Users:* call-takers at 181/112 centres. *Description:* real-time transcript, language identification (to route inter-state callers), severity flags, hoax-likelihood cues for human review, and auto-filled incident records. AI assists and never replaces the call-taker. *Evidence:* 10.89 crore 112 calls (FY23); about 37% hoax share in the Delhi 181 sample; NCRB recorded 4,48,211 crimes against women in 2023 ([The Week/PTI](https://www.theweek.in/wire-updates/national/2025/09/30/del31-ncrb-women.html)). *Alternatives:* human call-takers with manual forms; a CAG ERSS audit exists but was not read ([CAG](https://cag.gov.in/uploads/download_audit_report/2024/06-Chapter-III-069b809d2b80a42.67132610.pdf)). *Gnani:* very high (noisy telephony, `indic-auto` language ID on v3.0, code-mix). *Data:* role-played synthetic calls only. *Risks:* misrouting a distress call harms people; deprioritising a "hoax" can be fatal; no data on language mismatch at helplines.

**P22. Natural-language routing for transit IVRs.** *Evidence:* Rail Madad 139 already runs a 12-language IVR, and the portal has Bhashini voice input ([IndiaAI](https://indiaai.gov.in/news/indian-railways-unveils-multilingual-railmadad-grievance-portal-with-bhashini)). *Assessment:* already served; low novelty.

**P23. Regional-language heritage audio guides.** *Evidence:* UP and MP QR audio guides launched in English and Hindi only ([Outlook Traveller](https://outlooktraveller.com/amp/story/whats-new/uttar-pradesh-tourism-to-develop-qr-code-audio-tours-at-the-taj-mahal-and-other-heritage-sites)). *Assessment:* a nice-to-have; TTS alone suffices, and the harm is low.

**P24. Field-linguist transcription for endangered languages.** *Evidence:* SPPEL has documented 117 languages ([SPPEL](https://sppel.org/about-us.aspx)); mainstream Indic ASR performs poorly on dialects such as Garhwali ([arXiv 2601.04373](https://arxiv.org/pdf/2601.04373)). *Gnani:* none, since there are no weights to adapt. *Assessment:* valuable research, outside this challenge's stack.

**P25. Elderly "call before you pay" second-opinion line.** *Evidence:* LASI-based commentary on a "digital safety gap" among older adults ([ThePrint](https://theprint.in/opinion/from-aadhaar-to-upi-how-indias-digital-rails-can-include-not-exclude-older-adults/3053392/)); 11% digital literacy in a rural Mysore sample ([PMC8938771](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8938771/)). *Assessment:* a lighter, pre-incident version of P5 and P6. It is folded into them rather than scored separately.

---

## 4. Incumbents crowd education and agriculture, leaving fraud and helpline gaps open

For the strongest candidates, the competitive picture explains most of the innovation scores. **Fraud (P5, P6).** The government's response is advisory and reactive: the 1930 helpline, cybercrime.gov.in, and I4C messaging that police "do not arrest via video calls" ([Udayavani](https://udayavani.com/?p=1715424)). The notes did not research telco AI spam filters, so **[H]** the claim that no content-level, in-call, multilingual warning exists is an absence of evidence after a limited search, not proof. That claim must be checked before it appears in the pitch. The steelman against P6 is strong. Coercion works through fear and authority rather than language confusion. Bank-side transaction monitoring is a bigger lever. The one typology with hard numbers is shrinking. P5 competes only with human helplines and portals, but without 1930 wait-time data its gap is a hypothesis.

**Helplines (P21).** No AI call-taker assist for 181/112 appeared in the notes. The incumbent is a human with a form. The obstacle is integration with ERSS and the stakes, not competition.

**Skilling verification (P18).** The incumbent is self-reported data and manual calling. The CAG finding makes the accountability gap official.

**Health (P10).** Government apps are the system of record, and the startup pilots (Khushi Baby, Wadhwani AI, ARMMAN's Kilkari outbound IVR) were not researched, so P10's novelty is uncertain.

**Agriculture (P8, P9).** This is the most crowded field: KCC in 22 languages, Farmer.Chat (whose only independent study is from Kenya ([60 Decibels](https://60decibels.com/wp-content/uploads/2025/11/25.11.03_Digital-Green-Farmer.Chat_Report_Final_Updated.pdf))), Jugalbandi (171 of about 20,000 schemes at launch ([Microsoft](https://news.microsoft.com/source/asia/features/with-help-from-next-generation-ai-indian-villagers-gain-easier-access-to-government-services/))) and Kisan e-Mitra. A recurring pattern runs through these pilots: impressive demos, narrow content and self-reported metrics.

**Education (P14).** Incumbents have scale and government contracts, and the open space is narrow.

**NE disaster (P1).** Supply-side efforts exist (AI4Bharat, IIT Guwahati CLST ([Careers360](https://news.careers360.com/iit-guwahati-researchers-develop-speech-technologies-for-north-eastern-languages-nep-2020/amp)), Lemka, Google Flood Hub), but none combines official alerts with two-way local-language voice. The gap is genuine. It sits outside Gnani's language coverage.

---

## 5. Gnani adds telephony robustness, not language breadth

**Gnani's documented STT and TTS cover exactly 10 languages**: Bengali, English (en-IN), Gujarati, Hindi, Kannada, Malayalam, Marathi, Punjabi, Tamil and Telugu. **No Northeast language is supported.** The Prisma v3.0 page states that "Assamese is not supported" ([Gnani STT languages](https://docs.gnani.ai/api/STT/languages.md); [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md); [TTS voices](https://docs.gnani.ai/api/TTS/available-voices.md)). Marketing figures conflict with the docs: the models page claims Prisma supports "40+ languages" and Timbre "21+" ([Gnani models](https://www.gnani.ai/models)), and press and the Pipecat plugin list Assamese and Odia ([Pipecat](https://docs.pipecat.ai/api-reference/server/services/stt/gnani); [Business Today](https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19)). Build on the 10 documented languages and test anything else before relying on it.

| Capability | Gnani (documented) | AI4Bharat | Sarvam | Bhashini |
|---|---|---|---|---|
| Languages (ASR) | 10 | 22 scheduled incl. Bodo, Manipuri (IndicConformer, MIT, open weights) | 22–23 reported† | No official list found |
| NE languages | **None** | Assamese, Bodo, Manipuri | Unverified | Community code lists Assamese, Bodo, Manipuri TTS† |
| 8 kHz telephony | **Native streaming at 8 kHz**; claims "#1 in 8 of 9 languages on Kathbath Noisy 8kHz" (self-reported, no numbers) ([gnani.ai](https://gnani.ai/)) | Not documented in notes | Not documented in notes | Not documented |
| Code-mix | en-IN accepts Hinglish; v3.0 `codemix`/`transliterate` output styles | Not documented | Not documented | Not documented |
| Context biasing | v3.0 `keyterms` (≤200), `topic`, `previous_text` | — | — | — |
| Language ID | `indic-auto` (v3.0 only) | — | — | Listed in unofficial SDK |
| TTS telephony output | 8 kHz µ-law/A-law, REST/SSE/WebSocket | Indic Parler-TTS (20 langs + English) | Bulbul, ₹15–30 per 10K chars | Listed |
| Voice cloning | API, 5–30 s reference; **no consent policy documented** | — | — | Listed |
| Open weights / offline | **No**. HF cards ship no weights ([HF vachana](https://huggingface.co/gnani-ai/vachana)) | Yes | No | No |
| Pricing | Unpublished; 5,000 challenge credits | Free | Published ([Sarvam pricing](https://docs.sarvam.ai/api/pricing)) | Government |

Sources: [Gnani STT WebSocket](https://docs.gnani.ai/api/STT/stt-websocket.md), [TTS REST](https://docs.gnani.ai/api/TTS/tts-inference.md), [Voice clone](https://docs.gnani.ai/api/VC/voice-clone-embeddings.md), [IndicConformer](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual), [Indic Parler-TTS](https://huggingface.co/ai4bharat/indic-parler-tts), [bhashini-client-sdk](https://pypi.org/project/bhashini-client-sdk/0.2.2/).

**Where Gnani plausibly has an edge** is the combination of 8 kHz phone audio, noise, Hindi-English code-mix and telephony-native output encodings. These match the training-data claim ("14M+ hours of telephonic audio" on the challenge page, but "over one million hours" in the launch blog, a conflict) and the Noise Canceller and Mixed Vibes awards ([Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission)). All accuracy claims are relative or self-reported, and **no absolute WER or independent benchmark exists**. The entrant should run a small WER test on their own 8 kHz recordings. Comparing against IndicConformer is optional, and if done it should be framed as evaluation rather than as part of the product. **Where Gnani adds nothing**: language breadth, NE languages, offline or edge use, fine-tuning, and live captioning (no partials or timestamps). **Engineering constraints that shape the designs below**: REST STT accepts at most 30 s per request; streaming sessions last up to 15 min; server-side VAD closes a segment after 500 ms of silence by default; only final segments are returned; the docs' example segment latencies are 320–380 ms against a marketing "P95 under 200 ms"; diarization and multi-channel input are unsupported on REST and realtime ([STT limits](https://docs.gnani.ai/api/STT/limits.md); [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md)). The landing page's banner announces Prisma v3.0 while its build card says v2.5. The docs offer both, with v2.5 as the default.

### The Evon v3.3 conflict needs a five-minute check

The research notes disagree on Evon. The competition notes report that the challenge page lists **Evon v3.3 as a 30B mixture-of-experts LLM with "Apache 2.0 open weights on Hugging Face by request", "not yet on the API platform"**, linking `huggingface.co/gnani/gnani-evon-v3.3-30B-A3B`. The models page adds about 3.5B active parameters, 128K context and 11 Indian languages ([Gnani landing](https://www.gnani.ai/internship); [Gnani models](https://www.gnani.ai/models)). The technical notes report that **Gnani has released no open weights**: the `gnani-ai/vachana` card says "No model weights are shipped", and the `gnani-ai` HF organisation lists a single ASR card ([HF vachana](https://huggingface.co/gnani-ai/vachana); [HF gnani-ai org](https://huggingface.co/gnani-ai)). The two claims are not necessarily contradictory. The Evon link points to a **different namespace (`gnani`, not `gnani-ai`)** and is gated "by request", so a check of the `gnani-ai` org would not see it. Neither note confirms that weight files actually download. **Open the Evon link, check whether `.safetensors` files are listed, and submit the access request on day 1.** In practice, do not put Evon on the critical path. A 30B MoE needs a GPU node, and the rules require only one Gnani model, which Prisma and Timbre already satisfy.

---

## 6. The weighted matrix puts scam defence on top by a narrow margin

Each criterion is scored directly on its weight (for example, severity out of 15). Scores reflect the evidence above, the 11-day window, award fit and engagement-based shortlisting.

| Problem | Sev /15 | Users /10 | Innov /15 | Gnani /15 | Tech /10 | Data /10 | Impact /10 | Demo /5 | Scale /5 | MVP /5 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P6 Live scam-call shield | 14 | 9 | 10 | 14 | 7 | 5 | 6 | 5 | 3 | 4 | **77** |
| P5 Golden-hour fraud responder | 13 | 8 | 8 | 12 | 9 | 7 | 6 | 4 | 4 | 5 | **76** |
| P21 Helpline call-taker copilot | 14 | 8 | 9 | 14 | 7 | 4 | 5 | 4 | 3 | 4 | **72** |
| P18 Placement-verification calls | 8 | 6 | 10 | 13 | 9 | 6 | 6 | 3 | 5 | 5 | **71** |
| P10 ASHA voice-to-record | 11 | 7 | 9 | 11 | 8 | 6 | 6 | 4 | 3 | 4 | **69** |
| P8 PM-KISAN troubleshooter | 11 | 8 | 7 | 12 | 7 | 6 | 6 | 4 | 4 | 4 | **69** |
| P1 Flood two-way IVR (Barak Valley, Bengali-first) | 14 | 6 | 12 | 8 | 6 | 5 | 7 | 4 | 3 | 3 | **68** |
| P14 ORF miscue assessment | 13 | 9 | 7 | 9 | 6 | 6 | 7 | 4 | 4 | 3 | **68** |
| P13 Legal first-contact | 10 | 8 | 8 | 10 | 8 | 7 | 5 | 3 | 4 | 4 | **67** |
| P19 Kirana voice catalog | 6 | 7 | 8 | 11 | 8 | 7 | 5 | 4 | 4 | 5 | **65** |

### Why each problem got its scores

**P6 (77).** Severity is near-maximum because losses are the largest documented harm in the notes. It loses a point because the losses cover all cyber fraud, not voice scams alone, and digital-arrest complaints are falling. Users: 9, since anyone with a phone is exposed. Innovation: only 10 of 15, because telco spam filtering is unresearched and may overlap. Gnani: 14, the best match to documented strengths. Technical feasibility: 7, because real-time capture of a live phone call is the hard part and the demo must simulate it. Data: 5, because no public Indic scam-call corpus exists and the rules forbid real calls. Impact: 6, because deployment needs telco, OEM or bank distribution and faces legal questions. Demo: 5/5, since a live warning interrupting a fake CBI officer is the most watchable 60 seconds on this list, which also matters for engagement.

**P5 (76).** Slightly lower severity and innovation than P6 because the harm has already occurred and the flow is guidance. It is higher on feasibility, data and MVP (simple pipeline, public advisories). Gnani: 12, because it doesn't need 8 kHz call audio. **It is the de-risked fallback for P6.**

**P21 (72).** Severity and Gnani fit match P6. Data: 4, because only role-played distress calls are ethical. Impact: 5, because nothing works without ERSS integration and the stakes punish errors.

**P18 (71).** Moderate severity: the harm is accountability failure, not direct injury. It scores maximum on scalability and MVP and high on Gnani fit (outbound telephony is Gnani's commercial core), but demo appeal is low, which hurts engagement-based shortlisting.

**P10 (69).** Documented burden, but the evidence is mostly qualitative and journalistic. Users: 7, because the notes contain no national ASHA headcount. Innovation: 9, because pilots were unresearched. Impact: 6, because government apps cannot be written to.

**P8 (69).** Real exclusion at lakh scale, but Kisan e-Mitra competes directly (innovation 7) and portal data must be simulated.

**P1 (68).** Severity 14 and innovation 12 (no two-way NE voice channel found). Users: 6, because the Barak Valley variant reaches a fraction of Assam's flood population. **Gnani: 8 only because the scored variant is Bengali-first.** An Assamese/Bodo-first build would score about 4, roughly 64 in total, since Gnani supports neither. Tech, data and MVP are low because FLEWS feeds are not confirmed public and Sylheti accuracy is unknown.

**P14 (68).** Severe and widespread, but incumbents (innovation 7), unmeasured child-speech accuracy on telephony-trained STT (Gnani 9, tech 6) and miscue alignment make 11 days tight.

**P13 (67).** RAG-friendly and feasible, but trust is the binding constraint and liability caps impact.

**P19 (65).** Low severity, the English-preference counter-evidence, and proximity to Gnani's own example mean many entrants will build it.

**Tie-break for fifth place.** P10 and P8 tie at 69. P10 goes forward because its burden evidence is more direct and it has no single government incumbent like Kisan e-Mitra. P1, at 68, is discussed as the Northeast path in Section 9.

---

## 7. Five candidates survive deep analysis, and one is clearly buildable in eleven days

All five plans share a schedule logic. Measure credits on **31 Oct**. Freeze scope by **3 Nov**. Run evaluations on **5 Nov**. **Post the demo on LinkedIn and X on the evening of Friday 6 Nov**, giving about four days of organic engagement before the cutoff. Nominate the posts on 7 Nov. Keep **10 Nov** as a buffer that ends before 11:59 PM IST. Only one link per platform can be nominated, so the 60-second cut should be the nominated post, with the long walkthrough linked from it. Engagement exchanges are prohibited, so share only through genuine networks (college groups, family, the disaster-research community).

### 7.1 P6: live scam-call shield ("Kavach")

**Problem definition.** Voice scammers impersonate police, CBI, couriers or banks and coerce victims, disproportionately older people (per the SG statement), into transferring money or sharing OTPs during the call. The victim has no independent, real-time check in their own language while the pressure is on.

**Personas.** *Kamla Devi, 68, Lucknow.* Speaks Hindi, uses WhatsApp, lives alone, and her son works in Bengaluru. *Rajesh, 34, the son.* Wants an alert if his mother is on a suspicious call. *Secondary:* a bank fraud-ops analyst who would license the detection engine.

**User journey.** Kamla receives a call from "Mumbai Crime Branch" about a parcel with drugs. She taps "Kavach sun lo" ("Kavach, listen"), or it auto-activates for unknown numbers on speaker. Within one or two utterances of the scam cues, a calm Hindi voice whispers: "Yeh call dhokha ho sakta hai. Police video call pe arrest nahi karti. Call kaatiye." ("This call may be a fraud. Police do not arrest on video calls. Hang up.") Rajesh gets an SMS or WhatsApp alert. After she hangs up, Kavach offers the golden-hour flow (P5-lite): "Kya aapne paise bheje?" ("Did you send any money?"), then 1930 and a complaint draft.

**Current versus proposed workflow.** Today the victim stays on the call, sometimes for hours. Help arrives only if a relative intervenes or the victim later calls 1930, by which time money has moved. With Kavach, an independent voice interrupts in-call within seconds of the first scam cues, a trusted contact is alerted, and post-call reporting starts immediately.

**Architecture.**

```
Phone call (speaker) ──► capture (laptop/Android mic) ──► resample to 8 kHz 16-bit PCM
   │                                                   (demo also replays 8 kHz µ-law + noise files)
   ▼
Gnani Prisma v3.0 WebSocket (x-sample-rate 8000, keyterms = scam lexicon, codemix output)
   ▼ final segments (~0.3–0.4 s after each VAD close)
FastAPI risk engine: rolling 60-s transcript window
   ├─ rule layer: typology cue lexicon (authority + threat + secrecy + payment/OTP), multi-cue scoring
   └─ classifier: multilingual sentence embeddings + logistic regression (trained on synthetic scripts)
       └─ optional LLM (any) only to phrase the *explanation*, never to decide
   ▼ risk ≥ threshold
Gnani Timbre TTS (hi / hi-en voice, 8 kHz µ-law or 16 kHz) ──► spoken warning
   ├─ React dashboard: live transcript, cue highlights, risk meter
   └─ trusted-contact alert (simulated) + post-call golden-hour flow (Timbre + Prisma)
```

**Gnani API integration plan.** STT runs on `wss://api.vachana.ai/stt/v3/stream` with `model=prisma-v3.0`, `x-sample-rate: 8000` and 1,024-byte frames. Tune `x-min-silence-ms` down from 500 ms to cut latency, and test whether that fragments sentences. Use `keyterms` for scam vocabulary and named agencies. **Run every evaluation with and without keyterms**, because biasing could raise false positives. Use `language_code=indic-auto` only if a second language is added (v3.0 only). Use REST STT (≤30 s clips) for batch evaluation. TTS uses `timbre-v2.5` with the `hi-en` Hinglish voice, or `timbre-v3.0` for regional languages, over REST for warnings and SSE for longer post-call guidance, requesting `pcm_mulaw` at 8000 Hz for the "phone-native" demo. The diarization gap matters here because REST and realtime don't separate speakers. **[H]** In a Twilio-style bridge, send the caller's leg as its own stream, since multi-channel input is unsupported. In the speakerphone demo, treat the mixed transcript as one stream: the detection cues come mostly from the caller anyway. Optional *Jugaad* feature: with explicit recorded consent, clone the son's voice via `vachana-vc-v1` so the warning comes "from Rajesh". The cloning docs publish no consent rules, so implement your own consent capture and clone only your own team's voices.

**Datasets.** No public Indic scam-call corpus was found. Build a **synthetic, consented corpus**: about 24 scam scripts across four typologies (digital arrest, KYC/account block, parcel/customs, refund/OTP) and about 16 hard benign calls (a genuine bank reminder, a courier delivery, a relative asking for money for a real reason). Write them from I4C advisory patterns and news reconstructions, record them with friends in Hindi/Hinglish and one more Gnani language (Bengali or Kannada), and produce clean, 8 kHz µ-law and noise-mixed variants (street, fan, crowd at several SNRs). Hand-correct transcripts for the WER reference. Never use real recorded calls ([challenge rule](https://www.gnani.ai/internship)).

**Backend and frontend.** The backend is FastAPI: a WebSocket relay to Gnani, the risk engine, a TTS endpoint, and SQLite for the evaluation log. The frontend is a React dashboard: phone-mock UI, live transcript with highlighted cues, risk gauge, warning playback, and post-call flow. A Streamlit page shows the evaluation table (WER and detection metrics by condition).

**MVP scope.** In scope: live streaming detection in Hindi/Hinglish, one regional language for the post-call flow only, spoken warnings, trusted-contact alert (mocked), golden-hour checklist plus complaint draft, and an evaluation report. Out of scope: Android call-audio capture, real telephony numbers, bank integration, on-device inference.

| Date | Day | Work |
|---|---|---|
| Sat 31 Oct | 1 | Confirm registration and credits; generate API key; one STT minute and one TTS paragraph to **measure credit burn**; WebSocket hello-world at 8 kHz; Evon access check; join Gnani Discord |
| Sun 1 Nov | 2 | Write 40 scripts; record with consenting friends; create 8 kHz/noise variants; hand transcripts |
| Mon 2 Nov | 3 | Streaming pipeline mic/file → Gnani → FastAPI → React live transcript |
| Tue 3 Nov | 4 | Risk engine (rules + classifier); thresholds; **scope freeze** |
| Wed 4 Nov | 5 | Timbre warnings (8 kHz µ-law), trusted-contact mock, post-call golden-hour flow |
| Thu 5 Nov | 6 | Evaluation: WER clean vs 8 kHz vs noise; precision/recall; time-to-warning; keyterms on/off; fix worst failures |
| Fri 6 Nov | 7 | Record the 60-s demo and 3-min walkthrough; write explanation; **post on LinkedIn and X in the evening** with hashtags and tag |
| Sat 7 Nov | 8 | Nominate posts via the emailed form; publish repo and evaluation table; reply to comments |
| Sun 8 Nov | 9 | Second-language polish; README; architecture diagram |
| Mon 9 Nov | 10 | Hardening; record backup demo; final write-up edits |
| Tue 10 Nov | 11 | Verify submission fields and contributions; submit well before 11:59 PM IST |

**Test metrics.** WER and CER on the corpus by condition (clean, 8 kHz, 8 kHz + noise), reported honestly even if poor. Scam-detection recall and precision, and false-alarm rate on hard benign calls. **Time-to-warning**, measured in seconds from the first scam cue to audio warning onset. End-to-end latency per segment. Credits consumed per call-minute.

**Risks and mitigations.** *Legal and privacy* (recording or listening to calls, DPDP): consent-first design, local processing of the transcript, no storage by default, and a clear statement that the demo simulates capture. *False positives* that erode trust: multi-cue thresholds, a benign hard set, and "may be fraud" phrasing. *Latency* from VAD: tune the silence timer and warn on cumulative cues rather than waiting for full sentences. *Credit exhaustion:* evaluate on REST clips and cache transcripts. *Scope creep:* the post-call flow is a checklist, not a second agent. *Over-claiming:* cite the falling digital-arrest trend and say no age-breakdown data exists.

**Demo scenario (60 s).** 0–8 s: hook, "₹22,845 crore lost to cyber fraud in 2024 (MHA, as reported)". 8–35 s: a split screen of a fake "CBI officer" call in Hinglish on speaker, with the transcript streaming and cues lighting up. At about 30 s, Kavach whispers its warning in Hindi and the son's phone buzzes. 35–50 s: post-call flow, "Call 1930 now", with the complaint draft generated from her spoken account. 50–60 s: evaluation overlay ("works at 8 kHz with street noise: recall X%, warning in Y s"), "Built on Gnani Prisma + Timbre", hashtags.

**Competitive advantages.** It works on content, not caller numbers. It speaks in the user's language during the call. It is evaluated on phone-quality noisy audio, which is Gnani's home turf. It targets Noise Canceller with measured evidence and has the most shareable story on this list.

### 7.2 P5: golden-hour fraud responder ("Turant")

**Problem definition.** After a fraud, victims lose time working out whom to call and what to say. Rapid reporting enables blocking or reversal (₹5,489 crore saved†), but the reporting channels are online-heavy (66% of RBI ombudsman complaints arrive via the portal).

**Personas.** *Suresh, 52, a Kannada-speaking shop owner* who just sent ₹40,000 to a fake "electricity department" UPI ID. *His daughter*, who is helping remotely.

**Journey and workflow.** Today he panics, searches online and maybe calls the bank, often without the transaction ID ready. With Turant, he speaks in Kannada. The agent asks five or six structured questions (when, how much, which app or UTR, the scammer's number, whether he shared an OTP), speaks the exact next actions in order (call 1930 now, call the bank to freeze the account, keep screenshots), and produces a complaint draft in English plus his language, ready to paste into cybercrime.gov.in and to read out to the 1930 operator.

**Architecture.** React voice UI (browser mic at 16 kHz, with an IVR-style 8 kHz mode) → Gnani Prisma STT (REST per turn, ≤30 s) → FastAPI state machine (deterministic slot filling; an LLM only for slot extraction from free speech, validated against regexes for amounts, UTRs and phone numbers) → Timbre TTS for each prompt → complaint-draft PDF/text. The knowledge base is curated I4C/RBI guidance with RAG over a small vetted set, and every answer cites its source.

**Gnani plan.** Prisma v3.0 with `codemix` output; `keyterms` for bank and app names; Timbre v3.0 multilingual voices (Kannada, Hindi, Tamil, Bengali); optional 8 kHz µ-law output to show IVR readiness.

**Datasets.** Synthetic victim narratives written from public advisories and news reconstructions; complaint category lists from cybercrime.gov.in; no real account numbers.

**MVP scope.** Three languages, four fraud typologies, complaint draft, and a checklist. No filing automation.

| Date | Work |
|---|---|
| 31 Oct | API setup, credit measurement, KB collection |
| 1–2 Nov | Slot-filling state machine; STT/TTS loop in Hindi |
| 3 Nov | Kannada and Bengali; scope freeze |
| 4 Nov | Complaint-draft generator; validation rules |
| 5 Nov | Test 30 synthetic narratives; slot accuracy; time-to-complete |
| 6 Nov | Demo video; post in the evening |
| 7–9 Nov | Nominate; polish; README |
| 10 Nov | Submit |

**Metrics.** Slot-extraction accuracy (amount, UTR, time, number); task completion time versus a manual-portal baseline timed by the builder; WER per language; user comprehension in a small consented pilot with family members.

**Risks.** Wrong or outdated procedure, mitigated by citing and dating every instruction. Users might delay calling 1930 to talk to the bot, so it says "call 1930 now" in the first ten seconds. Lower demo drama than P6.

**Demo.** A Kannada-speaking victim talks to Turant; within 90 seconds he has the 1930 script read aloud and a pasted complaint. **Advantage:** zero integration dependency and fully buildable. It is the safest Real Deal candidate.

### 7.3 P21: women's-helpline call-taker copilot ("Saathi Desk")

**Problem definition.** 181/112 call-takers handle high volumes (10.89 crore ERSS calls in FY23), with a large hoax share (about 37% in the Delhi 181 sample), while typing incident details by hand. Inter-state callers may speak languages the call-taker does not.

**Personas.** *Priya, a 181 call-taker in Delhi* on a 12-hour shift. *A Bengali-speaking migrant domestic worker* calling at night.

**Journey and workflow.** Today Priya listens, asks questions, types into the form, and routes manually. If the language doesn't match, she searches for a colleague. With Saathi Desk, the call audio streams to a live transcript with detected language. Severity cues (weapon, injury, child, ongoing violence) raise a red flag. The form auto-fills location, nature and persons involved, and Priya confirms or edits. A "possible non-genuine" cue is shown only as advisory and never auto-drops a call. A language-match suggestion routes the call to a Bengali-speaking colleague.

**Architecture.** Telephony bridge or simulator (8 kHz) → Gnani Prisma v3.0 streaming with `indic-auto` → FastAPI: severity classifier (rules + embeddings) and an incident-schema extractor → React call-taker console. Gnani TTS is used only for caller-side hold or acknowledgement messages in the detected language.

**Gnani plan.** `indic-auto` language detection (v3.0 only); 8 kHz streaming; `keyterms` for locality names; `pcm_mulaw` TTS. The lack of diarization means the caller's leg is streamed separately.

**Datasets.** Role-played synthetic distress calls with consenting actors (no real recordings); a schema derived from public helpline descriptions; noise-mixed variants.

**MVP scope.** Hindi, Bengali, Tamil; three severity levels; auto-filled form; language routing hint.

| Date | Work |
|---|---|
| 31 Oct | Setup, credit test, ethics note and script guidelines |
| 1 Nov | Write and record 30 role-play calls, 8 kHz/noise variants |
| 2–3 Nov | Streaming console; language ID; scope freeze |
| 4 Nov | Severity flags and form extraction |
| 5 Nov | Evaluation: LID accuracy, severity recall, field accuracy |
| 6 Nov | Demo video; post in the evening |
| 7–9 Nov | Nominate; polish |
| 10 Nov | Submit |

**Metrics.** Language-ID accuracy at 8 kHz; severity recall on high-risk calls (the priority metric); form-field accuracy; seconds saved per call versus manual typing in a simulated trial.

**Risks.** Misclassification harms a real caller, so the copilot is advisory only, with no automated routing or dropping. Synthetic distress audio is ethically sensitive, so use scripted, non-graphic scenarios. Without ERSS integration it is a demonstrator only. It competes with P6 for Noise Canceller. **Demo.** A noisy Bengali call is auto-detected, flagged red and auto-filled in 20 seconds while a split screen shows the manual baseline. **Advantage:** the cleanest fit to "noisy telephonic audio" plus language ID, but less shareable and riskier to portray.

### 7.4 P18: outbound placement-verification calls ("Pakka Placement")

**Problem definition.** Skilling schemes report placement without verifiable evidence. The CAG found about 41% reported placed, often unverifiable, and 94.53% of bank details missing.

**Personas.** *A state skill-mission monitoring officer* who needs audited placement numbers. *Ravi, 22, a PMKVY electrician graduate in Tamil Nadu* who answers a two-minute call.

**Journey and workflow.** Today training partners self-report and spot checks are manual. With Pakka Placement, a scheduled outbound call in Tamil asks consent, then: are you working, with which employer, since when, monthly wage band, and whether the job matches your trade. Answers are transcribed and structured, low-confidence answers are flagged for human callback, and a dashboard shows verified versus claimed placement by training centre.

**Architecture.** Call scheduler (FastAPI) → TTS prompts (Timbre, 8 kHz µ-law) → telephony simulator in the browser or WebRTC at 8 kHz (**[H]** a real PSTN number needs a provider and KYC, so stay simulated) → Prisma STT per answer (REST ≤30 s) → answer normaliser (yes/no, employer, number extraction) → confidence scoring → Streamlit dashboard comparing claimed and verified rates.

**Gnani plan.** Timbre v3.0 voices that speak all 10 languages; Prisma with `keyterms` for employer and trade names; 8 kHz throughout.

**Datasets.** Synthetic trainee roster (names, centres, claimed placement); recorded synthetic answers with noise; public PMKVY dashboard and CAG categories for the schema.

**MVP scope.** Tamil, Hindi, Telugu; a five-question script; a dashboard with a "claimed vs verified" gap.

| Date | Work |
|---|---|
| 31 Oct | Setup, credit test, script design |
| 1–2 Nov | TTS prompt chain and STT answer capture at 8 kHz |
| 3 Nov | Answer normalisation and confidence; scope freeze |
| 4 Nov | Dashboard and roster simulation |
| 5 Nov | Evaluate 40 synthetic calls: field accuracy, completion rate, WER |
| 6 Nov | Demo video; post in the evening |
| 7–9 Nov | Nominate; polish |
| 10 Nov | Submit |

**Metrics.** Answer-field accuracy, call completion rate in simulation, low-confidence flag precision, credits per verified record.

**Risks.** Bad phone numbers (poor bank-data quality suggests contact data is also poor); respondents may misreport; a low-engagement topic. **Demo.** Ten simulated calls in Tamil complete in parallel, and the dashboard reveals a centre claiming 80% placement where 30% is verified (synthetic numbers, labelled as such). **Advantage:** trivially scalable, and it uses the most enterprise-realistic Gnani pattern. Its weakness is virality.

### 7.5 P10: ASHA voice-to-structured-record ("Bolo Report")

**Problem definition.** ASHAs re-enter the same visit data across several apps and paper registers, on their own phones and data, which costs unpaid time and data quality.

**Personas.** *Sunita, an ASHA in rural Karnataka* who records 8–10 home visits a day and is more comfortable speaking than typing. *Her ANM supervisor*, who needs consistent records.

**Journey and workflow.** Today Sunita fills a paper register, then each app, typing 20–30 fields per form (about 12 minutes in an older Gujarat study). With Bolo Report, she speaks a 60–90-second visit summary in Kannada-English code-mix ("Lakshmi, 7 months pregnant, BP 130/85, IFA tablets diya, next ANC on 12th"). The system extracts a structured record, reads it back for yes/no confirmation, and exports per-app field maps (mock RCH/ANC formats) for copying or syncing.

**Architecture.** Android-friendly React PWA (offline recording queue; uploads when connected) → Prisma v3.0 (`codemix`, `keyterms` for drugs, vitals and scheme names; split audio into ≤30-s REST chunks or use streaming) → FastAPI extractor (LLM with JSON schema plus rule validators for vitals ranges and dates) → Timbre read-back in Kannada → export view.

**Datasets.** Synthetic visit narratives built from public ANC/HBNC field definitions (**[H]** not in the notes; collect from official MoHFW forms); recorded by consenting volunteers with household noise.

**MVP scope.** One visit type (ANC), Kannada and Hindi, 15 fields, confirmation read-back, export.

| Date | Work |
|---|---|
| 31 Oct | Setup, credit test, collect ANC form fields |
| 1 Nov | Write and record 30 synthetic visit narratives |
| 2–3 Nov | STT + extraction + validators; scope freeze |
| 4 Nov | Read-back TTS; offline queue; export |
| 5 Nov | Evaluate field-level precision/recall, WER, time vs typing |
| 6 Nov | Demo video; post in the evening |
| 7–9 Nov | Nominate; polish |
| 10 Nov | Submit |

**Metrics.** Field-level accuracy (especially vitals and dates); critical-error rate (wrong BP or weeks of pregnancy); time to complete versus typing the same form; WER on code-mixed medical terms with and without keyterms.

**Risks.** Mis-extracted vitals are dangerous, so mandatory read-back and range validators are required. No integration with government apps, so it is positioned as an assistive pre-fill. Synthetic data only. **Demo.** A 60-second spoken visit becomes a filled form in about 10 seconds, read back in Kannada, beside a timer for manual entry. **Advantage:** a clear Real Deal story and good use of Gnani keyterm biasing. Its novelty versus unresearched pilots is uncertain.

---

## 8. Three finalists differ in where the voice sits: in the call, after it, or behind it

| | **#1 P6 Live scam-call shield** | **#2 P5 Golden-hour responder** | **#3 P21 Helpline call-taker copilot** |
|---|---|---|---|
| Why it should be built | The largest documented harm on the list (₹22,845 cr in 2024†), delivered through voice calls that no current tool inspects for content | Speed of reporting demonstrably recovers money (₹5,489 cr saved†) and channels are portal-first | Huge call volumes (10.89 crore 112 calls, FY23), with call-takers doing manual triage in a multilingual country |
| What makes it different | Warns *during* the call, in the user's language, from call content rather than caller ID | Turns a panicked spoken narrative into an ordered action plan and complaint text | Assists the human taking the call, so the AI never decides on its own |
| Why Gnani is essential | 8 kHz streaming, noise, Hinglish code-mix, keyterm biasing, µ-law TTS: the documented telephony edge | Multilingual phone-native STT/TTS across 10 languages; works over IVR | Noisy 8 kHz input plus `indic-auto` language ID on v3.0 |
| Demoable prototype | Live fake-scam call interrupted by a Hindi warning; evaluation overlay | Kannada victim completes the flow in about 90 s | Noisy Bengali call auto-flagged and form auto-filled |
| Evidence to show judges | WER and detection recall at 8 kHz under noise, with and without keyterms; time-to-warning | Slot accuracy; completion time versus a manual-portal baseline | LID accuracy and severity recall at 8 kHz |
| Failure modes | Call capture infeasible in production; false alarms; coercion overrides warnings; legal challenge | Advice goes stale; users delay calling 1930; less novel | Misrouted distress call; ethical problems with synthetic distress audio; no ERSS access |

P6 and P5 share about 70% of their code (same STT/TTS plumbing and fraud knowledge base). If real-time capture or latency fails by Day 4, **pivot to P5 without losing work**, and keep P6's offline evaluation as the Noise Canceller evidence.

---

## 9. Recommendation: build the scam-call shield, with the golden-hour flow as its safety net

**Build P6, the live scam-call shield**, scoped to Hindi/Hinglish detection, one additional Gnani language for the post-call flow, and a rigorous 8 kHz noisy-audio evaluation. Aim it at **Noise Canceller** (Mixed Vibes as the alternative framing) while leaving P5's golden-hour flow inside it as both feature and fallback.

The justification rests on five points that are each traceable to evidence. First, the harm is the largest documented on the list, and the attack channel is a voice call, so speech AI is structurally required rather than added for show. Second, it sits squarely on the Gnani capabilities that are documented and differentiated (8 kHz streaming STT, code-mix output styles, keyterm biasing, µ-law TTS). That makes the "genuine use of Gnani technology" check easy to pass, which a Northeast build could not guarantee. Third, it fits the selection mechanics. Internship shortlisting starts with verified organic engagement, and "an AI that stops scammers from robbing your parents" is the most shareable story among the 25 problems, while Demo Day Drop rewards the same 60-second drama. Fourth, it fits the entrant. The work is streaming FastAPI services, an ML classifier, a React dashboard and a Streamlit evaluation page, all of which match the stated skills, and the data-analysis skills turn into the evaluation table that makes the entry credible. Fifth, it is honest about its limits. The pitch should say that digital-arrest complaints peaked in 2024 and are falling, that no data breaks victims down by age or language, and that production call capture raises open legal questions. Admitting these limits will make a better impression at interview than over-claiming.

**Why not the Northeast, despite the entrant's background.** The Northeast problems are severe, and the two-way flood IVR is arguably the most *novel* gap in the notes. The obstacle is stack fit: Gnani supports no NE language, Assamese is explicitly excluded, the FLEWS feed is not confirmed to be public, and 3,841 villages have no mobile coverage at all. If the entrant still prefers an NE entry, the only version where Gnani stays central is the **Barak Valley (Cachar/Silchar) Bengali-first flood IVR (68/100)**. It would convert simulated CAP/FLEWS alerts into Bengali voice bulletins through Timbre and take inbound Bengali reports through Prisma onto a DDMA map built with the entrant's existing disaster-monitoring dashboards. Assamese or Bodo would be an explicitly labelled AI4Bharat extension. Before committing, test Gnani's `bn-IN` STT on Sylheti-accented speech on Day 1. If accuracy is poor, the NE option collapses and P6 should proceed. A third path keeps the background in play: after submission, the scam-shield's evaluation harness (8 kHz, noise, code-mix) transfers directly to a future NE flood IVR once Gnani or AI4Bharat covers the languages.

## Conclusion

The discovery exercise changes the question from "which Indian problem is biggest?" to "where does this specific speech stack carry the solution?" Many large needs (foundational reading, NE disasters, farmer advisory) are either crowded with incumbents or fall outside Gnani's 10 documented languages. The overlap of severe harm, uncrowded space and Gnani-specific strength is narrow, and it sits on noisy phone calls. Within that overlap, scam defence wins because it scores well both on a judge's rubric and in a LinkedIn feed, which this competition explicitly rewards.

The most valuable thing the entrant can produce in eleven days is the evaluation table, more than the polished app. No independent WER benchmark of Gnani on 8 kHz noisy code-mixed Indian speech exists in any source found. A small, honest measurement of exactly that (clean versus phone-quality versus noise, keyterms on and off, scam recall and time-to-warning) would be new evidence. It serves as an award argument, an interview talking point and a reusable harness for any later telephony project, including a Northeast flood line.

---

## 10. Bibliography

All accessed 2026-10-30. Publication dates are given where the research notes recorded them. A † in the body marks figures taken from search summaries or secondary restatements.

**Competition (official and press)**
- Gnani AI, "The Great Indian AI Internship Challenge" landing page (undated; live countdown on 2026-10-30). https://www.gnani.ai/internship
- Gnani AI, Registration form and programme terms (undated). https://www.gnani.ai/great-indian-ai-internship-registration-form
- CXOToday, "Gnani AI launches The Great Indian AI Internship Challenge" (2026-10-01). https://cxotoday.com/media-coverage/gnani-ai-launches-the-great-indian-ai-internship-challenge/
- FinTech BizNews, "Great Indian AI Internship Challenge by Gnani AI" (2026-10-01). https://fintechbiznews.com/fintech-technology/great-indian-ai-internship-challenge-by-gnani-ai
- Inc42, IndiaAI Mission selects Soket AI, Gnani AI, Gan AI (headline only; undated in notes). https://inc42.com/buzz/indiaai-mission-soket-ai-gnani-ai-gan-ai-to-develop-indigenous-ai-models/

**Gnani technology**
- Gnani docs: Quick start. https://docs.gnani.ai/api/introduction/quick-start
- Gnani docs: STT languages. https://docs.gnani.ai/api/STT/languages.md
- Gnani docs: Prisma v3. https://docs.gnani.ai/api/STT/models/prisma-v3.md
- Gnani docs: STT WebSocket. https://docs.gnani.ai/api/STT/stt-websocket.md
- Gnani docs: STT limits. https://docs.gnani.ai/api/STT/limits.md
- Gnani docs: TTS available voices. https://docs.gnani.ai/api/TTS/available-voices.md
- Gnani docs: TTS REST inference. https://docs.gnani.ai/api/TTS/tts-inference.md
- Gnani docs: Voice clone embeddings. https://docs.gnani.ai/api/VC/voice-clone-embeddings.md
- Gnani docs index (llms.txt). https://docs.gnani.ai/llms.txt
- Gnani models page. https://www.gnani.ai/models
- Gnani homepage. https://gnani.ai/
- Gnani blog, Vachana STT launch (page dated 3 Jul 2026 on fetch; launch reported Feb 2026). https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission
- Hugging Face, gnani-ai/vachana card. https://huggingface.co/gnani-ai/vachana
- Hugging Face, gnani-ai organisation. https://huggingface.co/gnani-ai
- Hugging Face, Evon v3.3 (link from challenge page; access not verified). https://huggingface.co/gnani/gnani-evon-v3.3-30B-A3B
- Business Today, Gnani zero-shot voice cloning TTS (2026-02-19). https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19
- Outlook Business, Sarvam and Gnani launch models at IndiaAI Summit (2026-02-18). https://www.outlookbusiness.com/amp/story/news/sarvam-gnani-ai-launches-advanced-ai-models-at-the-indiaai-summit
- Pipecat, Gnani STT docs. https://docs.pipecat.ai/api-reference/server/services/stt/gnani
- PyPI pipecat-gnani; livekit-plugins-gnani. https://pypi.org/project/pipecat-gnani/ ; https://pypi.org/project/livekit-plugins-gnani/
- AI4Bharat IndicConformer 600M (HF; GitHub). https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual ; https://github.com/AI4Bharat/IndicConformerASR
- AI4Bharat Indic Parler-TTS. https://huggingface.co/ai4bharat/indic-parler-tts
- Sarvam API pricing. https://docs.sarvam.ai/api/pricing
- bhashini-client-sdk 0.2.2 (unofficial). https://pypi.org/project/bhashini-client-sdk/0.2.2/

**Access, fraud, finance**
- MoSPI/PIB, Comprehensive Modular Survey: Telecom 2025 (May 2025). https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/may/doc2025529560001.pdf
- Gupta, Ponticelli & Tesei, NBER w27192 (language barriers and farmer advice). https://www.nber.org/papers/w27192
- Scroll, cyber fraud losses 2024. https://scroll.in/latest/1084796/indians-lost-rs-22845-crore-to-cyber-fraud-in-2024-a-206-rise-from-previous-year-centre
- IBTimes, 22.6 lakh cybercrimes 2024. https://www.ibtimes.co.in/over-22-6-lakh-cyber-crimes-registered-over-rs-22845-crore-lost-by-citizens-2024-centre-893487
- Drishti IAS, SC directions on digital-arrest scams (Aug 2026). https://www.drishtiias.com/daily-updates/daily-news-analysis/supreme-court-directs-measures-to-curb-digital-arrest-scams/print_manually
- Outlook Money, why senior citizens are targeted. https://www.outlookmoney.com/news/digital-arrest-scams-why-senior-citizens-are-being-targeted-and-what-to-do
- Udayavani, I4C advisory. https://udayavani.com/?p=1715424
- RBI, Annual Report of Ombudsman Scheme 2024-25. https://website.rbi.org.in/web/rbi/-/publications/annual-report-of-ombudsman-scheme-2024-25
- NPCI, UPI 123PAY overview. https://npci.org.in/what-we-do/upi-123pay/product-overview

**Agriculture, health, government, legal**
- mKisan, KCC features. https://mkisan.gov.in/Home/KCCFeature
- IIMA Agro-Economic Policy Brief (Sept 2017). https://www.iima.ac.in/sites/default/files/2022-12/Agro-Economic%20Policy%20Briefs%20%28Issue%201%2C%20Sept.%202017%29%20-%20Final8cc0.pdf
- AJAEES Karnataka KCC study (AgEcon). https://ageconsearch.umn.edu/record/367932/files/Raja4242024AJAEES114511.pdf
- Rajya Sabha PQ 266 (29-11-2024), PM-KISAN e-KYC. https://rsdebate.nic.in/bitstream/123456789/753867/1/PQ_266_29112024_U506_p927_p928.pdf
- Factly, PM-KISAN failures by state. https://factly.in/pm-kisan-transactions-less-than-1-failure-rate-but-wide-variation-across-states
- Onmanorama, Kerala PM-KISAN invalid accounts (2023-09-21). https://onmanorama.com/news/kerala/2023/09/21/over-two-lakh-farmers-denied-payment-pm-kisan-samman-nidhi-invalid-bank-account.html
- CAG Report No.1 of 2023, Ch.4. https://cag.gov.in/uploads/download_audit_report/2023/Chapter-4_CAR-2_2020-21_ENG_Report-No.1-of-2023-0641d9dc8d9ae45.18448201.pdf
- Morung Express, Nagaland PM-KISAN CAG. https://morungexpress.com/in-nagaland-even-dead-govt-employees-getting-pm-kisan-scheme-benefit-cag
- 60 Decibels, Farmer.Chat Kenya study (Nov 2025). https://60decibels.com/wp-content/uploads/2025/11/25.11.03_Digital-Green-Farmer.Chat_Report_Final_Updated.pdf
- Microsoft Source, Jugalbandi (2023). https://news.microsoft.com/source/asia/features/with-help-from-next-generation-ai-indian-villagers-gain-easier-access-to-government-services/
- New Lines Magazine, ASHA digital burden. https://newlinesmag.com/reportage/indias-digital-health-push-is-overworking-its-front-line-women/
- Ideas for India, digitalisation and health workers. https://www.ideasforindia.in/topics/productivity-innovation/is-digitalisation-a-double-edged-sword-for-workers-in-indias-public-healthcare-system
- Preprints.org 202507.1082, Muzaffarpur triple burden (2025, not peer-reviewed). https://www.preprints.org/manuscript/202507.1082/v1
- SEWA Rural / NMJI, ASHA digital form timing. https://sewarural.org/sewa/wp-content/uploads/2020/10/NatlMedJIndia.pdf
- IIMB, Challenges of telemedicine (2022). https://www.iimb.ac.in/sites/default/files/2022-02/Challenges-telemedicine.pdf
- AIIMS Bibinagar eSanjeevani study (CiteDrive). https://www.citedrive.com/en/discovery/evaluating-the-quality-of-telemedicine-consultations-in-indias-esanjeevani-ayushman-bharat-health-and-wellness-center-platform-insights-from-a-prospective-observational-study/
- PMC scoping review on telemedicine barriers (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11414145
- Digital Health News, Tele-MANAS RTI. https://www.digitalhealthnews.com/tele-manas-helpline-handles-over-24-lakh-calls-since-2022-launch-rti-reveals
- PIB, CPGRAMS/Samadhan Didi (Aug 2026; Jul 2026). https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc202689948801.pdf ; https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jul/doc2026729936201.pdf
- The Wire, India Justice Report 2025 paralegal decline. https://thewire.in/law/legal-aids-shrinking-footprint-38-drop-in-grassroots-volunteers-threatens-access-for-vulnerable
- Rajya Sabha PQ (21-12-2023), Tele-Law. https://rsdebate.nic.in/bitstream/123456789/746019/1/PQ_262_21122023_U2184_p308_p314.pdf
- Drishti IAS, NLU Delhi legal-aid study (Jul 2019). https://www.drishtiias.com/daily-updates/daily-news-analysis/quality-of-free-legal-aid

**Education, accessibility, work, commerce, safety, other**
- ASER 2024 National findings. https://asercentre.org/wp-content/uploads/2022/12/ASER-2024-National-findings.pdf
- PIB/MoE ASER summary (Feb 2025). https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/feb/doc202524496701.pdf
- Careers360, PARAKH 2024 gaps. https://news.careers360.com/parakh-rashtriya-sarvekshan-result-2024-state-govt-schools-sc-st-far-behind-class-3-6-9-maths-science-language-evs-exam-survey
- Wadhwani AI, ORF programme; Vaachan Samiksha. https://wadhwaniai.org/programs/oral-reading-fluency-ai-solution ; https://www.wadhwaniai.org/vaachan-samiksha-leveraging-ai-to-bridge-the-literacy-divide/
- IIT Bombay, TARA. https://acr.iitbombay.org/?p=47007
- Sattva, Read Along impact report (Google-commissioned, 2020). https://www.sattva.co.in/wp-content/uploads/2020/09/Sattva_Google_Read-Along-IA-Report.pdf
- Rajya Sabha PQ 265 (07-08-2024), UDID. https://rsdebate.nic.in/bitstream/123456789/750939/1/PQ_265_07082024_U1902_p520_p520.pdf
- Deccan Herald, CAG on UDID Karnataka. https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fcag-flags-slow-implementation-of-unique-id-for-persons-with-disabilities-project-in-karnataka-3118516
- ISLRTC, interpreters. https://islrtc.nic.in/?p=6487
- ThePrint, older adults and digital rails. https://theprint.in/opinion/from-aadhaar-to-upi-how-indias-digital-rails-can-include-not-exclude-older-adults/3053392/
- PMC8938771, DAHLIA study. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8938771/
- Outlook Money, e-Shram registrations (2025). https://www.outlookmoney.com/news/eshram-portal-has-over-3068-crore-registration-with-more-than-half-from-women
- PRS, CAG summary of PMKVY. https://prsindia.org/files/policy/policy_committee_reports/CAG_Summary-PMKVY.pdf
- Moneylife, PMKVY CAG findings. https://moneylife.in/article/94-percentage-bank-details-missing-underage-candidates-certified-placements-unverifiable-in-pm-kaushal-vikas-yojana-cag/79358.html
- ThePrint, Apna (2020). https://theprint.in/economy/apna-linkedin-for-poor-indian-workers-who-dont-know-english-gets-8-million-investment/493134/
- YourStory, PayNearby MSME index. https://yourstory.com/smbstory/indian-retail-msme-embrace-digital-technology-paynearby
- ONDC FY25-26 newsletter. https://ondc.org/public/assets/newsletters/ondc-fy25-26-in-focus.pdf
- dev.to, Dukaan Digital kirana prototype. https://dev.to/isaqureshi/dukaan-digital-teaching-an-ai-to-read-a-kirana-shop-so-small-stores-can-compete-on-ondc-2p0i
- The Week/PTI, NCRB crimes against women 2023 (2025-09-30). https://www.theweek.in/wire-updates/national/2025/09/30/del31-ncrb-women.html
- Rajya Sabha PQ 262 (20-12-2023), ERSS-112. https://rsdebate.nic.in/bitstream/123456789/745509/1/PQ_262_20122023_S192_p96_p97.pdf
- Deccan Herald, Delhi 181 calls Jul–Nov 2024. https://www.deccanherald.com/india/delhi/delhi-eve-teasing-to-matrimonial-scams-woman-helpline-receives-over-2-lakh-calls-in-4-months-3302908
- CAG, ERSS chapter (2024). https://cag.gov.in/uploads/download_audit_report/2024/06-Chapter-III-069b809d2b80a42.67132610.pdf
- IndiaAI, RailMadad Bhashini portal. https://indiaai.gov.in/news/indian-railways-unveils-multilingual-railmadad-grievance-portal-with-bhashini
- Outlook Traveller, UP QR audio tours. https://outlooktraveller.com/amp/story/whats-new/uttar-pradesh-tourism-to-develop-qr-code-audio-tours-at-the-taj-mahal-and-other-heritage-sites
- SPPEL, about. https://sppel.org/about-us.aspx
- arXiv 2601.04373, dialect ASR (Garhwali) (2026). https://arxiv.org/pdf/2601.04373

**Northeast and disaster**
- Down To Earth, Sikkim GLOF no EWS (2023-10-04). https://www.downtoearth.org.in/natural-disasters/sikkim-floods-why-wasn-t-early-warning-system-set-up-at-glacial-lake-known-to-be-highly-vulnerable-experts-ask-92116
- Eos Landslide Blog, Sikkim GLOF. https://eos.org/thelandslideblog/sikkim-glof-october-2023
- EastMojo, GLOF report and recommendations (2023-11-23). https://eastmojo.com/sikkim/2023/11/23/report-and-recommendations-on-the-glof-disaster-of-teesta-valley/
- Dhaka Tribune, Assam floods 2022. https://www.dhakatribune.com/world/south-asia/273050/assam-floods-toll-tops-100-as-5.5-million-affected
- Scroll, Silchar floods 2022. https://scroll.in/latest/1026826/assam-floods-toll-rises-to-108-situation-remains-critical-in-silchar-town
- Deccan Herald, Assam floods 2024. https://www.deccanherald.com/amp/story/india%2Fassam%2Fassam-flood-situation-worsens-eight-dead-over-16-lakh-hit-3091792
- NESAC, Disaster Management Support (FLEWS). https://nesac.gov.in/scientific-programmes/disaster-management-support/
- ASDMA, FLEWS project. https://asdma.gov.in/project_flood_warning.html
- News On AIR, Mizoram landslides (May 2024). https://www.newsonair.gov.in/death-toll-in-multiple-landslides-in-mizorams-aizawl-district-climbed-to-29-after-two-more-bodies-recovered
- IANS, cell broadcast launch (2026-05-02). https://ianslive.in/govt-launches-cell-broadcast-alert-system-for-real-time-disaster-warnings--20260502131531
- Drishti IAS, emergency alert readout mandate. https://www.drishtiias.com/daily-updates/daily-news-analysis/emergency-alert-messages-in-cell-phones/print_manually
- Deccan Herald, Google SOS alerts Assam 2022. https://www.deccanherald.com/business/technology/assam-floods-google-brings-sos-crisis-alerts-help-details-on-maps-search-apps-1122092.html
- Sentinel Assam, 3,841 villages without coverage (June 2025). https://www.sentinelassam.com/amp/story/topheadlines/3841-villages-in-northeast-remain-out-of-mobile-network-coverage
- Internet Society Pulse, Manipur shutdown 200 days. https://pulse.internetsociety.org/blog/internet-shutdown-in-manipur-has-now-crossed-200-days
- Amnesty International, Manipur displaced (May 2025). https://www.amnesty.org/en/latest/news/2025/05/authorities-should-urgently-rehabilitate-thousands-displaced-in-two-years-of-ethnic-violence-in-manipur/
- Newslaundry, Manipur relief camps (2025-12-08). https://www.newslaundry.com/amp/story/2025%2F12%2F08%2Fovercrowded-underfed-manipur-planned-to-shut-relief-camps-in-dec-but-many-still-trapped
- XCEPT, health access in Manipur camps (Oct 2025). https://www.xcept-research.org/publication/unseen-and-unrecorded-the-impact-of-conflict-and-forced-displacement-on-access-to-healthcare-for-women-and-children-in-manipur/
- Wikipedia, languages by native speakers in India (Census compilation). https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers_in_India
- Careers360, IIT Guwahati NE speech technologies (Mar 2022). https://news.careers360.com/iit-guwahati-researchers-develop-speech-technologies-for-north-eastern-languages-nep-2020/amp
- Morung Express, MWire Labs Lemka. https://morungexpress.com/mwire-labs-launches-voice-ai-system-lemka-for-six-ne-languages
- AIKosh, NE-STT multilingual model. https://aikosh.indiaai.gov.in/home/models/details/northeast_stt_multilingual_speech_to_text_model.html
