# Broen Mellem Menneskehukommelse og AI-Hukommelse

**Forskningsrapport — 16. februar 2026**
**Kontekst:** Kris, lastbilchauffeur, 60-70 timer/uge, kun Android + Termux, voice-first workflow, Qdrant vector DB, Claude Code CLI.

---

## Indhold

1. [Problemformulering](#1-problemformulering)
2. ["Personal AI" systemer der husker dit liv](#2-personal-ai-systemer)
3. [Second Brain metodologier + AI-kobling](#3-second-brain-metodologier)
4. [Memory-augmented agents i praksis](#4-memory-augmented-agents)
5. [CLAUDE.md og kontekst-patterns](#5-claudemd-og-kontekst-patterns)
6. [Voice-first memory](#6-voice-first-memory)
7. [Lifelogging til AI-kontekst](#7-lifelogging-til-ai-kontekst)
8. [Syntese: Hvad virker for Kris?](#8-syntese)
9. [Implementeringsforslag](#9-implementeringsforslag)
10. [Kilder](#10-kilder)

---

## 1. Problemformulering

Kernesporgsmalet: Hvordan far man en AI til at kende et menneske lige sa godt som mennesket kender sig selv?

Det er et *bro-problem*. Pa den ene side er menneskets levede erfaring — fragmentarisk, emotionel, kontekstrig, fordelt over tid. Pa den anden side er AI'ens kontekstvindue — struktureret, tekstbaseret, sessionsbegroenset, men med perfekt genkaldelse inden for sit vindue.

Broen skal lose tre ting:
1. **Capture**: Fa viden fra Kris' hoved og hverdag ind i et system
2. **Structure**: Organiser det sa AI'en kan finde det
3. **Retrieve**: Lever det praecist nar det er relevant

Kris' saerlige begraninsninger:
- Ingen PC, kun Android telefon
- 60-70 timer i lastbil om ugen — handerne er optaget
- Voice er primaer input-modalitet
- Allerede har: Claude Code CLI, Qdrant, Python scripts, Telegram bridge
- Budget: Begroenset, men villig til at investere i det rigtige

---

## 2. "Personal AI" Systemer

### 2.1 Limitless (tidligere Rewind.ai)

**Hvad det er:** Startet som Rewind.ai i 2022 med lokal skaermoptagelse. Pivoterede i 2024 til Limitless Pendant — en diskret magnetisk disk der klippes pa tojet og optager samtaler kontinuerligt.

**Hvordan det virker:**
- 100 timers batteri (solid-state batteri)
- Optager alt du horer og siger
- Transkriberer og opsummerer automatisk
- Soegbar database over dit liv
- Meta har opkobt Limitless i 2025/2026

**Styrker:**
- "Put it on and forget it" — ingen aktiv indsats
- Perfekt til moeder og samtaler
- Soegbar hukommelse over hele dit liv

**Svagheder:**
- Primaert designet til kontormiljo/moeder, ikke lastbilkabine
- Closed-source, lukket oekosystem
- Meta-ejet nu — privatlivsbekymringer
- Koster $99-199 for pendant + abonnement
- Ingen API til at koble med Qdrant/Claude

**Implementerbarhed for Kris:** LAV. Lukket system, ingen API, fokuseret pa corporate meetings.

### 2.2 Omi (tidligere Tab)

**Hvad det er:** Open-source AI wearable. Lille rund enhed der baeres som halskaede. Konstant lytning, transkription, opsummering.

**Hvordan det virker:**
- $89 for forbrugerversion, ~$70 for developer kit
- 64GB lager, aluminium, let
- Koerer samtaler gennem GPT-4o
- Husker kontekst per bruger
- Open-source platform — kildekoden er pa GitHub (BasedHardware/omi)
- Gratis plan: 1.200 min cloud-transkription/maned + ubegroenset lokal transkription
- Aktiveres med "Hey Omi"

**Styrker:**
- OPEN SOURCE — kan tilpasses
- Billig ($89)
- Kontinuerlig kontekst-tracking
- Kan potentielt kobles til egne systemer via API
- Developer kit tilgaengelig

**Svagheder:**
- Afhaengig af telefonens Bluetooth-forbindelse
- Cloud-transkription krover internet
- GPT-4o lock-in (men open source = kan aendres)
- Stadig tidlig hardware — batteri og paalidelighed ukendt i praxis

**Implementerbarhed for Kris:** MEDIUM-HOJ. Open-source betyder at data kan routes til Qdrant. $89 er overkommeligt. Sporgsmalet er om Bluetooth + lastbilstoj fungerer i praksis.

### 2.3 Personal.ai

**Hvad det er:** Platform der bygger en "Personal Language Model" (PLM) baseret pa dine data. Modellen laerer din stil, dine meninger, dine fakta.

**Hvordan det virker:**
- Upload beskeder, dokumenter, integrationer
- Bygger "Memory Stacks" — sammenkoblede vidensnoder
- Kombinerer korttidshukommelse (aktive samtaler) og langtidshukommelse (alt du har uploaded)
- Chrome extension til at gemme webindhold
- PLM traener pa din Memory Stack og efterligner din udtryksform

**Styrker:**
- Troenet pa DIG — ikke generisk AI
- Memory Stacks er en elegant struktur
- Personaliseret output der lyder som dig

**Svagheder:**
- Enterprise-prissaetning, ikke transparent
- Lukket platform
- Ingen CLI, ingen Termux-integration
- Kraever PC/browser for uploading via Chrome extension
- Ingen voice-first workflow

**Implementerbarhed for Kris:** LAV. Kraever browser, er lukket, enterprise-prissat. Men konceptet "Memory Stacks" er vaerd at stjale.

### 2.4 Memories.ai / Project LUCI

**Hvad det er:** Privacy-first wearable pin vist pa CES 2026. On-device AI-processering.

**Hvordan det virker:**
- Lokal AI-indeksering og analyse
- Valgfri cloud-synkronisering kun for udvalgte minder
- End-to-end kryptering

**Styrker:** Privacy-first, on-device processering.
**Svagheder:** Ikke tilgaengelig endnu, lukket oekosystem.
**Implementerbarhed for Kris:** LAV — for tidligt, for lukket.

---

## 3. Second Brain Metodologier + AI-Kobling

### 3.1 PARA (Tiago Forte)

**Metoden:** Projects, Areas, Resources, Archive. Organiser alt digitalt indhold i 4 kategorier baseret pa *actionability*.

**AI-integration i 2025-2026:**
- Tiago Forte pivoterer officielt BASB til AI-first i 2026
- "Second Brain Enterprise" kohort laerer folk at koble PARA med AI
- Dokumentation der plejede at tage uger sker nu pa timer

**Styrker:**
- Velproevet system (400.000+ solgte boger)
- Handlingsorienteret — organiserer efter *hvad du vil gore*, ikke emne
- Let at forstaa

**Svagheder:**
- Designet til Notion/Evernote, ikke til CLI/terminal
- Kraever aktiv sortering — Kris har ikke tid til det
- AI-integrationen er stadig kohort-baseret, ikke selvstoendig vaerktoj

**Implementerbarhed for Kris:** MEDIUM. PARA-tankegangen er god (Projects > Areas > Resources > Archive), men Kris' system skal vaere voice-in med automatisk kategorisering. Den manuelle sortering er en showstopper.

### 3.2 Zettelkasten + AI

**Metoden:** Atomare noter med unikke ID'er, linket til hinanden. Viden vokser organisk som et netvaerk.

**AI-integration:**
- Obsidian + RAG pipeline: Scan markdown-filer → embeddings → vector database → sporg dine noter
- "Smart Second Brain" Obsidian-plugin: Chat med dine noter via RAG
- MOC-baseret RAG: Brug Map of Content noter til at lave fokuseret retrieval
- NER + Graph LLM: Automatisk entity-extraction og knowledge graphs fra noter

**Styrker:**
- Perfekt match med vector databases — atomare chunks er ideelle til embedding
- Linkstrukturen giver AI ekstra kontekst
- Skalerer uendeligt
- Obsidian vaults er bare markdown-filer — trivielt at embedde i Qdrant

**Svagheder:**
- Kraever at man SKRIVER noter — Kris taler
- Obsidian kraever grafisk interface (men filerne er bare .md)
- Aktiv linking-indsats

**Implementerbarhed for Kris:** HOJ — men kun hvis voice memos automatisk konverteres til atomare noter. Den raae Zettelkasten-metodik (link-baseret tankning) passer perfekt til Qdrant. Kris behover ikke Obsidian — bare markdown-filer + embeddings.

### 3.3 Johnny Decimal

**Metoden:** Alt fa et unikt numerisk ID (10-19 = Finans, 20-29 = Projekter osv.). Maks 10 omrader, maks 10 kategorier per omrade.

**AI-integration:**
- Johnny Decimal Architect: GPT der hjaelper med at designe systemet
- Kan kombineres med PARA (PARA for flow, JD for lokationer)

**Styrker:**
- Ekstremt simpelt
- Deterministisk — du VED altid hvor noget er
- God til filsystemer (som Kris' VPS)

**Svagheder:**
- Maks 100 kategorier er begraensende for et helt livs viden
- Primaert for filer, ikke for semantisk soegning
- AI behover ikke numeriske ID'er — den kan soege semantisk

**Implementerbarhed for Kris:** LAV for AI-hukommelse, men MEDIUM for mappestruktur pa VPS. Ydrasils mappestruktur (app/, data/, docs/, research/, scripts/) er allerede en slags JD-system.

### 3.4 Syntese: Hvad skal Kris tage fra Second Brain?

| Metode | Tag dette | Drop dette |
|--------|-----------|------------|
| PARA | Actionability-hierarkiet | Manuel sortering |
| Zettelkasten | Atomare noter + links | Kravet om at skrive |
| Johnny Decimal | Klar mappestruktur | Numerisk rigiditet |

**Den ideelle kombination:** Voice memo → automatisk transkription → atomare Zettelkasten-chunks → embeddet i Qdrant → organiseret med PARA-lignende metadata (project/area/resource/archive) → filer i en klar mappestruktur.

---

## 4. Memory-Augmented Agents i Praksis

### 4.1 Claude Code's Hukommelsessystem

**Tre lag af hukommelse:**

1. **CLAUDE.md (projekt-niveau):** Instruktioner, regler, kontekst der gaelder for hele projektet. Laeses ved hver session-start.

2. **MEMORY.md (bruger-niveau):** Globale bruger-preferencer i `~/.claude/projects/<project>/memory/MEMORY.md`. De forste 200 linjer indlaeses automatisk i system-prompten. Udover 200 linjer laeses IKKE automatisk — detaljerede noter skal i separate topic-filer.

3. **Auto-memory:** Claude skriver selv noter baseret pa hvad den opdager under sessioner. Gemmes i memory-mappen.

**Begraninsninger:**
- 200-linje graense for automatisk indlaesning
- Ingen semantisk soegning — kun flade tekstfiler
- Ingen persistens mellem sessions ud over CLAUDE.md og MEMORY.md
- Claude Code 2.1.0 (jan 2026) forbedrede 3x, men stadig ikke nok

### 4.2 Claude-Mem Plugin

**Hvad det er:** Tredjepartsudvidelse der automatisk capturer alt Claude goer, komprimerer det med AI, og injicerer relevant kontekst i fremtidige sessioner.

**Hvordan det virker:**
- Fanger hver tool-execution (fillaesning, skrivning, soegning)
- Komprimerer observationer til semantiske resumeer via Claude Agent SDK
- Gemmer alt i lokal SQLite database
- Fuld-tekst og vektor-soegning
- Genererer automatisk CLAUDE.md-filer med aktivitetstidslinjer
- Injicerer relevant kontekst ved session-start

**Styrker:**
- Automatisk — ingen indsats
- Lokal storage (SQLite)
- Baade fuld-tekst og vektor-soegning

**Svagheder:**
- Fokuseret pa *koding*, ikke personlig viden
- Fanger tool-brug, ikke voice memos eller livsbegivenheder
- Plugin-afhaengighed

**Implementerbarhed for Kris:** MEDIUM. Konceptet er godt (automatisk capture + kompression + injection), men Kris har brug for det udvidet til personlig viden, ikke kun kodningssessioner.

### 4.3 Mem0 — Universal Memory Layer

**Hvad det er:** Open-source memory layer for AI-applikationer. Y Combinator-backed, $24M funding i okt 2025.

**Hvordan det virker:**
- Dynamisk extraktion af vigtig information fra samtaler
- Tre storage-teknologier: Vector DB (semantisk soegning), Graph DB (relationer), Key-Value store (hurtig fact-retrieval)
- Virker med alle LLM-providers: OpenAI, Anthropic, Ollama
- Python og JS SDK
- Bruges af Netflix, Lemonade, Rocket Money

**Performance:**
- 91% lavere p95 latency end alternativer
- 90%+ token-besparelse
- arXiv paper: 2504.19413

**Styrker:**
- Open source
- Tre-lags arkitektur (vektor + graf + KV) er state-of-the-art
- Provider-agnostisk
- Skalerer til produktion
- Kan kobles med Qdrant som vector store

**Svagheder:**
- Kraever opsaetning af tre databaser for fuld funktionalitet
- Kompleksitet — overkill for enkeltperson?
- Ingen direkte voice-integration

**Implementerbarhed for Kris:** HOJ. Mem0 kan installeres pa VPS, bruge Qdrant som vector store (allerede korer), og give Claude Code et memory-lag der persisterer pa tvaers af sessions. Python SDK passer til eksisterende scripts.

### 4.4 Supermemory — Universal Memory API

**Hvad det er:** Memory API der bygger knowledge graphs fra dine data. Grundlagt af 19-arig, backed af Google-folk.

**Hvordan det virker:**
- Ingest fra URLs, PDF'er, tekst, filer, emails
- Automatisk chunking og rensning
- Multimodal data
- MCP-integration (Claude, Cursor osv.)
- Hybrid Search: blanding af memory og retrieval
- 10x hurtigere end Zep, 25x hurtigere end Mem0

**Styrker:**
- Ekstremt hurtigt
- MCP-integration ud af boksen
- Bredt input-format

**Svagheder:**
- Nyere projekt, mindre modent end Mem0
- Hosted service — data hos dem
- Self-hosting guide tilgaengelig men kraever mere arbejde

**Implementerbarhed for Kris:** MEDIUM. MCP-integrationen er interessant, men Kris har allerede Qdrant. Det vigtigste at laere er deres hybrid search-tilgang.

### 4.5 Anthropic's Officielle Memory Tool

Lanceret september 2025 som beta. Gemmer og genfinder information via en memory-filmappe der persisterer mellem sessions.

**Implementerbarhed for Kris:** HOJ — det er allerede det Kris bruger via MEMORY.md. Men det er tekstbaseret, ikke semantisk.

---

## 5. CLAUDE.md og Kontekst-Patterns

### 5.1 Hvad Power Users Goer

Baseret pa research af `steipete/agent-rules`, `AGENTS.md`-standarden, og community patterns:

**Tier 1: Basale patterns (Kris har allerede dette)**
- Projekt-CLAUDE.md med identitet, regler, mappestruktur
- MEMORY.md med laerte praeferencer
- Skills-filer for modular viden

**Tier 2: Avancerede patterns**
- **Kontekst-injection via scripts:** Kris' `ctx`-kommando soeger Qdrant og injicerer relevant kontekst. Dette er *bedre* end hvad de fleste power users goer.
- **Session logging:** Kris' 3-lags system (tmux → Qdrant → dagbog) er ekstremt sjaldent i community.
- **Skill-baseret routing:** Trigger-baseret auto-loading af skill-filer. Kris har dette.

**Tier 3: Det der mangler**
- **Personlig knowledge base:** Kris' Qdrant indeholder rutedata og sessionslogger, men ikke *personlig viden* — holdninger, praeferencer, livsbegivenheder, relationer, droemme, frustrationer.
- **Episodisk hukommelse:** Hvad skete der i tirsdags? Hvad sagde chefen? Hvordan folte Kris sig?
- **Semantisk soegning pa personlig kontekst:** `ctx` kan soege, men databasen mangler det personlige lag.

### 5.2 AGENTS.md Standarden

Lanceret juli 2025. Brugt af 60.000+ open-source projekter. Supported af Cursor, Codex, Gemini CLI, GitHub Copilot, VS Code.

**Relevans for Kris:** AGENTS.md er en superset af CLAUDE.md. Kris' eksisterende CLAUDE.md er allerede kompatibelt. Forskellen er at AGENTS.md har en Planner + Executor arkitektur — men det er primaert for kodning, ikke personlig AI.

### 5.3 Det Vigtigste Pattern: Kontekst-Lagdeling

```
Lag 1: System prompt (CLAUDE.md) — identitet, regler, struktur     [altid]
Lag 2: Memory (MEMORY.md) — laerte praeferencer, setup-detaljer      [altid, 200 linjer]
Lag 3: Skills (.claude/skills/) — moduler viden, on-demand            [triggered]
Lag 4: Retrieval (ctx/Qdrant) — dynamisk kontekst fra soegning       [on-demand]
Lag 5: Session — hvad der sker lige nu                                [ephemeral]
```

**Kris har lag 1-5 implementeret.** Det der mangler er at Lag 4 (Qdrant) indeholder *personlig* viden, ikke kun teknisk/rute-viden.

---

## 6. Voice-First Memory

### 6.1 Status for Voice-to-Knowledge i 2026

Stemme er ved at blive den primaere input-modalitet for viden-capture. I 2026 er fokus pa at goere voice-interaktioner kontekstbevidste med taet integration til eksisterende vidensystemer.

### 6.2 Whisper pa Android/Termux

**Det er muligt at koere Whisper lokalt pa Android via Termux:**

- `whisper.cpp` (C++) kan bygges i Termux
- `termux-whisper` wrapper: Let, privacy-fokuseret, offline transkription, batch-processing
- Kraever 2-4 GB fri RAM for storre modeller
- Kan bruge Termux's audio-optagelse direkte

**Workflow:**
```
Optag voice memo (Termux/app) → Whisper transkription (lokal) → Tekst
```

**Styrker:** Gratis, offline, privacy-first, ingen cloud.
**Svagheder:** Kraever RAM, langsommere end cloud, akkuratesse afhaenger af model-storrelse.

### 6.3 Cloud-baseret transkription

- **Groq Whisper API:** Gratis tier, ekstremt hurtig (allerede brugt i Kris' voice-app)
- **OpenAI Whisper API:** $0.006/minut
- **Google Speech-to-Text:** Gratis op til 60 min/maned

### 6.4 Den Komplette Voice-First Pipeline

```
1. CAPTURE:   Voice memo (Android app / Termux)
2. TRANSCRIBE: Groq Whisper API (gratis, hurtig) ELLER lokal whisper.cpp
3. PROCESS:   Claude API / lokal LLM extraherer:
               - Fakta og holdninger
               - Beslutninger og begrundelser
               - Humor og energi-niveau
               - Naevnte personer og relationer
               - Action items
4. STRUCTURE: Atomare noter i markdown-format
5. EMBED:     text-embedding-3-small → Qdrant
6. RETRIEVE:  ctx-kommando ved naeste Claude Code session
```

**Allerede implementeret hos Kris:** Trin 1-2 (voice-app → Groq transkription). Trin 5-6 (Qdrant + ctx). **Mangler: Trin 3-4** — den intelligente processering fra raatt transkript til struktureret viden.

---

## 7. Lifelogging til AI-Kontekst

### 7.1 Wearable-landskabet i 2026

| Enhed | Pris | Fokus | Open Source | API |
|-------|------|-------|-------------|-----|
| Limitless Pendant | $99-199 | Moeder | Nej | Nej (Meta-ejet) |
| Omi | $89 | Samtaler, produktivitet | Ja | Ja |
| Looki L1 | $199 | Visuel lifelogging | Nej | Ukendt |
| LUCI (Memories.ai) | TBA | Privacy-first minder | Nej | Nej |
| Plaud NotePin | $169 | Moeder/noter | Nej | Begraenset |

### 7.2 DIY Lifelogging med Android

For Kris er den mest realistiske tilgang:

**Passiv capture:**
- Automatisk voice memo-optagelse under korsel (tidstriggeret)
- Lokationsdata fra telefonen (rute-tracking allerede aktiv)
- Telegram-beskeder (allerede bridget)

**Aktiv capture:**
- Voice memos nar noget er vigtigt ("Hey, husk dette...")
- Foto af ting der skal huskes
- Kort tekst-noter via Telegram

**Automatisk processering:**
- Cron job pa VPS der processer nye voice memos
- Transkription → strukturering → embedding
- Daglig opsummering genereret automatisk

### 7.3 Fra Raadata til AI-Kontekst

Den kritiske transformation er:

```
RAADT:    "Ja, sa jeg snakkede med Lars i dag og han sagde at den
           nye rute pa Trjborg starter mandag, og sa tankte jeg
           at det maske var bedre at..."

STRUKTURERET:
  type: episodisk_hukommelse
  dato: 2026-02-16
  personer: [Lars, kollegaer]
  emne: ruteaendring
  fakta:
    - Ny rute pa Trjborg starter mandag
  holdninger:
    - Kris overvejer om aendringen er god
  action_items: []
  humeur: reflekterende
```

Denne transformation kraever et LLM-kald (Claude Haiku er billigt nok) og et godt prompt der ved hvad der skal extraheres.

---

## 8. Syntese: Hvad Virker for Kris?

### 8.1 Kris' Unikke Position

Kris er i en usadvanligt STAERK position sammenlignet med de fleste:

| Komponent | Status | Styrke |
|-----------|--------|--------|
| Vector DB (Qdrant) | Korer | Semantisk soegning klar |
| CLI AI (Claude Code) | Aktivt | Daglig brug |
| Retrieval (ctx) | Virker | On-demand kontekst-injection |
| Session logging | 3-lags | Automatisk |
| Voice capture | Voice-app | Groq transkription |
| Telegram bridge | Aktiv | Input/output kanal |
| VPS | Korer | Backend-processering |
| Kontekst-filer | CLAUDE.md + MEMORY.md + Skills | Komplet |

**Det der mangler er EN TING:** En pipeline der tager Kris' voice memos, Telegram-beskeder og daglige oplevelser og goer dem til *soegbar personlig viden* i Qdrant.

### 8.2 Hvad Kris IKKE Behover

- **Limitless/wearable hardware** — for dyrt og lukket for vaerdien
- **Personal.ai** — lukket platform, enterprise-prissat
- **Obsidian/Notion** — kraever PC og grafisk interface
- **Kompleks Mem0 3-database setup** — overkill for en person
- **AGENTS.md migration** — CLAUDE.md virker allerede fint

### 8.3 Hvad Kris BEHOVER

1. **Voice memo → struktureret viden pipeline** (Trin 3-4 fra afsnit 6.4)
2. **Personlig Qdrant-collection** separat fra teknisk/rute-data
3. **Daglig auto-processering** af nye inputs (voice, Telegram, sessioner)
4. **Episodisk hukommelse** — hvad skete der, hvem var der, hvordan folte du dig
5. **Semantisk soegning pa personligt lag** via ctx-kommandoen

---

## 9. Implementeringsforslag

### 9.1 Fase 1: Personal Memory Collection (1-2 timer)

**Opret ny Qdrant collection:**
```python
# "kris_personal" collection i Qdrant
# Felter: text, type (fact/opinion/episode/decision/relation),
#         date, people, topic, source (voice/telegram/session)
```

**Udvid ctx-kommandoen** til at soege i baade eksisterende og personlig collection.

### 9.2 Fase 2: Voice Memo Processing Pipeline (2-3 timer)

**Script:** `scripts/process_voice_memo.py`
```
Input:  Raat transkript fra voice memo
Output: Strukturerede chunks embeddet i kris_personal

Trin:
1. Modtag transkript (allerede fra Groq)
2. Claude Haiku-kald: "Extrahér fakta, holdninger, beslutninger,
   personer, humeur fra dette voice memo"
3. Generer atomare noter (Zettelkasten-stil)
4. Embed hver note i Qdrant med metadata
5. Log til daglig opsummering
```

**Pris:** ~$0.01-0.05 per voice memo (Haiku er billig).

### 9.3 Fase 3: Telegram Integration (1 time)

Kris' Telegram-beskeder proceseres allerede. Tilfoej:
- Automatisk embedding af daglige chat-logs i `kris_personal`
- Entity-extraction (personer, steder, beslutninger)
- Sentiment/humeur-tagging

### 9.4 Fase 4: Daglig Personal Digest (1 time)

**Cron job kl. 23:00:**
```
1. Saml alle nye personlige memories fra dagen
2. Generer "Dagens Overblik" — et kort resumé af hvad Kris oplevede
3. Embed overblick som episode-note
4. Opdater MORNING_BRIEF.md med personlig kontekst
```

### 9.5 Fase 5: Proaktiv Kontekst-Injection (avanceret)

Nar Claude Code starter en session:
1. Tjek dato/tid
2. Hent relevante personlige memories for idag og de seneste dage
3. Injicer i konteksten: "Kris naevnte i gar at han var traet af ruteaendringer..."

### 9.6 Samlet Arkitektur

```
                    CAPTURE LAG
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  Voice   │  │ Telegram │  │ Session  │
    │  Memos   │  │ Messages │  │  Logs    │
    └────┬─────┘  └────┬─────┘  └────┬─────┘
         │             │             │
         v             v             v
    ┌────────────────────────────────────┐
    │      PROCESSING LAG               │
    │  Groq Whisper → Claude Haiku      │
    │  Extrahér: fakta, holdninger,     │
    │  beslutninger, relationer, humeur │
    └──────────────┬─────────────────────┘
                   │
                   v
    ┌────────────────────────────────────┐
    │      STORAGE LAG                  │
    │  Qdrant: kris_personal collection │
    │  + Markdown filer som backup      │
    └──────────────┬─────────────────────┘
                   │
                   v
    ┌────────────────────────────────────┐
    │      RETRIEVAL LAG                │
    │  ctx "query" → semantisk soegning │
    │  → injiceret i Claude Code session│
    └────────────────────────────────────┘
```

### 9.7 Prisoversigt

| Komponent | Pris/maned | Note |
|-----------|-----------|------|
| Qdrant | $0 | Allerede koerende |
| Groq Whisper | $0 | Gratis tier |
| Claude Haiku processing | ~$1-3 | 50-100 memos/maned |
| OpenAI embeddings | ~$0.50 | text-embedding-3-small |
| VPS | $0 | Allerede betalt |
| **Total** | **~$2-4/maned** | |

### 9.8 Alternativ: Omi Hardware Tilfoejelse ($89 engangskob)

Hvis Kris vil have *passiv* capture uden at taenke over det:
- Kob Omi developer kit ($70)
- Fork open-source koden
- Route transkriptioner til VPS → Qdrant pipeline
- Fordel: Fanger samtaler Kris ikke ville have taenkt pa at optage
- Ulempe: Endnu en enhed at lade/baere

---

## 10. Kilder

### Personal AI Systemer
- [Limitless (Rewind.ai)](https://www.limitless.ai/) — AI memory pendant
- [Omi AI](https://www.omi.me/) — Open-source AI wearable, $89
- [Omi GitHub](https://github.com/BasedHardware/omi) — Open source kode
- [Personal.ai](https://www.personal.ai/memory) — Personal Language Model platform
- [Memories.ai Project LUCI](https://tech.david-cheong.com/memories-ai-luci-wearable-pin-ces2026/) — Privacy-first wearable
- [Limitless vs Bee vs Omi sammenligning](https://www.umevo.ai/blogs/ume-all-posts/limitless-vs-bee-vs-omi-the-wearable-ai-showdown)
- [Top 10 AI Assistants med Memory i 2026](https://www.dume.ai/blog/top-10-ai-assistants-with-memory-in-2026)
- [AI Wearables 2026](https://www.plaud.ai/blogs/articles/9-life-changing-ai-wearable-devices-in-2026)

### Second Brain Metodologier
- [Building a Second Brain](https://www.buildingasecondbrain.com/) — Tiago Forte
- [Tiago Fortes 2025 Annual Review](https://fortelabs.com/blog/tiago-fortes-2025-annual-review/) — BASB pivot til AI-first
- [Johnny Decimal System](https://johnnydecimal.com/) — Numerisk organisering
- [Zettelkasten + Obsidian + RAG](https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/)
- [Smart Second Brain Obsidian Plugin](https://www.obsidianstats.com/plugins/smart-second-brain)
- [RAG for Personal Knowledge Management](https://forum.obsidian.md/t/obsidian-rag-personal-ai-bot/93020)

### Memory-Augmented Agents
- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory) — Officiel dokumentation
- [Claude-Mem Plugin](https://github.com/thedotmack/claude-mem) — Persistent memory for Claude Code
- [Claude-Mem Dokumentation](https://docs.claude-mem.ai/introduction)
- [Mem0 — Universal Memory Layer](https://mem0.ai/) — Open source, Y Combinator
- [Mem0 GitHub](https://github.com/mem0ai/mem0) — Kildekode
- [Mem0 arXiv Paper](https://arxiv.org/abs/2504.19413) — Akademisk reference
- [Supermemory](https://supermemory.ai/) — Universal Memory API
- [Supermemory GitHub](https://github.com/supermemoryai/supermemory)
- [Mem0 vs Supermemory sammenligning](https://blog.logrocket.com/building-ai-apps-mem0-supermemory/)
- [Anthropic Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)

### Kontekst-Patterns
- [AGENTS.md Standard](https://agents.md/) — Aaben standard for AI coding agents
- [AGENTS.md GitHub](https://github.com/agentsmd/agents.md)
- [steipete/agent-rules](https://github.com/steipete/agent-rules) — Best practices samling
- [Persistent Memory for Claude Code Guide](https://agentnativedev.medium.com/persistent-memory-for-claude-code-never-lose-context-setup-guide-2cb6c7f92c58)
- [Claude Agent Context Engineering](https://binaryverseai.com/claude-agent-sdk-context-engineering-long-memory/)

### Voice-First Memory
- [Whisper pa Android/Termux](https://huggingface.co/blog/Javedalam/wwhisper-cli) — HuggingFace guide
- [termux-whisper](https://github.com/itsmuaaz/termux-whisper) — Privacy-fokuseret Whisper wrapper
- [FastKeyboard-Whisper til Termux](https://github.com/EddiGits/FastKeyboard-Whisper)
- [Whisper Notes App](https://whispernotes.app/whisper-app) — Local-first transkription

### Lifelogging
- [Looki L1 AI Wearable](https://www.looki.ai/looki-l1) — Proaktiv visuel capture
- [Meta koeber Limitless](https://www.allaboutai.com/ai-news/meta-just-bought-the-ai-memory-pendant-startup-limitless/) — Branchen konsoliderer
- [Wearable data + LLM agents](https://www.nature.com/articles/s41467-025-67922-y) — Nature Communications paper

---

## Konklusion

Kris har allerede 80% af infrastrukturen. Den manglende 20% er en **processing pipeline** der tager raae voice memos og daglige inputs og konverterer dem til struktureret, soegbar personlig viden i Qdrant.

Det er ikke et hardware-problem (ingen ny wearable noedvendig). Det er ikke et database-problem (Qdrant koerer allerede). Det er et **processing-problem**: et Python script + et godt prompt + en cron job.

Estimeret tid til minimum viable implementation: **4-6 timer**.
Estimeret loebende omkostning: **$2-4/maned**.

Resultatet: En AI der husker hvad Kris sagde i tirsdags, hvad han synes om ruteaendringer, hvem Lars er, og at Kris er traet om fredagen.
