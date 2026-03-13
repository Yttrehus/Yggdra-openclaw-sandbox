# Session-drift Pipeline

**Dato:** 2026-03-10
**Klar til:** PoC-klar (mangler: implementation af MVP hooks)

## Opsummering
- Nul-friktions session-management via Claude Code hooks (SessionStart, PostToolUse, PreCompact, SessionEnd)
- Research viser: 17 lifecycle events tilgængelige, hooks kan udføre fil-operationer direkte
- Arkitektur i 4 lag: auto-capture → pre-compaction save → state-audit → cross-session timeline

## Origin Story
Opstod fra idé-parkering: "Session-drift pipeline (M7): Automatisér den daglige drift-loop." Yttre mister kontekst mellem sessioner fordi hooks kun *minder* men ikke *udfører*. VPS har fuldt hook-system (save_checkpoint.py + load_checkpoint.sh via Groq) — PC-løsningen skal gøre det samme uden ekstern API.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-06-session-drift-research.md (681 linjer, dato 2026-03-10). Indeholder: komplet lifecycle event-tabel (17 events), gap-analyse, hook-begrænsninger, arkitektur-forslag med kode-eksempler for alle 4 hooks, implementeringsplan i 4 faser, VPS-sammenligning, kilder.

**Fra PLAN.md idé-parkering:**
> Session-drift pipeline (M7): Automatisér den daglige drift-loop: state-capture (NOW.md, PROGRESS.md, chatlog) ved commits, session-kontinuitet ved start, og OODA-baseret løbende state-audit.

## Cowork Output (2026-03-10)

### Hovedkonklusion
Claude Code's hook-system (17 lifecycle events) er fuldt tilstrækkeligt til nul-friktions session-management uden ekstern API. Ingen Groq eller anden service nødvendig.

### Nøgle-hooks
| Hook | Formål |
|---|---|
| **SessionStart** (startup/resume) | Inject NOW.md i Claude's kontekst automatisk |
| **PostToolUse** (Bash matcher) | Auto-dump chatlog ved git commit |
| **PreCompact** (auto/manual) | Gem state til NOW.md FØR context ryddes |
| **SessionEnd** | Arkivér session i PROGRESS.md |

### Arkitektur i 4 lag
1. **Auto-capture:** PostToolUse detekterer `git commit` → kører dump-chatlog.js. SessionStart outputter NOW.md → Claude får context
2. **Pre-compaction save:** PreCompact hook appender snapshot til NOW.md + PROGRESS.md
3. **State-audit:** SessionStart (resume) validerer NOW.md alder, PROGRESS.md eksistens, PLAN.md integritet
4. **Cross-session timeline:** (fremtidig) JSONL event-log over alle sessions

### Gap-analyse
- Git commit detection: hook *minder* → skal *udføre* (auto-dump)
- Session-start context: manuelt → auto-inject NOW.md
- Pre-compaction save: ingenting → state captured automatisk
- State-audit: ingen → konsistens-check ved resume

### Begrænsninger
- Hooks kan IKKE trigge tool calls eller se fremtidigt input
- PostToolUse kan ikke ændre allerede eksekveret resultat
- JSONL transcript format er ikke public API (kan ændre sig)
- Max 10 min timeout per hook (konfigurerbar)

### Sammenligning med VPS (Yggdra)
Samme hook-arkitektur, men PC-løsningen er enklere: ingen Groq API, brute-force transcript dump i stedet for smart summarization. Færre dependencies.

### Implementeringsplan
- **Fase 1 (1-2 timer):** auto-dump-on-commit.sh + SessionStart NOW.md inject. Umiddelbar værdi.
- **Fase 2 (1 time):** pre-compact-save.sh + session-end-archive.sh
- **Fase 3 (1-2 timer):** validate-state.sh (state audit ved resume)
- **Fase 4 (2 timer, optional):** episodes.jsonl cross-session timeline

**Estimat:** 4-6 timer total, < 500 linjer bash/json, nul eksterne dependencies.

### Konfiguration
Komplet `.claude/settings.json` med alle 4 hooks klar. Hook-scripts klar som skeletons.

### Action items
- [ ] Opret .claude/hooks/ directory
- [ ] Implementér auto-dump-on-commit.sh (fase 1)
- [ ] Konfigurér PostToolUse hook i settings.json
- [ ] Implementér SessionStart hook (NOW.md inject)
- [ ] Test: commit + verify hook kører
