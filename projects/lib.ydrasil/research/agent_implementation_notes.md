# Agent Implementation Notes

**Created:** 2026-03-08
**Location:** `/root/Yggdra/scripts/agents/`
**Purpose:** Runnable reference implementations of the agent patterns from Chapter 6

---

## What Was Built

Five modules that implement the core agent patterns discussed in the research chapter, from simplest to most complex:

### 1. `tool_definitions.py` — Tool Infrastructure
The foundation. Everything else depends on this.

- **@tool decorator** — Extracts metadata from docstrings + type hints automatically. You write a normal Python function, the decorator generates the JSON schema the LLM needs.
- **ToolRegistry** — Stores tools, dispatches calls by name, wraps errors. The LLM outputs `{"name": "calculator", "arguments": {"expression": "2+2"}}`, the registry finds the function and calls it.
- **Schema generation** — Produces both OpenAI and Anthropic tool-call formats from the same Python type hints.
- **Error wrapping** — Critical pattern. If a tool crashes, the LLM gets a structured error message it can reason about, not a Python traceback.

Key insight from the research: "Spend 80% of your time on tool definitions, 20% on agent logic."

### 2. `state_manager.py` — Persistence via Markdown
Three patterns for agent memory between steps:

- **PlanManager** — Write/read/update a PLAN.md checklist. The "Plan-and-Execute" pattern. Agent reads the plan at each iteration to know where it is.
- **StateManager** — Key-value pairs in a markdown table. Like a tiny database, but human-readable and Git-friendly.
- **EpisodicLog** — Append-only observation log. Every tool call, every finding, every decision gets logged. Enables post-hoc analysis.
- **AgentWorkspace** — Combines all three into a directory with PLAN.md + STATE.md + LOG.md.

Why markdown? LLMs understand it natively. Humans can read it. Git tracks changes. No database dependency.

### 3. `react_agent.py` — The Core Loop
Minimal but complete ReAct implementation:

- Think → Act → Observe → Repeat
- Uses OpenAI-compatible API (works with Groq's free tier out of the box)
- Circuit breaker: max iterations (default 10) prevents infinite loops
- Cost tracking: estimates $ cost per run using token counts
- Optional workspace integration for persistent state
- Full audit trail of every iteration

This is the architecture at Level 4 on the spectrum (where "agent" begins).

### 4. `eval_harness.py` — Measurement
"You cannot trust self-reports about agent effectiveness."

- **TestCase** — Query + expected answer (substring match or custom validator)
- **Validators** — `contains()`, `matches_number()`, `any_of()` for common patterns
- **EvalHarness** — Runs agent on test suite, collects pass/fail + cost + latency
- **EvalReport** — Markdown report with summary table, per-tag breakdown, detailed results
- **JSON export** — Machine-readable results for tracking over time

Includes two pre-built test suites (math + reasoning).

### 5. `supervisor_agent.py` — Multi-Agent Coordination
The most complex pattern. Use only when simpler patterns are insufficient.

- **Supervisor** decomposes tasks and delegates to workers
- **Workers** are focused agents with specialized system prompts
- **Synthesis** step combines worker outputs
- **Human-in-the-loop** gate for approval before returning (optional)
- Star topology: workers never talk to each other (prevents loop scenarios)
- Pre-built worker configs: researcher, writer, critic, analyst

The research says single-agent beats multi-agent 2-6x for most tasks. This implementation exists to show the pattern for the cases where decomposition genuinely helps.

---

## Design Decisions

### Why Groq as default provider?
Free tier, fast inference, OpenAI-compatible API. Good for learning and testing. Switch to OpenAI/Anthropic for production by changing one parameter.

### Why urllib instead of the openai package?
Zero dependencies beyond stdlib. The OpenAI API is just HTTP + JSON. Using urllib makes the implementation transparent — you can see exactly what's being sent.

### Why no async?
Simplicity. Async adds complexity without benefit for sequential agent loops. For parallel worker execution in the supervisor, Python's concurrent.futures would be the next step.

### Why markdown for state?
Three reasons: (1) LLMs read markdown natively — inject STATE.md into the prompt and the agent understands its own state. (2) Humans can read it — open the file and see what the agent did. (3) Git-friendly — diffs show exactly what changed between iterations.

---

## The Practitioner's Ladder (Mapped to Code)

| Level | Pattern | Module | When |
|-------|---------|--------|------|
| L1 | Cron + script | (not here — just use cron) | Scheduled, deterministic |
| L3 | LLM-in-the-loop | `tool_definitions.py` alone | One judgment step |
| L4 | ReAct agent | `react_agent.py` | 3-7 step dynamic tasks |
| L4+ | Plan-and-Execute | `state_manager.py` + `react_agent.py` | 10+ steps, audit trail |
| L5 | Multi-agent | `supervisor_agent.py` | Genuinely parallelizable |
| All | Evaluation | `eval_harness.py` | Always. Measure everything. |

---

## Running the Examples

```bash
# Activate the venv
source /root/Yggdra/scripts/venv/bin/activate

# Run any module's demo
python -m agents.tool_definitions
python -m agents.state_manager
python -m agents.react_agent        # Requires Groq API key
python -m agents.eval_harness       # Requires Groq API key
python -m agents.supervisor_agent   # Requires Groq API key
```

Or from the scripts directory:
```bash
cd /root/Yggdra/scripts
python agents/tool_definitions.py
python agents/state_manager.py
```

---

## Cost Estimates (Groq Free Tier)

| Module | Estimated cost per run |
|--------|----------------------|
| tool_definitions | $0 (no LLM calls) |
| state_manager | $0 (no LLM calls) |
| react_agent demo | ~$0.001 (1-3 LLM calls) |
| eval_harness (math suite) | ~$0.004 (4 test cases x 1-3 calls) |
| supervisor demo | ~$0.005 (plan + 3 workers + synthesis) |

Groq free tier: 30 requests/minute, 14,400/day. More than enough for development.

---

## Relation to Chapter 6

These implementations directly correspond to the patterns cataloged in the research:

- **Section 6.3** (What IS an Agent?) → `react_agent.py` implements the ReAct loop, the point where "agent" begins
- **Section 6.4** (Architecture Patterns) → All five modules cover the pattern catalog
- **Section 6.5** (Tool Use) → `tool_definitions.py` implements the defenses: schema validation, error wrapping, circuit breakers
- **Section 6.6** (Hybrid Pattern) → Using tools without the full agent loop = hybrid
- **Section 6.7** (What Breaks) → `eval_harness.py` addresses "you need objective measurement"
- **Section 6.8** (Human-in-the-Loop) → `supervisor_agent.py` implements the approval gate
- **Section 6.11** (Practitioner's Ladder) → The modules are ordered by the ladder
