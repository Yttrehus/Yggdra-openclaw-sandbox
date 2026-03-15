# Voice-First AI App — Project State

**Gemt:** 2026-02-11 kl. 20:25 CET
**Status:** Research fase — iteration 2 af planlægning

---

## Kris' Vision (komplet)

En voice-first AI-assistent fuldt integreret i hans Android-telefon:

1. **Voice chat** — tale ind → AI → tale ud, helt uden skærm, via Bluetooth headset i lastbil (10-15 timer/dag)
2. **Fil-håndtering** — send/modtag filer og billeder, fane der fungerer som Google Drive
3. **Telefon-integration via Tasker** — email (læs, sortér indbakke), kalender (læs, tilføj), Trello, generel telefon-kontrol via voice
4. **Skærm-læsning** — AI kan se hvad Kris ser (accessibility-baseret)
5. **TransportIntra tracking** — track alle outputs, filer, data som i webapp'en
6. **Observability** — maskinlog af ALT, watchdog der alerter ved stalls, post-mortem analyse
7. **Visualisering** — "nano banana pro" (skal researches) + dashboard
8. **Navigation** — truck-specifik routing (Google Maps er dårligt til lastbiler)

---

## Anbefalet Arkitektur: Alternativ D (Hybrid)

### App (simpel, custom):
- Voice recording → VPS (Groq Whisper STT) → Claude med Qdrant-kontekst → ElevenLabs TTS → afspil i headset
- Chat-fane (tekst + voice)
- Fil-fane (upload/download til VPS)
- Push notifications

### VPS Backend (eksisterende infra):
- FastAPI: audio → Groq Whisper → Claude API + Qdrant → ElevenLabs → audio retur
- Fil-storage endpoint
- Observability daemon (watchdog + maskinlog)

### Tasker (telefon-kontrol):
- Email: AutoNotification → HTTP POST til VPS → Claude sorterer
- Kalender: read/write
- Trello: HTTP API
- Trigger: Volume-knap hold 2 sek → start app

### Observability:
- Lag 1: Struktureret maskinlog (JSONL med timestamps, duration, cost per handling)
- Lag 2: Watchdog daemon (alert ved stalls >5 min, loops, fejl)
- Lag 3: Post-mortem analyse on-demand

---

## Research Resultater (færdige)

### Tasker + AI
- 350+ actions, HTTP requests til Claude API virker
- AutoInput læser skærm (men Android 15/Samsung problemer)
- AutoNotification fanger emails/kalender
- TTS via Bluetooth virker (Say action)
- Wake word: AutoVoice drainer batteri, Porcupine har IKKE dansk
- Pris: Tasker $4 + AutoApps $1.35/md
- POCC er mest ambitiøse eksisterende Tasker AI-projekt

### Eksisterende Voice Apps
- ChatGPT Plus ($20/md): bedst voice, ingen custom data, ingen wake word
- VoiceGPT: har wake word ("Hey Chat"), lav kvalitet, gratis
- SpeakGPT (open source): Kotlin, 25-30K linjer, custom API endpoints, Apache 2.0, aktivt vedligeholdt (jan 2026), INGEN fil-håndtering
- Pipecat: stærkeste framework (WebRTC), kræver mest byggetid
- Aimybox SDK: modulær voice assistant SDK, men slowing activity

### STT Priser
- Groq Whisper: $0.04/time (turbo), free tier = 8 timer/dag, dansk understøttet, 217x realtime speed
- OpenAI Whisper: $0.006/min ($0.36/time), dansk, 3-10 sek latency
- GPT-4o Mini Transcribe: $0.003/min ($0.18/time)

### TTS Priser
- OpenAI tts-1: $15/1M tegn, dansk DÅRLIG kvalitet
- ElevenLabs: fra $5/md (30K credits), dansk GOD kvalitet
- Google Cloud TTS: $4/1M tegn (WaveNet), dansk OK

### Wake Word
- Porcupine: IKKE dansk. Kun EN, FR, DE, IT, JA, KO, ZH, PT, ES
- AutoVoice continuous: drainer batteri
- **Bedste løsning: fysisk trigger** (volume-knap, BT headset-knap, NFC tag)

### Miessler
- Bruger ElevenLabs TTS til agent voice output
- HAR INGEN mobil løsning — alt er terminal
- PAIMM Tier 3: "Voice overtakes typing" — men har ikke bygget det selv
- Pris: ~$250/md (Claude $200 + ElevenLabs $20 + diverse)

---

## Red Team Resultater

| Problem | Alvorlighed | Mitigation |
|---------|-------------|------------|
| Ingen dansk wake word | Høj | Fysisk trigger (volume-knap) |
| Android 15 bryder Accessibility | Middel | Begrænset skærm-læsning, fokus på API-baseret kontrol |
| SpeakGPT fork er 25K linjer | Middel | Byg simpel app fra bunden i stedet (~5K linjer) |
| Lastbilstøj + voice recognition | Middel | Groq Whisper er robust, Samsung headset har noise cancellation |
| ElevenLabs dansk kvalitet | Lav | Test først, fallback til Google Cloud TTS |
| Tasker UX er klodset | Lav | Tasker kun til automation, ikke til primær chat |

---

## TODO — Næste Research Runde

1. [ ] **Google Cloud $300 credit** — hvad kan vi bruge dem til? Specielt:
   - Google Maps Directions API med vehicle restrictions (lastbil-navigation)
   - Google Cloud Speech-to-Text vs Groq Whisper
   - Google Cloud TTS vs ElevenLabs
   - Cloud Run for serverless endpoints
2. [ ] **"Nano banana pro"** — søg på nettet, visualiserings-device/tool?
3. [ ] **Truck-specifik navigation** — Google Maps API, HERE Maps, TomTom, Sygic Truck
4. [ ] **Tænk mere alternativt** — er der en helt anden tilgang vi ikke har overvejet?
5. [ ] **App-framework valg** — Kotlin native vs Flutter vs React Native for vores use case
6. [ ] **Observability implementering** — konkret design af maskinlog + watchdog

---

## Constraints

- Kris er i lastbil 10-15 timer/dag
- Android telefon + Samsung Bluetooth headset
- $300 Google Cloud credit (80 dage)
- VPS allerede kørende (Ubuntu, Docker, Qdrant, Claude Code)
- Kris er IKKE udvikler — appen skal bare virke
- Dansk sprog er primært

---

## Telegram Bridge Status (separat projekt)

- v3 kører, voice + tekst virker, 1:1 tmux spejling virker
- **Bugs stadig åbne:** duplikerede beskeder, besked-afkortning, 409 conflict (multiple bot instances)
- Bridge er midlertidig løsning mens vi bygger appen

---

## Lektioner Lært

1. **Gå ikke i gang med at bygge før planlægning er færdig** — Sonnet sprang til kode 3 gange
2. **Research FØR planlægning** — de fleste fejl skyldes manglende fakta
3. **Tidsbevidsthed** — tjek klokken, giv statusopdateringer, max 5 min per agent
4. **3 gange sad agenter fast i timevis** — sæt altid max_turns/timeout
5. **Front-load constraints** — "Porcupine har ikke dansk" ændrer hele planen
