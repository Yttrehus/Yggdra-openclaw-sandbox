# AI-Workflow Research: Personal Knowledge Management & Always-On Capture

**Dato:** 2026-02-02
**Status:** Afsluttet research
**Formaal:** Kortlaegning af state-of-the-art inden for personlige AI-systemer, always-on capture, og PKM-workflows

---

## Indholdsfortegnelse

1. [Daniel Miesslers Fabric & PAI](#1-daniel-miesslers-fabric--pai)
2. [AI Wearables & Pendants](#2-ai-wearables--pendants)
3. [Professionelle "Capture Everything"-Workflows](#3-professionelle-capture-everything-workflows)
4. [State of the Art Arkitekturer](#4-state-of-the-art-arkitekturer)
5. [Konkrete Vaerktoejer der Virker i Dag](#5-konkrete-vaerktoejer-der-virker-i-dag)
6. [Anbefalinger til Ydrasil](#6-anbefalinger-til-ydrasil)

---

## 1. Daniel Miesslers Fabric & PAI

### 1.1 Fabric Framework

**Kilde:** [GitHub - danielmiessler/fabric](https://github.com/danielmiessler/fabric) | [Fabric Origin Story](https://danielmiessler.com/blog/fabric-origin-story)

Fabric er et open-source framework (skrevet i Go) til at augmentere mennesker med AI. Det loeser "AI-integrationsproblemet" ved at tilbyde:

- **200+ Patterns** — Genanvendelige prompt-skabeloner til specifikke opgaver (opsummering, analyse, ekstraktion osv.)
- **25+ AI-udbydere** — Unified interface til OpenAI, Anthropic, Gemini, Ollama, Azure, AWS Bedrock m.fl.
- **CLI-first** — Kommandolinje-baseret, kan pipes sammen med andre vaerktoejer
- **Pattern-specifik model-routing** — "Brug GPT-4 til analyse, Claude til skrivning"

**Seneste opdateringer (2025-2026):**
- v1.4.380 (jan 2026): Microsoft 365 Copilot-integration
- v1.4.356 (dec 2025): Fuld i18n-support (10 sprog)
- v1.4.350 (dec 2025): Swagger/OpenAPI dokumentation
- v1.4.334 (nov 2025): Claude Opus 4.5 support
- v1.4.203 (jun 2025): Amazon Bedrock support

**Vigtig skelnen:** Fabric handler om *hvad* man spoerger AI om (patterns/prompts). PAI handler om *hvordan* ens digitale assistent opererer (infrastruktur).

### 1.2 Personal AI Infrastructure (PAI)

**Kilde:** [PAI Blog Post](https://danielmiessler.com/blog/personal-ai-infrastructure) | [GitHub - PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure) | [Cognitive Revolution Podcast](https://www.cognitiverevolution.ai/pioneering-pai-how-daniel-miessler-s-personal-ai-infrastructure-activates-human-agency-creativity/)

PAI er Miesslers fulde agentic AI-platform. Hans digitale assistent hedder **Kai**.

#### Arkitektur: 7 Lag

| Lag | Funktion |
|-----|----------|
| **Intelligence** | Model + scaffolding (context management, Skills, Hooks, AI Steering Rules) |
| **Context** | Alt systemet ved om brugeren, 3 memory-tiers |
| **Personality** | Kvantificerede traits (0-100 skala) der former tone og adfaerd |
| **Tools** | Skills, MCP-integrationer, Fabric patterns (200+) |
| **Security** | Defense-in-depth: settings, constitutional rules, validation, code patterns |
| **Orchestration** | Hook-system (17 hooks paa 7 lifecycle events) |
| **Interface** | CLI-first, voice notifications, terminal management |

#### Memory System (3 Tiers)

- **Tier 1 — Session Memory:** Claude Codes native `projects/` med 30-dages transcript retention
- **Tier 2 — Work Memory:** Strukturerede directories til aktive projekter (META.yaml, ISC.json, items/, agents/, research/, verification/)
- **Tier 3 — Learning Memory:** Akkumuleret visdom organiseret per maaned, algoritme-forbedringer, failures, syntetiserede moenstre. Inkluderer SIGNALS-system med 3.540+ ratings

#### Signal Capture System

- **Eksplicitte ratings:** "8" eller "3 - det var forkert" — fanges af ExplicitRatingCapture hook
- **Implicit sentiment:** Emotionel toneanalyse via ImplicitSentimentCapture hook
- **Failure captures:** Lave ratings (1-3) trigger fuld kontekst-bevaring

#### Skills System

**67 Skills** med **333 workflows** total. Hver skill har:
```
SKILL.md     (hvornaar/hvorfor)
Workflows/   (trin-for-trin procedurer)
Tools/       (CLI-scripts til deterministiske opgaver)
```

#### Tech Stack

| Komponent | Vaerktoej |
|-----------|-----------|
| Platform | Claude Code (Anthropic) |
| Orchestration | GitHub (Issues, Actions, TASKLIST.md) |
| Digital Employees | MoltBot (PAI-enabled autonome agenter) |
| Voice | ElevenLabs |
| Integrationer | MCP (Model Context Protocol) servers |
| Patterns | Fabric (200+ specialiserede prompts) |
| Life logging | **Limitless Pendant** |
| Content curation | Threshold (AI-powered content app) |

#### Miesslers AI Maturity Model (PAIMM)

**Kilde:** [Personal AI Maturity Model](https://danielmiessler.com/blog/personal-ai-maturity-model)

| Level | Navn | Periode | Beskrivelse |
|-------|------|---------|-------------|
| 0 | Natural | Pre-2022 | Ingen AI |
| 1 | Chatbots | 2023-2025 | ChatGPT/Claude ad hoc |
| 2 | Agentic | 2025-2027 | AI-agenter med tools, APIs, handlinger |
| 3 | Orchestrated | 2027+ | Fuld DA-orkestrering af dagligdag |

Miessler opererer paa Level 2 med Kai. Hans vision: Alle virksomheder vil levere APIs designet til vores Digital Assistants — ikke til os direkte.

### 1.3 Miesslers Limitless Pendant-Setup

**Kilde:** [UL Newsletter #473](https://newsletter.danielmiessler.com/p/ul-473)

Miessler kalder Limitless Pendant "the best AI hardware accessory I've used so far." Han bruger det til:
- Altid-paa optagelse af samtaler og moedenoter
- Real-time synkroniseret transskription
- Fuld API-adgang til samtaledata
- Let at slukke for sensitive samtaler
- Integreret i hans PAI som life-logging komponent

---

## 2. AI Wearables & Pendants

### 2.1 Overblik over Markedet

**Kilder:** [TechCrunch Hottest AI Wearables](https://techcrunch.com/2025/11/21/the-hottest-ai-wearables-and-gadgets-you-can-buy-right-now/) | [IkigaiTeck AI Wearables](https://www.ikigaiteck.io/ai-wearables-the-6-most-interesting-devices-bee-friend-limitless-omi-plaud-notepin-and-rabbit-r1) | [UMEVO Showdown](https://www.umevo.ai/blogs/ume-all-posts/limitless-vs-bee-vs-omi-the-wearable-ai-showdown)

| Device | Pris | Batteri | Fokus | API |
|--------|------|---------|-------|-----|
| **Limitless Pendant** | ~$300 | 6-7 timer | Produktivitet, moedenoter | Ja |
| **Plaud NotePin** | $169 | 20 timer | Professionel notat-tagning | Via app |
| **Plaud NotePin S** | ~$169 | 20 timer | Nyere, mere wearable design | Via app |
| **Omi** | $89 | Variabel | Eksperimentel, open-source-venlig | Ja |
| **Bee** | $49.99 | Variabel | Budget, daglig capture | Via app |
| **Friend** | $129 | Variabel | Social/emotionel companion | Begraenset |

### 2.2 Limitless Pendant (Anbefalet)

**Kilde:** [Limitless.ai](https://www.limitless.ai/) | [Amazon](https://www.amazon.com/Limitless-AI-Pendant-Transcription-Weatherproof/dp/B0FLMHBVT4) | [Real-World Review](https://thoughts.jock.pl/p/voice-ai-hardware-limitless-pendant-real-world-review-automation-experiments) | [Marketplace.org](https://www.marketplace.org/story/2025/10/23/whats-it-like-to-use-wearable-ai-tech)

**Styrker:**
- Bedste software-integration i kategorien
- Koerer i baggrunden paa Mac/Windows og fanger system-audio (Zoom/Teams)
- Synkroniserer fysiske optagelser med digitale moedenoter
- Speaker identification (20 sekunders voice training)
- Developer API til struktureret samtaledata
- Understøtter GPT-5, Claude, Gemini som AI-backend
- IP54 vandresistent
- 8 farvevalg

**Svaghed:**
- Forveksler til tider talere
- UI/software "catching up" ift. hardware
- Abonnement nødvendigt for fuld AI-funktionalitet
- Score: ~7.8/10 fra uafhængig reviewer

**VIGTIG NYHED:** Meta opkoebte Limitless i december 2025 ([TechCrunch](https://techcrunch.com/2025/12/05/meta-acquires-ai-device-startup-limitless/)). Limitless siger de deler Metas vision om "personal superintelligence to everyone" og vil hjaelpe med at bygge AI-enabled wearables.

### 2.3 Plaud NotePin / NotePin S

**Kilde:** [Plaud.ai](https://www.plaud.ai/products/plaud-notepin) | [Plaud NotePin S](https://www.plaud.ai/products/plaud-notepin-s) | [Gadgeteer Review](https://the-gadgeteer.com/2025/04/09/plaud-notepin-review-ai-wearable-note-taker/)

**Styrker:**
- 20 timers kontinuerlig optagelse (langt bedste batteri)
- 64 GB lokal storage
- 40 dages standby
- Kun 0.59 oz / 0.61 oz
- Baeres som magnetisk pin, clip, armbånd eller halskæde
- GDPR-compliant
- Gratis starter-plan (300 min/måned transskription)

**Svaghed:**
- Kræver Plaud-app til AI-features
- Mindre avanceret software end Limitless
- Abonnement for fuld funktionalitet

### 2.4 Omi

**Kilde:** [Omi.me](https://www.omi.me/) | [Product Hunt](https://www.producthunt.com/products/open-source-ai-necklace-friend)

- $89, open-source-venlig
- Lytter kontinuerligt, koerer samtaler gennem ChatGPT
- Husker kontekst fra hele dagen
- Kan baeres som halskæde eller klæbes paa med medicinsk tape
- Mere eksperimentel/DIY end de andre

### 2.5 Bee

**Kilde:** [IkigaiTeck](https://ikigaiteck.com/pages/ai-wearables-bee-friend-limitless-omi-plaud-notepin-and-rabbit-r1)

- $49.99 — billigste option
- Clip eller armbånd
- Fungerer som ekstern hukommelse
- Automatiske påmindelser og daglige opsummeringer
- God til folk der skifter meget mellem samtaler

### 2.6 Friend

**Kilde:** [TechBuzz Review](https://www.techbuzz.ai/articles/friend-ai-necklace-review-the-129-wearable-that-bullies-you) | [SF Standard Profile](https://sfstandard.com/2025/11/16/avi-schiffmann-friend-ai-pendant-loneliness-profile/)

- $129, hvid pendant
- Fokus paa emotionel companion, IKKE produktivitet
- Google Gemini 2.5 integration
- Blandede anmeldelser — "eavesdrops constantly and somehow manages to bully its own users"
- **Ikke anbefalet til professionelt brug**

### 2.7 Privacy-Overvejelser

Privacy er den stoerste barriere for adoption. Europaeiske aktorer taenker privacy som kerneforretning. Det vil tage lang tid foer always-on recording bliver socialt acceptabelt. Hvid indikator-LED paa Limitless kan ikke slukkes (kun dimmes).

---

## 3. Professionelle "Capture Everything"-Workflows

### 3.1 Daniel Miesslers Tilgang (Level 2 Agentic)

Se sektion 1. Miessler har det mest avancerede offentligt dokumenterede personlige AI-system. Kerneprincip: **"System architecture matters more than which model you use."**

Hans daglige workflow:
- Limitless Pendant fanger alt mundtligt
- Fabric patterns behandler input
- PAI/Kai orkestrerer via Claude Code + MCP
- 3.540+ signal-datapunkter informerer systemets adfaerd
- 3.000+ blogindlaeg og 500+ nyhedsbreve indekseret via RAG med Cloudflare Workers + vector database
- Newsletter-opsummering fra 3.000+ kilder automatiseret

### 3.2 Tiago Fortes Second Brain + AI

**Kilde:** [Building a Second Brain](https://buildingasecondbrain.com/) | [Forte Labs Blog](https://fortelabs.com/blog/tiagos-2025-projects-questions-and-intentions/)

**CODE-framework:**
1. **Capture** — Indsaml ideer fra alle kilder
2. **Organize** — Sorter med PARA-systemet (Projects, Areas, Resources, Archive)
3. **Distill** — Ekstraher essensen
4. **Express** — Brug viden til at skabe

**AI-integration (2025-2026):**
- AI automatiserer nu Distill og Organize faserne
- Capture forbliver menneskelig — AI kan ikke vide hvad der er strategisk relevant for dig
- "Second Brain Enterprise" program med AI-integration
- Ny bog "Life in Perspective" kommer efteraar 2026
- AI commoditiserer indhold — vaerdien skifter fra "listicle content" til dybere indsigter
- Forte bruger primaert Notion som platform

**Kritik i AI-eraen:** Metoden afhaenger af brugerens evne til at stille de rigtige spoergsmaal ("Favorite Questions"). I en verden hvor AI kan besvare naesten alt, ligger den reelle konkurrencefordel i kvaliteten af prompts og klarheden af vision.

### 3.3 August Bradleys PPV Life Design

**Kilde:** [Notion Life Design](https://www.notionlifedesign.com/) | [YearZero.io](https://www.yearzero.io/)

- **Pillars, Pipelines & Vaults (PPV)** — Life Operating System i Notion
- Nu med custom-traenede AI coaches (Life & Business Coach + Notion Coach)
- Traenet paa alt PPV-indhold, August essays, og community-diskussioner
- PPV Version 2.0 med forbedret automatisering
- "DuoCycles" — ny tilgang til review-cycles der erstatter monthly/quarterly reviews
- 6+ aars raffinement, 35k+ nyhedsbrev-abonnenter

### 3.4 Justin Johnsons "Seneca" System

**Kilde:** [RunDataRun - Unlocking Your Second Brain](https://rundatarun.io/p/unlocking-your-second-brain)

Custom RAG-powered Second Brain:
- **Obsidian** som bedrock (lokal, filbaseret, privat)
- **Custom RAG API** — lokalt hostet Python API
- **LlamaIndex** til at laese Markdown, skabe embeddings
- **ChromaDB** som lokal vector database
- Fuld privacy, ingen cloud-afhaengighed

### 3.5 Khoj — Open-Source AI Second Brain

**Kilde:** [GitHub - khoj-ai/khoj](https://github.com/khoj-ai/khoj)

- Self-hostable AI second brain
- Svar fra web eller egne dokumenter
- Custom agents, schedulerede automationer, deep research
- Understøtter alle store LLMs (GPT, Claude, Gemini, Llama, Qwen, Mistral)
- Gratis og open-source

### 3.6 OmniVault (Qdrant Hackathon Vinder)

- Indekserer lokale filer og web-browsing
- Multimodal semantisk soegning
- Chrome-extension der highlighter og scroller til fundet tekst
- Stack: Qdrant + Redis + CLIP + Ollama
- Lokal-first, privacy-preserving

---

## 4. State of the Art Arkitekturer

### 4.1 Agentic RAG (Dominant Paradigme 2025-2026)

**Kilde:** [LangWatch RAG Blueprint](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026) | [AIFire RAG Project Blueprint](https://www.aifire.co/p/the-2025-26-rag-project-blueprint-for-a-standout-ai-career)

I stedet for simpel "soeg → returner → svar" giver man en agent tools og et loop. Agenten beslutter selv:
- Hvilken type soegning den vil lave
- Hvilke API-kald den skal foretage
- Gentager i et loop indtil bedste svar er fundet

**Multi-agent approaches:** Flere agenter koerer parallelt, soeger i forskellige systemer, en aggregator analyserer og opsummerer.

### 4.2 MCP (Model Context Protocol)

**Kilde:** [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol) | [MCP Documentation](https://modelcontextprotocol.io/) | [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)

MCP er den nye standard for AI-tool-integration:
- Loeser N*M problemet (5 modeller x 5 datakilder = 25 integrationer → 1 per kilde)
- Doneret til Linux Foundation i dec 2025 (OpenAI og Block som medstiftere)
- 5.000+ community MCP-servere
- Understøttet af Claude, Gemini, Cursor, Replit, VS Code, GitHub Copilot
- **2026:** MCP UI Framework + multimodal support (billeder, video, audio)

### 4.3 Voice-First Agentic Architecture

**Kilde:** [Voice AI Primer](https://voiceaiandvoiceagents.com/) | [ElevenLabs 11ai](https://elevenlabs.io/blog/introducing-11ai)

Moderne voice-first pipeline:
```
Mikrofon/Pendant → STT (Speech-to-Text) → LLM Reasoning → TTS (Text-to-Speech) → Handling
                                            ↓
                                     Tool Execution via MCP
                                            ↓
                                     Memory/Vector DB Update
```

- Speech-to-Speech modeller eliminerer separat STT/TTS
- Sub-300ms latency er opnaaelig (Deepgram)
- ElevenLabs 11ai: Voice-first personal assistant med MCP-integration

### 4.4 Typisk Self-Hosted PKM-Arkitektur

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPTURE LAG                               │
│  Limitless Pendant / Plaud NotePin / Mikrofon                │
│  Browser Extension / Obsidian / Manual Input                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  PROCESSING LAG                              │
│  Whisper/Deepgram (STT) → Chunking → Embedding              │
│  Fabric Patterns (opsummering, ekstraktion)                  │
│  LlamaIndex/LangChain (orchestration)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   STORAGE LAG                                │
│  Qdrant / ChromaDB / Weaviate (vector DB)                    │
│  Obsidian / Markdown files (human-readable)                  │
│  SQLite / PostgreSQL (metadata, relationer)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  RETRIEVAL LAG                                │
│  Semantisk soegning via Qdrant                               │
│  MCP Server til AI-adgang                                    │
│  Agentic RAG (multi-step reasoning)                          │
│  CLI / Web UI / Voice Interface                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Konkrete Vaerktoejer der Virker i Dag

### 5.1 Transskription

**Kilde:** [AssemblyAI Comparison](https://www.assemblyai.com/blog/best-api-models-for-real-time-speech-recognition-and-transcription) | [Deepgram vs Whisper Benchmark](https://research.aimultiple.com/speech-to-text/) | [Northflank STT Benchmarks](https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2026-benchmarks)

| Vaerktoej | Type | Pris | Latency | Bedst til |
|-----------|------|------|---------|-----------|
| **GPT-4o-transcribe** | API | ~$0.006/min | ~500ms | Hoejeste accuracy |
| **Deepgram Nova-3** | API | $0.0043/min | <300ms | Real-time, lav latency |
| **AssemblyAI Universal-2** | API | ~$0.0025/min | ~400ms | Audio intelligence features |
| **faster-whisper** | Self-hosted | GPU-cost | Variabel | Privacy, GDPR, kontrol |
| **WhisperX** | Self-hosted | GPU-cost | Variabel | Word-level timestamps, diarization |

**Anbefaling for self-hosting:** faster-whisper paa CPU er muligt men langsomt. GPU (selv en lille) giver markant bedre performance.

### 5.2 Vector Databases

| Database | Sprog | Self-host | Cloud | Saerligt |
|----------|-------|-----------|-------|----------|
| **Qdrant** | Rust | Docker | Qdrant Cloud | MCP server, FastEmbed, Edge support |
| **ChromaDB** | Python | Ja | Nej | Simpelt, godt til prototyper |
| **Weaviate** | Go | Docker | Weaviate Cloud | Multimodal, GraphQL |
| **Pinecone** | - | Nej | Kun cloud | Managed, skalerbart |
| **FAISS** | C++/Python | Ja | Nej | Meta, hurtigst til similarity search |

**Qdrant MCP Server:** [mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) — bruger FastEmbed (sentence-transformers/all-MiniLM-L6-v2) som default, Apache 2.0 licens.

### 5.3 Orchestration Frameworks

**Kilde:** [RAG Frameworks 2026](https://research.aimultiple.com/rag-frameworks/) | [Firecrawl Best RAG Frameworks](https://www.firecrawl.dev/blog/best-open-source-rag-frameworks)

| Framework | Fokus | Overhead | Bedst til |
|-----------|-------|----------|-----------|
| **LlamaIndex** | Data & retrieval | ~6ms | RAG over dokumenter, knowledge bases |
| **LangChain** | General orchestration | ~10ms | Multi-tool agents, komplekse workflows |
| **LangGraph** | Graph-baseret orchestration | ~14ms | Stateful agents, cykliske workflows |
| **Haystack** | Production RAG | ~5.9ms | Skalerbare pipelines |
| **DSPy** | Signature-first | ~3.5ms | Minimal boilerplate, akademisk |
| **Dify** | Low-code RAG | - | Hurtig prototyping, UI |

**Praksis:** Start med LlamaIndex for RAG. Tilfoej LangChain/LangGraph naar kompleksiteten vokser.

### 5.4 Embedding Modeller

| Model | Dimensioner | Brug |
|-------|-------------|------|
| **all-MiniLM-L6-v2** | 384 | Default i Qdrant FastEmbed, hurtig |
| **text-embedding-3-small** | 1536 | OpenAI, god balance |
| **text-embedding-3-large** | 3072 | OpenAI, hoejeste kvalitet |
| **nomic-embed-text** | 768 | Open-source, god til Ollama |
| **CLIP** | 512/768 | Multimodal (tekst + billeder) |

### 5.5 LLM Platforms

| Platform | Brug i PKM |
|----------|------------|
| **Claude Code** | Miesslers primaere platform for PAI/Kai |
| **Ollama** | Lokal LLM-koersel (Llama, Qwen, Mistral) |
| **OpenAI API** | GPT-4o, GPT-4o-transcribe |
| **Anthropic API** | Claude Opus 4.5, Sonnet |

### 5.6 Andre Relevante Vaerktoejer

| Vaerktoej | Funktion |
|-----------|----------|
| **Obsidian** | Lokal markdown-baseret PKM |
| **Fabric** | 200+ AI prompt patterns (CLI) |
| **Khoj** | Open-source AI second brain |
| **Otter.ai** | Moede-transskription (cloud) |
| **Notion** | Struktureret PKM (August Bradley's PPV) |
| **Threshold** | AI-powered content curation (Miessler) |
| **ElevenLabs** | Voice synthesis + 11ai assistant |

---

## 6. Anbefalinger til Ydrasil

### 6.1 Hvad Vi Allerede Har

Ydrasil har allerede en solid grundstruktur der matcher state-of-the-art:
- **Qdrant vector database** (koerer paa localhost:6333)
- **Python embedding scripts**
- **Cron-baseret automatisering** (daglig backup, auto-dagbog, hourly embedding)
- **tmux pipe-pane capture** (session logging)
- **Markdown-baseret vidensbase** (docs/, data/)

### 6.2 Lavskaels Forbedringer (Kan Goeres Nu)

1. **Installer Fabric** — `go install github.com/danielmiessler/fabric@latest`
   - Brug patterns til at behandle rutedata, samtaler, dagboegsindlaeg
   - Pattern-eksempler: `extract_wisdom`, `summarize`, `create_action_items`

2. **MCP Server til Qdrant** — Installer mcp-server-qdrant
   - Giver Claude Code direkte semantisk soegning i vores vidensbase
   - Erstatter/supplerer `ctx`-kommandoen

3. **Forbedret Embedding Pipeline**
   - Tilfoej chunking-strategi (overlap chunks for bedre retrieval)
   - Overvej at skifte til nomic-embed-text for bedre kvalitet

### 6.3 Medium-Skaels Forbedringer

4. **Limitless Pendant eller Plaud NotePin**
   - Limitless: Bedre software, API, men Meta-opkoeb skaber usikkerhed (~$300)
   - Plaud NotePin: 20 timers batteri, billigere ($169), GDPR-compliant
   - Begge giver hands-free capture af mundtlige noter under ruten

5. **Voice-to-Qdrant Pipeline**
   - Pendant/telefon optager → Whisper/Deepgram transskriberer → Embedding → Qdrant
   - Automatiseret via cron eller webhook

6. **PAI-inspireret Skills System**
   - Vi har allerede `.claude/skills/` — udvid med Miesslers struktur:
   - SKILL.md + Workflows/ + Tools/ per skill
   - Signal capture (ratings) for kontinuerlig forbedring

### 6.4 Stoerre Vision

7. **Fuld Agentic RAG**
   - Multi-step reasoning over rutedata, kundehistorik, dagboeg
   - Agent der kan svare: "Hvilke kunder har haft problemer de sidste 3 mdr?"

8. **MCP-integration med eksterne systemer**
   - TransportIntra data via MCP
   - Kalender-integration
   - SMS/besked-integration for ruteaendringer

### 6.5 Prioriteret Raekkefoelge

| Prioritet | Handling | Indsats | Vaerdi |
|-----------|----------|---------|--------|
| 1 | MCP Server til Qdrant | Lav | Hoej |
| 2 | Installer Fabric | Lav | Medium |
| 3 | Forbedret chunking i embedding pipeline | Medium | Hoej |
| 4 | Plaud NotePin til rute-capture | Lav (koeb) | Hoej |
| 5 | Voice-to-Qdrant pipeline | Medium | Hoej |
| 6 | PAI-inspireret Skills-struktur | Medium | Medium |
| 7 | Fuld Agentic RAG | Hoej | Hoej |

---

## Kilder

### Daniel Miessler / Fabric / PAI
- [Fabric GitHub](https://github.com/danielmiessler/Fabric)
- [PAI GitHub](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [PAI Blog Post (Dec 2025)](https://danielmiessler.com/blog/personal-ai-infrastructure)
- [Fabric Origin Story](https://danielmiessler.com/blog/fabric-origin-story)
- [Personal AI Maturity Model](https://danielmiessler.com/blog/personal-ai-maturity-model)
- [Cognitive Revolution Podcast](https://www.cognitiverevolution.ai/pioneering-pai-how-daniel-miessler-s-personal-ai-infrastructure-activates-human-agency-creativity/)
- [Semgrep Webinar](https://semgrep.dev/events/building-your-personal-ai-infrastructure-with-daniel-miessler/)
- [Fabric DeepWiki](https://deepwiki.com/danielmiessler/fabric)

### AI Wearables
- [Limitless.ai](https://www.limitless.ai/)
- [Limitless Amazon](https://www.amazon.com/Limitless-AI-Pendant-Transcription-Weatherproof/dp/B0FLMHBVT4)
- [Limitless Real-World Review](https://thoughts.jock.pl/p/voice-ai-hardware-limitless-pendant-real-world-review-automation-experiments)
- [Meta Acquires Limitless (TechCrunch)](https://techcrunch.com/2025/12/05/meta-acquires-ai-device-startup-limitless/)
- [Limitless In-Depth Review (Skywork)](https://skywork.ai/skypage/en/Limitless-AI-An-In-Depth-Review-and-Analysis/1976154402840047616)
- [Marketplace.org AI Wearable Experience](https://www.marketplace.org/story/2025/10/23/whats-it-like-to-use-wearable-ai-tech)
- [Plaud NotePin](https://www.plaud.ai/products/plaud-notepin)
- [Plaud NotePin S](https://www.plaud.ai/products/plaud-notepin-s)
- [Plaud NotePin Review (Gadgeteer)](https://the-gadgeteer.com/2025/04/09/plaud-notepin-review-ai-wearable-note-taker/)
- [Omi.me](https://www.omi.me/)
- [Friend AI Review](https://www.techbuzz.ai/articles/friend-ai-necklace-review-the-129-wearable-that-bullies-you)
- [IkigaiTeck AI Wearables Overview](https://www.ikigaiteck.io/ai-wearables-the-6-most-interesting-devices-bee-friend-limitless-omi-plaud-notepin-and-rabbit-r1)
- [TechCrunch Hottest AI Wearables](https://techcrunch.com/2025/11/21/the-hottest-ai-wearables-and-gadgets-you-can-buy-right-now/)
- [Living On Record (Substack)](https://ekavc.substack.com/p/living-on-record-my-first-ten-days)

### PKM & Workflows
- [Building a Second Brain](https://buildingasecondbrain.com/)
- [Tiago Forte 2025 Annual Review](https://fortelabs.com/blog/tiagos-2025-projects-questions-and-intentions/)
- [August Bradley Notion Life Design](https://www.notionlifedesign.com/)
- [August Bradley YearZero](https://www.yearzero.io/)
- [Khoj AI Second Brain](https://github.com/khoj-ai/khoj)
- [Decoding ML Second Brain Course](https://github.com/decodingai-magazine/second-brain-ai-assistant-course)
- [RunDataRun Seneca System](https://rundatarun.io/p/unlocking-your-second-brain)
- [Radiant App Second Brain Tools](https://radiantapp.com/blog/best-second-brain-apps)

### Arkitektur & Frameworks
- [LangWatch RAG Blueprint 2025-2026](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)
- [RAG Frameworks Comparison 2026](https://research.aimultiple.com/rag-frameworks/)
- [Firecrawl Best Open-Source RAG Frameworks 2026](https://www.firecrawl.dev/blog/best-open-source-rag-frameworks)
- [LLM Orchestration 2026](https://research.aimultiple.com/llm-orchestration/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Voice AI Primer](https://voiceaiandvoiceagents.com/)
- [ElevenLabs 11ai](https://elevenlabs.io/blog/introducing-11ai)

### Transcription
- [AssemblyAI Real-Time STT Comparison](https://www.assemblyai.com/blog/best-api-models-for-real-time-speech-recognition-and-transcription)
- [Deepgram vs Whisper Benchmark](https://research.aimultiple.com/speech-to-text/)
- [Open-Source STT Benchmarks 2026](https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2026-benchmarks)
- [Whisper Self-Hosting Guide](https://rackdiff.com/en/blog/whisper-self-hosting-guide)
- [Voice Writer API Comparison](https://voicewriter.io/blog/best-speech-recognition-api-2025)

### Vector Databases
- [Qdrant Documentation](https://qdrant.tech/documentation/overview/)
- [Qdrant MCP Server](https://www.kdjingpai.com/en/mcp-server-qdrant/)
- [Top 10 Open-Source Vector Databases](https://medium.com/@techlatest.net/from-milvus-to-qdrant-the-ultimate-guide-to-the-top-10-open-source-vector-databases-7d2805ed8970)
