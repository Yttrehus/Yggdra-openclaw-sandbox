# Speech-to-Text Pricing Research (Februar 2026)

**Formaal:** Sammenligning af STT-tjenester til transskribering af 100-200 timers audio.
**Use case:** 100 lastbilchauffoerer, 1-2 timer audio hver.
**Budget:** 500 DKK (~$70 USD) + $300 Google Cloud credit.

---

## Samlet Prisoversigt

| Tjeneste | Pris/minut | Pris/time | 100 timer | 200 timer | Gratis tier |
|---|---|---|---|---|---|
| **Groq Whisper v3 Turbo** | $0.0007 | $0.04 | **$4** | **$8** | ~8 timer/dag (free) |
| **Groq Whisper v3 Large** | $0.00185 | $0.111 | **$11.10** | **$22.20** | ~8 timer/dag (free) |
| **AssemblyAI Universal** | $0.0025 | $0.15 | **$15** | **$30** | 185 timer gratis ($50 credit) |
| **OpenAI Whisper** | $0.006 | $0.36 | **$36** | **$72** | Ingen |
| **OpenAI GPT-4o Mini Transcribe** | $0.003 | $0.18 | **$18** | **$36** | Ingen |
| **OpenAI GPT-4o Transcribe** | $0.006 | $0.36 | **$36** | **$72** | Ingen |
| **GCP STT V2 (Dynamic Batch)** | $0.003 | $0.18 | **$18** | **$36** | 60 min/maaned |
| **GCP STT V2 (Standard)** | $0.016 | $0.96 | **$96** | **$192** | 60 min/maaned |
| **Deepgram Nova-3 (batch)** | $0.0077 | $0.462 | **$46.20** | **$92.40** | $200 signup credit |
| **whisper.cpp (lokal)** | Gratis | Gratis | **$0** | **$0** | N/A (CPU tid) |

---

## Detaljeret Gennemgang

### 1. Groq Whisper API

**Priser (februar 2026):**
- Whisper Large v3 Turbo: **$0.04/time** (228x realtid)
- Whisper Large v3: **$0.111/time** (217x realtid)
- Minimum fakturering: 10 sekunder per request

**Free tier rate limits:**
- 20 requests/minut
- 2.000 requests/dag
- 7.200 audio-sekunder/time (= 2 timer audio/time)
- 28.800 audio-sekunder/dag (= 8 timer audio/dag)

**Beregning (betalt):**
- 100 timer: 100 x $0.04 = **$4.00** (ca. 29 DKK)
- 200 timer: 200 x $0.04 = **$8.00** (ca. 57 DKK)

**Beregning (gratis tier, 8 timer/dag):**
- 100 timer / 8 timer pr. dag = ~13 dage
- 200 timer / 8 timer pr. dag = ~25 dage
- Filstoerrelse: max 25 MB per request (free), 100 MB (dev tier)
- 25 MB ~ 25 min MP3 ved 128kbps, saa man skal chunke laengere filer

**Vurdering:** Absolut billigst. Selv betalt koster 200 timer kun $8. Free tier kan klare det paa 2-4 uger. Ultrahurtig (228x realtid = 1 time audio paa ~16 sekunder).

---

### 2. OpenAI Whisper API

**Priser:**
- Whisper: **$0.006/minut** ($0.36/time)
- GPT-4o Transcribe: **$0.006/minut** ($0.36/time) — bedre accuracy
- GPT-4o Mini Transcribe: **$0.003/minut** ($0.18/time) — billigere

**Beregning (Whisper):**
- 100 timer: 6.000 min x $0.006 = **$36** (ca. 256 DKK)
- 200 timer: 12.000 min x $0.006 = **$72** (ca. 512 DKK) — OVER BUDGET

**Beregning (GPT-4o Mini Transcribe):**
- 100 timer: 6.000 min x $0.003 = **$18** (ca. 128 DKK)
- 200 timer: 12.000 min x $0.003 = **$36** (ca. 256 DKK)

**Vurdering:** Flat-rate, ingen volumenrabat. 200 timer med Whisper overstiger budgettet. GPT-4o Mini Transcribe er et godt alternativ til $36 for 200 timer.

---

### 3. Google Cloud Speech-to-Text V2

**Priser:**
- Standard (Chirp model): **$0.016/minut** ($0.96/time)
- Dynamic Batch (op til 24t forsinkelse): **$0.003/minut** ($0.18/time)
- Dynamic Batch (logged): **$0.00225/minut** ($0.135/time)
- Gratis tier: 60 minutter/maaned

**Beregning (Dynamic Batch):**
- 100 timer: 6.000 min x $0.003 = **$18**
- 200 timer: 12.000 min x $0.003 = **$36**

**Beregning (Dynamic Batch Logged):**
- 100 timer: 6.000 min x $0.00225 = **$13.50**
- 200 timer: 12.000 min x $0.00225 = **$27**

**Med $300 GCP credit: FULDSTAENDIG GRATIS for begge scenarier.**

**Vurdering:** Med den eksisterende $300 credit er dette effektivt gratis. Selv Dynamic Batch Standard koster kun $36 for 200 timer. "Logged" betyder Google maa bruge data til traening — acceptabelt for rutineaudio. Latency op til 24 timer er fint naar det ikke er realtid. Chirp-modellen er Googles bedste og inkluderet i standardprisen.

---

### 4. Deepgram Nova-3

**Priser:**
- Pay-As-You-Go (batch): **$0.0077/minut** ($0.462/time)
- Growth Plan (batch): **$0.0065/minut** ($0.39/time)
- $200 gratis credit ved signup (udloeber ikke)

**Beregning (med $200 credit):**
- $200 / $0.0077 = ~25.974 min = **~433 timer gratis**
- 200 timer: GRATIS (inden for $200 credit)

**Vurdering:** $200 signup credit daekker 200+ timer. Ingen kreditkort noedvendigt. Nova-3 har god accuracy. Per-sekund fakturering (betaler kun for faktisk audio). Dog dyrere end Groq hvis man betaler.

---

### 5. AssemblyAI

**Priser:**
- Universal (pre-recorded): **$0.15/time** ($0.0025/minut)
- Universal-3 Pro: **$0.21/time**
- Gratis tier: $50 credit = ~185 timer pre-recorded, ~333 timer streaming

**Beregning:**
- 100 timer: Gratis (inden for $50 credit)
- 200 timer: 185 timer gratis + 15 timer x $0.15 = **$2.25** extra
- Alternativt: fuld 200 timer x $0.15 = **$30**

**Vurdering:** Free tier daekker naesten 200 timer. Base pricing er meget billigt. Speaker diarization koster extra (+$0.02/time) men er billigt. God API, god dokumentation.

---

### 6. Lokal Whisper (whisper.cpp / faster-whisper)

**Pris:** Gratis (open source)

**whisper.cpp paa VPS uden GPU:**
- Small model (~461 MB): Kan koere CPU-only
- Medium model (~1.5 GB): Kan koere, men langsomt
- Large model (~3 GB): Urealistisk paa typisk VPS uden GPU
- Hastighed paa CPU: ~0.3-1x realtid med small model (1 time audio = 1-3 timer processing)
- Med quantized modeller: hurtigere, lavere RAM-forbrug

**faster-whisper (CTranslate2):**
- 4x hurtigere end standard Whisper
- Lavere memory footprint
- CPU-only er muligt men stadig langsomt for large model

**Realistisk for 200 timer paa VPS (4 CPU cores, ingen GPU):**
- Small model: ~200-600 timer processering (8-25 dage non-stop)
- Medium model: ~400-1200 timer processering (17-50 dage)
- Large model: Ikke praktisk

**Vurdering:** Gratis men ekstremt langsomt. 200 timer audio kan tage uger paa en VPS. Kun realistisk hvis man har adgang til en maskine med GPU, eller hvis man har maaneder til raadighed. Kan ikke anbefales til dette projekt medmindre GPU er tilgaengelig.

---

## Anbefaling

### Primaer anbefaling: AssemblyAI (gratis tier)

| Faktor | Vurdering |
|---|---|
| Pris for 200 timer | ~$2.25 (ca. 16 DKK) |
| Setup-kompleksitet | Lav (simpel API) |
| Gratis tier | 185 timer inkluderet |
| Accuracy | Hoej (Universal model) |
| Dansk support | Ja (99 sprog) |

AssemblyAI giver 185 timer gratis. For 200 timer koster det kun ~$2.25 ekstra. Simpel API, god dokumentation, ingen rate-limiting issues.

### Alternativ 1: Groq Whisper v3 Turbo (billigst betalt)

- 200 timer = $8 (~57 DKK)
- Ultrahurtig (228x realtid)
- Free tier: 8 timer/dag → 25 dage for 200 timer
- Kraever file-chunking (25 MB max per request)

### Alternativ 2: Deepgram Nova-3 ($200 gratis credit)

- 200 timer = gratis (inden for $200 signup credit)
- God accuracy med Nova-3
- Credits udloeber ikke
- Kraever signup

### Alternativ 3: Google Cloud STT V2 Dynamic Batch (med $300 credit)

- 200 timer = ~$36 (men daekket af $300 credit = gratis)
- Chirp model (Googles bedste)
- 24-timers latency OK for batch-job
- GCP credit er allerede tilgaengelig

### Budget-konklusion

Med 500 DKK ($70) budget:

| Strategi | Pris | Kommentar |
|---|---|---|
| AssemblyAI free + Groq | ~$10 | Bedste kombination |
| Deepgram $200 credit | $0 | Signup-credit daekker alt |
| GCP $300 credit | $0 | Allerede tilgaengeligt |
| Alt betalt via Groq | $8 | Billigst rent betalt |
| OpenAI Whisper | $72 | Over budget ved 200t |

**Alle loesninger passer inden for budgettet.** Selv den dyreste (OpenAI Whisper, $72 for 200t) er taet paa graensen. Groq, AssemblyAI, Deepgram og GCP er alle langt under budget.

**Anbefalet fremgangsmaade:**
1. Start med **AssemblyAI** (185 timer gratis, simpel API)
2. Brug **Groq Whisper Turbo** til resten ($0.04/time) eller til speed-kritiske jobs
3. Gem **GCP $300 credit** til andre formaal (det er for dyrt per time til STT sammenlignet med alternativer)

---

## Kilder

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Groq Pricing](https://groq.com/pricing)
- [Groq Rate Limits](https://console.groq.com/docs/rate-limits)
- [Deepgram Pricing](https://deepgram.com/pricing)
- [AssemblyAI Pricing](https://www.assemblyai.com/pricing)
- [Google Cloud Speech-to-Text Pricing](https://cloud.google.com/speech-to-text/pricing)
- [whisper.cpp GitHub](https://github.com/ggml-org/whisper.cpp)
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)

*Sidst opdateret: 22. februar 2026*
