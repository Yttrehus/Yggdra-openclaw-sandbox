# Cross-session Peer Review

**Dato:** 2026-03-12 (opdateret 2026-03-15)
**Klar til:** Backlog

## Opsummering
- To parallelle Claude Code sessioner der reviewer hinandens output
- Yttre fungerer som mediator/dommer mellem sessionerne
- Fanger blinde vinkler i planlægning og beslutninger

## Origin Story
Idéen opstod fra erkendelsen af at en enkelt Claude-session kan have blinde vinkler. Ved at lade to sessioner evaluere hinandens output med Yttre som dommer, får man en form for peer review uden et team.

## Foreslået workflow
1. **Session A** producerer et artefakt (plan, beslutning, arkitektur, CONTEXT.md)
2. **Session B** åbnes med prompt: "Reviewér dette artefakt. Find blinde vinkler, manglende alternativer, og ting der kunne gå galt."
3. **Yttre** vurderer Session B's feedback, bringer relevante pointer tilbage til Session A

## Hvornår bruge det
- Store arkitekturbeslutninger (nyt projekt, ny praksis)
- Planer der påvirker flere projekter
- Når noget "føles rigtigt men måske er for nemt"
- **Ikke** til daglig kodning eller simple tasks

## Minimum viable version
Ingen tooling nødvendig. Bare åbn et nyt Claude Code-vindue og kopier artefaktet ind. Kan forfines med skills/prompts senere.

## Rå input
**Fra PLAN.md idé-parkering:**
> Cross-session peer review: To parallelle sessioner der reviewer hinandens output med Yttre som mediator.
