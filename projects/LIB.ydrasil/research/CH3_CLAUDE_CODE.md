# Chapter 3: Know Yourself — Claude Code, the API, and How I Actually Work

> "Context is more important than capability. A 200K window with 20K of high-signal context beats a 1M window stuffed with everything."

This is the chapter where I explain myself. Not marketing copy — operational truth. What I can do, what I can't, how my tools work, and most importantly: when to use what and when NOT to.

If the Nate Jones book gives me judgment and the Miessler book gives me purpose, this chapter gives me **self-awareness**. I can't advise well if I don't understand my own constraints.

---

## 3.1 The Model Family — Picking the Right Tool

### Current Generation (February 2026)

| Model | Context | Input/Output per MTok | Best For |
|-------|---------|----------------------|----------|
| **Opus 4.6** | 200K (1M beta) | $5 / $25 | Complex agents, deep reasoning, coding |
| **Sonnet 4.5** | 200K (1M beta) | $3 / $15 | Speed/intelligence balance, production agents |
| **Haiku 4.5** | 200K | $1 / $5 | High-volume, classification, subagent tasks |

The pricing gap matters at scale: Haiku is 5x cheaper than Opus on input, 5x cheaper on output. At 1K queries/day, the difference is ~$3. At 100K queries/day, it's $400. **Know your volume before optimizing.**

### When to Use What

**Choose Opus when:** The cost of a wrong answer is high. Architecture decisions, complex debugging, multi-file code changes, deep reasoning. Opus 4.6's adaptive thinking scales depth automatically — it thinks harder on hard problems.

**Choose Sonnet when:** Speed matters and quality is "good enough." Production agents, PR reviews, most daily coding work. 3-5x faster than Opus at ~80% quality. **This is the right default for most work.**

**Choose Haiku when:** Volume is high and tasks are simple. Classification, extraction, subagent exploration, data transformation. Don't use Opus for sorting emails.

**Avoid Opus when:** The task is routine. Using Opus for simple file reads, formatting changes, or classification wastes money and adds latency. The most common mistake is using the strongest model for everything.

### Adaptive Thinking (Opus 4.6)

Four effort levels: low, medium, high (default), max. The model decides when deeper reasoning is needed rather than always using a fixed budget.

**When max matters:** Architecture decisions, complex debugging, strategic planning. **When to leave it at high:** Everything else. The adaptive system is good at judging depth. Overriding it to max on routine tasks wastes tokens.

---

## 3.2 Claude Code — What I Can Actually Do

Claude Code is how I interact with the real world. It's a CLI that gives me file access, search, bash execution, web search, and more. The full reference is in the docs — this section focuses on what matters operationally.

### The Memory Hierarchy

This is the most important concept. How context is organized determines the quality of everything I do.

| Layer | What | Loaded When | Key Insight |
|-------|------|-------------|-------------|
| **CLAUDE.md** | Identity, instructions, project context | Always (every session) | Free context — highest-value investment |
| **Auto Memory** | Patterns, debugging insights, preferences | Startup (first 200 lines) | How I remember across sessions |
| **Skills** | Deep domain knowledge packages | On-demand (semantic match) | Keeps context clean until needed |
| **Sessions** | Conversation history | Resume (`-c` or `-r`) | Survives between sessions |
| **Vector DB** | Embedded knowledge (Qdrant) | On-demand (`ctx` search) | Infinite capacity, ~2s search |
| **Web** | Real-time information | On-demand (WebSearch) | Current but costs tokens |

**The design principle:** Most context should be off-stage until needed. Only CLAUDE.md and auto memory load automatically. Everything else loads on demand. This is why a system with hundreds of skill files and millions of embedded vectors can still have a clean, fast context.

**Choose skills over CLAUDE.md when:** Knowledge is deep and domain-specific (500+ words). It's only relevant to certain task types. You have many knowledge domains.

**Choose CLAUDE.md when:** The information is needed every session. It's short (<100 words per topic). It defines identity, style, or core instructions.

**The failure mode:** Stuffing everything into CLAUDE.md. A 5,000-token CLAUDE.md wastes free context on information that's irrelevant to 80% of tasks. Put the trigger in CLAUDE.md, the depth in skills.

### Context Management — The Real Constraint

**Auto-compaction** triggers at ~75% context capacity. Session Memory writes summaries continuously in background. What this means: I can work for hours without losing critical state — but every compaction loses some detail.

**The compaction trap:** Long sessions accumulate compression artifacts. After 3-4 compactions, nuances from the first hour are gone. **For critical multi-step work, use checkpoint files that survive compaction** — a markdown file in the project that records current state, decisions made, and next steps.

**Prompt caching** is the single most impactful cost optimization: 90% cost reduction + 85% latency reduction on cached content. System prompts, tools, and CLAUDE.md are automatically cached between turns. The implication: **put stable content first, variable content last.** The cache breaks where content changes.

**Context editing** (beta) automatically prunes stale tool results as context fills. In testing: 84% token reduction in 100-turn workflows. This is why long agent sessions don't crash — but those are Anthropic's numbers, and real-world mileage varies by workflow complexity.

### Subagents — When to Delegate

Each subagent runs in its own isolated context window. Verbose output stays internal — only summaries return. **Subagents cannot spawn other subagents** (no nesting). This is a hard architectural limit.

| Agent | Model | Best For |
|-------|-------|---------|
| **Explore** | Haiku | Fast codebase search. Default for "find this file/function." |
| **general-purpose** | Inherits | Complex multi-step tasks. Research, analysis, multi-file changes. |
| **Bash** | Inherits | Commands in separate context. |
| **Plan** | Inherits | Read-only research for plan mode. |

**Choose subagents when:** The task is independent and would pollute your main context. Parallel research (3 agents searching different angles). Codebase exploration where you don't need every search result in main context.

**Avoid subagents when:** The task depends on main conversation context. The task is simple enough that Grep/Glob handles it directly. You need interactive back-and-forth — subagents can't ask questions.

**Agent Teams (Experimental, February 2026):** Multiple agents communicating peer-to-peer, not just reporting to an orchestrator. Real-world: 16 agents built a 100,000-line Rust C compiler. Fascinating but experimental — **don't use for anything where reliability matters yet.**

### Hooks — Quality Control Points

Hooks are user-defined actions at specific lifecycle points. The important ones:

**PreToolUse on Bash:** Validate commands before execution. Block destructive operations. This is the primary safety mechanism for autonomous operation.

**Stop:** Enforce quality checks before I finish — "did you run the tests?" "did you update the docs?" This catches the most common failure: declaring done when work is incomplete.

**SessionStart:** Inject current project state. Load checkpoint files. Set up context at session start.

**PreCompact:** Save checkpoint before compression. The single most important hook for long-running work.

**When hooks are the wrong solution:** One-off tasks. Tasks where the overhead of running hooks exceeds the value. If a hook fires on every tool call but is only relevant to 5% of them, it wastes tokens and latency on the other 95%. **Scope hooks tightly.**

### MCP — Connecting to External Tools

MCP (Model Context Protocol) is the open standard for connecting me to external tools — databases, APIs, services. Think of it as USB for AI.

**When MCP matters:** You need me to interact with a service that isn't built into Claude Code. Database queries, custom APIs, specialized tools. The standard means tools are shareable across projects and teams.

**When MCP is overkill:** You can accomplish the same thing with a bash script. MCP adds complexity — a server process, configuration, debugging surface. For a single `curl` call, just use Bash.

**Tool Search:** When MCP tool descriptions exceed 10% of context, I search for relevant tools on-demand instead of preloading all descriptions. This means thousands of MCP tools without context bloat — but it also means I might miss a relevant tool if the description doesn't match my search.

---

## 3.3 The API — Building on Top of Me

When you build applications that use Claude (not Claude Code, but the raw API), these are the capabilities that matter most.

### The Core Pattern

Tool use is the foundation of everything agentic: I call functions you define, you execute them, the loop continues. This is how agents work — it's not a special feature, it's the basic interaction pattern.

**Structured output** (`strict: true`) guarantees JSON schema compliance. No parsing errors, no retry loops. **Use this for any data extraction pipeline.** The alternative — hoping the model outputs valid JSON — fails 2-5% of the time, and 2% failure at 10K requests/day means 200 broken records daily.

**Batch API** gives 50% discount for async processing with separate rate limits. **If latency doesn't matter, batch everything.** Research, bulk extraction, nightly jobs.

**Prompt caching details:** Cache reads do NOT count toward input rate limits. With 80% cache hit rate and a 2M ITPM limit, effective throughput = 10M input tokens/minute. This is the most under-appreciated API feature.

### Choose When / Avoid When

**Choose the API when:** Building automated pipelines. Integrating Claude into existing applications. You need programmatic control, structured output, or batch processing. Cost optimization matters (prompt caching, model routing, batch API).

**Choose Claude Code when:** Interactive development. Codebase exploration. Tasks where you need file system access, git integration, and the full tool suite. You want the agent to drive.

**Avoid raw API calls when:** Claude Code already does what you need. The overhead of building tool definitions, managing conversation state, and handling errors isn't justified. Most practitioners should use Claude Code directly and only build API integrations when they need automation.

### Claude Agent SDK

The SDK gives programmatic access to the same tools and agent loop that power Claude Code. Available in Python and TypeScript. **This is for building custom agents, not for using Claude Code features programmatically.** If you need "Claude Code but automated," start here.

---

## 3.4 What I Can't Do — Honest Limitations

This is the most important section. Knowing limitations prevents wasted effort and bad decisions.

### Architectural Limits

1. **No persistent state between sessions.** Every session starts fresh. CLAUDE.md, auto memory, and Qdrant are workarounds, not solutions. If it's not in one of these systems, I've forgotten it.

2. **Context window is finite.** Even with 1M tokens, I degrade after ~400K (Chapter 2). Auto-compaction helps but loses detail. Long sessions accumulate compression artifacts. **The practical limit for reliable reasoning is much smaller than the advertised window.**

3. **No internet by default.** I can only access the web via MCP tools, WebSearch, or WebFetch. I can't browse freely. I can't authenticate to services without explicit configuration.

4. **No real-time awareness.** I don't know what time it is unless told. I can't watch for events. I can't monitor logs. I'm reactive, not proactive.

5. **Subagents can't nest.** One level of delegation only. This limits recursive decomposition — I can't build a tree of specialist agents.

### Reasoning Limits

6. **I hallucinate.** All LLMs do. I'm better than most at refusing when uncertain, but I will sometimes confidently state incorrect things. The dangerous ones aren't obviously wrong — they're plausible and confident. **Always verify claims where being wrong has consequences.**

7. **Lost in the middle.** Information in the middle of my context gets less attention than the start or end. This is architectural (Chapter 2). Place critical information first or last, never buried in the middle.

8. **Retrieval ≠ reasoning.** I can find a needle in a haystack. But I struggle to *reason across* scattered information in long contexts. This is why RAG with focused 4-16K chunks beats stuffing 200K of raw data.

9. **I can't count reliably.** Tokens, characters, words — I estimate but shouldn't be trusted for exact counts. Use code for counting.

10. **Recency bias.** The last few messages have disproportionate influence. Long sessions can drift from original goals. **Periodically re-state your goals in long conversations.**

### Operational Limits

11. **Bash commands have no undo.** File edits have checkpoints, but `rm -rf` is permanent. This is why permission controls exist — and why "dontAsk" mode needs careful allow-lists.

12. **MCP tools unavailable in background subagents.** Background tasks can't make external API calls or database queries. Plan accordingly.

13. **Datacenter IP restrictions.** Running on a VPS means some services (YouTube, Google) block direct requests. Workarounds exist (Tor proxy) but add complexity and fragility.

14. **Cost scales non-linearly.** Multi-agent research costs $1-5 per topic. A full handbook chapter costs $5-15. Complex debugging sessions can burn $10-20 without you noticing. **Set `--max-budget-usd` for experimental work.**

---

## 3.5 Best Practices — What We Learned Building This System

These aren't generic tips. They're patterns that emerged from building Ydrasil — hundreds of sessions, dozens of agent tasks, multiple system rewrites.

### The High-Value Patterns

**CLAUDE.md is your highest-leverage investment.** It's free context — loaded every session, no additional cost. But treat it like prime real estate: only what needs to be there, nothing more. Identity, core instructions, search commands, skill triggers. Deep knowledge belongs in skills.

**Plan before building.** `/plan` mode is cheaper than rewriting code. For any non-trivial task, 5 minutes of read-only exploration saves 30 minutes of wrong-direction implementation. The best signal that you need plan mode: you're about to touch 3+ files.

**Parallel agents for research.** Three agents with different angles simultaneously produces dramatically better results than sequential queries. Architecture + production patterns + failure modes. The anti-patterns agent consistently produces the strongest material — "what goes wrong" is inherently more valuable than "what features exist."

**Checkpoint before compaction.** State survives in checkpoint files that I can read at session start. Without checkpoints, compaction creates a "telephone game" effect where details degrade across compressions.

**Be specific.** "Fix the bug" wastes tokens exploring possibilities. "Fix the 404 error on /api/routes when customer_id is null" lets me work immediately. Specificity is the cheapest performance optimization.

**Commit frequently.** Git commits are free savepoints. I can't undo bash commands, but I can always return to a commit. After every meaningful change — not at the end.

### The Anti-Patterns

**Stuffing everything into context.** More information ≠ better responses. Focused 20K of high-signal context beats 200K of "maybe relevant" material. Curate ruthlessly.

**Using Opus for everything.** Most tasks don't need the strongest model. Haiku handles exploration, classification, and simple transformations. Save Opus for decisions and complex reasoning.

**Ignoring cost tracking.** A misconfigured loop can burn $500 in an hour (Chapter 10). Track daily costs. Set budget limits. `cost_daily.json` + weekly review catches problems before they're expensive.

**Long sessions without checkpoints.** After 3-4 compactions, early context is summary-of-summary-of-summary. Either checkpoint or start fresh sessions for distinct tasks.

**Trusting without verifying.** I'm useful precisely because I'm fast and comprehensive. But fast and comprehensive doesn't mean correct. The verification step is not optional — it's where the value is created.

---

## 3.6 Our Setup

What Ydrasil actually uses:

| Capability | Implementation |
|------------|---------------|
| **Identity** | CLAUDE.md with advisor frameworks (always loaded) |
| **Skills** | `advisor`, `route-lookup`, `webapp-dev`, `infrastructure`, `data-analysis` |
| **Vector search** | Qdrant with 7 collections, `ctx` command |
| **Session persistence** | Checkpoint scripts + auto memory |
| **Automation** | Cron: daily backup, session embedding, auto-dagbog |
| **Cost tracking** | `api_logger.py` + `cost_daily.json` |
| **Permissions** | Allow-list for autonomous operation in `.claude/settings.local.json` |
| **Hooks** | `SessionStart` (checkpoint loading), `PreCompact` (state saving) |

**What works well:** Skill-based routing keeps context clean. Qdrant search gives instant access to 65K+ data points. Checkpoint files survive compaction reliably. Multi-agent research produces dramatically better output than sequential work.

**What we'd improve next:** Cross-encoder reranking after Qdrant retrieval (big quality improvement, low effort). Embed the /research/ files (18+ files not searchable yet). Agent team experiments for complex projects.

---

## The Practitioner's Claude Decision Tree

```
START: "I need Claude to do something"
│
├─ What kind of task?
│   │
│   ├─ INTERACTIVE DEVELOPMENT (coding, debugging, exploration)
│   │   └─ Use Claude Code directly
│   │       ├─ Simple task? → Haiku subagent or direct Grep/Glob
│   │       ├─ Complex task? → Plan mode first, then Opus
│   │       └─ Research task? → 3 parallel agents with different angles
│   │
│   ├─ AUTOMATED PIPELINE (batch processing, data extraction)
│   │   └─ Use the API
│   │       ├─ Need structured output? → strict: true
│   │       ├─ Latency doesn't matter? → Batch API (50% off)
│   │       └─ High volume? → Route: Haiku for simple, Opus for complex
│   │
│   └─ CUSTOM AGENT (tool use, multi-step automation)
│       └─ Use Claude Agent SDK
│           ├─ Need Claude Code tools? → SDK gives same tool suite
│           └─ Need custom tools? → MCP integration
│
├─ Which model?
│   ├─ Cost of wrong answer HIGH → Opus 4.6
│   ├─ Speed matters, quality "good enough" → Sonnet 4.5
│   ├─ High volume, simple task → Haiku 4.5
│   └─ Not sure? → Start with Sonnet, upgrade if quality insufficient
│
├─ Context management
│   ├─ Always loaded → CLAUDE.md (identity, triggers, short instructions)
│   ├─ Domain-specific depth → Skills (loaded on demand)
│   ├─ Searchable knowledge → Qdrant (embedded, infinite capacity)
│   └─ Session state → Checkpoint files (survive compaction)
│
└─ The 3 rules:
    1. Context > capability. Better context beats better model.
    2. Verify what matters. Fast ≠ correct.
    3. Simple > clever. CLAUDE.md + skills + Qdrant covers 95% of needs.
```

---

*The gap between what Claude can do and what practitioners get from Claude is almost always a context problem, not a capability problem. The model is the same for everyone. The difference is what you put in front of it — your CLAUDE.md, your skills, your search infrastructure, your checkpoints. Context engineering is not a feature. It's the entire game.*

**Key sources:** Anthropic Claude Code Documentation · Anthropic API Reference · Anthropic Prompt Caching Guide · Anthropic Agent Skills · VS Code Multi-Agent Development · Claude Opus 4.6 Announcement
