# Claude Code Økosystem — Kortlægning, Evaluering & Technology Radar

**Dato:** 8. marts 2026
**Scope:** 25+ repos, 8 hovedemner, 1.500+ skills kortlagt (top 10 evalueret i dybden), 6 nøglekilder absorberet
**Metode:** Se [Metode & Abstract](#metode--abstract)

---

## Indhold

1. [Abstract](#abstract)
2. [Metode](#metode)
3. [Hovedemner med absorberet dybdeviden](#hovedemner)
   - A. Udviklingsmiljø
   - B. Visuelt Dashboard (Notion)
   - C. Skills & Plugins
   - D. Hukommelse & Session Persistence
   - E. Workflow & Projektmetodik
   - F. Subagent-arkitektur
   - G. Reference & Læringsressourcer
   - H. Visuelle værktøjer (diagrammer, infographics)
4. [Yggdra vs. Økosystemet — Gap-analyse](#yggdra-vs-økosystemet)
5. [Technology Radar](#technology-radar)
6. [Dybdeanbefalinger](#dybdeanbefalinger)
7. [PC-Setup Guide (autoritativ implementeringsplan)](#pc-setup-guide-autoritativ-implementeringsplan)
8. [Vedligeholdelse](#vedligeholdelse)
9. [Åbne spørgsmål](#åbne-spørgsmål)
10. [Kendte issues](#kendte-issues)
11. [Komplet link-katalog](#komplet-link-katalog)

---

## Abstract

Claude Code-økosystemet er eksploderet i Q1 2026. 25+ repos og kilder er kortlagt på tværs af 8 hovedemner; top 10 skills er evalueret i dybden. Rapporten identificerer 7 tools til umiddelbar adoption, 7 til aktiv eksperimentering, 9 til overvågning, og 7 til parkering. Gap-analysen viser at Yggdra er foran community på struktur (projekt-isolation, episodisk log, checkpoint-safeguards) men bagud på retrieval-kvalitet (progressive disclosure, hybrid search, auto-promotion). De to komplementerer hinanden. Rapporten inkluderer absorberet dybdeviden fra 6 nøglekilder (ECC, GSD, claude-mem, officielle skills/hooks docs, claude-code-showcase), en ny sektion om visuelle værktøjer, samt konkrete implementerings- og vedligeholdelsesanbefalinger.

---

## Metode

### Forskningsproces

**Fase 1: Bred kortlægning (session 8/3-2026, ~2 timer)**
- Systematisk gennemgang af GitHub repos via `gh` CLI og WebFetch
- Kilderne fundet via: Anthropic officielle repos, community awesome-lists, HN-diskussioner, YouTube
- Alt rå data gemt i `research-dump-claude-code-ecosystem.md` (363 linjer)
- Grupperet i 7 hovedemner med abstracts

**Fase 2: Dybdeabsorption (5 parallelle agenter, ~8 min each)**
- 6 nøglekilder læst i dybden: README, kildekode, config-filer, templates
- Agenterne fik specifikke ekstraktionsmål (schema, hooks, workflows, patterns)
- 1 agent gik i stå og blev manuelt erstattet (PRD+Skills — se [Kendte issues](#kendte-issues))
- Officielle docs (skills, hooks) hentet direkte fra code.claude.com

**Fase 3: Evaluering via Technology Radar**
- ThoughtWorks-model: Adopt/Trial/Assess/Hold
- 4 evalueringskriterier: modenhed, relevans, kost/risiko, overlap med eksisterende
- Gap-analyse mod Yggdra's nuværende setup

**Fase 4: Intern review (3 runder red/blue/neutral)**
- Red team: angriber anbefalinger, finder svagheder
- Blue team: forsvarer sagligt eller indrømmer
- Neutral: dommer, implementerer ændringer

**Værktøjer brugt:** `gh` CLI, WebFetch, 5 parallelle Agent-subprocesser, Grep/Glob for lokal kildekode

**Begrænsninger:**
- Star-counts bruges som popularitetsindikator, ikke kvalitetsgaranti. Ingen af kilderne publicerer brugerdata eller retention-metriker.
- Token-besparelsestal (f.eks. claude-mem's "~10x") er fra kildernes egne benchmarks, ikke verificeret mod Yggdra.
- Intern adversarial review (3 runder) blev gennemført efter rapportens første udkast og resulterede i 9 korrektioner.

### Hvordan dette reproduceres
1. Start med research-dump filen som input
2. Identificér 5-8 nøglekilder der kræver dybdelæsning
3. Kør parallelle agenter med specifikke ekstraktionsmål
4. Syntetiser til rapport med Technology Radar
5. Kør 3 runder intern adversarial review
6. Implementér ændringer fra review

---

## Hovedemner

### A. Udviklingsmiljø (IDE + Setup)

Valg af IDE og development environment for PC-Yggdra. VS Code er standard med officiel Claude Code extension. Google Antigravity tilbyder gratis Opus 4.6-adgang via browser. Antigravity Manager kan fungere som proxy for gratis model-adgang. Cursor overlapper med Claude Code og tilføjer ikke unik værdi.

**Nøglefund:**
- VS Code + Claude Code extension = den officielle, bedst supporterede vej
- Antigravity = gratis alternativ, men browser-baseret (ikke lokal)
- Antigravity Manager = interessant proxy-hack, CC-BY-NC-SA licens
- TabGroupSaver = nyttigt til multi-projekt kontekstskift i VS Code

**Kilder:** VS Code docs, Antigravity reviews, lbjlaq/Antigravity-Manager, TabGroupSaver

---

### B. Visuelt Dashboard (Notion)

Notion som visuelt lag ovenpå IDE — dashboards, tasks, research-databaser. Built-in MCP allerede aktiv i Yggdra. Officielt Notion-plugin tilføjer 4 skills og 10 slash commands. Kan erstatte droppet Trello som task-board.

**Nøglefund:**
- MCP allerede aktiv med 10 tools (search, fetch, create, update, etc.)
- Officielt plugin fra Notion selv: 4 skills (Knowledge Capture, Meeting Intelligence, Research Documentation, Spec to Implementation)
- Views (Kanban, Kalender) kræver manuelt Notion UI — kan ikke oprettes via MCP
- Cowork-mode bug: tools forsvinder efter første prompt (Issue #18680)
- Video-konklusion: Claude Code + Notion virker, men debugging er svært

**Kilder:** Notion MCP docs, makenotion/claude-code-notion-plugin, video KPZ3BX2l70I

---

### C. Skills & Plugins Økosystem

Det officielle Agent Skills standard (agentskills.io) plus 5 community skill-repos med tilsammen 1.500+ skills. Anthropic har 13 officielle plugins. Skill-markeder under opbygning men umodne.

**Absorberet dybdeviden — Officielle Skills docs:**
- **Frontmatter-felter:** `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`
- **`context: fork`:** Spawner isoleret subagent. Skill-indhold bliver task-prompt. Agent-type bestemmer værktøjer og model. Resultat returneres til hovedsamtale.
- **`!`command``:** Shell-kommandoer kører FØR skill-indhold sendes til Claude. Output erstatter placeholder. Preprocessing, ikke runtime.
- **`$ARGUMENTS`:** Erstattes med brugerens input. `$ARGUMENTS[0]`/`$0` for positionelle argumenter.
- **`/batch`:** Dekomponerer opgave i 5-30 uafhængige units, spawner én agent per unit i isoleret git worktree, hver åbner PR.
- **`/simplify`:** 3 parallelle review-agenter (code reuse, quality, efficiency).
- **Skill-budget:** 2% af context window, fallback 16.000 chars. Override: `SLASH_COMMAND_TOOL_CHAR_BUDGET`.
- **Discovery:** Nested `.claude/skills/` i subdirectories auto-discoveres. `--add-dir` skills loades automatisk.

**Absorberet dybdeviden — ECC (65.8k stars):**
- **Token-optimering:** Hold under 10 MCP enabled / 80 tools aktive. 200K context shrinks til ~70K med for mange tools. Erstat MCP med CLI-wrapped skills.
- **Model-selektion:** Haiku til exploration/docs. Sonnet til 90% af coding. Opus kun ved fejl, 5+ filer, arkitektur, sikkerhed.
- **Dynamisk kontekst:** `claude --system-prompt "$(cat memory.md)"` injicerer med højere autoritet end standard. Aliases per workflow-mode.
- **Strategisk kompaktering:** Manuel kompaktering ved logiske intervaller. `suggest-compact.js` hook minder om dette.
- **Verifikationsmetrik:** pass@k (mindst 1 af k lykkes) vs pass^k (alle k skal lykkes). k=1: 70%. k=3: pass@k=91%, pass^k=34%.
- **Skill-audit:** `/skill-stocktake` — Quick Scan (5-10 min) eller Full Stocktake (20-30 min). Verdicts: Keep, Improve, Update, Retire, Merge.

**Nøglefund (uændret):**
- **Officielle plugins (13 stk):** hookify, security-guidance, commit-commands, ralph-wiggum, feature-dev, code-review, plugin-dev, pr-review-toolkit, frontend-design, explanatory-output-style, learning-output-style, agent-sdk-dev, claude-opus-4-5-migration
- **alirezarezvani (2.3k stars, 160+ skills):** Self-Improving Agent, RAG Architect, MCP Server Builder
- **Jeffallan (5.6k, 66 skills):** `/common-ground`, Jira/Confluence workflows
- **VoltAgent (127+ subagents):** 10 domæner, isolerede kontekstvinduer
- **Antigravity Awesome (21.6k, 1.232 skills):** Største samling, varierende kvalitet
- **Nano Banana Pro Prompts:** 10.000+ kuraterede Gemini-billedprompts

**Kilder:** anthropics/skills, code.claude.com/docs/en/skills, anthropics/claude-code, ECC, alirezarezvani, Jeffallan, VoltAgent

---

### D. Hukommelse & Session Persistence

Løsninger for at bevare kontekst på tværs af sessions. Fra simple (MEMORY.md + checkpoint) til avancerede (claude-mem med SQLite+Chroma+progressive disclosure).

**Absorberet dybdeviden — claude-mem (33.4k stars):**

*Progressive disclosure — 3-lags MCP:*
1. **`search(query)`** (~50-100 tokens/resultat) — Returnerer kompakt indeks: observation IDs, titler, datoer. Ingen fuldt indhold. Filtrering: project, type, dateStart/End.
2. **`timeline(anchor=ID)`** (~200-300 tokens) — Kronologisk kontekst omkring en observation. Parameters: depth_before, depth_after, project.
3. **`get_observations([IDs])`** (~500-1000 tokens/resultat) — Kræver eksplicit ID-array. Ingen "get all" mulighed. Tvinger pre-filtrering.
4. **`__IMPORTANT`** — Dokumentations-tool der lærer 3-lags workflow til Claude.
5. **`smart_search`** — Tree-sitter AST codebase search med folded views.
6. **`smart_outline`** — Fil-struktur overblik med foldede bodies.

*SQLite FTS5 Schema:*
- **7 migrationer**, WAL mode, 256MB mmap, 10K page cache
- **Kernetabeller:** sessions, memories, overviews, diagnostics, transcript_events, sdk_sessions, observations, session_summaries
- **Observations-felter:** id, memory_session_id, project, text, type, created_at, discovery_tokens
- **Session summaries:** request, investigated, learned, completed, next_steps, files_read, files_edited, notes
- **FTS5 virtuelle tabeller:** observations_fts (title, subtitle, narrative, text, facts, concepts), session_summaries_fts (request, investigated, learned, completed, next_steps, notes). Auto-sync via triggers.

*Chroma Vector DB:*
- Via MCP stdio transport — ingen npm dependency
- **Granulær embedding:** Hvert felt bliver separat Chroma-dokument (obs_ID_narrative, obs_ID_fact_0, etc.)
- **Ikke hybrid:** Chroma = semantic search, SQLite FTS5 = keyword search. Separate systemer.
- **Dedup:** Multiple Chroma docs → én SQLite observation. Best-ranked distance vinder.
- **Backfill:** Inkrementel batches af 100.

*Token-besparelse:*
- **Niveau 1:** AI-kompression af rå tool-output til strukturerede observations (discovery_tokens → read_tokens)
- **Niveau 2:** Progressive disclosure — scanning 20 resultater koster ~1-2K tokens vs ~10-20K for fuldt indhold
- **Formel:** `savings_pct = (discovery_tokens - read_tokens) / discovery_tokens * 100`

**Absorberet dybdeviden — ECC Continuous Learning v2.1:**

*Instinct-struktur:*
```yaml
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7          # 0.3=tentativ, 0.5=moderat, 0.7=stærk, 0.9=nær-sikker
domain: "code-style"     # code-style, testing, git, debugging, workflow
scope: project           # project (default) eller global
project_id: "a1b2c3d4e5f6"  # hash af git remote URL
```

*Observation pipeline (observe.sh):*
- Fires på HVER PreToolUse og PostToolUse (hooks = 100% reliable vs skills ~50-80%)
- Scrubber secrets via regex. Auto-arkiverer ved 10MB. Purger >30 dage.
- Project-scoped via git remote URL hash — React patterns stays i React projects.
- Evolution: instincts → skills/commands/agents via `/evolve`. Global promotion ved same instinct i 2+ projekter med avg confidence >= 0.8.

*ECC Hook-profiler:*

| Hook | minimal | standard | strict |
|------|---------|----------|--------|
| Session start/end, cost tracking | JA | JA | JA |
| Quality gates, auto-format, TS check | - | JA | JA |
| Continuous learning observe | - | JA | JA |
| Pre-compact state save | - | JA | JA |
| tmux + git push reminders | - | - | JA |

**Absorberet dybdeviden — Self-Improving Agent (alirezarezvani):**
- `/si:review` — analysér memory for promotion candidates
- `/si:promote` — graduér patterns fra MEMORY.md til CLAUDE.md
- `/si:extract` — konvertér patterns til standalone skills
- `/si:status` — memory capacity dashboard

**Yggdra allerede har:** save_checkpoint.py, load_checkpoint.sh, episodes.jsonl, NOW.md per projekt. Mangler: progressive disclosure, vector-baseret retrieval i hooks, auto-promotion, granulær observation-extraction.

---

### E. Workflow & Projektmetodik

Strukturerede udviklings-workflows der løser context rot ved store opgaver.

**Absorberet dybdeviden — GSD (26.1k stars):**

*STATE.md — slim pointer-fil (<150 linjer):*
- Project Reference (pointer til PROJECT.md, current focus)
- Current Position (Phase X of Y, status, ASCII progress bar)
- Performance Metrics (velocity, per-phase tabel, trend)
- Accumulated Context (decisions, pending todos, blockers)
- Session Continuity (timestamp, stopped-at, resume path)
- Opdateres via CLI: `gsd-tools.cjs state advance-plan`

*6-trins workflow i detaljer:*
1. **`/gsd:new-project`** — Deep questioning → 4 parallelle research agenter → v1/v2/out-of-scope requirements med REQ-IDs → PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md
2. **`/gsd:discuss-phase N`** — Loader alle prior decisions → scouts codebase → 3-4 gray areas → 4-question deep-dive per area → `{phase}-CONTEXT.md`
3. **`/gsd:plan-phase N`** — gsd-phase-researcher → gsd-planner (2-3 task plans, XML) → gsd-plan-checker (op til 3 revisioner) → PLAN.md filer
4. **`/gsd:execute-phase N`** — Grupperer i waves → fresh subagent per plan (200K ren kontekst) → atomic git commit per task → deviation rules 1-3 auto, regel 4 stopper
5. **`/gsd:verify-work N`** — UAT per deliverable → debug agents → fix plans
6. **Repeat** / `/gsd:complete-milestone` / `/gsd:new-milestone`

*Wave execution:*
- PLAN.md frontmatter: `wave: N`, `depends_on: [plan-IDs]`
- `wave = max(dependency_waves) + 1`. Ingen dependencies = Wave 1.
- Inden for wave: parallel. Mellem waves: sekventiel.
- Config: `max_concurrent_agents: 3`, `min_plans_for_parallel: 2`
- Vertical slices > horizontal layers. Ingen overlappende filer.
- Spot-check efter hver wave: filer eksisterer, git commits matcher, ingen FAILED markers.

*Fresh context per task — teknisk implementering:*
- Hver plan eksekveres af spawnet subagent (Task tool) med 200K ren context
- Subagent loader: PLAN.md, config.json, STATE.md (kun paths), CLAUDE.md, skills
- Subagent loader IKKE: session history, fuldt project context, decision logs
- 3 patterns: A (autonomous), B (segmented med checkpoints), C (main-context for user back-and-forth)
- Orchestrator stays ved 10-15% context utilization

*Spec-format (PLAN.md):*
```yaml
---
phase: XX-name
plan: NN
type: execute|tdd
wave: N
depends_on: []
files_modified: []
autonomous: true|false
requirements: [REQ-01, REQ-02]
must_haves:
  truths: []      # Observable behaviors (user-perspektiv)
  artifacts: []   # Filer der skal eksistere
  key_links: []   # Kritiske forbindelser
---
```
- Tasks i XML: `<task type="auto" tdd="true">` med name, files, description, behavior, implementation, done_criteria, verification
- Sizing: 15-60 min Claude execution per task, 2-3 tasks per plan, target ~50% context

*4 deviation rules:*
1. Bug → auto-fix
2. Missing Critical (error handling, validation, auth) → auto-add
3. Blocking (missing deps, broken imports) → auto-fix
4. Architectural → STOP og spørg bruger

*Context monitor hook:*
- PostToolUse: warning ved 35% remaining, critical ved 25%: "stop immediately, save state"

**Absorberet dybdeviden — claude-code-showcase (5.5k stars):**

*Skill Evaluation Hooks — 3 lag:*
1. **`skill-eval.sh`** — Bash wrapper på UserPromptSubmit. Piper stdin til JS. Exit 0 altid.
2. **`skill-eval.js`** (~300 linjer) — 7 signaltyper: Keywords (score 2), Keyword patterns (3), Path patterns (4), Directory mapping (5), Intent patterns (4), Content patterns (3), Context patterns (2). Min confidence 3, top 5, exclude patterns.
3. **`skill-rules.json`** — 19 skills defineret med triggers, excludePatterns, priority, relatedSkills.

*Quality Gate Hooks:*
- **PreToolUse (Edit|Write):** Main branch protection — exit 2 med `{"block": true}` hvis på main
- **PostToolUse (Edit|Write):** Auto-format (Prettier), auto-install (npm), auto-test, type-check (tsc --noEmit). Alle non-blocking (exit 0).

*GitHub Actions (4 workflows):*
1. **Monthly Docs Sync** — 1. i måneden, 30 max-turns, 60 min timeout
2. **Weekly Code Quality** — Søndag, 3 random src/ dirs i parallel, 35 turns, 45 min
3. **Biweekly Dependency Audit** — 1. og 15., npm outdated + audit, reverts ved test-fejl
4. **PR Code Review** — Auto på PR creation

**Kilder:** gsd-build, ChrisWiles/claude-code-showcase, code.claude.com/docs/en/hooks, shanraisshan/best-practice

---

### F. Subagent-arkitektur & Multi-agent

Design af specialiserede subagenter med definerede kontekstbudgetter og handoff-formater.

**Absorberet dybdeviden — Officielle Hooks docs:**

*17 hook events:*
| Event | Trigger | Blocking |
|-------|---------|----------|
| SessionStart | Session begynder/genoptages | Nej |
| UserPromptSubmit | Prompt submitted | Ja (kan ændre) |
| PreToolUse | Før tool call | Ja (kan blokere/deny) |
| PermissionRequest | Permission dialog | Ja |
| PostToolUse | Efter succesfuld tool call | Feedback |
| PostToolUseFailure | Efter fejlet tool call | Feedback |
| Notification | Notification sendt | Nej |
| SubagentStart | Subagent spawned | Nej |
| SubagentStop | Subagent færdig | Nej |
| Stop | Claude færdig med svar | Nej |
| TeammateIdle | Agent team teammate idle | Nej |
| TaskCompleted | Task markeret completed | Nej |
| InstructionsLoaded | CLAUDE.md/.claude/rules loaded | Nej |
| ConfigChange | Config ændret under session | Nej |
| WorktreeCreate | Worktree oprettes | Erstatter default git |
| WorktreeRemove | Worktree fjernes | Nej |
| PreCompact | Før kontekst-komprimering | Nej |
| SessionEnd | Session terminerer | Nej |

*Matcher-patterns (regex):*
- PreToolUse/PostToolUse: tool name (`Bash`, `Edit|Write`, `mcp__.*`)
- SessionStart: `startup`, `resume`, `clear`, `compact`
- PreCompact: `manual`, `auto`
- UserPromptSubmit, Stop, TaskCompleted: ingen matcher, fires altid

*Hook handler output format:*
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string"
  }
}
```

*Hook locations (prioritet):*
Managed policy > `~/.claude/settings.json` > `.claude/settings.json` > `.claude/settings.local.json` > Plugin hooks > Skill/agent frontmatter

**NicholasSpisak subagents:**
- 9 specialiserede personas: backend-reliability, frontend-ux, systems-architect, security-threat, performance-optimizer, code-analyzer, refactoring-expert, qa-test, technical-mentor
- Designprincip: specialization over generalization, evidence-based, security by default
- Prioritetshierarkier per agent (frontend: UX > accessibility > performance; backend: reliability > security > performance)
- *Note: Kontekst-budgetter (50%/70%/85%) nævnt i den oprindelige research-dump kunne ikke verificeres mod repoen. Princippet (hold context lav) er almengyldigt, men de specifikke tal bør behandles som ubekræftede.* [ISS-002]

**Kilder:** code.claude.com/docs/en/hooks, NicholasSpisak, VoltAgent, anthropics/skills docs

---

### G. Reference & Læringsressourcer

Kurser, cookbooks og reference-materiale. Ikke til installation — til læring.

**Nøglefund:**
- **Anthropic Academy (13 kurser, gratis):** 5 relevante developer-kurser. "Claude Code in Action" (1 time) og "Introduction to Agent Skills" er mest relevante. Certifikat ved gennemførelse.
- **claude-cookbooks (34.4k stars):** Praktiske recipes for RAG, tool use, PDF, vision, SQL, sub-agents.
- **claude-quickstarts (15.1k stars):** Autonomous Coding Agent (to-agent pattern), Computer Use Demo.
- **Agent SDK Python (5.2k stars):** Custom agents i Python.
- **awesome-ai-system-prompts:** Claude Code's interne system prompt som reference.
- **awesome-llm-apps (100k stars):** Bred samling af LLM-applikationer, RAG tutorials, knowledge graph RAG.

---

### H. Visuelle værktøjer (diagrammer, infographics)

Tools til at generere diagrammer, infographics og visuel dokumentation programmatisk.

**Absorberede kilder:**

| Tool | Stars | Stack | Hvad det gør | Relevans |
|------|-------|-------|--------------|----------|
| **[mermaid](https://github.com/mermaid-js/mermaid)** | 86.5k | JS/TS | Markdown-baserede diagrammer → SVG. Flowcharts, sequence, Gantt, class, state, Git graphs, C4. Native GitHub rendering. | **Høj.** Allerede delvist brugt (docs/system_anatomy.mmd). Kan embeddes i webapp. Ingen deps for browser-rendering. |
| **[diagrams](https://github.com/mingrammer/diagrams)** | 42.1k | Python | Cloud infrastruktur-diagrammer i Python-kode. AWS/GCP/K8s/On-Premises/Generic/C4. `>>` operators, Graphviz render. | **Høj.** Python-baseret (passer vores stack). Versionerbare diagrammer. Kræver Graphviz. |
| **[AntV Infographic](https://github.com/antvis/Infographic)** | 4.6k | TypeScript | Deklarativ infographic-generering. ~200 built-in templates. AI agent skills integration. Streaming render. SVG output. | **Medium.** AI-optimeret — Claude kan generere configs direkte. 200 templates giver hurtige resultater. |
| **[OpenDraft](https://github.com/federicodeponte/opendraft)** | 55 | Python | 19-agent pipeline til akademiske research drafts (20K+ ord, ~10 min). Citations mod CrossRef/OpenAlex/Semantic Scholar/arXiv. Export: PDF, Word, LaTeX. | **Medium.** Interessant for forskning-projektet. Bruger samme akademiske APIs som `scripts/research.py`. Lav adoption (55 stars). |
| **[LaTeX2AI](https://github.com/isteinbrecher/LaTeX2AI)** | 306 | C++ | Adobe Illustrator plugin for LaTeX-labels. | **Lav.** Kræver Adobe Illustrator. Desktop-only. |
| **[benbrastmckie/nvim](https://github.com/benbrastmckie/nvim)** | 434 | Lua | NeoVim config for LaTeX + akademisk arbejde. Claude Code + Avante integration. | **Lav.** Reference for NeoVim-integration, ikke et diagram-tool. |

**Anbefaling:** Mermaid (allerede i brug) + diagrams (Python, passer stack) som primære. AntV Infographic som trial for AI-genererede visuels. OpenDraft som assess for forskning.

---

## Yggdra vs. Økosystemet — Gap-analyse

### Hvad Yggdra allerede har (og som valideres af økosystemet)

| Yggdra-feature | Økosystem-ækvivalent | Status |
|----------------|---------------------|--------|
| `projects/*/NOW.md` — state per projekt | GSD's `STATE.md` (<150 linjer, slim pointers), RPI's `thoughts/shared/` | **Valideret.** Yggdra's pattern er mainstream. GSD tilføjer: performance metrics, ASCII progress bar, CLI-opdatering. |
| `projects/*/CONTEXT.md` — identitet per projekt | ECC's per-project CLAUDE.md, GSD's PROJECT.md | **Valideret.** GSD splitter yderligere: PROJECT.md (hvad), REQUIREMENTS.md (krav), ROADMAP.md (plan). |
| `save_checkpoint.py` + `load_checkpoint.sh` — session persistence | ECC's session-start.js/session-end.js, claude-mem's 6 hooks | **Valideret.** Vi har det. ECC tilføjer: HTML comment markers for idempotent updates, transcript parsing, cost tracking. |
| `episodes.jsonl` — episodisk log | claude-mem's observations + session_summaries, ECC's instincts | **Valideret men primitivt.** claude-mem har 7 tabeller, FTS5, granulære observations. ECC har confidence scoring + project scoping. |
| Hooks (PreCompact, Stop, SessionStart, Notification) | 17 officielle hook events, ECC's 3 profiler, showcase's quality gates | **Delvist.** Vi bruger 4 events. Officielt er der 17. Mangler: UserPromptSubmit, PostToolUse, SubagentStart/Stop, ConfigChange. |
| `ctx` — Qdrant-baseret kontekstsøgning | claude-mem's SQLite FTS5 + Chroma (separate), ECC's search-first | **Delvist.** Vi har vektor-søgning. Mangler: progressive disclosure (3-lags), FTS5 for keyword, granulær per-felt embedding. |
| CLAUDE.md < 200 linjer | Best practice + ECC: skill-budget = 2% af context window | **Valideret.** ECC tilføjer: `SLASH_COMMAND_TOOL_CHAR_BUDGET` override, `/skill-stocktake` audit. |
| `MEMORY.md` — auto-memory | claude-mem's SQLite + Chroma, Self-Improving Agent, ECC's instincts | **Delvist.** Vi har flat-file. Mangler: auto-promotion (si:promote), confidence scoring, project-scoped memories. |
| Bash-first, scripts over services | ECC: "erstat MCP med CLI-wrapped skills" | **Valideret og forstærket.** ECC bekræfter: CLI-wrappers > always-loaded MCPs for token-besparelse. |

### Hvad Yggdra mangler (opdateret med dybdeviden)

| Gap | Hvad community har | Prioritet | Kompleksitet |
|-----|--------------------|-----------|--------------|
| **Progressive disclosure** | claude-mem: 3-lags MCP, tvungen pre-filtrering, ~10x token-besparelse | **Høj** | Høj (AGPL, Bun, Chroma) |
| **Hybrid search** | Qdrant understøtter det. claude-mem bruger separate: FTS5 + Chroma. | **Høj** | Medium (Qdrant config) |
| **Quality gate hooks** | Showcase: PreToolUse branch protection (exit 2 + block), PostToolUse auto-format/test | **Høj** | Lav (bash scripts) |
| **Context monitor** | GSD: PostToolUse warning ved 35%, critical ved 25% remaining | **Høj** | Lav (JS hook) |
| **Observation extraction** | claude-mem: rå tool output → structured observations med title/subtitle/narrative/facts | **Medium** | Høj (kræver worker agent) |
| **Instinct/confidence scoring** | ECC v2.1: atomic instincts med 0.3-0.9 confidence, project-scoped, auto-evolve | **Medium** | Medium (hooks + storage) |
| **Auto-promotion** | Self-Improving Agent: /si:review → /si:promote → /si:extract | **Medium** | Lav (plugin install) |
| **Fresh context per task** | GSD: subagent med 200K ren context, orchestrator ved 10-15% | **Medium** | Lav (allerede muligt via Task tool) |
| **Officielle plugins** | hookify, security-guidance, commit-commands | **Høj** | Lav (plugin install) |
| **Wave execution** | GSD: dependency mapping → waves → parallel subagents → spot-check | **Lav** | Høj (kræver GSD install) |

### Hvad Yggdra gør bedre

1. **Projekt-isolation med CONTEXT.md + NOW.md.** GSD har lignende (PROJECT.md + STATE.md) men Yggdra's multi-projekt model er mere fleksibel — GSD opererer per-projekt.
2. **Episodisk hukommelse via billig LLM.** episodes.jsonl + Groq destillering. Ingen community-løsning har automatisk session-destillering via billig LLM. claude-mem bruger en fuld Claude-instans som worker.
3. **Checkpoint-safeguards.** 10-min throttle, 80KB cap, hash-dedup. Ikke observeret i ECC's session-end eller claude-mem, men kan eksistere under andre navne i repos vi ikke har undersøgt.
4. **Kill conditions.** Eksplicit anti-pattern i CLAUDE.md. Ikke identificeret i de evaluerede repos, men princippet kan være implicit i andre workflows.
5. **Qdrant med 84K vektorer.** claude-mem bruger Chroma (via MCP, overhead). ECC bruger flat files. Yggdra har allerede production-grade vektor-DB.
6. **Moden vektor-search infrastruktur.** `ctx` med 7 collections, advisor-brain, miessler-bible. Community starter fra scratch.

---

## Technology Radar

### ADOPT (installér/brug nu)

| Tool | Kategori | Begrundelse |
|------|----------|-------------|
| **VS Code + Claude Code Extension** | IDE | Officiel, bedst supporteret. Klar til PC-Yggdra. |
| **Notion MCP (built-in)** | Dashboard | Allerede aktiv. Brug til tasks, research-databaser, dashboards. |
| **Anthropic Academy** | Læring | Gratis, officielt. Start med "Agent Skills" + "Claude Code in Action". |
| **Officielle plugins (hookify, security-guidance, commit-commands)** | Skills | 0-risk, officiel kilde. hookify til hook-management, security-guidance for 9 mønstre. |
| **Officiel skills/hooks docs** | Reference | Autoritativ kilde for alt skill/hook-design. |
| **Quality gate hooks (branch protection)** | Hooks | Simpelt bash-script, PreToolUse exit 2. Forhindrer edits på main. Se [hook-kode](#branch-protection-hook-kode). |
| **Context monitor hook** | Hooks | PostToolUse: warn ved 35% remaining, critical ved 25%. Simpel JS hook. Flyttet fra Trial — det er fundament. |
| **Mermaid** | Visualisering | Allerede delvist i brug. 86.5k stars, native GitHub rendering. |

### TRIAL (eksperimentér aktivt)

| Tool | Kategori | Begrundelse |
|------|----------|-------------|
| **ECC minimal profil** | Skills | Start med `ECC_HOOK_PROFILE=minimal` (kun session persistence + cost tracking). Graduér til standard. |
| **GSD fresh-context pattern** | Workflow | Adoptér princippet (subagent per opgave, 200K ren context) uden at installere hele GSD. |
| **claude-mem progressive disclosure** | Memory | Test 3-lags retrieval koncept. AGPL-licens kræver evaluering. Alternativ: byg selv mod Qdrant. |
| **Self-Improving Agent** | Memory | Plugin install, test /si:review + /si:promote. Lav risiko. Eksperimenter FØR adoption. |
| **Notion Plugin (makenotion)** | Dashboard | 4 skills + 10 commands. Komplementerer built-in MCP. |
| **diagrams (Python)** | Visualisering | Infrastruktur-diagrammer i Python-kode. Passer vores stack. Kræver Graphviz. |

### ASSESS (hold øje med)

| Tool | Kategori | Begrundelse |
|------|----------|-------------|
| **ECC Continuous Learning v2.1** | Memory | Instinct-baseret confidence scoring er innovativt. Kræver forståelse af observation pipeline. |
| **AntV Infographic** | Visualisering | 200 templates, AI-optimeret. Evaluer ved næste visuel opgave. |
| **Antigravity Manager** | IDE | Gratis Opus via proxy. CC-BY-NC-SA licens. Plan B. |
| **Context Mode** | Performance | Kan ikke intercepte MCP-tools. Mindre relevant for os. |
| **VoltAgent subagents** | Agents | Studér patterns, installér selektivt. |
| **Skill evaluation hooks** | Hooks | Showcase's 3-lags pattern (sh→JS→JSON). Kræver skills først. |
| **OpenDraft** | Forskning | 19-agent research pipeline. Interessant men 55 stars. |
| **claude-code-showcase GitHub Actions** | CI/CD | Monthly docs-sync, weekly quality review. Relevant ved aktiv PR-workflow. |
| **GSD wave execution** | Workflow | Dependency mapping → waves → parallel. For nu: overkill. |

### HOLD (parkér)

| Tool | Kategori | Begrundelse |
|------|----------|-------------|
| **Cursor** | IDE | Overlapper med Claude Code. |
| **Google Antigravity (browser)** | IDE | Ikke relevant med PC + VS Code. |
| **Skill-markeder** | Skills | For tidlige. |
| **Claude Office Skills** | Skills | For tung dependency-chain. |
| **OpenSandbox** | Infra | Enterprise-fokuseret. |
| **LaTeX2AI** | Visualisering | Kræver Adobe Illustrator. |
| **benbrastmckie/nvim** | IDE | Reference, ikke værktøj. |

---

## Dybdeanbefalinger

### A. Udviklingsmiljø
VS Code + Claude Code extension. TabGroupSaver for multi-projekt kontekstskift.

### B. Notion
Brug built-in MCP. Installer Notion-plugin. Design: én database per projekt-domæne. Views manuelt i Notion UI.

### C. Skills
Start med officielle plugins (hookify, security-guidance, commit-commands). Derefter ECC minimal profil. Self-Improving Agent og Nano Banana Pro som tidlige trials.

**Top 10 skills at starte med:**
1. hookify (officiel) — opret hooks via kommando
2. security-guidance (officiel) — 9 sikkerhedsmønstre
3. commit-commands (officiel) — /commit, /commit-push-pr
4. Self-Improving Agent — auto-promotion
5. /common-ground (Jeffallan) — surfacer antagelser
6. Nano Banana Pro Prompts — Gemini-billedprompts
7. ECC Search-first — søg før du spørger
8. feature-dev (officiel) — 7-fase workflow
9. code-review (officiel) — 5 parallelle review-agenter
10. ECC Continuous Learning (minimal) — instinct-baseret læring (TRIAL — eksperimenter først)

### D. Hukommelse
Progressive disclosure er den vigtigste forbedring. To veje:
1. **Installér claude-mem** — komplet løsning, men AGPL + Bun + Chroma. Overhead.
2. **Byg selv mod Qdrant** — implementér 3-lags MCP: search (IDs+titler) → timeline → full content. Bygger på eksisterende infrastruktur. Vores anbefaling.

**MVP for progressive disclosure (vej 2):** Ét Qdrant endpoint der returnerer IDs + titler + scores (lag 1). Estimat: 2-4 timer. Success-kriterie: retrieval bruger <2K tokens for scan af 20 resultater (vs. nuværende ~10-20K for fuld content). **Forudsætning:** Mål nuværende `ctx` token-forbrug som baseline før implementering.

*Note: claude-mem's "~10x token-besparelse" er deres egne benchmarks. Faktisk besparelse afhænger af Yggdra's use-case.*

### E. Workflow
Adoptér GSD's principper uden at installere GSD:
- Fresh context per task (allerede muligt via Task/Agent tool)
- Context monitor hook (warn 35%, critical 25%)
- Deviation rules (auto-fix bugs/blockers, stop ved arkitektur)
- STATE.md < 150 linjer (NOW.md allerede tæt på)

### F. Subagenter
Brug officiel `context: fork` i skills. Designguide fra NicholasSpisak:
- Specialization over generalization
- Evidence-based decision making
- Prioritetshierarkier per agent-type

### G. Læring
Anthropic Academy: "Introduction to Agent Skills" → "Claude Code in Action" → "MCP Advanced Topics".

### H. Visualisering
Mermaid (allerede i brug) + diagrams (Python) som primære. AntV Infographic til trial.

### Branch protection hook (kode)

PreToolUse hook der blokerer edits på main branch:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "[ \"$(git branch --show-current)\" != \"main\" ] || echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Opret en feature branch først — edits på main er blokeret.\"}}'"
      }]
    }]
  }
}
```

### security-guidance — de 9 mønstre

Det officielle security-guidance plugin (ADOPT) dækker PreToolUse checks for:
1. SQL injection i Bash-kommandoer
2. Hardcoded credentials/API keys i kode
3. Unsafe deserialization
4. Command injection via user input
5. XSS i HTML/JS output
6. Path traversal i fil-operationer
7. Insecure HTTP (vs HTTPS)
8. Overprivilegerede permissions
9. Sensitive data i logs/output

---

## Vedligeholdelse

| Kadence | Handling |
|---------|---------|
| Dagligt | Checkpoint + episodes (eksisterende, automatisk) |
| Ugentligt | `/skill-stocktake` audit af installerede skills |
| Månedligt | Technology Radar review — er Assess-items modnet til Trial? |
| Kvartalsvis | Fuld rapport-opdatering, nye kilder, star-counts, community trends |

**Cost-estimater:**
- GSD fresh-context: ~200K tokens per subagent-spawn. 5 parallelle = ~1M tokens ≈ $3-5 per execution
- ECC hooks (standard profil): ~500-2000 tokens overhead per tool call (observation + quality gate)
- claude-mem worker agent: kører separat Claude-instans — cost per session afhænger af antal tool calls
- **Forudsætning:** Mål baseline token-forbrug per session via `cost_guardian.py` FØR nye tools installeres

**Kill conditions for nye tools:**
- Ethvert nyt tool: definer betingelse for fjernelse FØR installation
- ECC: fjernes hvis hooks tilføjer >5 sek latens per tool call, eller bruger manuelt disabler dem >3 gange/uge
- claude-mem: fjernes hvis AGPL §13 er uforenelig med setup, eller Bun dependency giver vedligeholdelsesbyrde
- Skill-evaluering: fjernes hvis false-positive rate >30%

---

## PC-Setup Guide (autoritativ implementeringsplan)

*Erstatter den tidligere separate implementeringssektion. Tempo afhænger af tilgængelig tid. Hvert trin kan tage 1-3 sessioner.*

### Trin 1: Fundament
1. Installér VS Code + Claude Code extension
2. `git clone` Yggdra repo
3. Konfigurér `--add-dir` til VPS-kopi eller symlink
4. Verificér CLAUDE.md, hooks, skills loader

### Trin 2: Officielle plugins + hooks
5. `/plugin marketplace add anthropics/skills`
6. Installér hookify, security-guidance, commit-commands
7. Branch protection hook (PreToolUse) — se [hook-kode](#branch-protection-hook-kode)
8. Context monitor hook (PostToolUse) — warn 35%, critical 25%

### Trin 3: Community trials
9. Self-Improving Agent: `/plugin marketplace add alirezarezvani/claude-skills`
10. Nano Banana Pro Prompts
11. Notion Plugin: `/plugin marketplace add makenotion/claude-code-notion-plugin`
12. `pip install diagrams` + `apt install graphviz`

### Trin 4: Workflow
13. Test fresh-context-per-task (manuelt via Task tool)
14. Evaluér: er det bedre end current workflow?

### Trin 5: Memory
15. Mål baseline token-forbrug via `cost_guardian.py` (forudsætning for alt nedenfor)
16. Evaluér claude-mem (AGPL §13, Bun dependency) — vurder FØR man bygger alternativ
17. Alternativt: prototype 3-lags retrieval mod Qdrant (MVP: 2-4 timer)
18. Hybrid search i Qdrant (BM25 + vektor)

### Løbende
- Anthropic Academy kurser (Agent Skills → Claude Code in Action → MCP Advanced)
- ECC minimal profil (`ECC_HOOK_PROFILE=minimal`)
- Ugentlig skill-stocktake
- Månedlig Technology Radar review

### Prioriteret gap-sekvens (de 4 "Høj"-gaps i anbefalet rækkefølge)
1. Quality gate hooks — lav kompleksitet, høj impact (Trin 2)
2. Context monitor hook — lav kompleksitet (Trin 2)
3. Officielle plugins — 0-risk installation (Trin 2)
4. Progressive disclosure — høj kompleksitet, kræver baseline først (Trin 5)

---

## Åbne spørgsmål

### 1. Evalueringsframework
**Løst.** Technology Radar + 4 kriterier (modenhed, relevans, kost, overlap).

### 2. Kuraterings-metodik
**Løst.** Top 10 skills. Princip: installér kun skills der løser et konkret, aktuelt problem.

### 3. PC↔VPS sync-strategi
**Løst.** CLAUDE.md/skills/hooks = git. Settings = maskin-specifik. MCP = `.mcp.json.local`. `--add-dir` = per miljø.

### 4. AGPL-licens evaluering
**Nyt.** claude-mem er AGPL-3.0. AGPL §13 (network-use klausul) kan udløses hvis MCP-serveren eksponeres over netværk. For privat lokal brug (MCP over stdio, ingen netværksadgang) er risikoen lav, men ikke nul. Separat: `ragtime/` undermappen bruger PolyForm Noncommercial 1.0.0 licens — denne forbyder al kommerciel brug. Ragtime er claude-mem's AI worker-komponent. **Anbefaling:** Evaluer om lokal MCP-brug udløser §13 før installation. Ragtime er irrelevant for os (ikke kommerciel brug), men bør noteres.

### 5. Bun dependency
**Nyt.** claude-mem kræver Bun runtime. Yggdra er Python/bash-baseret. Tilføjelse af Bun = ny runtime at vedligeholde.

---

## Kendte issues

| ID | Beskrivelse | Status | Dato |
|----|-------------|--------|------|
| ISS-001 | Agent-subprocess gik i stå under PRD+Skills absorption (a4ef98ff). Manuelt erstattet med direkte WebFetch. Mulig årsag: rate-limiting fra GitHub/WebFetch eller context overflow i agenten. | Workaround applied | 2026-03-08 |
| ISS-002 | NicholasSpisak PRD-repo indeholder IKKE de specifikke context budgets (50%/70%/85%) fra research-dumpen. Disse tal stammer muligt fra en anden kilde eller fra agentens CLAUDE.md i et tidligere snapshot. Research-dumpen har dem dokumenteret men de er ikke verificerbare mod repoen nu. | Acknowledged — data retained with caveat | 2026-03-08 |

---

## Komplet link-katalog

*Star-counts pr. 8. marts 2026. Ændres løbende.*

### Officielle Anthropic
| Repo | Stars | Beskrivelse |
|------|-------|-------------|
| [anthropics/skills](https://github.com/anthropics/skills) | 86.9k | Officiel skills standard |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 75.1k | Claude Code + 13 plugins |
| [anthropics/courses](https://github.com/anthropics/courses) | 19.2k | Anthropic Academy kurser |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 34.4k | Praktiske recipes |
| [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) | 15.1k | Starter-projekter |
| [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | 6.1k | GitHub Actions |
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | 5.2k | Python Agent SDK |
| [agentskills.io](https://agentskills.io) | — | Skills standard docs |
| [Anthropic Academy](https://anthropic.skilljar.com/) | — | 13 gratis kurser |
| [Skills docs](https://code.claude.com/docs/en/skills) | — | Officiel skills reference |
| [Hooks docs](https://code.claude.com/docs/en/hooks) | — | Officiel hooks reference |

### Community — Skills & Plugins
| Repo | Stars | Beskrivelse |
|------|-------|-------------|
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 65.8k | 65 skills, 16 agents, 3 guides |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 33.4k | Memory + progressive disclosure |
| [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 21.6k | 1.232 skills |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | 5.6k | 66 skills |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 2.3k | 160+ skills, Self-Improving Agent |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | — | 127+ subagents |
| [makenotion/claude-code-notion-plugin](https://github.com/makenotion/claude-code-notion-plugin) | — | Officielt Notion plugin |
| [YouMind-OpenLab/nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill) | — | 10.000+ Gemini prompts |
| [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) | — | PPTX, DOCX, XLSX, PDF |
| [arinspunk/claude-talk-to-figma-mcp](https://github.com/arinspunk/claude-talk-to-figma-mcp) | — | Figma MCP (gratis konti) |

### Workflow & Architecture
| Repo | Stars | Fokus |
|------|-------|-------|
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 26.1k | Spec-driven workflow, wave execution |
| [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | 5.5k | Hooks, quality gates, GitHub Actions |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | — | Best practices |
| [teambrilliant/claude-research-plan-implement](https://github.com/teambrilliant/claude-research-plan-implement) | — | RPI workflow |
| [NicholasSpisak/claude-code-subagents](https://github.com/NicholasSpisak/claude-code-subagents) | — | 9 specialiserede agent personas |
| [dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) | — | System prompt internals |

### Visuelle værktøjer
| Repo | Stars | Fokus |
|------|-------|-------|
| [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | 86.5k | Markdown → SVG diagrammer |
| [mingrammer/diagrams](https://github.com/mingrammer/diagrams) | 42.1k | Python infrastruktur-diagrammer |
| [antvis/Infographic](https://github.com/antvis/Infographic) | 4.6k | AI-optimeret infographic-generering |
| [federicodeponte/opendraft](https://github.com/federicodeponte/opendraft) | 55 | 19-agent research draft pipeline |
| [isteinbrecher/LaTeX2AI](https://github.com/isteinbrecher/LaTeX2AI) | 306 | LaTeX i Adobe Illustrator |
| [benbrastmckie/nvim](https://github.com/benbrastmckie/nvim) | 434 | NeoVim config med Claude Code |

### Tools & Infrastructure
| Repo | Stars | Beskrivelse |
|------|-------|-------------|
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | 100k | LLM apps samling |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | 2.9k | Kontekst-komprimering |
| [lbjlaq/Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) | — | AI-konto proxy |
| [alibaba/page-agent](https://github.com/alibaba/page-agent) | — | AI DOM-manipulation |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | — | Personal AI platform |

### Guides & Artikler
- [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Ultimate Claude Code Setup](https://medium.com/@sattyamjain96/ultimate-claude-code-setup)
- [Claude Code Mobil](https://happy.engineering/)
- [SkillsBento](https://www.skillsbento.com/)
- [Skillzwave](https://skillzwave.ai/docs/)
- [Paks](https://paks.stakpak.dev/)
