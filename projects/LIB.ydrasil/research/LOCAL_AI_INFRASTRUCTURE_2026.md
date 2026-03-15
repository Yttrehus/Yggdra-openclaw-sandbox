# Deep Research: Lokal AI-infrastruktur — Fra OpenClaw til Miesslers Vision

**Dato:** 2026-02-02

---

## 1. Videoen: OpenClaw-advarslen

**Video:** [Nate B Jones — "What Nobody's Telling You About OpenClaw"](https://youtu.be/p9acrso71KU)

**OpenClaw** (tidl. Clawdbot/Moltbot) er en open-source AI-agent med 145.000+ GitHub-stars der kører lokalt og kan styre dit system, browse, sende beskeder via WhatsApp/Telegram etc.

**Nates advarsel:** Sikkerhedsforskere kalder det "basically AutoGPT with more access and worse consequences." Du giver en AI fuld systemadgang — passwords, databaser, alt.

**Relevans:** OpenClaw er præcis den type system Ydrasil bygger — men Ydrasil gør det smartere: kontrolleret, modulært, med specifik adgang via MCP-servere og dedikerede scripts.

---

## 2. Daniel Miesslers Vision: Personal AI Infrastructure (PAI)

### Filosofi
**Scaffolding > Model.** Det handler ikke om hvilken AI du bruger, men om systemet rundt om den. Kontekst-styring, custom skills og adfærdsregler er vigtigere end rå model-kapacitet.

### 7 arkitektur-komponenter
1. **Intelligence** — Model + scaffolding
2. **Context** — 3-lags hukommelse: hot/warm/cold
3. **Personality** — Kvantificerede personlighedstræk (0-100 skala)
4. **Tools** — Skills, integrationer, Fabric patterns
5. **Security** — Defense-in-depth med validering
6. **Orchestration** — Hook-system og agent-styring
7. **Interface** — CLI, voice, fremtidigt AR

### TELOS-systemet
10 filer der definerer brugeren: MISSION.md, GOALS.md, PROJECTS.md, BELIEFS.md, MODELS.md, STRATEGIES.md, NARRATIVES.md, LEARNED.md, CHALLENGES.md, IDEAS.md.

### Personal AI Maturity Model (PAIMM)

| Tier | Periode | Beskrivelse |
|------|---------|-------------|
| 1: Chatbots | Nov 2022 - Sent 2024 | Basal samtale, ingen hukommelse |
| **2: Agents** | Sent 2024 - Tidligt 2027 | **← Ydrasil er her** |
| 3: Assistants | Sent 2026+ | Proaktive ledsagere der arbejder mod dine mål |

### Lokal AI i PAI
Miesslers roadmap nævner eksplicit *"Local Model Support: Run PAI with local models (Ollama, llama.cpp)"* som kommende feature. Hans system kører i dag på Claude (cloud), men lokal support er planlagt.

---

## 3. Praktisk Vej: Cloud → Lokal

### Fase 1: NU (0-3 måneder, gratis/billigt)

**Installer Ollama på VPS'en:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3:mini
```

Brug til:
- Intent-klassificering i voice pipeline (erstatter cloud API)
- Embeddings (erstatter OpenAI embeddings)
- Simple Fabric patterns med lokal model

**Installer whisper.cpp (CPU-only):**
- tiny/base modeller kører fint på CPU
- Fjerner afhængighed af OpenAI Whisper API

**Implementer hybrid-routing:**
- Simpelt → lokalt (klassificering, embeddings)
- Komplekst → Claude API (kodning, ræsonnering)
- Besparelse: 30-70% færre API-kald

**Opret TELOS-filer** (Miessler-inspireret):
- MISSION.md, GOALS.md, PROJECTS.md i `/data/`

### Fase 2: 3-9 måneder (hardware-investering)

**Budget-build til lokal AI (~4.300 DKK):**

| Komponent | Specifikation | Pris (ca.) |
|-----------|---------------|------------|
| GPU | RTX 3060 12GB (brugt) | 1.500 DKK |
| CPU | AMD Ryzen 5 5600X | 800 DKK |
| RAM | 32GB DDR4 3200MHz | 600 DKK |
| Bundkort | B550 AM4 | 500 DKK |
| SSD | 512GB NVMe | 400 DKK |
| PSU | 650W 80+ Bronze | 500 DKK |
| **Total** | | **~4.300 DKK** |

Kan køre: 7B modeller (7-10 tok/sek), 13B med kvantisering, Whisper medium/large.

**Alternativ:** Mac Mini M4 24GB (~10.000 DKK) — kører 32B modeller, enklere, mere energieffektivt.

### Fase 3: 9-18 måneder (fuld lokal)

- RTX 3090/4090 (24GB VRAM) for 70B modeller
- Fuld PAI-framework lokalt
- 3-lags hukommelse (hot/warm/cold)
- Voice interface med lokal TTS
- Fuld uafhængighed fra cloud

---

## 4. VRAM-krav

| Model | Parametre | VRAM (4-bit) | CPU RAM | CPU-hastighed |
|-------|-----------|-------------|---------|---------------|
| Phi-3 Mini | 3.8B | 3GB | 8GB | Hurtigt |
| Gemma 2B | 2B | 2GB | 6GB | Hurtigt |
| Llama 3 8B | 8B | 5GB | 16GB | Langsomt |
| Mistral 7B | 7B | 5GB | 16GB | Langsomt |
| Llama 3 70B | 70B | 38GB | 64GB+ | Ubrugeligt |

**VPS'en kan køre Phi-3 Mini og Gemma 2B i dag uden GPU.**

---

## 5. Ærlig vurdering: Lokal vs. Cloud

### Fordele ved lokal
- Fuldt dataejerskab
- Ingen løbende API-omkostninger
- Offline-kapabelt
- Ingen leverandør-afhængighed

### Ulemper (vær ærlig)
- **Kvalitetsgab er reelt**: Selv 70B modeller når IKKE Claude Opus 4.5 i kodning/ræsonnering
- **Hardware koster**: 4.300-15.000 DKK + strøm
- **Vedligeholdelse**: Du opdaterer selv
- **Energi**: RTX 4090 bruger 450W under belastning
- **Støj**: Desktop-PC med GPU er ikke lydløs

### Den smarte strategi: Hybrid
Forskning viser **30x reduktion i cloud-omkostninger** mens **87-97% kvalitet bevares**:
1. **Lokalt**: Embeddings, klassificering, simple svar, Whisper, Qdrant
2. **Cloud**: Kompleks kodning, lang ræsonnering, critique/review
3. **Gradvis migration**: Flyt flere opgaver lokalt efterhånden som modeller forbedres

---

## 6. Ydrasil vs. OpenClaw vs. Miesslers PAI

| Aspekt | OpenClaw | Ydrasil | Miesslers PAI |
|--------|----------|---------|---------------|
| Arkitektur | Alt-i-en agent | Modulær (scripts + DB + webapp) | Modulært pack-system |
| Hukommelse | Simpel persistent | Qdrant vector DB | 3-tier (hot/warm/cold) |
| Sikkerhed | Kritiseret | Kontrolleret (specifikke scripts) | Defense-in-depth |
| Interface | Chat apps | Webapp + CLI + Voice | CLI + Voice + AR |
| Lokal/Cloud | Cloud API + lokal exec | Cloud API + lokal DB | Cloud (lokal planlagt) |

---

## 7. Næste skridt

1. **I dag**: `ollama pull phi3:mini` på VPS'en
2. **Denne uge**: Hybrid-routing i voice pipeline
3. **Denne måned**: TELOS-inspirerede kontekst-filer
4. **Når budget tillader**: Brugt RTX 3060 12GB → hjemmeserver

---

## Kilder

- [Nate B Jones — OpenClaw Warning](https://youtu.be/p9acrso71KU)
- [Daniel Miessler — Personal AI Infrastructure](https://danielmiessler.com/blog/personal-ai-infrastructure)
- [Daniel Miessler — PAIMM](https://danielmiessler.com/blog/personal-ai-future-state)
- [GitHub: Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [GitHub: Fabric](https://github.com/danielmiessler/Fabric)
- [GitHub: Ollama](https://github.com/ollama/ollama)
- [Running Fabric Locally with Ollama](https://knasmueller.net/running-fabric-locally-with-ollama)
- [2026 Local LLM Hardware Guide](https://medium.com/@jameshugo598/the-2026-local-llm-hardware-guide-surviving-the-ram-crisis-fa67e8c95804)
- [Build AI PC Specs 2026](https://techpurk.com/build-ai-pc-specs-2026-local-llms/)
- [Docker: Hybrid AI](https://www.docker.com/blog/hybrid-ai-and-how-it-runs-in-docker/)
- [Building Private Cloud for Local AI 2026](https://ifeeltech.com/blog/building-private-cloud-local-ai-hardware-guide-2026)
- [Gary Marcus on OpenClaw](https://garymarcus.substack.com/p/openclaw-aka-moltbot-is-everywhere)
- [CNBC: OpenClaw Rise](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html)
