# Work Intake & Project Taxonomy

**Dato:** 2026-03-15
**Status:** Delvist implementeret
**Priority:** Medium-high (enabler for alt andet arbejde)

## Opsummering

To systemer der tilsammen giver overblik over hvad der eksisterer og hvad der skal gøres:

1. **Backlog taxonomy** — filnavne-konvention der viser modenhed: `raw.` → `brief.` → `RDY.`
2. **Project taxonomy** — mappenavne-konvention der viser stage: `BMS.` / `REF.` / `LIB.` / `KNB.` / `DLR.` / `SIP.` / `PoC.`
3. **TRIAGE.md** — prioriteret overblik, session-forslag, afhængigheder

## Backlog taxonomy (filnavne i 0_backlog/)

| Præfiks | Betydning | Eksempel |
|---------|-----------|---------|
| `raw.` | Rå idé, scope uklart | `raw.visualisering.md` |
| `brief.` | Skrevet ud, men kræver forberedelse | `brief.notion-spejling.md` |
| `RDY.` | Ready to go — kan startes som projekt | `RDY.context-engineering.md` |

## Project taxonomy (mappenavne i projects/)

Format: `STAGE.projektnavn/`

### Pipeline-stages (aktiv udvikling)

| Præfiks | Navn | Betydning |
|---------|------|-----------|
| **PoC** | Proof of Concept | Eksperiment. "Virker det?" |
| **DLR** | Discovery-Led Roadmap | Aktiv research/design |
| **SIP** | Staged Implementation Plan | Under opbygning |

### Done-stages (færdige, i brug)

| Præfiks | Navn | Betydning | Analogi |
|---------|------|-----------|---------|
| **BMS** | Baseline Module System | Kører automatisk, vedligeholdes | Motor |
| **REF** | Reference | Statisk opslagsværk, slå op | Ordbog |
| **LIB** | Library | Stor samling, browse | Bibliotek |
| **KNB** | Knowledge Base | Kurateret viden, forståelse | Lærebog |

### Specielle mapper

| Mappe | Rolle |
|-------|-------|
| `0_backlog/` | Idéer (raw/brief/r2g). Ikke en stage |
| `1_archive/` | Døde projekter. Ikke i brug |

## TRIAGE.md

Flat fil i `0_backlog/`. Scanbar på 10 sekunder. Opdateres ved session-start.
Indeholder: prioriteret liste, modenhed, afhængigheder, session-forslag.

## Regler

1. Ét præfiks per mappe. `SIP.DLR.projekt` findes ikke
2. Præfiks er sandheden. Mapper > metadata
3. Demotion er OK. SIP → DLR når antagelser fejler
4. Backlog-filer har `raw.`/`brief.`/`RDY.` præfiks. Stage-præfikser starter når brief bliver projektmappe
5. Archive er for døde ting. Færdigt-men-brugt = BMS/REF/LIB/KNB

## Status

- [x] TRIAGE.md oprettet og brugt (session 20+21)
- [x] Project taxonomy designet (session 17, brief.project-taxonomy.md)
- [x] Backlog taxonomy designet (session 21)
- [ ] Migration: `git mv` alle mapper + backlog-filer
- [ ] Opdater CONTEXT.md, CLAUDE.md, BLUEPRINT.md med nye stier

## Kill condition

Hvis præfiks-omdøbning skaber mere friktion end det løser efter 3 projekter (~4-6 uger): drop præfikser, brug CONTEXT.md metadata i stedet.

## Origin

- Session 11-13: PoC/DLR/SIP/BMS designet, droppet som for tungt
- Session 17: REF/LIB/KNB tilføjet for done-stages
- Session 20: TRIAGE.md oprettet som work-intake deliverable
- Session 21: Backlog taxonomy (raw/brief/r2g), merger med project-taxonomy
