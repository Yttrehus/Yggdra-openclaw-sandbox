# Context Engineering

**Dato:** 2026-03-12 (opdateret 2026-03-15)
**Klar til:** Backlog (research udført, PoC-klar for hooks)

## Opsummering
- Systematisér hvordan Claude Code bruges effektivt: CLAUDE.md, compaction, skills, session-management, subagents
- Research udført med 8 kilder (Anthropic officiel + community) — gemt i research/_ARC/context-engineering-research.md
- Trukket ud af PLAN.md M7 som selvstændigt projekt
- **Inkluderer session-drift-pipeline** som Fase 1 (hooks-implementation)

## Origin Story
Startede som M7 i PLAN.md: "Context engineering — Systematisér hvordan Claude Code bruges effektivt." I session 10 blev det klart at dette var for stort til et modul og blev trukket ud som selvstændigt projekt. Research udført: @import syntax, .claude/rules/, compaction-instruktioner, ~80% kontinuitet er realistisk mål.

Session-drift-pipeline (tidl. separat brief) er nu absorberet — det er den konkrete hooks-implementation inden for context engineering-scopet.

## Faser

### Fase 1: Session-drift hooks (PoC-klar, 4-6 timer)
Nul-friktions session-management via Claude Code hooks. Research viser: 17 lifecycle events tilgængelige, hooks kan udføre fil-operationer direkte.

**Nøgle-hooks:**
| Hook | Formål |
|---|---|
| **SessionStart** | Inject NOW.md i Claude's kontekst automatisk |
| **PostToolUse** (Bash matcher) | Auto-dump chatlog ved git commit |
| **PreCompact** | Gem state til NOW.md FØR context ryddes |
| **SessionEnd** | Arkivér session i PROGRESS.md |

**Arkitektur i 4 lag:**
1. Auto-capture: PostToolUse detekterer `git commit` → kører dump-chatlog.js
2. Pre-compaction save: PreCompact hook appender snapshot til NOW.md + PROGRESS.md
3. State-audit: SessionStart (resume) validerer NOW.md alder, PROGRESS.md eksistens
4. Cross-session timeline: (fremtidig) JSONL event-log over alle sessions

**Estimat:** 4-6 timer, <500 linjer bash/json, nul eksterne dependencies.

### Fase 2: CLAUDE.md & skills best practices
1. CLAUDE.md best practices (under 200 linjer, progressive disclosure)
2. Skills-arkitektur (hvad er et skill, hvornår laves et nyt)
3. Subagent-strategi

### Fase 3: Compaction & kontinuitet
1. Compaction-strategi (hvornår, hvordan, hooks)
2. Session-management (state-filer, plan-filer)
3. Mål: ~80% kontinuitet mellem sessions

## Rå input
- **Research:** research/_ARC/context-engineering-research.md (8 kilder, session 10)
- **Session-drift research:** ~/parallel-tasks/output-06-session-drift-research.md (681 linjer, 2026-03-10)
- **VPS reference:** Samme hook-arkitektur som VPS (save_checkpoint.py + load_checkpoint.sh), men PC-løsningen er enklere — ingen Groq API.

## Begrænsninger (hooks)
- Hooks kan IKKE trigge tool calls eller se fremtidigt input
- PostToolUse kan ikke ændre allerede eksekveret resultat
- JSONL transcript format er ikke public API (kan ændre sig)
- Max 10 min timeout per hook (konfigurerbar)
