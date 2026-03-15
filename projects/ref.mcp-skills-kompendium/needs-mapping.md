# Yggdra-behov → Løsnings-mapping

Hver backlog-brief mappet til konkret løsningstype.

| # | Brief | Behov | Løsningstype | Konkret forslag |
|---|-------|-------|-------------|-----------------|
| 1 | context-engineering | Auto-inject state, pre-compact save, chatlog dump | **Bash hooks** | Claude Code hooks (PreToolUse/PostToolUse). 4-6 timer. |
| 2 | integrationer | Google Calendar, Sheets, Drive | **MCP** | Google Calendar MCP + Google Sheets MCP (samme OAuth som Gmail) |
| 3 | notion-spejling | Synk disk→Notion, mobil-adgang | **Hook + eksisterende MCP** | Notion MCP allerede installeret. Hook-baseret synk. |
| 4 | mcp-skills-kompendium | Audit af MCP/skills landskab | **Meta-projekt** | Dette dokument. |
| 5 | research-architecture | Søg i fragmenteret viden, VPS-synk | **Qdrant MCP eller bash** | Qdrant MCP (direkte) eller forbedret ctx-wrapper (bash-first) |
| 6 | visualisering | Diagrammer, infographics, data-viz | **Eksisterende tools** | Excalidraw MCP (installeret) + Mermaid (VS Code) |
| 7 | voice-integration | Voice-to-text noter/idéer | **Bash script** | Whisper API eller ElevenLabs (allerede betalt) via script |
| 8 | cross-session-peer-review | To sessions reviewer hinanden | **Workflow/skill** | Prompt-template som skill. Ingen tooling nødvendig. |
| 9 | integrationer (bogføring) | Økonomisk overblik | **MCP + data** | Google Sheets MCP. Men data skal indsamles først. |

## Løsningstype-fordeling

- **Bash hooks/scripts:** 3 (context-engineering, voice, notion-synk)
- **MCP:** 3 (Calendar, Sheets, Qdrant)
- **Eksisterende tools:** 2 (visualisering, kompendium)
- **Workflow/skill:** 1 (peer-review)

## Observation
Majoriteten af behov løses med bash eller eksisterende tools. MCP er relevant for Google-integrationer og Qdrant — alt andet er overkill.
