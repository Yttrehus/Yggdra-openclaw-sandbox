# CLAUDE.md - Yggdra PC (Udviklings-instans)

## Vision
Yggdra er et personligt kognitivt exoskeleton. Denne instans (PC) er dedikeret til **udvikling, research og context engineering**. Driftsopgaver og tunge services (Qdrant, Docker, cron) bor på VPS (Ydrasil).

## Domæneopdeling
- **PC (Her):** Udvikling, research-arkitektur, context-engineering, lokal episodisk log, projektstyring.
- **VPS (Ydrasil):** Drifts-services, Qdrant (84K vektorer), LIVE webapp (TransportIntra), 18 cron jobs, voice pipeline.
- **Bro:** Brug SSH for remote commands og Qdrant-søgning (ctx).

## Projekter

Alle projekter bor i `projects/` med stage-præfiks: `BMS.`/`REF.`/`LIB.`/`KNB.`/`DLR.`/`SIP.`/`PoC.`
Hvert projekt har en CONTEXT.md. Backlog-briefs bruger `raw.`/`brief.`/`r2g.` præfiks i `0_backlog/`.

## Hvad læses automatisk

Kun denne fil (CLAUDE.md) og CONTEXT.md (via @import). Alt andet læses efter behov.

## Kontekst-kilder (læses efter behov)

- PROGRESS.md — fuld narrativ per session, destilleret
- BLUEPRINT.md — systemarkitektur (5 emergente lag, filstruktur, designprincipper)
- chatlog.md — komplet sessionsdata (roden, genereret af projects/BMS.auto-chatlog/chatlog-engine.js)
- projects/0_backlog/TRIAGE.md — prioriteret backlog-overblik med modenhed og afhængigheder
- projects/*/CONTEXT.md — projekt-specifik kontekst

## Principper
- **Bash-first:** Scripts over komplekse tools.
- **State på disk:** Markdown og JSONL in git.
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
