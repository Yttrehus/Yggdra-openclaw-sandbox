# Yggdra

## Metadata
- **Status:** Session 33 (Agent). APA-standarder implementeres i research.
- **Sidst opdateret:** 2026-03-21 (session 33)

## Hvor er vi

### Seneste Agent Sessioner (33 — 2026-03-21)
- **Session 33:** 
  - **Audit:** Startet gennemgang af `2_research/` for at tilføje APA-referencer.
  - **Update:** `SOURCE_REGISTRY.md` opdateret med korrekt referenceliste (API'er og RSS feeds).
  - **Kontinuitet:** Fortsat implementering af kvalitetskrav fra session 32.

### Tidligere Agent Sessioner (32 — 2026-03-19)
- **Session 32:** 
  - **Temporal Reranking PoC:** `memory_v2/search_rerank.py` valideret.
  - **Evergreen Management:** `memory_v2/evergreen.py` implementeret.
  - **Research Standard:** `05.RESEARCH_KVALITET/APA_STANDARDS.md` oprettet (APA 7th).
  - **Rapport:** Anmodet om synkronisering af drifts-scripts i `RAPPORT.md`.

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
- **SIP.agent-sandbox:** `05.RESEARCH_KVALITET/APA_STANDARDS.md` (APA) aktiv og i brug.
- **2_research:** Audit af `videns-vedligeholdelse` for APA-alignment i gang.
- **BMS.auto-chatlog:** v3 fungerer.

## Beslutninger
- **APA 7th:** Alle væsentlige påstande i `2_research/` SKAL have kildehenvisninger.
- **Temporal Decay:** Relevans falder over tid (halveringstid 30 dage).
- **Evergreen:** Kernedokumenter (manualer, blueprints) er undtaget decay.

## Hvad mangler
- [ ] Fortsæt audit af `2_research/` (næste: `DECAY_MODEL.md`).
- [ ] Synkronisér `ai_intelligence.py` og `intelligence_sources.json` til PC (se `RAPPORT.md`).
- [ ] Implementér Blog-RSS Pipeline (Udvidelse 1 i `PIPELINE_DESIGN.md`).
- [ ] Verificér ingestion til Qdrant med gyldig API-nøgle.
