# Yggdra

## Metadata
- **Status:** Session 34 (Agent). Retrieval Evaluation Framework etableret.
- **Sidst opdateret:** 2026-03-22 (session 34)

## Hvor er vi

### Seneste Agent Sessioner (34 — 2026-03-22)
- **Session 34:**
  - **Eval Framework:** Dataset (`dataset.json`) og eval-engine (`eval_engine.py`) oprettet i `SIP.agent-sandbox/retrieval_eval/`.
  - **Retrieval Engine V2:** Ny engine med temporal decay, evergreen beskyttelse og reranking implementeret i `retrieval_v2/engine.py`.
  - **Reranker PoC:** Simuleret semantisk reranking (Gap 2) tilføjet i `retrieval_v2/reranker.py`.
  - **Blog-RSS Pipeline PoC:** Udvidelse 1 fra `PIPELINE_DESIGN.md` valideret i `pipeline_v2/rss_poc.py`.
  - **Pricing Monitor PoC:** Udvidelse 2 fra `PIPELINE_DESIGN.md` valideret i `pipeline_v2/pricing_diff.py`.
  - **Validering:** Syntetisk benchmark bekræfter nu både decay-logik og query-baseret reranking. RSS PoC bekræfter 7-dages filter-logik. Pricing PoC detekterer prisændringer korrekt.
  - **Fuld APA Audit:** Hele `2_research/llm-landskab/` (9 filer) er nu fuldt APA-refererede (epistemisk sporbarhed).
  - **Gap Lukning:** Gap 1 (RSS), Gap 2 (Reranking), Gap 3 (Måling) og Gap 4 (Temporal Decay) adresseret på PoC-niveau. Samt færdiggørelse af research-audit.

### Tidligere Agent Sessioner (33 — 2026-03-21)
- **Session 33:**
  - **WARM Memory:** `data/LEARNINGS.md` etableret (ALBA-pattern).
  - **Fuld APA Audit:** Alle 19 research-filer APA-refererede.

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md, RAPPORT.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── DAGBOG.md                 ← agentens løbende log
├── 0_backlog/                ← briefs + TRIAGE.md
├── 2_research/               ← V4+V6 destillater (APA-aligned)
├── BMS.auto-chatlog/         ← chatlog-engine
├── SIP.agent-sandbox/        ← Agentens eget udviklingsrum (Eval, Retrieval v2)
└── data/
    ├── LEARNINGS.md          ← WARM memory (lessons learned)
    └── extracted_facts.json  ← Semantisk hukommelse
```

### Aktive projekter
- **SIP.agent-sandbox:** Retrieval Evaluation Framework og Engine v2 aktive.
- **2_research:** Epistemisk fundament konsolideret.

## Beslutninger
- **Baseline Måling:** Vi bygger ikke nye retrieval-features uden at kunne måle impact via `retrieval_eval`.
- **Evergreen:** Filer i `BLUEPRINT.md`, `IDENTITY.md`, `SOUL.md` og `KNB.manuals/` er undtaget decay.
- **ALBA Pattern:** Brug HOT (NOW/CONTEXT), WARM (LEARNINGS) og COLD (Archive/Qdrant) lag.

## Hvad mangler
- [ ] Kør benchmark mod live Qdrant data (kræver tunnel/nøgler).
- [ ] Implementér Reranking (Gap 2) i Engine v2.
- [ ] Synkronisér `ai_intelligence.py` til PC (se `RAPPORT.md`).
