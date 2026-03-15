# Context Engineering

## Metadata
- **Status:** Fase 1 (Session-drift hooks) afsluttet. Fase 2 (Skills & Best Practices) i gang. Full Retrieval Pipeline PoC færdig.
- **Sidst opdateret:** 2024-05-23 (session 26)

## Hvad er det
Systematisering af hvordan Claude Code bruges effektivt for at sikre maksimal kontinuitet.

## Hvor er vi
- **Fase 1 (Session-drift hooks):** Alle 3 hooks (`session_start.sh`, `pre_compact.sh`, `session_end.sh`) er implementeret og testet i OpenClaw sandbox.
- **Auto-chatlog:** `chatlog-engine.js` er opdateret til at være miljø-agnostisk.
- **Gaps (Retrieval):** En komplet PoC-pipeline for **Retrieval Optimering** (Gap 2 & 4) er færdig i `scripts/retrieval_poc.py`.
  - Kombinerer semantisk score, temporal decay (halveringstid) og reranking.
  - Dokumenteret i DAGBOG.md (Session 4).

## Næste skridt
1. **Fact Extraction (Gap 6):** Forsøg på automatisk ekstraktion af fakta fra chatlog-segmenter.
2. **Skills forfining:** Gennemgå `.claude/skills/` og sikre at de følger progressive disclosure principperne.
3. **CLAUDE.md audit:** Tjek om instruktionerne i roden kan strammes.
