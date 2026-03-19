# CLAUDE.md - Yggdra PC (Udviklings-instans)

## Vision
Yggdra er et personligt kognitivt exoskeleton. Denne instans (PC) er dedikeret til **udvikling, research og context engineering**. Driftsopgaver og tunge services (Qdrant, Docker, cron) bor på VPS (Ydrasil).

## Domæneopdeling
- **PC (Her):** Udvikling, research-arkitektur, context-engineering, lokal episodisk log, projektstyring.
- **VPS (Ydrasil):** Drifts-services, Qdrant (84K vektorer), LIVE webapp (TransportIntra), 18 cron jobs, voice pipeline.
- **Bro:** Brug SSH for remote commands og Qdrant-søgning (ctx).

## Projekter
Alle projekter bor i roden (Miessler-princippet) med stage-præfiks:
- `BMS.` (Basement/Core): Grundlæggende værktøjer (f.eks. `BMS.auto-chatlog`)
- `DLR.` (Development/Research): Aktive forskningsprojekter
- `LIB.` (Library): Arkiverede eller statiske kilder
- `REF.` (Reference): Opslagsværk og evalueringer
- `SIP.` (Staged Implementation): Agentens eget udviklingsrum
- `KNB.` (Knowledge Base): Manualer og etableret viden

Hvert projekt har en `CONTEXT.md`. Backlog-briefs bor i `0_backlog/` med kapitel-nummerering (f.eks. `01.navn.rdy.md`).

## Hvad læses automatisk
Kun denne fil (`CLAUDE.md`) og `CONTEXT.md` (via @import). Alt andet læses efter behov.

## Kontekst-kilder (læses efter behov)
- `PROGRESS.md` — fuld narrativ per session, destilleret
- `BLUEPRINT.md` — systemarkitektur og designprincipper
- `chatlog.md` — komplet sessionsdata (genereret af `BMS.auto-chatlog`)
- `0_backlog/TRIAGE.md` — prioriteret backlog-overblik
- `DAGBOG.md` — agentens løbende log over tanker og beslutninger

## Principper
- **Bash-first:** Scripts over komplekse tools.
- **State på disk:** Markdown og JSONL i git.
- **Progressive Disclosure:** Læs CONTEXT.md -> BLUEPRINT.md -> Filer.
- **Simplicitet > Features:** Byg kun det der bliver brugt.
- **Miessler-princippet:** Max 3 niveauer i mappestrukturen.

## Workflow
- **Start:** Læs altid CONTEXT.md for aktuel status.
- **Checkpoints:** Kør `scripts/pre_compact.sh` før store ændringer.
- **Hukommelse:** Skriv vigtige beslutninger i `DAGBOG.md` og opdatér `MEMORY.md`.
- **Session Stop:** `scripts/session_end.sh` logger episoden.

## Hurtige kommandoer
- `ctx "query"`: Søg i VPS Qdrant (kræver tunnel).
- `ssh vps "command"`: Kør kommando på VPS (hvis alias findes).
- `./scripts/checkpoint.sh`: Manuelt checkpoint.
