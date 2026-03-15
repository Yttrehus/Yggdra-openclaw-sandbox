# Steelman Red Team — Styrket kritik

## Angreb-for-angreb vurdering

| # | Angreb | Vurdering |
|---|--------|-----------|
| 1 | Qdrant MCP tunneling | **Holder stærkt** — SSH-alias er simplere end alle 3 MCP-scenarier |
| 2 | 18 deliverables / scope | **Holder stærkt** — kapacitetsproblem, ikke sekvenseringsproblem |
| 3 | Bash-first princip-brud | **Holder stærkt** — CLAUDE.md siger "Scripts over MCP" |
| 4 | Token-budget | **Holder delvist** — reel men overdrevet i tal (lazy loading) |
| 5 | Vedligeholdelsesbyrde | **Holder stærkt** — 14 dependencies uden SLA |
| 6 | writing-plans redundans | **Holder stærkt** — parallelt system til eksisterende PDCA |
| 7 | TDD urealistisk | **Holder delvist** — misfit for scripts, fair for webapp |
| 8 | brainstorming overflødig | **Holder delvist** — sker naturligt i samtale |
| 9 | git-worktrees prematur | **Holder stærkt** — ingen evidence for behov |
| 10 | research-digest symptom | **Holder delvist** — engangs-oprydning bedre end on-demand skill |
| 11 | Ingen solnedgangsklausul | **Holder stærkt** — formfejl der undergraver troværdighed |
| 13 | Nul-baseline | **Holder stærkt** — systemet virker allerede |

6 holder stærkt, 5 holder delvist, 0 svage.

## Det stærkeste samlede argument
Anbefalingen løser problemer der ikke er dokumenteret som problemer, med værktøjer der modsiger brugerens designprincipper, i et omfang der ignorerer brugerens kapacitet.

## Foreslåede justeringer
1. Reducér til max 3 deliverables
2. Drop Qdrant MCP (SSH virker, bash-first)
3. Bevar kun skills der forstærker eksisterende workflow
4. Tilføj solnedgangsklausul per anbefaling
5. Tilføj nul-baseline eksplicit
6. Adressér token-budget
7. Differentier MCP (runtime-risiko) fra skills (markdown, lav risiko)
