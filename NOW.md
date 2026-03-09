# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-09
**Status:** M2 afsluttet, M3 næste

## Næste step

M3: Terminal/Shell (WSL) — Zsh, prompt, aliases

## Seneste session (2026-03-09)

- Genoprettede kontekst fra crashed session (Sonnet → Opus)
- Oprettede PLAN.md med fuld historik fra forrige session
- Oprettede repo: github.com/Yttrehus/Basic-setup
- CLAUDE.md fik workflow-regler
- Fixede keybinding: Ctrl+½ → toggle terminal (oem_5)
- Oprettede workspace-fil og NOW.md
- Windows git konfigureret (user, email, SSH-nøgle) → Claude kan selv committe+pushe
- PostToolUse hook: opfanger git commit fra Claude → minder om NOW.md opdatering
- Oprettede global skill: session-state.md (NOW.md/PLAN.md workflow)

## Vigtig kontekst

- Claude Code Bash-tool kører i Windows, ikke WSL
- Windows git er nu konfigureret med SSH — Claude kan commit+push selv
- WSL git bruges til manuelle commits fra terminalen
- PostToolUse hook i ~/.claude/settings.json opfanger Claudes git commits
- Global skill session-state.md gælder alle projekter

## Åbne tråde

- VS Code håndbog (Yttre foreslog det)
- JetBrains Mono font ikke installeret
- Notion-struktur venter
- Context engineering som M5
