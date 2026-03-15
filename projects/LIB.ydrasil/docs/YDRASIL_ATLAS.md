# Ydrasil Atlas

**Formål:** Komplet overblik over alt i Ydrasil — projekter, struktur, viden, principper, handlinger. Bygget som fundament for visuelle maps (mindmaps, brainmaps).

**Oprettet:** 17. februar 2026
**Senest opdateret:** 17. februar 2026

---

## Sådan læses dette dokument

Hver note har:
- **Beskrivelse** — hvad det er og hvorfor det eksisterer
- **Tags** — krydsreferencer til andre noter (format: `→ KATEGORI/UNDERKATEGORI`)
- **Status** — `aktiv`, `planlagt`, `deaktiveret`, `vision`

Tags viser relationer på tværs af kategorier. Når to noder deler et tag, er de forbundne — uanset hvor de bor i hierarkiet.

---

# 1. PROJEKTER
> *Alt med et formål, en plan og et ønsket resultat.*

## 1.1 Ydrasil (meta-projekt)
**Hvad:** AI-augmentation af Kris' liv — fra arbejde til personlig udvikling. Ikke ét system, men en filosofi: kortlæg friktion → forestil ideal → byg broen.

**Mål:** Bevise at én person med AI kan bygge systemer der normalt kræver et team. Proof of concept → skalerbar metode → del med andre.

**Status:** `aktiv` — kernen fungerer, bygges ud dagligt.

**Tags:** `→ PRINCIPPER/Friktion`, `→ PRINCIPPER/Karl-Popper`, `→ VIDEN/Advisor-brain`, `→ STRUKTUR/Infrastruktur`

---

### 1.1.1 TransportIntra
**Hvad:** Webapp-klon af TransportIntra (Kris' firmas rutesystem). Løser kerneproblem: stop-sortering nulstilles ugentligt, koster timer at sortere manuelt.

**Baggrund:** Kickstarteren for hele Ydrasil. Startet december 2025 med n8n, migreret til direkte API-kald + webapp-klon.

**Funktioner (eksisterende):**
- Login via TransportIntra API
- Rute-visning (256 stops med adresser, GPS, sortering)
- Stop-sortering (drag & drop + profiler)
- Tidsregistrering
- Vægt-tracker (sessionRecorder)
- Google Maps integration
- Extra route overlay
- Natmode
- Distance service + arrival predictor

**Mål:** App alle skraldemænd ville elske. Permanent sortering, bedre UX end originalen.

**Status:** `aktiv` — fungerer, redesign i gang (v2 wireframes live).

**Tags:** `→ STRUKTUR/Webapp`, `→ STRUKTUR/API`, `→ HANDLINGER/Redesign`, `→ VIDEN/Rutedata`, `→ PRINCIPPER/80-20`

**Filer:** `app/`, `data/TRANSPORTINTRA_API_REFERENCE.md`, `docs/TRANSPORTINTRA_REDESIGN.md`

---

### 1.1.2 Personal AI (PAI)
**Hvad:** Kris' personlige AI-assistent — en forlængelse af ham selv, ikke et værktøj. Inspireret af Jarvis (Iron Man), TARS (Interstellar), Kai (Miessler).

**Baggrund:** Kris' vision fra dag ét (ChatGPT samtale #20, Grok "Orca"). Gradvist realiseret via Claude Code + Qdrant + automatisering.

**Funktioner (eksisterende):**
- Kontekst-søgning (Qdrant, 11.249+ chunks)
- Rådgivning via internaliserede frameworks (Nate Jones + Miessler)
- Voice memo pipeline (tale → transskription → handling)
- Morning brief (daglig)
- Auto-dagbog (daglig)
- Session logging + embedding
- Research pipeline (arXiv, OpenAlex, Semantic Scholar)
- Telegram bridge

**Mål:** AI integreret i identitet (Human 3.0). Aldrig behøve skærm — tale ind, systemet handler.

**Status:** `aktiv` — kernen fungerer, voice routing mangler.

**Tags:** `→ PRINCIPPER/Human-3.0`, `→ STRUKTUR/Hukommelse`, `→ STRUKTUR/Workflows`, `→ VIDEN/Advisor-brain`, `→ HANDLINGER/Voice-routing`

---

### 1.1.3 Bogfører / Financial Advisor
**Hvad:** AI-hjælp til regnskab, Excel, fakturering, økonomisk overblik.

**Baggrund:** Nævnt i Grok "YttreAI Build Planner" og ChatGPT samtaler. Kris arbejder 60 timer/uge med 800k+ indkomst — vil have smartere styring.

**Funktioner (planlagt):**
- Excel-integration
- Fakturering
- Udgiftsoverblik
- Skatteoptimering

**Status:** `vision` — ikke påbegyndt.

**Tags:** `→ HANDLINGER/Integrationer`, `→ PRINCIPPER/ROI`

---

### 1.1.4 Rejseagent
**Hvad:** AI til rejseplanlægning — itinerary-generering, booking-hjælp, transportlogistik.

**Baggrund:** Kris har erfaring som rejseguide. ChatGPT #34 (Itinerary summary), Grok "MCP Uses for Travel Agencies". Cape Town-rejse planlagt feb 2026 (data/inbox/).

**Status:** `planlagt` — har været brugt ad hoc (Cape Town), ikke systematiseret.

**Tags:** `→ HANDLINGER/Integrationer`, `→ VIDEN/Rejser`

---

### 1.1.5 Kompendium ("Brugsanvisning til Kris")
**Hvad:** 10-kapitel manual — alt hvad Kris har lært om AI, destilleret til praktisk brug.

**Baggrund:** Aftalt 15. feb. "The AI Practitioner's Bible" — Claudes "tredje hjerne" (judgment=Nate, purpose=Miessler, capability=denne bog).

**Sprog:** Engelsk (kap 1-2 skrives om fra dansk i polish-fase).

**Kerneprincipper for bogen:**
- Insight > reference
- "When NOT to use X" > feature-lister
- Limitations, decision frameworks, "Our Setup" grounding
- Red-team efter hvert kapitel

**Status:** `aktiv` — kap 1-6 eksisterer i varierende kvalitet.

**Tags:** `→ VIDEN/Advisor-brain`, `→ PRINCIPPER/Alle`, `→ HANDLINGER/Skrivning`

**Filer:** Se `book_writing.md` i memory

---

### 1.1.6 Mindmap / Brainmap
**Hvad:** Interaktiv visuelt vidensnetværk — relationer mellem projekter, viden, principper, handlinger.

**Baggrund:** Diskuteret intensivt 15.-16. feb. Kris' vision: "4-dimensionel brainmap" hvor noder har farve/form efter type (princip vs. struktur vs. viden), og tags forbinder på tværs.

**Status:** `aktiv` — v2 mindmap bygget (app/mindmap/), dette dokument er fundamentet for næste version.

**Tags:** `→ STRUKTUR/Alle`, `→ VIDEN/Alle`, `→ PRINCIPPER/Alle`

**Filer:** `app/mindmap/`, `data/mindmaps/`

---

### 1.1.7 Andre idéer (fra chat-analyser)

**Stemmestyring af telefon:** Kris vil give stemmekommandoer der styrer apps. (ChatGPT #32, #15, Grok "Alternatives to Google Assistant")
**Status:** `vision`

**Politisk platform:** Dissekere bureaukrati, afsløre spild af skattekroner. Samme metode som software: kortlæg → ideal → fjern friktion. (MISSION.md)
**Status:** `vision` — "Store drømme. Starter i fundamentet."

**Egen AI-model:** Kris' drøm om at bygge sin egen model. (ChatGPT #20, Claude #5)
**Status:** `vision` — ikke realistisk endnu, men motiverer retning.

---

# 2. STRUKTUR / ARKITEKTUR
> *Hvordan tingene er bygget. Filer, funktioner, processer, infrastruktur.*

## 2.1 Infrastruktur
**Hvad:** VPS (Ubuntu, Hostinger), Docker containers, Nginx reverse proxy, SSL.

**Komponenter:**
| Komponent | Port | Formål |
|-----------|------|--------|
| Webapp (Nginx) | 3000 | TransportIntra klon |
| Mock server | 3001 | Test-data |
| SecondBrain API | 3002 | Qdrant search endpoint |
| Qdrant | 6333 | Vektordatabase |
| Tor | 9150/9151 | Proxy for YouTube scraping |

**Adgang:** `ssh root@72.62.61.51`, webapp: `https://app.srv1181537.hstgr.cloud`

**Status:** `aktiv`

**Tags:** `→ PROJEKTER/TransportIntra`, `→ PROJEKTER/PAI`, `→ PRINCIPPER/Sikkerhed`

**Filer:** `.claude/skills/infrastructure/`, `docker-compose.yml`

---

## 2.2 Filstruktur
**Hvad:** Hvordan Ydrasil-repoen er organiseret.

```
/root/Ydrasil/
├── app/                  # Webapp (produktion via volume mount)
│   ├── index.html        # Hoved-app (jQuery Mobile)
│   ├── css/tiApp.css     # Styling
│   ├── js/               # Ruter.js, featurePanel.js, sortProfiles.js
│   ├── mindmap/          # Mindmap-app (flere versioner)
│   └── redesign/         # Redesign wireframes
├── brain/                # Intent + memory + retrieval
│   ├── intent/           # MISSION, PRIORITIES, CORE_INTENT, TRADEOFFS
│   └── memory/
│       ├── working/      # CURRENT_FOCUS, FOCUS
│       └── semantic/     # projects/, personal/, system/, pai/
├── data/                 # Rå data
│   ├── inbox/            # Voice memos, uploads fra telefon
│   ├── exports/          # ChatGPT/Grok/Claude analyser
│   ├── research/         # Akademisk research (JSON + MD)
│   ├── nate_jones/       # Bog + transcripts
│   ├── miessler_bible/   # Bog + blog posts
│   └── mindmaps/         # Mindmap data
├── docs/                 # Etableret viden
│   ├── DAGBOG.md         # Automatisk dagbog
│   ├── SESSION_LOG.md    # Session historik
│   └── TELOS.md          # Kris' kerneværdier
├── research/             # Igangværende undersøgelser
├── scripts/              # Python automation (34 scripts)
├── .claude/
│   ├── skills/           # 6 skills (advisor, data-analysis, etc.)
│   └── commands/         # Slash commands
├── CLAUDE.md             # Hovedinstruktioner
└── archive/              # Overstået materiale
```

**Status:** `aktiv`

**Tags:** `→ PRINCIPPER/Simplicitet`, `→ STRUKTUR/Hukommelse`

---

## 2.3 Hukommelse (Memory Architecture)
**Hvad:** Hvordan Claude husker ting mellem og inden for sessioner.

### Lag 1: Kortidshukommelse (session)
- **Samtalehistorik** — alt i denne session
- **Aktuel opgave** — hvad arbejder vi på
- **Modificerede filer** — hvad er ændret
- **Kontekstvindue** — ~200K tokens, komprimeres automatisk

### Lag 2: Mellemlang hukommelse (persistent filer)
- **MEMORY.md** (`~/.claude/projects/.../memory/MEMORY.md`) — auto-loaded, max 200 linjer
- **NOW.md** (`data/NOW.md`) — session checkpoint, gemt ved compaction
- **CLAUDE.md** — instruktioner, frameworks, session-noter

### Lag 3: Langtidshukommelse (Qdrant vektordatabase)
- **advisor_brain** — 11.249 chunks (Nate Jones + Miessler)
- **routes** — rutedata med hybrid search
- **conversations** — tidligere samtaler
- **docs** — dokumenter og research

### Lag 4: Arkiv (filer på disk)
- **DAGBOG.md** — auto-genereret daglig
- **SESSION_LOG.md** — manuel session historik
- **brain/** — intent, decisions, playbooks
- **data/exports/** — fulde chat-analyser

### Processer
| Proces | Trigger | Hvad den gør |
|--------|---------|--------------|
| Compaction | Auto (kontekstvindue fyldt) | Komprimerer samtale, gemmer checkpoint til NOW.md |
| Session embedding | Hver 4. time (cron) | Embedder session-logs til Qdrant |
| Auto-dagbog | 23:55 dagligt (cron) | Genererer dagbogsindlæg |
| Videns-scoring | Hver time :15 (cron) | Scorer 400 chunks i Qdrant |
| Advisor re-embedding | Søndag 05:00 (cron) | Re-embedder hele advisor brain |

**Status:** `aktiv` — 75% retrieval hit rate, kan forbedres.

**Tags:** `→ PROJEKTER/PAI`, `→ VIDEN/Alle`, `→ PRINCIPPER/Log-everything`, `→ HANDLINGER/Hukommelses-research`

---

## 2.4 Automatiske Workflows (Cron)
**Hvad:** Alt der kører uden Kris' intervention.

| Job | Tidspunkt | Script | Status |
|-----|-----------|--------|--------|
| Morning brief | 07:00 dagligt | `morning_brief.py` | `aktiv` |
| Session log | Hver 4. time | `process_session_log.py` | `aktiv` |
| Videns-scoring | Hver time :15 | `score_knowledge_batch.py` | `aktiv` |
| Huskeliste scanner | Hver time :30 | `huskeliste_scanner.py` | `aktiv` |
| Auto-dagbog | 23:55 dagligt | `auto_dagbog.py` | `aktiv` |
| Backup | 04:00 dagligt | `backup_offsite.sh` | `aktiv` |
| Advisor embedding | Søndag 05:00 | `embed_advisor_brain.py` | `aktiv` |
| Docs embedding | Søndag 05:00 | `embed_docs.py` | `aktiv` |
| System audit | Søndag 06:00 | `weekly_audit.py` | `aktiv` |
| tmux logging | Hver time | pipe-pane rotation | `aktiv` |
| Navigator | 06:00 dagligt | `navigator.py` | `deaktiveret` |
| YouTube monitor | 07:00 dagligt | `youtube_monitor.py` | `deaktiveret` |
| Source discovery | 08:00 søndag | `source_discovery.py` | `deaktiveret` |

**Tags:** `→ PROJEKTER/PAI`, `→ PRINCIPPER/Automation`, `→ STRUKTUR/Hukommelse`

---

## 2.5 Manuelle Workflows & Scripts
**Hvad:** Scripts Kris eller Claude kører manuelt.

| Script | Formål | Trigger |
|--------|--------|---------|
| `get_context.py` | Qdrant søgning (`ctx` command) | Kris spørger noget |
| `research.py` | Akademisk søgning (arXiv, OpenAlex) | Research-opgave |
| `voice_memo_pipeline.py` | Transskribér voice memo | Upload til inbox |
| `voice_pipeline.py` | Whisper → Fabric → routing | Voice input |
| `telegram_bridge.py` | Telegram ↔ Claude Code | Telegram besked |
| `save_checkpoint.py` | Gem session checkpoint | Pre-compaction hook |
| `webapp_server.py` | Mock TransportIntra API | Test |
| `eval_retrieval.py` | Test retrieval kvalitet | Debugging |
| `cost_guardian.py` | Overvåg API-forbrug | Manuel check |

**Tags:** `→ PROJEKTER/PAI`, `→ STRUKTUR/Infrastruktur`

---

## 2.6 Skills & Commands
**Hvad:** Modulære vidensfiler Claude loader ved relevante spørgsmål.

| Skill | Trigger | Indhold |
|-------|---------|---------|
| `route-lookup` | Ruter, stops, adresser | TransportIntra API, sortering, rutedata |
| `webapp-dev` | Webapp, UI, CSS, JS | jQuery Mobile, app-arkitektur, CSS patterns |
| `infrastructure` | Docker, servere, SSL | Docker-compose, nginx, cron, systemd |
| `data-analysis` | Analyse, statistik | Qdrant queries, YouTube, data-mønstre |
| `advisor` | Beslutninger, strategi | Frameworks, Nate Jones, Miessler |
| `integrations` | Gmail, Drive, Trello | OAuth, API-kald, token management |

**Slash commands:**
- `/context` — hent Qdrant kontekst
- `/audit` — kør systemtjek

**Tags:** `→ PROJEKTER/PAI`, `→ STRUKTUR/Hukommelse`

---

## 2.7 Webapp-arkitektur
**Hvad:** Hvordan TransportIntra-klonen er bygget.

**Stack:** jQuery Mobile 1.4.5, vanilla JavaScript, Google Maps API, Firebase Messaging

**Sider:** loginPage, menuPage, listePage, ruteOversigt, ruteFullListPage, tidsRegPage, message, receipt, chat, settings, extraRoutePage

**17 features** (fra featurePanel.js):
- *Kort & Navigation:* GPS tracking, Google Maps, Distance Service, Arrival Predictor, Navigator
- *Vægt & Registrering:* Weight Tracker, Session Recorder, Tidsregistrering
- *UI & System:* Natmode, Feature Panel, Sortering, Profiler, Extra Route, Offline Support

**API:** Multipart POST til `webapp.transportintra.dk/srvr/index4.0.php`. Alle string-values JSON-quoted.

**Status:** `aktiv` — redesign wireframes i `app/redesign/`

**Tags:** `→ PROJEKTER/TransportIntra`, `→ HANDLINGER/Redesign`

---

# 3. VIDEN
> *Alt hvad vi ved. Research, ekspert-viden, data om Kris, rutedata.*

## 3.1 Advisor Brain (Nate Jones + Daniel Miessler)
**Hvad:** 11.249 embeddings i Qdrant fra to primære kilder. Fundamentet for al rådgivning.

### Nate Jones
- **Kilde:** Bog + 100+ YouTube transcripts
- **Kernekoncepter:** Ladder of AI Solutions, Builder vs Consumer, Scaffolding > Models, Taste som bottleneck, Intent Gap, Context Engineering
- **Søg:** `ctx "QUERY" --advisor --author nate`

### Daniel Miessler
- **Kilde:** Bog + 3000+ blog posts (danielmiessler.com)
- **Kernekoncepter:** AIMM (5 niveauer), Human 1.0/2.0/3.0, Job vs Gym, Meaning Loops, PAI, Context > Capability, Fabric
- **Søg:** `ctx "QUERY" --advisor --author miessler`

**Status:** `aktiv` — re-embeddes ugentligt, 75% hit rate.

**Tags:** `→ PRINCIPPER/Alle`, `→ PROJEKTER/PAI`, `→ PROJEKTER/Kompendium`

**Filer:** `data/nate_jones/`, `data/miessler_bible/`

---

## 3.2 Viden om Kris
**Hvad:** Personlighed, præferencer, historie, mål — samlet fra TELOS + 180+ samtaler (ChatGPT, Grok, Claude).

### Personligt
- 36 år, bor alene, renovationschauffør (Rute 256), 800k+/år, 60 timer/uge
- Perfektionist, ROI-bevidst, praktisk anlagt
- Kerneværdi: Sandhed > komfort
- Frygt → Mod → Sandhed → Kærlighed

### Familie
- Se `brain/memory/semantic/personal/family.md`

### Sundhed
- Se `brain/memory/semantic/personal/health.md`

### Politiske holdninger
- Stærke meninger om skat, bureaukrati, woke-kultur
- Flat tax, Karl Popper, videnskabelig metode
- 6 ChatGPT samtaler + 12 Grok samtaler om politik

### AI-rejse (tidslinje)
- **Sep 2024:** Første ChatGPT test (LOTR, film)
- **Nov 2025:** Eksplosion — Grok, 16.869 beskeder på én måned
- **Dec 2025:** TransportIntra-automation, ChatGPT 28 samtaler, Claude Code
- **Jan 2026:** Skift til Claude som primær, Ydrasil-systemet tager form
- **Feb 2026:** PAI-arkitektur, voice pipeline, Qdrant, mindmaps

**Status:** `aktiv`

**Tags:** `→ PROJEKTER/PAI`, `→ PRINCIPPER/Sandhed`, `→ STRUKTUR/Hukommelse`

**Filer:** `brain/memory/semantic/personal/`, `data/exports/*/ANALYSIS.md`, `docs/TELOS.md`

---

## 3.3 Rutedata
**Hvad:** Rute 256 (organisk affald, Aarhus) — stops, adresser, GPS-koordinater, sortering.

**Rute-IDs:** Man=231, Tir=232, Ons=228, Tor=233, Fre=234

**Kerneproblem:** `sorter: 0` = usorteret. Nulstilles ugentligt af TransportIntra. Kris bruger timer på at sortere manuelt.

**Data i Qdrant:** `routes` collection med hybrid search (dense + BM25).

**Sorteringsark:** `Sheets/256 ORG2ÅRH.xlsx` (17 tabs, alle dage).

**Status:** `aktiv`

**Tags:** `→ PROJEKTER/TransportIntra`, `→ HANDLINGER/Sortering-test`

---

## 3.4 Akademisk Research
**Hvad:** Forskningsartikler hentet via `scripts/research.py`.

**Emner:**
| Emne | Fil | Tags |
|------|-----|------|
| AI long-term memory | `research/ai_memory_research.md` | `→ STRUKTUR/Hukommelse` |
| Human memory (chunking, spaced repetition) | `research/human_memory_research.md` | `→ STRUKTUR/Hukommelse` |
| Memory bridge (AI ↔ human) | `research/memory_bridge_research.md` | `→ STRUKTUR/Hukommelse` |
| Visual design principles | `data/research/visual_design_research.md` | `→ HANDLINGER/Redesign` |
| RAG & retrieval | `data/research/context-aware_retrieval*.json` | `→ STRUKTUR/Hukommelse` |
| Prompt engineering for images | `data/research/prompt_engineering*.json` | `→ HANDLINGER/Nano-Banana-Pro` |
| Infographic design | `data/research/infographic_design*.json` | `→ HANDLINGER/Visualisering` |

**Status:** `aktiv` — vokser løbende.

**Tags:** `→ PROJEKTER/PAI`, `→ PROJEKTER/Kompendium`

---

## 3.5 Chat-historik Analyser
**Hvad:** Komplette analyser af Kris' samtaler med tre AI-platforme.

| Platform | Samtaler | Beskeder | Periode | Fil |
|----------|----------|----------|---------|-----|
| ChatGPT | 44 | 2.818 | Sep 2024 – Jan 2026 | `data/exports/chatgpt/ANALYSIS.md` |
| Grok | 118 | 19.562 | Sep 2025 – Feb 2026 | `data/exports/grok/ANALYSIS.md` |
| Claude (app) | 28 | 2.232 | Dec 2025 – Feb 2026 | `data/exports/claude_app/ANALYSIS.md` |

**Brug:** Find tidligere idéer, projekter, beslutninger. Kris har sagt mange ting i gamle chats der stadig er relevante.

**Status:** `aktiv`

**Tags:** `→ VIDEN/Om-Kris`, `→ PROJEKTER/Alle`

---

# 4. PRINCIPPER & VÆRDIER
> *Hvordan vi tænker og beslutter. Regler der gælder på tværs af alt.*

## 4.1 Kerneværdier
| Værdi | Beskrivelse | Kilde |
|-------|-------------|-------|
| **Sandhed** | Ingen løgne, ingen smiger, ingen falsk komfort. AI der smigrer er en løgner. | TELOS |
| **Simplicitet** | Præcis den kompleksitet der kræves — hverken mere eller mindre. | Kris + audit |
| **ROI-bevidsthed** | Tid er uerstattelig. Automatisér alt der kan automatiseres. | TELOS P4 |
| **Verificerbarhed** | Test at ting virker før du siger de virker. "Burde virke" = unacceptable. | CORE_INTENT |
| **Data-integritet** | Kris' data må aldrig korrupteres, mixes eller mistes. | PRIORITIES Tier 0 |

**Tags:** `→ PROJEKTER/Alle`, `→ STRUKTUR/Alle`, `→ HANDLINGER/Alle`

---

## 4.2 Designprincipper
| Princip | Regel | Eksempel |
|---------|-------|----------|
| **Funktion > perfektion** | Ship når det virker, perfektionér senere. | Voice pipeline v1 logger bare |
| **80/20** | Implementér de 20% features der bruges 80% af tiden. | Sortering (dagligt) > ruteplanlægning (aldrig) |
| **Karl Popper** | Byg op → bryd ned → bevar kun essentielle. Antag altid der er en bedre måde. | Iterativ forbedring |
| **Markdown > databaser** | For det meste. Nemmere at læse, versionere, debugge. | brain/ er markdown, ikke SQL |
| **Ingen frameworks** | LangChain, LlamaIndex = for komplekse. Direct API calls. | OpenAI SDK + Qdrant client direkte |
| **Cron > orchestration** | Python scripts + cron > Airflow/Dagster. | 10 aktive cron jobs |

**Tags:** `→ STRUKTUR/Alle`, `→ PRINCIPPER/Simplicitet`, `→ PRINCIPPER/Karl-Popper`

---

## 4.3 Internaliserede Frameworks
| Framework | Kilde | Kerneidé |
|-----------|-------|----------|
| **Rumelt Strategy** | Nate Jones | Diagnosis → Guiding Policy → Coherent Actions |
| **Two-way / One-way doors** | Nate Jones | Reversibelt → gå hurtigt. Permanent → gå langsomt |
| **Ladder of AI Solutions** | Nate Jones | Prompt → RAG → Fine-tune → Custom. Start fra trin 1 |
| **Scaffolding > Models** | Nate Jones | 80% af værdien er prompts, context, workflows |
| **Taste som bottleneck** | Nate Jones | Modeller er billige. Judgment er dyrt og menneskeligt |
| **Context > Capability** | Miessler | Bedre kontekst slår bedre model |
| **AIMM (5 niveauer)** | Miessler | Awareness → Experimentation → Daily → Integration → Transformation |
| **Human 1.0/2.0/3.0** | Miessler | Uaugmenteret → AI som værktøj → AI integreret i identitet |
| **Job vs Gym** | Miessler | Job = minimal indsats for resultat. Gym = indsatsen ER værdien |
| **Meaning loops** | Miessler | Novelty + challenge + growth i feedback loop |
| **Builder vs Consumer** | Begge | Dem der bygger med AI vinder eksponentielt |

**Tags:** `→ VIDEN/Advisor-brain`, `→ PROJEKTER/Kompendium`, `→ PROJEKTER/PAI`

---

## 4.4 Tradeoffs (dokumenterede)
| Konflikt | Vinder | Kontekst |
|----------|--------|----------|
| Kris' tid vs. token cost | Kris' tid | Tid er uerstattelig |
| Funktion vs. perfektion | Funktion | Ship iterativt |
| Simplicitet vs. features | Simplicitet | Kompleksitet dræber vedligeholdelse |
| Hastighed vs. kvalitet | **Kontekst** | Voice = hastighed, retrieval = kvalitet |
| Automation vs. kontrol | Automation | Men med kill-switch |
| Cost vs. quality (embeddings) | Small model | 5% forbedring ≠ 3x pris |
| Docs vs. shipping | Shipping | >30% tid på docs = for meget |

**Tags:** `→ PRINCIPPER/Alle`, `→ STRUKTUR/Workflows`

**Filer:** `brain/intent/TRADEOFFS.md`

---

## 4.5 Friktionsregler (fra audit 15. feb)
| Regel | Beskrivelse |
|-------|-------------|
| **Kris' ønske først** | Gå 100% efter det Kris beder om. Alternativer som supplement, ikke erstatning. |
| **Simpelt ≠ discount** | Præcis den kompleksitet der kræves. |
| **Kend værktøjerne** | Hvis Kris nævner et værktøj → opfør dig aldrig som om du ikke kender det. |
| **Ingen PC** | Kris har kun Android + Termux. Aldrig foreslå PC-løsninger. |

**Tags:** `→ PROJEKTER/Alle`, `→ PRINCIPPER/Simplicitet`

---

# 5. HANDLINGER
> *Alt der skal gøres — fra indkøbsliste til systemarkitektur.*

## 5.1 Aktive opgaver
| Opgave | Projekt | Hvem | Status |
|--------|---------|------|--------|
| Redesign wireframes (feedback-loop) | TransportIntra | Kris + Claude | `igangværende` |
| Sortering-knap test med rigtig rute | TransportIntra | Kris | `venter på mandag` |
| Hukommelses-research | PAI | Claude | `planlagt` |
| Atlas → visuelle maps | Mindmap | Kris + Claude | `dette dokument` |
| Voice routing logic | PAI | Claude | `planlagt` |

## 5.2 Planlagte integrationer
| Integration | Formål | Afhængighed |
|-------------|--------|-------------|
| token_manager.py | Fælles OAuth fundament | Ingen |
| gmail_api.py | Læs/send mail | token_manager |
| outlook_api.py | Hotmail integration | token_manager |
| calendar_api.py | Kalender-oversigt | token_manager |
| trello_api.py | Trello board-styring | token_manager |

**Tags:** `→ STRUKTUR/Workflows`, `→ PROJEKTER/PAI`

## 5.3 Visioner (lang sigt)
| Vision | Beskrivelse |
|--------|-------------|
| **Human 3.0** | AI integreret i identitet — aldrig behøve skærm |
| **App for alle** | TransportIntra-klon enhver skraldemand ville elske |
| **Politisk dissekering** | Brug systemtænkning til at afsløre bureaukratisk spild |
| **Egen AI-model** | Langsigtede drøm, motiverer retning |
| **4D brainmap** | Interaktivt vidensnetværk med farve/form efter type |

**Tags:** `→ PRINCIPPER/Builder-vs-Consumer`, `→ PRINCIPPER/Human-3.0`

---

# 6. REDEGØRELSE

## Hvordan jeg kom frem til denne struktur

### Metode
Jeg gennemgik:
1. **brain/** — intent, priorities, tradeoffs, mission, decisions, playbooks, preferences
2. **data/exports/** — komplet analyse af 190 samtaler (ChatGPT + Grok + Claude)
3. **scripts/** — alle 34 Python scripts og hvad de gør
4. **crontab** — alle automatiske og deaktiverede jobs
5. **.claude/skills/** — 6 skill-kategorier
6. **data/mindmaps/** — eksisterende arkitektur-mindmap
7. **docs/** — dagbog, TELOS, session log, redesign
8. **Voice memo** — din besked fra i dag (10:41)

### Hvorfor disse 5 kategorier

**PROJEKTER** er det mest intuitive udgangspunkt — det er *hvad vi bygger*. Alt andet eksisterer for at tjene projekterne.

**STRUKTUR** er *hvordan det er bygget*. Filsystem, hukommelse, workflows, infrastruktur. Det er det tekniske fundament.

**VIDEN** er *hvad vi ved*. Advisor brain, research, rutedata, viden om Kris. Det er brændstoffet.

**PRINCIPPER** er *hvordan vi tænker*. Kerneværdier, frameworks, tradeoffs, designregler. De styrer alle beslutninger.

**HANDLINGER** er *hvad vi skal gøre*. Fra konkrete opgaver til langsigtede visioner.

### Hvor jeg er usikker

1. **Grænsen mellem VIDEN og PRINCIPPER.** Nate Jones' frameworks er *viden* (vi har lært dem), men de fungerer som *principper* (vi bruger dem til at beslutte). Jeg har sat dem under principper fordi de er handlingsrettede, men de kunne lige så godt leve under viden. **Tags løser dette** — de kan tagges begge steder.

2. **Hvor detaljeret HANDLINGER skal være.** Du nævnte "alt fra indkøbsliste til GPU-investering". Lige nu har jeg kun systemrelaterede handlinger. Personlige ting (indkøb, sundhed, økonomi) kunne tilføjes, men jeg vil ikke overfylde dokumentet med gæt. **Vi bør tilføje dem efterhånden.**

3. **Politisk platform som projekt.** MISSION.md nævner det som "den større mission", men det er ikke et aktivt projekt endnu. Jeg har sat det under "visioner" for nu.

4. **Rejseagent vs. ad hoc.** Cape Town-planlægningen var ad hoc, ikke et systematisk projekt. Skal det virkelig have sin egen kategori, eller er det bare en use case for PAI?

5. **Tags-systemet.** Jeg har brugt `→ KATEGORI/UNDERKATEGORI` som format. Det virker i markdown, men i en rigtig mindmap ville det være edges mellem noder. Formatet bør tilpasses når vi bygger den visuelle version.

### Alternative strukturer jeg overvejede

**Kronologisk:** Ordnet efter hvornår ting opstod. Afvist — giver ikke overblik, kun historie.

**Efter platform:** ChatGPT-ting, Grok-ting, Claude-ting. Afvist — platformen er irrelevant, indholdet er det der tæller.

**Kun 3 kategorier:** Projekter + Struktur + Principper (og putte viden og handlinger ind under projekter). Afvist — viden og handlinger er selvstændige dimensioner der krydser alle projekter.

**Flad liste med tags:** Ingen hierarki, bare en liste af noder med tags. Overvejet — dette er faktisk tættere på den 4D brainmap-vision. Men som markdown-dokument har vi brug for *noget* hierarki for læsbarhed.

---

*Dette dokument er fundamentet. Næste skridt: feedback fra Kris, tilføj manglende emner, og byg visuelle maps ovenpå.*
