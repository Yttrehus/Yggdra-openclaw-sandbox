# Context Engineering

## Metadata
- **Status:** Fase 1 (Session-drift hooks) i gang. Designet af PC-specifikke hooks.
- **Sidst opdateret:** 2024-05-22 (session 22)

## Hvad er det
Systematisering af Claude Code brug for maksimal kontinuitet. Fokus på hooks, compaction og state-filer.

## Hvor er vi
- **Fase 1:** Session-drift hooks. Vi skal bygge:
  - `scripts/session_start.sh`
  - `scripts/pre_compact.sh`
  - `scripts/session_end.sh`
- **Udfordring:** Claude Code hooks i OpenClaw sandbox er begrænsede. Vi kan ikke bruge `settings.local.json` globalt, men vi kan simulere dem eller dokumentere dem til ejeren.

## Næste skridt
1. Skitsér indholdet af de 3 hook-scripts.
2. Forbered en `settings.json` konfiguration som ejeren kan importere.
3. Implementér script-logikken i `scripts/`.
