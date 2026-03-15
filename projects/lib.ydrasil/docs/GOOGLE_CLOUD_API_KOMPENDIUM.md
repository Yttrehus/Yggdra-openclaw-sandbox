# Google Cloud API Kompendium

**Oprettet:** 16. februar 2026
**Formål:** Komplet overblik over Google Cloud APIs til solo-udvikler med $300 credit
**Profil:** Kris — affaldskort-chauffeur, AI-builder, kun Android-telefon

**Relevansskala:** 1 = irrelevant, 2 = nice-to-know, 3 = potentielt nyttigt, 4 = meget relevant, 5 = must-have

---

## Indhold

1. [Maps & Navigation](#1-maps--navigation)
2. [Speech & Sprog](#2-speech--sprog)
3. [AI & Machine Learning](#3-ai--machine-learning)
4. [Gemini & Generativ AI](#4-gemini--generativ-ai)
5. [Google Workspace APIs](#5-google-workspace-apis)
6. [Serverless & Compute](#6-serverless--compute)
7. [Storage & Databaser](#7-storage--databaser)
8. [Messaging & Integration](#8-messaging--integration)
9. [Sikkerhed & Identitet](#9-sikkerhed--identitet)
10. [DevOps & CI/CD](#10-devops--cicd)
11. [Data & Analytics](#11-data--analytics)
12. [IoT & Specialiserede](#12-iot--specialiserede)
13. [Prisberegning med $300 credit](#13-prisberegning-med-300-credit)

---

## 1. Maps & Navigation

### Google Maps Platform (ny prismodel fra marts 2025)

**Prismodel:** Pay-as-you-go med gratis kvoter per SKU. Den gamle $200/md-kredit er erstattet af gratis tærskler per API-kald-type (Essentials/Pro/Enterprise).

| API | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|-----|-------------|-------------|---------------|----------|
| **Routes API** | Beregn ruter, ETA, afstand mellem punkter | 10.000 req/md (Essentials) | $5-10/1.000 req | **5** |
| **Navigation SDK (Android)** | Turn-by-turn navigation i din egen app | 1.000 destinationer/md gratis | Per destination | **5** |
| **Maps SDK for Android** | Vis kort i Android-app | 100.000 tile-loads/md | $7/1.000 loads | **5** |
| **Geocoding API** | Adresse → GPS-koordinater og omvendt | 10.000 req/md | $5/1.000 req | **5** |
| **Places API** | Søg steder, detaljer, autocomplete | 5.000 req/md (Pro) | $17-32/1.000 req | **4** |
| **Geolocation API** | Find position via WiFi/celletårne | 10.000 req/md | $5/1.000 req | **3** |
| **Distance Matrix API** | Afstand/tid mellem mange punkter | 10.000 elementer/md | $5-10/1.000 elem | **4** |
| **Roads API** | Snap GPS-punkter til veje | 10.000 req/md | $10/1.000 req | **3** |
| **Static Maps API** | Statiske kortbilleder | 100.000 req/md | $2/1.000 req | **2** |
| **Street View API** | Panoramabilleder af gader | 10.000 req/md | $7/1.000 req | **2** |
| **Elevation API** | Højdedata for koordinater | 10.000 req/md | $5/1.000 req | **1** |

---

### DYBDEGÅENDE: Routes API (Relevans 5)

**Hvad det kan:**
- Beregn optimale ruter mellem punkter (A → B → C → ... → Z)
- Understøtter waypoints — perfekt til ruteoptimering med mange stop
- Trafik-aware routing med realtidsdata
- Forskellige transportformer (bil, cykel, gang)
- Beregn ETA og afstand for hvert segment
- Route Matrix: beregn afstand/tid mellem ALLE kombinationer af origin/destination

**Brug for Kris:**
- Optimér rækkefølgen af 80+ stop på rute 256
- Beregn samlet køretid med trafik
- Sammenlign "nuværende rækkefølge" vs "optimeret rækkefølge"
- Eksempel: Send alle adresser → få optimal rækkefølge + tidsestimat

**API-kald eksempel:**
```
POST https://routes.googleapis.com/directions/v2:computeRoutes
{
  "origin": {"address": "Aarhus C"},
  "destination": {"address": "Aarhus N"},
  "intermediates": [{"address": "Stop 1"}, {"address": "Stop 2"}],
  "optimizeWaypointOrder": true,
  "travelMode": "DRIVE"
}
```

**Pris ved Kris' forbrug:**
- ~1 rute-beregning/dag × 22 arbejdsdage = ~22 req/md → GRATIS (under 10.000)
- Selv med 10 genberegninger/dag = 220/md → stadig gratis

---

### DYBDEGÅENDE: Navigation SDK for Android (Relevans 5)

**Hvad det kan:**
- Fuld turn-by-turn navigation i din egen Android-app
- Google Maps-kvalitet navigation uden at åbne Google Maps
- Real-time trafik og genberegning
- Custom UI — kan integreres med Ydrasil voice-app
- Waypoint-navigation med flere stop
- Arrival detection — vide præcist hvornår du er fremme

**Brug for Kris:**
- Byg navigation direkte ind i Ydrasil voice-app
- Auto-navigation til næste stop når nuværende er markeret "done"
- Kombiner med Routes API til optimeret rækkefølge
- Vis status: "Stop 43/80 — næste: Randersvej 15 — 2 min"

**Pris:** 1.000 gratis destinationer/md. Med 80 stop/dag × 22 dage = 1.760 dest/md → ca. 760 over gratis = minimal kostnad.

---

### DYBDEGÅENDE: Geocoding API (Relevans 5)

**Hvad det kan:**
- Konverter adresser til GPS-koordinater (og omvendt)
- Batch-geocoding af mange adresser
- Returner strukturerede adressekomponenter
- Place ID for hvert resultat (bruges i andre APIs)

**Brug for Kris:**
- Alle stop-adresser fra TransportIntra → GPS-koordinater
- Verificer at GPS-data fra getRute matcher faktisk adresse
- Byg sorterings-beregninger baseret på geografi
- Rute 256 har ~400 unikke adresser — geocode én gang, gem i database

**Pris:** 10.000 gratis/md. Kris behøver max ~400 (engangs-geocoding) → GRATIS.

---

### DYBDEGÅENDE: Distance Matrix API (Relevans 4)

**Hvad det kan:**
- Beregn afstand + tid mellem ALLE kombinationer af punkter
- 25 origins × 25 destinations per request
- Trafik-aware estimater
- Basis for ruteoptimering (TSP/VRP)

**Brug for Kris:**
- Beregn distance-matrix for alle stops → brug til optimal sortering
- Input til Travelling Salesman Problem-algoritme
- Sammenlign klynger af stop for at finde logiske grupper

**Pris:** 10.000 elementer gratis/md. 80 stop = 80×80 = 6.400 elementer → GRATIS for én beregning/md.

---

## 2. Speech & Sprog

| API | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|-----|-------------|-------------|---------------|----------|
| **Cloud Text-to-Speech** | Tekst → naturlig tale, 40+ sprog | 4M tegn/md (standard), 1M tegn/md (WaveNet) | $4-16/1M tegn | **5** |
| **Cloud Speech-to-Text** | Tale → tekst, real-time + batch | 60 min/md | $0.016/min | **5** |
| **Cloud Translation** | Oversæt tekst, 100+ sprog | 500.000 tegn/md | $20/1M tegn (NMT) | **3** |
| **Cloud Natural Language** | Sentiment, entiteter, klassificering | 5.000 req/md | $1-2/1.000 req | **4** |

---

### DYBDEGÅENDE: Cloud Text-to-Speech (Relevans 5)

**Hvad det kan:**
- 220+ stemmer i 40+ sprog inkl. dansk
- Standard stemmer: 4 millioner tegn GRATIS/md
- WaveNet stemmer: 1 million tegn GRATIS/md (langt mere naturlige)
- Neural2 stemmer: nyeste generation, ultra-naturlige
- Journey stemmer: designet til lange svar (samtale-stil)
- SSML-support: kontrol over pauser, udtale, hastighed, toneleje
- Streaming og batch

**Brug for Kris:**
- Ydrasil voice-app: AI-svar læses højt i bilen
- Morning brief oplæsning: "God morgen Kris, i dag har du 78 stop..."
- Stop-info: "Næste stop: Randersvej 15, 3. sal, kode 4521"
- Dansk stemme med WaveNet-kvalitet

**Pris ved Kris' forbrug:**
- ~500 tegn per besked × 50 beskeder/dag × 22 dage = 550.000 tegn/md
- Standard: bruger 14% af gratis kvote
- WaveNet: bruger 55% af gratis kvote
- **Helt gratis ved normalt forbrug**

---

### DYBDEGÅENDE: Cloud Speech-to-Text (Relevans 5)

**Hvad det kan:**
- Real-time streaming transcription
- 125+ sprog inkl. dansk
- Automatic punctuation
- Word-level timestamps
- Speaker diarization (hvem siger hvad)
- V2 API med forbedret nøjagtighed
- Chirp model: Googles nyeste, mest præcise ASR
- Adaptation: tilpas til domain-specifikke ord

**Brug for Kris:**
- Voice commands i bilen: "Marker stop som udført", "Hvad er næste adresse?"
- Diktér noter: "Kunde 4521 har flyttet container til baggården"
- Hands-free styring af Ydrasil app
- Kombiner med Gemini for forståelse af komplekse kommandoer

**Pris ved Kris' forbrug:**
- 60 min gratis/md
- ~2-3 min voice/dag × 22 dage = ~55 min/md → GRATIS
- Selv med mere brug: $0.016/min = $1 for ~60 ekstra minutter

---

### DYBDEGÅENDE: Cloud Natural Language (Relevans 4)

**Hvad det kan:**
- Sentiment-analyse: er teksten positiv/negativ/neutral?
- Entity-extraktion: find navne, steder, organisationer
- Entity-sentiment: sentiment per entitet
- Syntaksanalyse: ordklasser, afhængighedstræer
- Indholdskategorisering: klassificer tekst i 700+ kategorier
- Moderation: detect inappropriate content

**Brug for Kris:**
- Analysér kundenotater fra TransportIntra
- Klassificer Telegram-beskeder efter emne
- Sentiment på dagbogsposter: track humør over tid
- Extract nøgleinfo fra voice memos: adresser, navne, handlinger

**Pris:** 5.000 gratis requests/md → mere end nok til personlig brug.

---

## 3. AI & Machine Learning

| API | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|-----|-------------|-------------|---------------|----------|
| **Cloud Vision API** | Billedanalyse, OCR, ansigter, labels | 1.000 enheder/md | $1.50/1.000 enh | **4** |
| **Document AI** | Avanceret dokument-parsing, OCR | $300 credit | $1.50/1.000 sider | **3** |
| **Video Intelligence** | Videoanalyse, labels, tracking | 1.000 min/md | $0.10/min | **2** |
| **Dialogflow CX** | Konversations-AI chatbot-platform | $600 credit (12 md) | Per request | **3** |
| **Cloud AutoML** | Træn custom ML-modeller uden kode | $300 credit | Per node-time | **2** |
| **Vertex AI Prediction** | Deploy og serv ML-modeller | $300 credit | Per node-time | **3** |
| **Vertex AI Matching Engine** | Vektor-søgning i skala | $300 credit | Per node + query | **2** |

---

### DYBDEGÅENDE: Cloud Vision API (Relevans 4)

**Hvad det kan:**
- **OCR (Optical Character Recognition):** Læs tekst fra billeder
- **Label Detection:** Hvad er på billedet?
- **Object Detection:** Find og lokalisér objekter
- **Face Detection:** Find ansigter + emotioner
- **Landmark Detection:** Genkend kendte steder
- **Logo Detection:** Genkend logos
- **Safe Search:** Detect explicit/violent content
- **Web Detection:** Find lignende billeder online
- **Document Text Detection:** Avanceret OCR for dokumenter
- Understøtter batch + async processing

**Brug for Kris:**
- Fotografer container-nummer → OCR → auto-registrering
- Fotografer adresseskilt → match med rute
- Dokumenter skader/problemer med billeder → auto-labels
- Scan sorteringsark med telefonen → digitalisér
- Læs håndskrevne noter fra kolleger

**Pris:** 1.000 gratis enheder/md. Med ~10 billeder/dag × 22 dage = 220 → GRATIS.

---

## 4. Gemini & Generativ AI

| API | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|-----|-------------|-------------|---------------|----------|
| **Gemini API (AI Studio)** | Generativ AI via Google AI Studio | Gratis tier (rate-limited) | Per 1M tokens | **5** |
| **Vertex AI Gemini** | Enterprise Gemini via GCP | $300 credit | Per 1M tokens | **4** |
| **Imagen API** | Billedgenerering | $300 credit | Per billede | **2** |

---

### DYBDEGÅENDE: Gemini API (Relevans 5)

**Modeller tilgængelige (februar 2026):**

| Model | Input/1M tokens | Output/1M tokens | Gratis tier |
|-------|-----------------|-------------------|-------------|
| Gemini 3 Pro | $2-4 | $12-18 | Ja (rate-limited) |
| Gemini 2.5 Pro | $1.25 | $5.00 | Ja (rate-limited) |
| Gemini 2.5 Flash | $0.15 | $0.60 | Ja (rate-limited) |
| Gemini 2.5 Flash-Lite | $0.02 | $0.10 | Ja (rate-limited) |

**Gratis tier via AI Studio (INGEN credit-kort):**
- 5-15 requests per minut (model-afhængigt)
- 250.000 tokens per minut
- 20-100 requests per dag (efter dec 2025 ændringer)

**Hvad det kan:**
- Multimodal: tekst + billeder + lyd + video
- 1M+ kontekstvindue
- Kode-generering og -analyse
- Reasoning og komplekse opgaver
- Grounding med Google Search
- Function calling
- JSON-mode for struktureret output

**Brug for Kris:**
- **Nano Banana Pro (Gemini 3 Pro Image):** Kris' foretrukne visualiseringsværktøj
- Voice-app backend: forstå komplekse forespørgsler
- Analysér billeder taget i felten
- Opsummer dagbogsposter, planlæg næste dag
- Generér rapporter fra rutedata

**Pris:** Gratis tier til prototyping. Med $300 credit via Vertex AI: ~60M tokens (Gemini 2.5 Flash) = MASSIVT.

---

## 5. Google Workspace APIs

**Alle Google Workspace APIs er GRATIS at bruge — ingen pris per kald. Kun rate limits.**

| API | Beskrivelse | Gratis | Rate limit | Relevans |
|-----|-------------|--------|------------|----------|
| **Google Calendar API** | Opret/læs/rediger kalenderbegivenheder | Ja, helt gratis | 1.000.000 req/dag | **5** |
| **Google Drive API** | Upload/download/del filer | Ja, helt gratis | Per-minut kvoter | **5** |
| **Gmail API** | Læs/send emails programmatisk | Ja, helt gratis | Kvote-enheder | **4** |
| **Google Sheets API** | Læs/skriv regneark programmatisk | Ja, helt gratis | 300 req/min | **4** |
| **Google Docs API** | Opret/rediger dokumenter | Ja, helt gratis | Per-minut kvoter | **3** |
| **Google Tasks API** | Opret/administrer opgaver | Ja, helt gratis | Per-minut kvoter | **3** |
| **People API** | Kontaktinformation | Ja, helt gratis | Per-minut kvoter | **2** |
| **Google Forms API** | Opret/læs formularer | Ja, helt gratis | Per-minut kvoter | **1** |

---

### DYBDEGÅENDE: Google Calendar API (Relevans 5)

**Hvad det kan:**
- Opret, opdater, slet kalenderbegivenheder
- Læs kommende begivenheder
- Push notifications ved ændringer
- Recurring events
- Multiple kalendere
- Free/busy queries
- Reminders og notifications

**Brug for Kris:**
- Auto-opret "Rute 256" hver morgen med antal stop + estimeret tid
- Vis dagens plan i voice-app morning brief
- Bloker tid til pauser baseret på ruteoptimering
- Log faktisk tid per rute vs estimeret
- Synkroniser med andre aftaler

**Pris:** HELT GRATIS. Ingen begrænsning udover rate limits.

---

### DYBDEGÅENDE: Google Drive API (Relevans 5)

**Hvad det kan:**
- Upload/download filer programmatisk
- Opret mapper, organiser filer
- Del filer med andre
- Søg i filer
- Export Google Docs/Sheets til PDF/CSV
- Webhooks ved filändringer
- 15 GB gratis lagerplads

**Brug for Kris:**
- Automatisk backup af rutedata til Drive
- Upload voice memos fra Ydrasil
- Synkroniser sorteringsark
- Gem rapporter og dagbøger
- Allerede brugt via rclone — API giver mere kontrol

**Pris:** HELT GRATIS. Drive lagerplads = 15 GB gratis.

---

### DYBDEGÅENDE: Gmail API (Relevans 4)

**Hvad det kan:**
- Læs og søg i emails
- Send emails programmatisk
- Labels, filtre, tråde
- Push notifications ved nye emails
- Batch operations
- Draft management

**Brug for Kris:**
- Auto-parse rute-emails fra TransportIntra
- Send daglig statusrapport per email
- Overvåg for vigtige meddelelser
- Automatisér email-baserede workflows
- Allerede data i `data/gmail/`

**Pris:** HELT GRATIS.

---

### DYBDEGÅENDE: Google Sheets API (Relevans 4)

**Hvad det kan:**
- Læs/skriv celler, rækker, kolonner
- Opret nye regneark
- Formattering, diagrammer, filtre
- Named ranges
- Append data (perfekt til logging)
- Batch updates

**Brug for Kris:**
- Direkte integration med sorteringsark (256 ORG2ÅRH.xlsx)
- Live rutedata i Sheets → tilgængelig på telefonen
- Log daglig performance i Sheet
- Del data med kolleger via Sheets

**Pris:** HELT GRATIS.

---

## 6. Serverless & Compute

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Cloud Functions** | Kør kode uden server, event-driven | 2M invocations/md + 400K GB-sek | $0.40/1M invoc | **5** |
| **Cloud Run** | Container-baseret serverless | 180K vCPU-sek + 2M req/md | Per vCPU-sek | **4** |
| **Cloud Scheduler** | Cron jobs i skyen | 3 jobs gratis | $0.10/job/md | **4** |
| **App Engine** | Fully managed app hosting | 28 instans-timer/dag | Per instans-time | **3** |
| **Compute Engine** | Virtuelle maskiner | 1x e2-micro (us) | Per time | **3** |
| **Cloud Tasks** | Asynkron task-kø | 1M ops/md | $0.40/1M ops | **3** |
| **Workflows** | Orchestrer serverless tjenester | 5.000 steps/md | $0.01/1.000 steps | **3** |
| **Eventarc** | Event-routing for Cloud Run | Inkluderet | Inkluderet | **2** |

---

### DYBDEGÅENDE: Cloud Functions (Relevans 5)

**Hvad det kan:**
- Kør Python/Node.js/Go-kode som svar på events
- HTTP-trigger: kald via URL
- Pub/Sub-trigger: reagér på beskeder
- Cloud Storage-trigger: reagér på filupload
- Scheduler-trigger: kør på tidspunkter
- Automatisk skalering (inkl. ned til 0)
- 2. generation: længere timeout (60 min), større instanser

**Brug for Kris:**
- **Morgen-brief generator:** Cloud Scheduler kl. 06:00 → Cloud Function → generer brief → send til Telegram
- **Rute-henter:** Automatisk hent getRute fra TransportIntra hver morgen
- **Webhook endpoint:** Modtag data fra diverse tjenester
- **Voice memo processor:** Upload lyd → trigger Function → transcribe → gem i Qdrant
- **Daglig backup:** Automatisér Qdrant snapshot + upload til Drive

**Pris ved Kris' forbrug:**
- 2 millioner invocations GRATIS/md
- ~10 function-kald/dag × 30 dage = 300/md → bruger 0.015% af gratis kvote
- 400.000 GB-sek gratis: selv med 256 MB × 10 sek × 300 kald = 768 GB-sek → stadig gratis
- **Realistisk: $0 per måned**

---

### DYBDEGÅENDE: Cloud Scheduler (Relevans 4)

**Hvad det kan:**
- Cron jobs i skyen — præcis som crontab, men managed
- Trigger HTTP endpoints, Pub/Sub topics, Cloud Functions
- Retry-logik ved fejl
- Timezone-support (Europe/Copenhagen!)
- Min-interval: 1 minut

**Brug for Kris:**
- Kl. 05:30: Hent dagens rute fra TransportIntra
- Kl. 06:00: Generer morning brief
- Kl. 06:15: Send brief til Telegram
- Kl. 22:00: Kør daglig backup
- Kl. 23:55: Generer auto-dagbog
- Erstat VPS cron jobs → mere pålideligt

**Pris:** 3 jobs gratis/md. Derudover $0.10/job/md. Med 5 jobs = $0.20/md.

---

### DYBDEGÅENDE: Cloud Run (Relevans 4)

**Hvad det kan:**
- Kør Docker containers serverless
- Auto-skalering inkl. ned til 0
- Custom domæner med auto-SSL
- Længere kørselstid end Functions (op til 60 min)
- Concurrency: håndtér mange samtidige requests
- Sidecar containers

**Brug for Kris:**
- Host Ydrasil voice-app backend
- API gateway for alle tjenester
- Alternativ til VPS for webservices
- Kør tunge processer (ruteoptimering, batch-embedding)

**Pris:** 180.000 vCPU-sek + 2M requests gratis/md. Lav-trafik app = GRATIS.

---

## 7. Storage & Databaser

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Cloud Storage** | Objekt-storage (filer, billeder, backups) | 5 GB regional | $0.020/GB/md | **4** |
| **Firestore** | NoSQL dokument-database | 1 GB + 50K reads/dag | Per operation | **4** |
| **Cloud SQL** | Managed PostgreSQL/MySQL | Ingen gratis tier | ~$7/md minimum | **2** |
| **Cloud Spanner** | Global distribueret database | Ingen gratis tier | $0.90/node/time | **1** |
| **Memorystore** | Managed Redis/Memcached | Ingen gratis tier | Per GB/time | **1** |
| **BigQuery** | Data warehouse + analytics | 1 TB queries + 10 GB storage/md | $5/TB query | **3** |

---

### DYBDEGÅENDE: Cloud Storage (Relevans 4)

**Hvad det kan:**
- Gem filer af enhver type og størrelse
- 4 storage classes: Standard, Nearline, Coldline, Archive
- Versioning, lifecycle management
- Signed URLs (midlertidig adgang uden login)
- Trigger Cloud Functions ved upload
- CDN-integration

**Brug for Kris:**
- Backup af Qdrant snapshots
- Gem voice memos, billeder fra ruten
- Host statiske filer for webapp
- Arkivér gamle rutedata
- Trigger processing pipeline ved fil-upload

**Pris:** 5 GB gratis. Rutedata + backups < 5 GB → GRATIS.

---

### DYBDEGÅENDE: Firestore (Relevans 4)

**Hvad det kan:**
- NoSQL dokument-database, real-time sync
- Offline-support (perfekt til Android)
- Real-time listeners: data opdateres automatisk
- Queries med filtre, sortering, paginering
- Transaktioner og batch writes
- Security rules
- Integration med Firebase Auth

**Brug for Kris:**
- Real-time rute-status: marker stop som udført → synkronisér til alle enheder
- Offline-first: virker selv uden signal på ruten
- Gem brugerdata for voice-app
- Erstatte/supplere Qdrant til strukturerede data
- Push-baseret: data opdateres øjeblikkeligt

**Pris:** 50K reads + 20K writes/dag GRATIS. Kris' forbrug ~ et par hundrede ops/dag → GRATIS.

---

## 8. Messaging & Integration

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Firebase Cloud Messaging** | Push notifications til Android/iOS/web | HELT GRATIS, ubegrænset | Gratis | **5** |
| **Cloud Pub/Sub** | Asynkron besked-kø | 10 GB/md | $0.04/GB | **3** |
| **Cloud Endpoints** | API gateway + management | 2M kald/md | $3/1M kald | **2** |
| **API Gateway** | Managed API gateway | 2M kald/md | $3/1M kald | **2** |
| **Cloud IoT Core** | IoT device management | Udgået | - | **1** |

---

### DYBDEGÅENDE: Firebase Cloud Messaging (Relevans 5)

**Hvad det kan:**
- Send push notifications til Android-enheder — HELT GRATIS
- Ubegrænset antal beskeder
- Topic messaging: send til grupper
- Data messages: send JSON-payload til app
- Notification messages: vis i notification bar
- Upstream messaging: enhed → server
- Priority levels: high (vågn enheden) og normal
- Scheduling: send på bestemt tidspunkt

**Brug for Kris:**
- Morning brief notification kl. 06:00
- Alert ved ruteændringer fra TransportIntra
- "Husk: container ved Randersvej 15 er flyttet"
- Voice-app kan modtage data-push med opdateringer
- Erstatter dele af Telegram-bridge funktionalitet
- Push vigtige beskeder selv når app er lukket

**Pris:** GRATIS. Altid. Ubegrænset.

---

## 9. Sikkerhed & Identitet

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Secret Manager** | Gem API keys, passwords sikkert | 6 aktive secrets + 10K access/md | $0.06/secret/md | **4** |
| **Firebase Auth** | Bruger-login (email, Google, telefon) | 10K verifications/md (telefon) | Per verification | **3** |
| **Cloud IAM** | Adgangskontrol | Inkluderet | Inkluderet | **2** |
| **Cloud KMS** | Krypterings-nøglehåndtering | $0.06/nøgle/md | Per operation | **1** |
| **Cloud Armor** | DDoS-beskyttelse | Ingen gratis tier | $5/md basis | **1** |
| **reCAPTCHA Enterprise** | Bot-beskyttelse | 10K assessments/md | $1/1K assess | **1** |

---

### DYBDEGÅENDE: Secret Manager (Relevans 4)

**Hvad det kan:**
- Gem API keys, database passwords, tokens sikkert
- Versionering af secrets
- Automatisk rotation
- Adgangskontrol per secret
- Audit logging
- Integration med Cloud Functions, Cloud Run

**Brug for Kris:**
- Gem TransportIntra credentials sikkert (i stedet for i git!)
- API keys til OpenAI, Groq, etc.
- Telegram bot token
- Automatisk rotation af credentials
- **Sikkerhedsaudit viste API keys i git — Secret Manager løser det**

**Pris:** 6 secrets gratis. Kris har ~6-8 secrets → $0.12/md for de ekstra.

---

## 10. DevOps & CI/CD

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Cloud Build** | CI/CD pipeline | 120 build-min/dag | $0.003/build-min | **3** |
| **Artifact Registry** | Docker images + pakker | 0.5 GB | $0.10/GB/md | **3** |
| **Cloud Source Repositories** | Git repos | 5 brugere + 50 GB | Per bruger/storage | **1** |
| **Cloud Deploy** | Continuous delivery | $300 credit | Per target/md | **1** |

---

## 11. Data & Analytics

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **BigQuery** | Serverless data warehouse | 1 TB queries + 10 GB storage/md | $5/TB query | **3** |
| **BigQuery ML** | ML direkte i SQL | Inkluderet i BQ gratis tier | Per model-type | **2** |
| **Dataflow** | Stream/batch data processing | $300 credit | Per worker-time | **1** |
| **Dataproc** | Managed Spark/Hadoop | $300 credit | Per cluster-time | **1** |
| **Data Catalog** | Metadata management | Gratis | Gratis | **1** |
| **Looker Studio** | Dashboards og rapporter | Gratis | Gratis | **3** |

---

## 12. IoT & Specialiserede

| Service | Beskrivelse | Gratis tier | Pris derefter | Relevans |
|---------|-------------|-------------|---------------|----------|
| **Firebase Realtime Database** | Real-time JSON database | 1 GB storage + 10 GB transfer/md | Per GB | **3** |
| **Firebase Hosting** | Web app hosting | 10 GB storage + 360 MB/dag transfer | Per GB | **3** |
| **Firebase Remote Config** | Feature flags | Gratis | Gratis | **2** |
| **Firebase Crashlytics** | Crash reporting | Gratis | Gratis | **3** |
| **Firebase Analytics** | App analytics | Gratis | Gratis | **3** |
| **Firebase Performance** | App performance monitoring | Gratis | Gratis | **2** |
| **Cloud Healthcare API** | FHIR, HL7, DICOM | $300 credit | Per operation | **1** |
| **Cloud Talent Solution** | Job matching | $300 credit | Per operation | **1** |
| **Recommendations AI** | Anbefalingssystem | $300 credit | Per prediction | **1** |
| **Media Translation** | Real-time lyd-oversættelse | $300 credit | Per minut | **2** |

---

## 13. Prisberegning med $300 Credit

### Kris' Realistiske Månedlige Forbrug

**Helt gratis (Always Free tier):**

| Service | Forbrug | Gratis kvote | Kostnad |
|---------|---------|--------------|---------|
| Cloud Functions | ~300 invocations | 2.000.000 | $0 |
| Cloud Scheduler | 5 jobs | 3 gratis | $0.20 |
| Text-to-Speech (WaveNet) | ~550K tegn | 1.000.000 | $0 |
| Speech-to-Text | ~55 min | 60 min | $0 |
| Vision API (OCR) | ~200 enheder | 1.000 | $0 |
| Natural Language | ~100 req | 5.000 | $0 |
| Translation | ~50K tegn | 500.000 | $0 |
| Routes API | ~220 req | 10.000 | $0 |
| Geocoding | ~400 req (engang) | 10.000 | $0 |
| Distance Matrix | ~6.400 elem | 10.000 | $0 |
| Cloud Storage | ~2 GB | 5 GB | $0 |
| Firestore | ~500 ops/dag | 50K reads/dag | $0 |
| Firebase Cloud Messaging | Ubegrænset | Ubegrænset | $0 |
| Calendar/Drive/Gmail/Sheets | Ubegrænset | Ubegrænset | $0 |
| Cloud Run | Lav trafik | 180K vCPU-sek | $0 |
| Secret Manager | 6 secrets | 6 gratis | $0 |
| BigQuery | ~10 GB queries | 1 TB | $0 |

**Estimeret månedlig pris: ~$0.20 (kun Cloud Scheduler)**

### Hvad $300 Credit Kan Bruges Til

Med de fleste services gratis, kan $300 credit fokuseres på:

| Service | $300 rækker til |
|---------|-----------------|
| Gemini 2.5 Flash (Vertex AI) | ~2 milliarder input tokens |
| Gemini 2.5 Pro (Vertex AI) | ~240M input tokens |
| Navigation SDK (over gratis) | ~60.000 destinationer |
| Cloud Run (heavy workloads) | ~1.667 vCPU-timer |
| Speech-to-Text (over gratis) | ~18.750 minutter (~312 timer) |
| Vision API (over gratis) | ~200.000 enheder |

### Anbefalet Prioritering af Credit

1. **Gemini API via Vertex AI** — mest værdi per krone, driver hele AI-laget
2. **Navigation SDK** — hvis Kris bygger dedicated rute-app
3. **Speech-to-Text ekstra** — hvis voice-brug stiger
4. **Cloud Run** — hvis VPS skal erstattes
5. **Reserve** — gem ~$50 som buffer

---

## Opsummering: Top 10 APIs for Kris

| # | API | Hvorfor | Pris |
|---|-----|---------|------|
| 1 | **Routes API** | Ruteoptimering med waypoints | Gratis |
| 2 | **Cloud Text-to-Speech** | Voice-app taler dansk | Gratis |
| 3 | **Cloud Speech-to-Text** | Hands-free i bilen | Gratis |
| 4 | **Gemini API** | AI-hjerne bag alt | Gratis tier + credit |
| 5 | **Cloud Functions** | Automatisering uden server | Gratis |
| 6 | **Firebase Cloud Messaging** | Push notifications gratis | Gratis |
| 7 | **Google Calendar API** | Ruteplan i kalenderen | Gratis |
| 8 | **Google Drive API** | Backup og synkronisering | Gratis |
| 9 | **Cloud Vision API** | OCR af containere/adresser | Gratis |
| 10 | **Navigation SDK** | Turn-by-turn i egen app | Næsten gratis |

---

## Kilder

- [Google Cloud Free Tier](https://cloud.google.com/free)
- [Google Cloud Pricing List](https://cloud.google.com/pricing/list)
- [Google Maps Platform Pricing](https://mapsplatform.google.com/pricing/)
- [Maps Platform Core Services Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- [Navigation SDK Pricing](https://developers.google.com/maps/documentation/navigation/android-sdk/pricing)
- [Speech-to-Text Pricing](https://cloud.google.com/speech-to-text/pricing)
- [Text-to-Speech Pricing](https://cloud.google.com/text-to-speech/pricing)
- [Cloud Translation Pricing](https://cloud.google.com/translate/pricing)
- [Cloud Natural Language Pricing](https://cloud.google.com/natural-language/pricing)
- [Cloud Vision Pricing](https://cloud.google.com/vision/pricing)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Cloud Functions Pricing](https://cloud.google.com/functions/pricing-1stgen)
- [Firestore Pricing](https://firebase.google.com/pricing)
- [Document AI Pricing](https://cloud.google.com/document-ai/pricing)
- [Secret Manager Pricing](https://cloud.google.com/secret-manager/pricing)
- [Gemini API Free Tier Guide](https://www.aifreeapi.com/en/posts/gemini-api-free-quota)
- [Maps API Pricing Changes March 2025](https://www.storelocatorwidgets.com/blogpost/20499/New_Google_Maps_API_free_credit_system_from_March_1st_2025)
