# Yggdra

## Metadata
- **Status:** Session 32 (Agent). Research-standarder (APA 7th) etableret. Temporal Reranking PoC valideret.
- **Sidst opdateret:** 2026-03-19 (session 32)

## Hvor er vi

### Seneste Agent Sessioner (32 — 2026-03-19)
- **Session 32:** 
  - **Temporal Reranking PoC:** `memory_v2/search_rerank.py` demonstrerer nu korrekt decay-effekt på gammel viden (halveringstid 30 dage).
  - **Evergreen Management:** `memory_v2/evergreen.py` implementeret til beskyttelse af kernedokumenter mod decay.
  - **Research Standard:** `05.RESEARCH_KVALITET/APA_STANDARDS.md` oprettet for at sikre kilde-sporbarhed (APA 7th).
  - **Gap Analyse:** Identificeret kritisk gap i Blog-RSS Pipeline (Anthropic, OpenAI, DeepMind). `ai_intelligence.py` mangler på PC for implementering.
  - **Rapport:** Anmodet om synkronisering af drifts-scripts i `RAPPORT.md`.

### Tidligere Agent Sessioner (22-31 — 2024-05-22/23)
- **Session 31:** Viden-pipeline proaktiv (Notifier integreret). SiP workflow stabiliseret. 
- **Session 30:** PoCs flyttet til `projects/sip/`. SiP struktur etableret. 
- **Session 29:** Agent Operations Manual oprettet.

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md, RAPPORT.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── DAGBOG.md                 ← agentens løbende log
├── 0_backlog/                ← briefs + TRIAGE.md
├── 2_research/               ← V4+V6 destillater (llm-landskab, ai-frontier, videns-vedligeholdelse)
├── BMS.auto-chatlog/         ← chatlog-engine
├── SIP.agent-sandbox/        ← Agentens eget udviklingsrum (PoCs, standarder)
└── scripts/                  ← utility scripts (get_context.py, memory.py, pre_compact.sh)
```

### Aktive projekter
- **SIP.agent-sandbox:** `memory_v2/` (reranking, evergreen) og `05.RESEARCH_KVALITET/` (APA) aktive.
- **2_research:** V4+V6 destillater. Fokus på `videns-vedligeholdelse` og `ai-frontier`.
- **BMS.auto-chatlog:** v3 fungerer (~3000 beskeder, 39 sessions).

## Beslutninger
- **APA 7th:** Alle væsentlige påstande i `2_research/` skal have kildehenvisninger.
- **Temporal Decay:** Relevans falder over tid (`score *= exp(-age_days / half_life)`), med undtagelse af "Evergreen" dokumenter.
- **Miessler-princippet:** Max 3 niveauer i mappestrukturen i hele workspace.

## Hvad mangler
- [ ] Synkronisér `ai_intelligence.py` og `intelligence_sources.json` til PC (se `RAPPORT.md`).
- [ ] Implementér Blog-RSS Pipeline (Udvidelse 1 i `PIPELINE_DESIGN.md`).
- [ ] Auditér eksisterende research-filer for manglende APA-referencer.
- [ ] Verificér ingestion til Qdrant med gyldig API-nøgle.
