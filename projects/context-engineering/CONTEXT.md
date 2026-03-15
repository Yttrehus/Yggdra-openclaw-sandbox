# Context Engineering

## Metadata
- **Status:** Fase 1 (Session-drift hooks) afsluttet (scripts bygget). Fase 2 påbegyndt.
- **Sidst opdateret:** 2024-05-23 (session 23)

## Hvad er det
Systematisering af Claude Code brug for maksimal kontinuitet. Fokus på hooks, compaction og state-filer.

## Hvor er vi
- **Fase 1:** Session-drift hooks. Scripts er implementeret i `scripts/`:
  - `session_start.sh`: Injekterer status og dagbog ved start.
  - `pre_compact.sh`: Advarer om compaction og kører auto-chatlog.
  - `session_end.sh`: Logger episoden og tjekker for ucommittede ændringer.
- **Konfiguration:** `hooks_config_example.json` oprettet som skabelon til ejeren.

## Næste skridt
1. **Fase 2:** CLAUDE.md & skills best practices.
   - Evaluere om de genoprettede skills (`checkpoint`, `session-resume`, `sitrep`) skal forfines.
   - Sikre at `CLAUDE.md` i roden altid afspejler de nyeste principper.
2. Teste hooks manuelt for at verificere output-formatet.
