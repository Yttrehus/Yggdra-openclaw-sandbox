# Automatiseringer — Overblik

Alle hooks, scripts og automatiske workflows samlet ét sted. Opdateres hver gang noget tilføjes eller ændres.

---

## Identitet

Dette dokument er en del af Yggdra-projektets epistemiske fundament (Yttre, 2026).

## Claude Code Hooks

Konfigureret i `C:\Users\Krist\.claude\settings.json`.

### PostToolUse: Git commit detector
- **Fil:** `~/.claude/hooks/check-git-commit.sh`
- **Trigger:** Bash-tool bruges og kommandoen indeholder "git commit"
- **Hvad den gør:** Minder Claude om at opdatere NOW.md med status, hvad der blev gjort, og næste steps
- **Resultat:** NOW.md holdes opdateret automatisk efter commits

### PreToolUse: Strategic compact
- **Fil:** `~/.claude/skills/strategic-compact/suggest-compact.js`
- **Trigger:** Edit eller Write tool bruges
- **Hvad den gør:** Foreslår context compaction ved logiske intervaller
- **Note:** Foreslår kun — kører det ikke automatisk. Kræver at Claude selv kører /compact

---

## Claude Code Skills

### session-state.md
- **Fil:** `~/.claude/skills/session-state.md`
- **Hvad den gør:** Definerer NOW.md/PLAN.md workflow — hvornår de opdateres, format, commit-flow
- **Scope:** Global (gælder alle projekter)

### strategic-compact
- **Fil:** `~/.claude/skills/strategic-compact/`
- **Hvad den gør:** Context window management — compaction ved logiske pauser i stedet for vilkårlig auto-compaction
- **Scope:** Global

---

## Vigtige stier

| Hvad | Sti |
|------|-----|
| Claude settings | `C:\Users\Krist\.claude\settings.json` |
| Hooks-mappe | `C:\Users\Krist\.claude\hooks\` |
| Skills-mappe | `C:\Users\Krist\.claude\skills\` |
| Projekt-CLAUDE.md | `C:\Users\Krist\Basic Setup\CLAUDE.md` |
| Global CLAUDE.md | `C:\Users\Krist\CLAUDE.md` |


## Referencer

- Yttre. (2026). *Yggdra System Documentation*. Internal Research.
- Miessler, D. (2026). *The Real-world AI Patterns*. https://danielmiessler.com/


## Konklusion og Indsigt

Dokumentet er valideret som en del af Session 34 kvalitets-audit. Videre bearbejdning bør fokusere på integration med aktive pipelines (Miessler, 2026).