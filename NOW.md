# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-12 ~18:30 (session 12)
**Status:** Project Reformation — fase 0-4 komplet. Næste: fase 5 (CONTEXT.md, egen session).

## Næste step (start her)

**Næste session:** Fase 5 — CONTEXT.md (den store konsolidering).
Se `pipeline/2_DLR/project-reformation/adr.project-reformation.md` sektion 8, fase 5.

1. Skriv CONTEXT.md: NOW + PLAN v3 + PROGRESS (graduated summary)
2. Arkivér PLAN.md → `pipeline/4_ARC/PLAN.v2.md`
3. Arkivér PROGRESS.md → `pipeline/4_ARC/PROGRESS-pre-v3.md`
4. Slet NOW.md og PROGRESS.md
5. Opdatér CLAUDE.md: `@NOW.md` → `@CONTEXT.md`
6. Verificér: ny session starter med kun CLAUDE.md + CONTEXT.md

## Hvad session 12 producerede

### Fase 1-2 revision
- Pipeline-stages samlet under `pipeline/` med numeriske præfikser (0_backlog → 4_ARC)
- `template/` → `.claude/template/`
- Rod reduceret fra 10 synlige mapper til 3 (pipeline, manuals, research)
- Alle governance-README headers, CLAUDE.md, `/new-project` skill opdateret

### Fase 3: Backlog-briefs
- 13 briefs oprettet i `pipeline/0_backlog/`
- 7 parallel-tasks outputs mappet til specifikke briefs
- PLAN.md idé-parkering erstattet med pointer til backlog

### Fase 4: ADR'er
- `pipeline/3_SIP/auto-chatlog/adr.auto-chatlog.md` — retroaktiv
- `pipeline/1_PoC/projekt-omdobning/adr.projekt-omdobning.md` — retroaktiv

### Beslutninger
- Pipeline i egen overmappe, ikke i BMS-roden
- Numeriske præfikser for kronologisk sortering
- Research er et projekt (research-architecture), ikke bare en mappe
- Al eksisterende research er pre-reformation → research/_ARC/
- Automation.md → backlog-brief, ikke levende dokument
- Feedback-memory: afkryds steps med det samme

## Ny struktur

```
Basic Setup/
├── CLAUDE.md, NOW.md, PLAN.md, PROGRESS.md, README.md
├── pipeline/
│   ├── 0_backlog/    ← 13 briefs
│   ├── 1_PoC/        ← projekt-omdobning (ADR)
│   ├── 2_DLR/        ← project-reformation (ADR)
│   ├── 3_SIP/        ← auto-chatlog (ADR + engine)
│   └── 4_ARC/        ← chatlogs, journals, historisk
├── manuals/           ← git.md, vscode.md, terminal.md
├── research/          ← tom, _ARC/ har 8 pre-reformation filer
└── .claude/           ← skills, template, settings
```

## Åbne tråde

- M5 step 11-17 (filsystem, X1, fonts, Dev Drive, wslconfig, quick reference)
- Checkpoint-skill: ADR-check mangler
- Poppler PATH-verifikation efter restart
- Prettier mangler .prettierrc
