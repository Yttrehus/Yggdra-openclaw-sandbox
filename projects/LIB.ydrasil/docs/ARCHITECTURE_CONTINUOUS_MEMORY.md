# Ydrasil Continuous Memory Architecture

**Created:** 2026-02-23
**Status:** Reference doc — building from this

## Core Insight

Every successful system (OpenClaw, Gastown, Nemori, MemGPT, GitHub Copilot, Miessler PAI) converges on the same pattern. The differences are surface-level. The principles are identical.

---

## The Universal Pattern

```
┌─────────────────────────────────────────────────┐
│                  LIVE SESSION                    │
│                                                  │
│  System prompt loads:                            │
│    1. Identity files (CLAUDE.md, MEMORY.md)      │
│    2. Last 5 episode summaries                   │
│    3. Hot context (NOW.md)                        │
│                                                  │
│  During conversation:                            │
│    - Agent can SEARCH memory (hybrid)            │
│    - Agent can STORE memory (with citations)     │
│                                                  │
│  Before compaction:                              │
│    - Silent flush: save important info to disk   │
│                                                  │
│  At session end:                                 │
│    - Distill session → 3-5 line episode          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│              MEMORY LAYERS                       │
│                                                  │
│  HOT    │ NOW.md, SESSION_RESUME.md              │
│         │ Always in context. ~2000 tokens.       │
│         │                                        │
│  WARM   │ episodes.jsonl (last 30 days)          │
│         │ BM25 searchable. Temporal decay.        │
│         │                                        │
│  COLD   │ Qdrant (advisor brain, routes, etc)    │
│         │ Hybrid search. Evergreen + decaying.    │
└─────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│               HEARTBEAT DAEMON                   │
│                                                  │
│  Every 30 min (08:00-22:00):                     │
│    1. Read HEARTBEAT.md checklist                │
│    2. Check: Trello, Telegram, Gmail,            │
│       Google Calendar, Google Tasks              │
│    3. If nothing: HEARTBEAT_OK (silent)          │
│    4. If something: notify via Telegram          │
│                                                  │
│  Channels are swappable — Trello/Telegram        │
│  may be replaced later. Architecture doesn't     │
│  depend on any specific service.                 │
└─────────────────────────────────────────────────┘
```

---

## 6 Principles

### 1. Segment first, distill second (Nemori)
Raw conversation → coherent episodes → durable semantic knowledge. Batch, segment by topic, then distill. Don't extract facts from a stream.

### 2. Validate at retrieval, not storage (GitHub Copilot)
Store everything loosely. When retrieving, check if it's still true. Cheaper and more robust than curating on write.

### 3. Temporal decay with evergreen exceptions (OpenClaw, Stanford)
`score × e^(-ln2/halflife × age_days)`. Halflife 30 days for conversations. No decay for identity/advisor knowledge. Accessed memories get refreshed.

### 4. Hybrid search = BM25 + vectors + RRF (all systems)
Agents search with keywords (BM25 wins). Users search with meaning (vectors win). Combine with Reciprocal Rank Fusion. Qdrant supports natively.

### 5. Pre-compaction flush (OpenClaw)
Before context compresses, a silent turn saves important knowledge to disk. Extend PreCompact hooks to let LLM choose what matters.

### 6. Files in git > fancy databases (Gastown, Tramel, Miessler)
For session memory: markdown/JSONL in git. BM25 searchable, version-controlled, human-readable. Reserve Qdrant for heterogeneous external knowledge.

---

## Build Order

| # | Component | Lines | Depends on |
|---|-----------|-------|------------|
| 1 | Episodic log (save_checkpoint → Haiku → episodes.jsonl) | ~30 | Nothing |
| 2 | Session resume (SessionStart reads last 5 episodes) | ~20 | 1 |
| 3 | Heartbeat daemon (cron → checklist → act or silence) | ~80 | Nothing |
| 4 | Hybrid search migration (Qdrant native BM25 + RRF) | ~50 | Nothing |
| 5 | Temporal decay in ctx search | ~20 | 4 |
| 6 | Pre-compaction flush (extend existing hook) | ~40 | 1 |
| 7 | Telegram input polling → dispatch | ~30 | 3 |

## Heartbeat Checklist Sources

Current (swappable):
- **Trello** — board status, stale cards, deadlines
- **Telegram** — incoming messages
- **Gmail** — new mail, urgent flags
- **Google Calendar** — upcoming events (next 2h)
- **Google Tasks** — inbox items, overdue

Architecture is source-agnostic. Each source is a Python function returning `list[str]` of alerts. Add/remove sources without changing the daemon.

---

## Key Sources

### Episodic Memory
- Nemori (arXiv 2508.03341) — episode segmentation + predict-calibrate distillation
- MemGPT/Letta (arXiv 2310.08560) — 3-tier memory, agent-managed
- Eric Tramel — BM25 MCP server, single file, <100 lines
- GitHub Copilot — JIT validation, citations, store_memory tool
- Agent Memory Survey (arXiv 2512.13564) — 100+ papers categorized

### Autonomy
- OpenClaw — heartbeat, hybrid search, temporal decay, pre-compaction flush
- Gastown/Beads (Steve Yegge) — git-backed tasks, seancing, worktree isolation
- Claude Code Scheduler — NLP scheduling, worktree isolation
- Miessler PAI — TELOS identity, UOCS capture, hook system, skills

### Retrieval
- Stanford Generative Agents (Park 2023) — recency × importance × relevance
- Qdrant native BM25 + RRF fusion + exp_decay formula rescore
- OpenClaw: vector 70% + BM25 30%, MMR lambda 0.7, halflife 30d
