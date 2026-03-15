# Context Engineering Rules

Disse regler sikrer maksimal kontinuitet på tværs af sessioner.

## State-filer
- **CONTEXT.md:** Projektets aktuelle tilstand (læses altid ved start).
- **DAGBOG.md:** Din løbende log over tanker og beslutninger.
- **PROGRESS.md:** Narrativ historik.

## Hooks & Checkpoints
- Brug `/checkpoint` skill før du afslutter en session.
- Vedligehold `scripts/` manuelt indtil de kan køres automatisk af hosten.

## Compaction
- Når Claude foreslår compaction, kør altid `scripts/pre_compact.sh` manuelt først for at sikre at chatloggen er opdateret.
- Sørg for at alle vigtige beslutninger fra den nuværende context er skrevet til `DAGBOG.md`.

## Arkitektur
- Følg domæneopdelingen: PC er til udvikling/research, VPS er til drift.
- Brug `ctx` kommandoen til at søge i VPS Qdrant (semantisk hukommelse).
