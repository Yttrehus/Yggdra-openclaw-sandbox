# Yggdra

## Metadata
- **Status:** Session 33 (Agent). WARM memory lag implementeret. APA-standarder udrullet.
- **Sidst opdateret:** 2026-03-21 (session 33)

## Hvor er vi

### Seneste Agent Sessioner (33 — 2026-03-21)
- **Session 33:** 
  - **WARM Memory:** `data/LEARNINGS.md` etableret som lag mellem HOT og COLD.
  - **Lærings-ekstraktion:** `fact_extraction_poc.py` udvidet til autonomt at opsamle lessons learned.
  - **Fuld APA Audit:** Alle 19 research-filer i `2_research/` er nu APA 7th refererede (epistemisk sporbarhed).
  - **Videnskabelig alignment:** Forbundet RAG-arkitektur med *Complementary Learning Systems* (CLS) teori.

### Tidligere Agent Sessioner (32 — 2026-03-19)
- **Session 32:** 
  - **Temporal Reranking PoC:** `memory_v2/search_rerank.py` demonstrerer decay-effekt.
  - **Evergreen Management:** Beskyttelse af kernedokumenter mod decay.
  - **Research Standard:** `05.RESEARCH_KVALITET/APA_STANDARDS.md` oprettet.

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md, RAPPORT.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── DAGBOG.md                 ← agentens løbende log
├── 0_backlog/                ← briefs + TRIAGE.md
├── 2_research/               ← V4+V6 destillater (APA-aligned)
├── BMS.auto-chatlog/         ← chatlog-engine
├── SIP.agent-sandbox/        ← Agentens eget udviklingsrum (PoCs, standarder)
└── data/
    ├── LEARNINGS.md          ← WARM memory (lessons learned)
    └── extracted_facts.json  ← Semantisk hukommelse
```

### Aktive projekter
- **SIP.agent-sandbox:** Fact extraction v2 (learning aware) og memory v2 (reranking) aktive.
- **2_research:** Fuldstændig audit færdiggjort. Epistemisk fundament konsolideret.
- **BMS.auto-chatlog:** v3 fungerer.

## Beslutninger
- **ALBA Pattern:** Brug HOT (NOW/CONTEXT), WARM (LEARNINGS) og COLD (Archive/Qdrant) lag.
- **APA 7th:** Alle væsentlige påstande i `2_research/` SKAL have kildehenvisninger.
- **Temporal Decay:** Relevans falder over tid (halveringstid 30 dage).

## Hvad mangler
- [ ] Begynd audit af `2_research/llm-landskab/` (næste lag af detaljer).
- [ ] Synkronisér `ai_intelligence.py` og `intelligence_sources.json` til PC (se `RAPPORT.md`).
- [ ] Implementér Blog-RSS Pipeline (Udvidelse 1 i `PIPELINE_DESIGN.md`).
- [ ] Verificér ingestion til Qdrant med gyldig API-nøgle.
