# GitHub Workflow & Expertise

**Dato:** 2026-03-14
**Status:** Raw — delvist implementeret, resten marinerer

## Hvad er gjort
- **Tags:** session-13..18 tagget og pushet. `git tag session-XX` ved session-slut fremover.
- **README:** Opdateret til nuværende struktur (PR #1, merged).
- **Branch workflow demonstreret:** fix/readme → PR → merge → cleanup. Første PR på repo.

## Hvad marinerer
- **Branch-per-task som vane:** Arbejd på branches, merge via PR. Main = rent. Kræver ingen tooling, bare en anden vane.
- **Git worktrees:** Flere working directories fra samme repo. Claude Code har det built-in (`isolation: "worktree"` i Agent-tool). Relevant for parallel sessioner der ikke skal forstyrre hinanden.
- **PR-based self-review:** Claude Code reviewer PR diff før merge. Erstatter manuel cross-session peer review.
- **GitHub Actions:** Ingen konkret use case endnu. Relevant den dag der er noget at automatisere (tests, CONTEXT.md-validering, chatlog-generation).
- **Issues som briefs:** Søgbar, filtrerbar, auto-close ved merge. Brief-systemet virker nu — parkeret til det ikke gør.

## Rå input
Fuld gennemgang i session (github-workflow, 2026-03-14). Dækkede: hvad professionelle gør med Claude Code + GitHub, hvad der er relevant for solo-Yttre, hvad der er team-noise.
