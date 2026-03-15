# CLAUDE.md - Yggdra PC (Udviklings-instans)

## Vision
Yggdra er et personligt kognitivt exoskeleton. Denne instans (PC) er dedikeret til **udvikling, research og context engineering**. Driftsopgaver og tunge services (Qdrant, Docker, cron) bor på VPS (Ydrasil).

## Domæneopdeling
- **PC (Her):** Udvikling, research-arkitektur, context-engineering, lokal episodisk log, projektstyring.
- **VPS (Ydrasil):** Drifts-services, Qdrant (84K vektorer), LIVE webapp (TransportIntra), 18 cron jobs, voice pipeline.
- **Bro:** Brug SSH for remote commands og Qdrant-søgning (ctx).

## Principper
- **Bash-first:** Scripts over komplekse tools.
- **State på disk:** Markdown og JSONL i git.
- **Progressive Disclosure:** Læs CONTEXT.md -> BLUEPRINT.md -> Filer.
- **Simplicitet > Features:** Byg kun det der bliver brugt.

## Workflow
- **Start:** Læs altid CONTEXT.md for aktuel status.
- **Checkpoints:** Kør `scripts/pre_compact.sh` før store ændringer.
- **Hukommelse:** Skriv vigtige beslutninger i `DAGBOG.md` og opdatér `MEMORY.md` (hvis aktuelt).
- **Session Stop:** `scripts/session_end.sh` logger episoden.

## Hurtige kommandoer
- `ctx "query"`: Søg i VPS Qdrant (kræver tunnel).
- `ssh vps "command"`: Kør kommando på VPS (hvis alias findes).
- `./scripts/checkpoint.sh`: Manuelt checkpoint.
