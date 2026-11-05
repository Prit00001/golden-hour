# Gnani AI: Technical Capabilities and Developer Offerings (as of 30 Oct 2026)

Research date: 2026-10-30. Gnani product naming is inconsistent across sources: "Vachana" (launch name / API domain api.vachana.ai), "Prisma" (STT model line), "Timbre" (TTS model line), "Inya" / "Inya VoiceOS" (voice-agent platform and the IndiaAI-Mission voice-to-voice model; inya.ai now 301-redirects to gnani.ai). Treat docs.gnani.ai as the most authoritative source; press and homepage figures are self-reported marketing unless noted.

## Speech-to-Text (Vachana STT / Prisma v2.5 and v3.0)

### Takeaway
The documented STT API supports exactly 10 languages (9 Indic + Indian English), real-time WebSocket streaming including 8 kHz telephony audio, Hindi-English code-mix handling, and auto language ID (v3.0 only). All accuracy claims are relative ("10-20% lower WER") with no absolute WER published; Assamese/Odia appear in press and the Pipecat plugin list but NOT in Gnani's own language docs.

### Cited Findings
- Official STT language list (both Prisma v2.5 and v3.0, REST/Realtime/Batch): Bengali bn-IN, English en-IN, Gujarati gu-IN, Hindi hi-IN, Kannada kn-IN, Malayalam ml-IN, Marathi mr-IN, Punjabi pa-IN, Tamil ta-IN, Telugu te-IN — 10 total — [Gnani docs: STT languages](https://docs.gnani.ai/api/STT/languages.md)
- Prisma v3.0 page states Assamese is not supported — [Gnani docs: Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md)
- CONFLICT: Pipecat docs list Assamese and Odia among supported STT languages (12 entries) and defer to the source repo for the authoritative list — [Pipecat Gnani STT docs](https://docs.pipecat.ai/api-reference/server/services/stt/gnani); Gnani's Vachana STT launch blog also names Odia and Assamese — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission); but official language docs list neither — [Gnani docs](https://docs.gnani.ai/api/STT/languages.md)
- Code-mixing: en-IN accepts English-Hindi mixed audio and outputs Latin script; v3.0 adds output styles `verbatim`, `transcribe`, `codemix` (keeps English words in Latin script) and `transliterate` (romanised output; Gnani says its accuracy "has not been measured") — [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md), [STT languages](https://docs.gnani.ai/api/STT/languages.md)
- Auto language detection: `language_code=indic-auto`, v3.0 only, returns `detected_language_code` — [STT languages](https://docs.gnani.ai/api/STT/languages.md)
- v3.0 is opt-in (`model=prisma-v3.0`); v2.5 is the default. v3.0 context hints: `keyterms` (up to 200), `topic` (up to 1,600 chars), `previous_text`, `speaker_names` (1-4) — [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md)
- Not supported on REST/Realtime: diarization, word-level timestamps, translation, multi-channel audio. Batch jobs do speaker separation as a separate step — [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md)
- Streaming: `wss://api.vachana.ai/stt/v3/stream`; raw 16-bit LE mono PCM; `x-sample-rate` 8000/16000 (default)/44100/48000; 1,024-byte frames (64 ms at 8 kHz); server-side VAD (default 500 ms silence to close a segment); only final transcripts per segment, no documented partial/interim results; example per-segment latency values 320-380 ms (no SLA) — [Gnani docs: STT WebSocket](https://docs.gnani.ai/api/STT/stt-websocket.md)
- Limits: REST 30 s per request (wav/mp3/ogg/flac/aac/m4a); streaming 15 min per session; batch up to 4 h per file, 100 files per job, 10 MB per file direct or 5 GiB via presigned upload; rate-limit returns HTTP 429 `RATE_LIMITED`; concurrency and request-rate numbers not published (shown in app.gnani.ai) — [Gnani docs: STT limits](https://docs.gnani.ai/api/STT/limits.md)
- Latency claim: "P95 under 200ms (streaming)" — [Hugging Face card gnani-ai/vachana](https://huggingface.co/gnani-ai/vachana); same "p95 200 ms" in [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission) (marketing; no methodology). Note the docs' example latencies (320-380 ms) exceed this and exclude the VAD silence wait.
- Accuracy claims (relative only): "30-40% lower WER on low-resource Indic languages" and "10-20% lower WER across top eight Indian languages"; competitors not named; detailed benchmark reports "on request" — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission)
- Homepage claims "#1 in 8 of 9 Indian languages on the Kathbath Noisy 8kHz benchmark" (no numbers shown) — [gnani.ai](https://gnani.ai/)
- Telephony robustness: handles 8-64 kbps bitrates and noisy networks — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission); "optimized for both broadband and 8kHz telephony audio" — [HF card](https://huggingface.co/gnani-ai/vachana)
- Training data CONFLICT: "over one million hours of real-world voice data" (launch blog; Outlook Business adds "across 1,056 domains") vs "14 million+ hours" (HF card, homepage) — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission); [Outlook Business](https://www.outlookbusiness.com/amp/story/news/sarvam-gnani-ai-launches-advanced-ai-models-at-the-indiaai-summit); [HF card](https://huggingface.co/gnani-ai/vachana)
- Scale claim: ~10 million calls/day — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission); homepage claims 50M+ daily voice interactions — [gnani.ai](https://gnani.ai/)

### Inferences
- For a hackathon, plan around the 10 documented languages; treat Assamese/Odia STT as "test before relying on it".
- No interim transcripts + VAD-based segmentation means voice-agent turn latency = silence timer (default 500 ms) + transcription; tune `x-min-silence-ms`.
- Native 8 kHz streaming input is a genuine practical advantage for phone/IVR projects versus models that need upsampling.

### Gaps
- No absolute WER figures or named benchmark tables found anywhere public.
- Exact rate limits / concurrency caps not published.
- Launch date ambiguity: the Gnani blog page is dated 3 July 2026 per fetch, but Outlook Business reported Vachana STT's launch on 18 Feb 2026; may be a re-dated page.

## Text-to-Speech and Voice Cloning (Vachana TTS / Timbre v2.5, v3.0)

### Takeaway
TTS covers the same 10 languages (plus Hinglish `hi-en` on v2.5), with 13 v3.0 voices and 42 v2.5 voices, telephony-native output (8 kHz µ-law/A-law), and an API for zero-shot voice cloning from 5-30 s of reference audio. No consent/usage rules for cloning are documented anywhere I found.

### Cited Findings
- Models: `timbre-v3.0`, `timbre-v2.5` (v2.0 slated for deprecation). v3.0: 13 voices (Shivani, Lakshmi, Kalpana, Chetana, Vasudha, Riyaa, Tarika, Avinash, Shubham, Prakash, Devansh, Yashraj, Harshad), each speaks all 10 languages (hi, en, ta, te, kn, ml, mr, pa, bn, gu). v2.5: 42 voices, each with a preferred language, plus Hinglish `hi-en` and `auto` script detection. Voices are not cross-compatible between models (400 error) — [Gnani docs: Available voices](https://docs.gnani.ai/api/TTS/available-voices.md)
- REST endpoint `POST https://api.vachana.ai/api/v1/tts/inference`, header `X-API-Key-ID`; sample rates 8000/16000/22050/24000/44100/48000 (default 48000); encodings linear_pcm, pcm_s16le, pcm_mulaw, pcm_alaw, oggopus; containers wav/raw/mp3/ogg/mulaw/alaw; no documented character limit (too-long text gives 500) — [Gnani docs: TTS REST](https://docs.gnani.ai/api/TTS/tts-inference.md)
- Delivery modes: REST, SSE streaming, WebSocket realtime; plus Audio Tags and a Text Normalization guide — [Gnani docs index](https://docs.gnani.ai/llms.txt)
- Voice cloning API: upload 5-30 s of clean reference audio to the embeddings endpoint, receive a `speaker_embedding` (example shape [1, 768], bfloat16), pass it to REST/SSE/WebSocket cloned-TTS endpoints. Page does not document supported languages, consent requirements, or usage restrictions — [Gnani docs: Voice clone embeddings](https://docs.gnani.ai/api/VC/voice-clone-embeddings.md)
- Press (19 Feb 2026): Vachana TTS, zero-shot cloning from "less than 10 seconds of audio", cross-lingual cloning, 12 languages incl. Odia and Assamese and Indian English; API plus on-prem options; no consent safeguards mentioned — [Business Today](https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19)
- CONFLICT: press says 12 TTS languages incl. Odia/Assamese; docs list 10 (no Odia/Assamese) — [Business Today](https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19) vs [Gnani docs](https://docs.gnani.ai/api/TTS/available-voices.md)
- Data policy (homepage, self-reported): "No customer voice data is used for model training without explicit agreement"; SOC 2, ISO 27001, GDPR/HIPAA/PCI-DSS, RBI/IRDAI data-residency claims — [gnani.ai](https://gnani.ai/)

### Inferences
- `pcm_mulaw`/`pcm_alaw` at 8 kHz means TTS output can be pushed straight onto PSTN/SIP trunks without transcoding.
- Because no consent policy is documented, a hackathon team using cloning should implement its own explicit-consent capture and only clone their own voices.

### Gaps
- No published TTS latency (TTFB) numbers; HF card says only REST > SSE > WebSocket qualitatively — [HF card](https://huggingface.co/gnani-ai/vachana).
- No published MOS/naturalness scores.
- Terms of service / acceptable-use text for voice cloning not located.

## Speech-to-Speech / Voice-Agent Platform (Inya VoiceOS, Agent Builder, Warp)

### Takeaway
Two distinct things: (1) a hosted Agent Builder (console + Platform REST API) with telephony integrations (Twilio number import, Webex Contact Center, DTMF, voicemail detection, language-switch prompts), and (2) "Inya VoiceOS", a 5B-parameter voice-to-voice model unveiled Feb 2026 as a research preview, with only ~6 languages per the CTO. A developer-accessible S2S API ("Gnani Warp v2.0") is listed on the homepage but I found no docs for it.

### Cited Findings
- Agent Builder docs cover: knowledge bases, agent creation/testing, number whitelisting, DTMF collection, advanced ASR settings, voicemail detection, dynamic variables, Jinja system prompts, language-switch prompt, integrations (Twilio SMS, Zoho CRM/Ticketing, email, custom actions), Webex Contact Center, Twilio number import, agent chaining, logs/analytics — [Gnani docs index](https://docs.gnani.ai/llms.txt)
- Platform API: create/list/update/delete agents, trigger test call, conversation logs/audio/stats, lookups for languages, regions, LLM models, transcriber and TTS config, FAQs, chat widget; OpenAPI/AsyncAPI specs published — [Gnani docs index](https://docs.gnani.ai/llms.txt)
- Three developer surfaces: Speech APIs (build your own pipeline), Agent Builder (Gnani runs the conversation), Platform API (manage agents from code) — [docs.gnani.ai](https://docs.gnani.ai)
- Inya VoiceOS: 5B-parameter voice-to-voice model unveiled at the India AI Impact Summit (Feb 2026) under the IndiaAI Mission, as a research preview — [Digit](https://www.digit.in/news/general/india-ai-impact-summit-2026-gnani-ai-unveils-indias-first-5b-voice-to-voice-ai-model-inya-voiceos.html); [Business Standard](https://www.business-standard.com/technology/tech-news/gnani-ai-unveils-5b-parameter-voice-to-voice-inya-voiceos-model-at-india-ai-summit-126021700403_1.html)
- CTO Ananth Nagaraj: "The first version is a 5-billion parameter model that currently supports six languages"; roadmap 14B model covering 12 languages, then 70B "within the next year" — [Outlook Business, 18 Feb 2026](https://www.outlookbusiness.com/amp/story/news/sarvam-gnani-ai-launches-advanced-ai-models-at-the-indiaai-summit)
- CONFLICT: other coverage says 15+ Indian languages — [Open Source For You](https://www.opensourceforu.com/2026/02/india-unveils-first-5b-voice-ai/); [callmissed blog](https://www.callmissed.com/blog/sovereign-voice-ai-at-scale-inside-gnani) (secondary)
- IndiaAI Mission selection: Gnani to build a 14B-parameter voice AI foundational model for multilingual real-time speech — [Inc42](https://inc42.com/buzz/indiaai-mission-soket-ai-gnani-ai-gan-ai-to-develop-indigenous-ai-models/)
- Homepage product lineup: Prisma (STT), Timbre v3.0 (TTS), Warp v2.0 (speech-to-speech), Evon v3.3 (language model); enterprise products Agents, Analytics, Biometrics (sub-second auth claim), Assist (sub-500 ms in-call hints); deploy on cloud/private cloud/on-prem/air-gapped; "40+ languages and dialects" — [gnani.ai](https://gnani.ai/)
- inya.ai/pricing now redirects (301) to gnani.ai — observed directly when fetching https://inya.ai/pricing on 2026-10-30.

### Inferences
- For a hackathon, the realistic S2S path is cascaded: Gnani STT stream -> your LLM -> Gnani TTS stream, via the LiveKit or Pipecat plugins. The 5B VoiceOS model should be treated as not generally available.
- "40+ languages" on the homepage conflicts with the 10 in the API docs; likely includes non-API/enterprise or foreign languages (Spanish named). Marketing-only.

### Gaps
- No public docs, languages, or access path for Warp v2.0 (S2S) or Evon v3.3 (LLM). "Evo"/"Evon"/"Aion" naming unverified.
- No documented direct SIP trunk / Exotel / Plivo integration beyond Twilio import and Webex; no published voice-agent end-to-end latency.
- Inya VoiceOS's six languages are not named in any source found.

## Open-Weight Models

### Takeaway
Gnani has released no open weights. The Hugging Face repos are API "cards"; the gnani-ai/vachana card explicitly says "No model weights are shipped", despite carrying Apache-2.0 metadata.

### Cited Findings
- gnani-ai/vachana HF card: hosted API only, "No model weights are shipped", inference on Gnani servers; out of scope: offline use, fine-tuning, weight access; not deployed on any HF Inference Provider; repo metadata licence Apache-2.0; install `pip install gnani-vachana transformers` and load with `trust_remote_code=True` — [HF gnani-ai/vachana](https://huggingface.co/gnani-ai/vachana)
- HF org lists one model, gnani-ai/gnani (ASR, "Prisma v2.5" card), no public datasets, no Spaces — [HF gnani-ai org](https://huggingface.co/gnani-ai); [HF gnani-ai/gnani](https://huggingface.co/gnani-ai/gnani)
- No sources found describing open weights or an open licence for Inya VoiceOS / the IndiaAI-Mission model — [Outlook Business](https://www.outlookbusiness.com/amp/story/news/sarvam-gnani-ai-launches-advanced-ai-models-at-the-indiaai-summit); [Business Today](https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19)
- Official integrations on GitHub/PyPI: pipecat-gnani and livekit-plugins-gnani (LiveKit reports model "vachana-stt-v3") — [PyPI pipecat-gnani](https://pypi.org/project/pipecat-gnani/); [PyPI livekit-plugins-gnani](https://pypi.org/project/livekit-plugins-gnani/); [GitHub Gnani-AI-Mintlify/pipecat-gnani](https://github.com/Gnani-AI-Mintlify/pipecat-gnani); [LiveKit docs](https://docs.livekit.io/agents/models/stt/gnani)

### Inferences
- The Apache-2.0 tag on the HF card most plausibly covers the wrapper code, not any model; do not assume rights to weights. Anything requiring offline/edge inference or fine-tuning cannot use Gnani.

### Gaps
- Whether IndiaAI-Mission terms will require Gnani to open-source the 14B model is not stated in any source found.

## Northeast Indian Language Support

### Takeaway
Gnani's documented APIs support NO Northeast Indian language. Assamese appears only in press releases and the Pipecat plugin list (and is explicitly listed as unsupported on the Prisma v3 page); Manipuri/Meitei, Bodo, Khasi, Mizo, Nagamese, Garo, Kokborok etc. appear in no Gnani source. AI4Bharat is the only verified option covering Bodo and Manipuri.

### Cited Findings
- Official STT and TTS language lists contain no NE language — [STT languages](https://docs.gnani.ai/api/STT/languages.md); [TTS voices](https://docs.gnani.ai/api/TTS/available-voices.md)
- Prisma v3.0: "Assamese is not supported" — [Prisma v3](https://docs.gnani.ai/api/STT/models/prisma-v3.md)
- Assamese claimed in: Vachana STT blog [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission), Vachana TTS press [Business Today](https://www.businesstoday.in/technology/story/gnaniai-launches-zero-shot-voice-cloning-tts-model-for-12-indic-languages-516896-2026-02-19), Pipecat STT list [Pipecat docs](https://docs.pipecat.ai/api-reference/server/services/stt/gnani)
- Manipuri, Bodo, Khasi, Mizo, Nagamese: not mentioned in any Gnani source reviewed (docs, HF, homepage, press) — absence across all sources above.
- AI4Bharat IndicConformer 600M multilingual: 22 official Indian languages incl. Bodo (brx) and Manipuri (mni), MIT licence, open weights — [HF ai4bharat/indic-conformer-600m-multilingual](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual); [GitHub IndicConformerASR](https://github.com/AI4Bharat/IndicConformerASR)
- AI4Bharat Indic Parler-TTS: 20 Indic languages + English; Bodo among emotion-prompt languages; Manipuri in speaker table — [HF ai4bharat/indic-parler-tts](https://huggingface.co/ai4bharat/indic-parler-tts); licence reported Apache-2.0 and gated by a secondary aggregator only — [dev.co](https://dev.co/ai/llms/indic-parler-tts) (unverified)
- IndicTrans2 covers Manipuri in Bengali and Meitei scripts, plus Assamese and Bodo (per third-party library table) — [libraries.io bhashini-translator](https://libraries.io/pypi/bhashini-translator) (secondary)
- Bhashini: no official ASR/TTS language list found; community code lists Assamese, Bodo, Manipuri TTS (Bodo male voice flagged broken); Khasi and Mizo not found — [HF smtiitm FastSpeech2 api.py](https://huggingface.co/smtiitm/FastSpeech2_HS_latest_models/blob/main/api.py); [PyPI bhashini-client-sdk](https://pypi.org/project/bhashini-client-sdk/0.2.2/)

### Inferences
- An NE-language project is a place where Gnani gives no measurable advantage; the builder would combine AI4Bharat open models (and possibly Gnani for the 10 major languages) or contribute data. Khasi, Mizo, Nagamese, Garo, Kokborok appear unserved by every option checked, which could itself be a problem statement.

### Gaps
- No verified coverage for Khasi, Mizo, Nagamese, Garo, Kokborok from any provider found.
- Google Cloud (Chirp) and Azure NE-language coverage not verified in this pass.

## API Docs, SDKs, Access, Pricing, Free Credits; Comparable Alternatives

### Takeaway
Self-serve signup at app.gnani.ai/voice gives an API key; docs are thorough (OpenAPI/AsyncAPI specs, Python SDK, LiveKit/Pipecat plugins). Public list pricing does not exist; the only free-credit evidence is promotional (100,000 free minutes for early Vachana STT adopters "valid till Jan 12", and a 2,000-free-minutes banner for Prisma v2.5). Sarvam publishes pricing; AI4Bharat is free and open.

### Cited Findings
- Access: sign up at https://app.gnani.ai/voice/ to generate a key; base URL https://api.vachana.ai; header `X-API-Key-ID` (WebSocket `x-api-key-id`) — [Gnani docs: Quick start](https://docs.gnani.ai/api/introduction/quick-start.md); alternative: email speechstack@gnani.ai — [HF card](https://huggingface.co/gnani-ai/vachana)
- SDKs: Python SDK (STT, batch STT, TTS), LiveKit plugin, Pipecat plugin; OpenAPI specs for STT, STTBatch, TTS, VC, agents; AsyncAPI for STT/TTS WebSockets — [Gnani docs index](https://docs.gnani.ai/llms.txt)
- Pricing: no pricing page on docs or homepage; "Book a Demo" CTA — [gnani.ai](https://gnani.ai/); [Gnani docs index](https://docs.gnani.ai/llms.txt)
- Free minutes: 100,000 free minutes for early adopters of Vachana STT "valid till Jan 12" (year unstated), and a 2,000-free-minutes banner for Prisma v2.5 — [Gnani blog](https://www.gnani.ai/resources/blogs/gnani-ai-launches-vachana-stt-a-foundational-indic-speech-to-text-model-trained-on-one-million-hours-under-the-indiaai-mission)
- Sarvam AI: STT ₹30/hour (₹45/hour with diarization), billed per second; Bulbul TTS v2 ₹15 and v3 ₹30 per 10K characters (v3 beta pricing); Saarika now listed as Legacy — [Sarvam docs pricing](https://docs.sarvam.ai/api/pricing); Bulbul V4 Flash reported 13 Oct 2026 at ₹20/10K chars (unverified, secondary) — [Analytics Insight](https://www.analyticsinsight.net/artificial-intelligence/sarvam-ai-bulbul-v4-flash-real-time-voice-model-for-indian-languages); Sarvam voice-agent pricing page exists — [Sarvam](https://www.sarvam.ai/products/voice-agents/pricing)
- Sarvam STT language count reported as 22-23 (no official list confirmed); Bulbul v3 reported at 11 languages — [Invideo blog](https://invideo.io/blog/sarvam-bulbul-indian-tts/) (secondary)
- AI4Bharat: IndicConformer (22 languages, MIT, open weights) and Indic Parler-TTS (20 Indic + English) — [HF IndicConformer](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual); [HF Indic Parler-TTS](https://huggingface.co/ai4bharat/indic-parler-tts)
- Bhashini: ASR, TTS, language detection, diarization, speaker verification, voice cloning, denoiser exposed via Dhruva pipeline APIs (per unofficial SDK) — [PyPI bhashini-client-sdk](https://pypi.org/project/bhashini-client-sdk/0.2.2/)
- Market reference for voice-agent pricing: typically $0.07-$0.19/min across vendors (third-party guide) — [Ringly](https://www.ringly.io/blog/ai-voice-agent-pricing)

### Inferences
- Where Gnani plausibly gives a measurable edge: 8 kHz telephony STT (self-claimed #1 on Kathbath Noisy 8kHz), telephony-native TTS encodings, production agent tooling (DTMF, voicemail, Twilio/Webex), on-prem/air-gapped deployment, and a cloning API. These should be verified by the team by running a small WER test on their own 8 kHz call audio against Sarvam and IndicConformer.
- Where Gnani gives no edge: language breadth (10 vs 22 for AI4Bharat/Sarvam), NE languages, open weights / offline use, published pricing.

### Gaps
- Gnani per-minute / per-character pricing, current free-tier terms, and rate-limit numbers: not public.
- Google Cloud Speech (Chirp) and Azure Speech Indian-language lists, 8 kHz support and pricing: not researched in this pass (tool budget) and should be checked before comparison.
- No independent third-party benchmark comparing Gnani vs Sarvam vs AI4Bharat found.
