# Context Engineering

## Metadata
- **Status:** Fase 1 (Session-drift hooks) afsluttet. Fase 2 (Skills & Best Practices) i gang. Temporal Decay PoC færdig.
- **Sidst opdateret:** 2024-05-23 (session 25)

## Hvad er det
Systematisering af hvordan Claude Code bruges effektivt for at sikre maksimal kontinuitet.

## Hvor er vi
- **Fase 1 (Session-drift hooks):** Alle 3 hooks (`session_start.sh`, `pre_compact.sh`, `session_end.sh`) er implementeret og testet i OpenClaw sandbox.
- **Auto-chatlog:** `chatlog-engine.js` er opdateret til at være miljø-agnostisk.
- **Gaps (Retrieval):** PoC for **Temporal Decay** (Gap 4) og **Reranking** (Gap 2) er færdig i `scripts/retrieval_poc.py`.
  - Viser hvordan en semantisk stærk men gammel note (score 0.95) korrekt bliver nedprioriteret til fordel for nyere information.
  - Implementerer præcis halveringstid-algoritme.

## Næste skridt
1. **Reranking med LLM:** Udvid PoC til at bruge en simpel LLM-baseret reranking (simuleret eller via provider).
2. **Skills forfining:** Gennemgå `.claude/skills/` og sikre at de følger progressive disclosure principperne.
3. **CLAUDE.md audit:** Tjek om instruktionerne i roden kan strammes.
