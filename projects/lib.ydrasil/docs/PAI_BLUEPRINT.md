# PAI Blueprint - Kris' Personal AI

Inspireret af Daniel Miessler's PAI v2 arkitektur, tilpasset til vores kontekst.

---

## Lag-model (fra fundament op)

```
┌─────────────────────────────────────────┐
│  5. WORKFLOWS & AGENTS                  │
│     Agentic flows, sub-agents, routing  │
├─────────────────────────────────────────┤
│  4. SKILLS & TOOLS                      │
│     Genanvendelige moduler, CLI, n8n    │
├─────────────────────────────────────────┤
│  3. CONTEXT SYSTEMS                     │
│     Hukommelse, RAG, data mapping       │
├─────────────────────────────────────────┤
│  2. KOGNITIV ARKITEKTUR                 │
│     Tænke-loop, beslutningsmodel        │
├─────────────────────────────────────────┤
│  1. KERNEVÆRDIER & PRINCIPPER           │
│     Hvem er Kris, hvad driver ham       │
└─────────────────────────────────────────┘
```

---

## Lag 1: Kerneværdier & Principper

Miessler bruger **TELOS** - 10 dokumenter der definerer identitet:

| Dokument | Formål | Vores version (TODO) |
|----------|--------|---------------------|
| MISSION.md | Overordnet mission | Hvad driver Kris? |
| GOALS.md | Konkrete mål | Kort + lang sigt |
| PROJECTS.md | Aktive projekter | Ydrasil, rute-optimering, ... |
| BELIEFS.md | Overbevisninger | Arbejdsfilosofi |
| MODELS.md | Mentale modeller | Hvordan Kris tænker om problemer |
| STRATEGIES.md | Strategier | Tilgange til at nå mål |
| NARRATIVES.md | Narrativer | Historien Kris fortæller |
| LEARNED.md | Erfaringer | Hvad har vi lært |
| CHALLENGES.md | Udfordringer | Hvad blokerer os |
| IDEAS.md | Idéer | Alt der popper op |

**Hvorfor det er vigtigt:** AI'en træffer bedre beslutninger når den forstår konteksten. Uden TELOS er den bare et værktøj. Med TELOS bliver den en forlængelse af Kris.

**Miesslers princip:** "Scaffolding > Model" - Arkitekturen er vigtigere end hvilken model man bruger.

---

## Lag 2: Kognitiv Arkitektur

Miesslers **7-fase inner loop** (videnskabelig metode):

```
OBSERVE → THINK → PLAN → BUILD → EXECUTE → VERIFY → LEARN
   ↑                                                  │
   └──────────────────────────────────────────────────┘
```

**Outer loop:** Current State → Desired State (via verifiable iteration)

### For os konkret:
- **OBSERVE:** Hvad er status? (rute, stops, data)
- **THINK:** Hvad er mulighederne?
- **PLAN:** Vælg tilgang
- **BUILD:** Definér succeskriterier (hvornår er det godt nok?)
- **EXECUTE:** Udfør
- **VERIFY:** Virkede det? Mål det.
- **LEARN:** Hvad lærte vi? Gem det.

### Beslutningshierarki (Miessler):
```
Goal → Code → CLI → Prompts → Agents
```
Brug den mest deterministiske løsning først. Kun brug AI-agents når simpler metoder ikke rækker.

---

## Lag 3: Context Systems

### Hukommelse (3-tier)

| Tier | Type | Indhold | Teknologi |
|------|------|---------|-----------|
| Hot | Aktiv kontekst | Nuværende session, aktuel rute | In-memory / prompt |
| Warm | Nær fortid | Sidste uges ruter, seneste beslutninger | Vector DB (Qdrant) |
| Cold | Arkiv | 2 års historisk data, alle logs | Filer + embeddings |

### RAG Pipeline

```
Spørgsmål → Embedding → Vektor-søgning → Top-K resultater → Prompt + kontekst → Svar
```

**Typer vi kan bruge:**
- **Hybrid RAG** (vektor + keyword) - Til rutedata, stop-historik
- **Agentic RAG** - Agent beslutter hvad der skal søges, iterativt
- **Graph RAG** - Relationer (stop → kunde → adresse → rute → dag)

### Data Mapping

Vores data og hvordan det skal struktureres:

```
TransportIntra API (live)
    ├── Ruter (header: id, status, headline)
    ├── Dispatches (stops: adresse, status, sorter, GPS)
    ├── Adresser (work vs kunde, lat/lng)
    └── Comments (err_codes, noter)

Google Sheets (planlægning)
    └── Rækkefølge per rute per dag

Historisk data (/data/routes/)
    ├── 577 JSON filer
    ├── 40.053 stops
    └── 343 dage, 2 år
```

**Embedding-strategi (TODO):**
- Chunk per stop (adresse + kunde + type + koder)
- Chunk per rute-dag (headline + alle stops + rækkefølge)
- Metadata-filtering (dato, rute_id, status)

---

## Lag 4: Skills & Tools

Miessler-koncept: **"Løs et problem én gang, derefter er det et modul."**

### Skill-struktur
```
Skills/
├── RuteManagement/
│   ├── SKILL.md          # Routing + domæne-viden + "USE WHEN"
│   ├── workflows/        # Step-by-step procedurer
│   └── tools/            # Scripts, CLI
├── DataAnalyse/
│   ├── SKILL.md
│   ├── workflows/
│   └── tools/
├── WebappDev/
│   ├── SKILL.md
│   ├── workflows/
│   └── tools/
└── ...
```

### Potentielle Skills for os
- **RuteManagement** - Forespørgsler om ruter, stops, rækkefølge
- **DataAnalyse** - Historisk analyse, mønstre, anomalier
- **WebappDev** - Ændringer til TI-klonen
- **n8nWorkflows** - Bygge og vedligeholde n8n flows
- **Sync** - Google Sheets ↔ TransportIntra synkronisering

---

## Lag 5: Workflows & Agents

### Agent-roller (fremtid)

| Agent | Model | Rolle |
|-------|-------|-------|
| Router | Haiku | Klassificér opgave, send til rette agent |
| Rute-agent | Sonnet | Ruteforespørgsler, TI API, daglig drift |
| Kode-agent | Sonnet/Opus | Webapp-ændringer, debugging |
| Data-agent | Haiku/Sonnet | Lookups, formatering, embeddings |
| Arkitekt | Opus | Planlægning, komplekse beslutninger |

### Miesslers Hook-system
Events der trigger automatisk:
- **SessionStart** → Load kontekst, tjek aktive opgaver
- **PostToolUse** → Log alt, fang outputs
- **Stop** → Opsummér session, gem learnings

---

## Miesslers 15 Principper (tilpasset os)

1. **Current State → Desired State** med verifikation
2. **Klar tænkning før prompts** - Forstå problemet først
3. **Scaffolding > Model** - Arkitektur > rå intelligens
4. **Determinisme** - Konsistente resultater, ikke tilfældige
5. **Kode før prompts** - Brug det mest pålidelige først
6. **Spec/Test/Evals** - Mål før du bygger
7. **UNIX filosofi** - Små, komponerbare, enkeltformåls-værktøjer
8. **SRE principper** - Behandl AI infra som produktion
9. **CLI interface** - Scriptbart, komponerbart
10. **Beslutningshierarki** - Goal → Code → CLI → Prompts → Agents
11. **Meta/self-update** - Systemet forbedrer sig selv
12. **Custom Skills** - Domæne-ekspertise pakker
13. **Custom History** - Automatisk dokumentation
14. **Agent personligheder** - Specialiserede stemmer/tilgange
15. **Videnskab som loop** - Hypotese → Eksperiment → Mål → Iterér

---

## AI Maturity Model (hvor er vi?)

| Level | Navn | Beskrivelse | Os? |
|-------|------|-------------|-----|
| 0 | Natural | Ingen AI | |
| 1 | Chatbots | ChatGPT/Claude chat | |
| 2 | **Agentic** | AI agents med tools, API, handlinger | **← Her** |
| 3 | Workflows | Automatiserede pipelines | Mål |
| 4 | Managed | Selv-optimerende systemer | Vision |

---

## Næste skridt (ikke nu, men retning)

1. **Skriv TELOS** - Start med MISSION, GOALS, PROJECTS
2. **Sæt Qdrant op** - Docker container på VPS
3. **Embed rutedata** - Start med nyeste 3 måneders data
4. **Første Skill** - RuteManagement med SKILL.md
5. **Router-prototype** - Simpel Haiku-baseret intent classifier
6. **Hook system** - Auto-log sessioner og learnings

---

## Åbne spørgsmål

- Hvilke kerneværdier definerer Kris' tilgang til arbejde og liv?
- Hvad er de 3-5 vigtigste mål lige nu?
- Hvor meget tid/penge bruger vi på AI i dag, og hvad er budgettet?
- Skal PAI'en primært køre via Telegram, CLI, webapp, eller alle tre?
- Hvordan ser Kris' ideelle morgen ud med en fungerende PAI?

---

*Kilder: [Daniel Miessler - PAI v2](https://danielmiessler.com/blog/personal-ai-infrastructure) | [GitHub repo](https://github.com/danielmiessler/Personal_AI_Infrastructure) | [AI Maturity Model](https://danielmiessler.com/blog/personal-ai-maturity-model)*
