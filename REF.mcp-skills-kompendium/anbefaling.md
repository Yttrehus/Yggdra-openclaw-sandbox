# Claudes anbefaling

Baseret på adversarial-processen (steelman → red team → steelman RT → neutral evaluator).

**Dette er min vurdering. Yttre beslutter selv.**

---

## Hvad den neutrale evaluator konkluderede

Red team vandt. Kernepointen: systemet virker allerede. Burden of proof er på anbefalingen.

Tre angreb ingen kunne imødegå:
1. **Bash-first brud** — MCP-servere er runtime-processer, ikke bash-scripts
2. **18 deliverables** — kapacitetsproblem for solo-developer med fuldtidsjob
3. **Nul-baseline** — 17 sessions uden disse tools. Hvad blokerer konkret?

## Anbefalet: 1 MCP + 2 skills

| # | Hvad | Hvorfor | Solnedgangsklausul |
|---|------|---------|-------------------|
| 1 | **Playwright MCP** | Browser-automation for TransportIntra QA. Ægte capability-gap. | Ikke brugt efter 3 sessioner → fjern |
| 2 | **Code review skill** (requesting-code-review, Superpowers) | Solo-developer blind spot. Markdown, nul risiko. | Evaluér efter 2 sessioners brug |
| 3 | **Security audit skill** (Trail of Bits) | Live webapp + root SSH = reel angrebsflade. | Evaluér efter første audit |

## Qdrant: bash først, MCP senere

Det nuværende `ctx`-alias + SSH virker. Forbedret bash-wrapper først. MCP kun ved bevist utilstrækkelighed — og kun når tunneling-problemet har en clean løsning.

## Parkeret (genbesøg ved konkret behov)

Alt andet fra research: Calendar, Sheets, Context7, writing-plans, TDD, brainstorming, git-worktrees, research-digest, session-state.

Ikke droppet — parkeret. Kompendiet eksisterer som opslagsværk når behovet opstår.

## Adversarial-processen

Fuld dokumentation i `research/adversarial/`:
- steelman.md — forsvar af original anbefaling
- red-team.md — angreb på planen
- steelman-red-team.md — styrket kritik
- neutral-evaluator.md — saglig syntese
