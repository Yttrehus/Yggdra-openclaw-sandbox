# AI Tools & Resources — Uge 10, 2026

Researched 8. marts 2026.

## 1. Context Mode — MCP-server til kontekst-komprimering

**Repo:** https://github.com/mksglu/context-mode (2.9k stars, MIT)
**Blog:** https://mksg.lu/blog/context-mode
**Install:** `claude mcp add context-mode -- npx -y context-mode`

### Hvordan det virker
- Spawner en isoleret sandbox per tool-kald
- Rå output (logs, CSV, git-output) komprimeres før det rammer kontekstvinduet
- Eksempel: 56 KB Playwright-snapshot → 299 bytes, 85 KB CSV → 222 bytes
- SQLite FTS5 til knowledge base (markdown chunked efter headings, BM25-ranking)
- Session continuity: fil-edits, git-ops, fejl trackes i SQLite
- PreToolUse hook intercepter tool-output og router gennem sandbox
- Understøtter 11 runtimes (JS, TS, Python, Shell, Ruby, Go, Rust, PHP, Perl, R, Elixir)

### 98%-påstanden — delvist sand
- Holder for specifikke scenarier (store Bash-outputs, log-analyse, CSV-parsing)
- Sessioner går fra ~30 min til ~3 timer før degradering — reelt nyttigt
- **Kan IKKE intercepte MCP-tool responses** — kun built-in tools (Bash, Curl, WebFetch)
- MCP-tools bruger JSON-RPC direkte til modellen, ingen PostToolUse hook
- Prompt caching gør verbose kontekst billigt alligevel — man bytter potentielt caching-fordele
- Uden hooks (fx Codex CLI) falder compliance til ~60%

### Vurdering for Ydrasil/Yggdra
- **Pro:** Længere sessioner, simpel SQLite FTS5, nem installation
- **Contra:** Vores setup bruger mange MCP-tools (Notion, Figma, YouTube) som ikke komprimeres. Vi har allerede save_checkpoint + episodes til session continuity. Kræver Node.js/npx.
- **Verdict:** Legitimt, men ikke game-changer. Kan eksperimenteres med ved behov.

### HN-diskussion
https://news.ycombinator.com/item?id=47193064
- Bedre tool-curation og subagent-delegation giver lignende fordele uden ekstra lag

---

## 2. Anthropic Academy — 13 gratis kurser

**URL:** https://anthropic.skilljar.com/
**GitHub:** https://github.com/anthropics/courses
**Lanceret:** 2. marts 2026. Gratis, email-signup, certifikat ved gennemførelse. Creative Commons.

### Relevante developer-kurser (5 stk)

1. **Claude Code in Action** (21 lektioner, ~1 time)
   - CLAUDE.md memory, slash commands, Hooks, MCP-server connections, SDK embedding

2. **Building with the Claude API** (16 lektioner)
   - Tool Use, RAG pipelines, Extended Thinking, Prompt Caching, MCP, Agent/Workflow patterns

3. **Introduction to Agent Skills**
   - Markdown-baserede Skills, team-distribution

4. **Introduction to Model Context Protocol** (8 lektioner)
   - Byg MCP servers/clients i Python, Tools/Resources/Prompts primitiver

5. **MCP Advanced Topics** (8 lektioner)
   - Sampling, Notifications, Transport (stdio, SSE, Streamable HTTP)

### Kan springes over
- Claude 101, AI Fluency, educator/student/nonprofit — for basalt
- Claude with Amazon Bedrock, Claude with Google Vertex AI — ikke relevant for VPS

### Mest nyttigt for os
- **Agent Skills** — officielle best practices for slash-command/skill-arkitektur
- **MCP Advanced Topics** — Streamable HTTP transport, kan erstatte bash-scripts med MCP-tools
- **Claude Code in Action** — hurtigt gennemløb for tips om Skills og SDK embedding
- **API-kurset** — Agent/Workflow patterns-sektionen

---

## 3. Claude Code Økosystem — komplet kortlægning

25+ repos og kilder researched og evalueret i separat rapport med Technology Radar.
**Se:** `research/claude_code_ecosystem_2026.md`

Highlights: 7 hovedemner, gap-analyse mod Yggdra, PC-Setup Guide, top 10 skills at starte med.

---

## 4. Andre nyheder uge 10

- **Claude-File-Recovery** — tool til at gendanne filer fra ~/.claude sessions
- **Claude Code v2.1.66-69** — nye versioner med `/claude-api` skill
- **Claude AI platform-fejl** — øgede fejl rapporteret på platformen
