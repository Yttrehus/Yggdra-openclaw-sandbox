# Chapter 2: The Context Window — What Models Can Actually See

> "GPT-4 effectively uses only ~10% of its 128K window for reasoning tasks. The other 90% are wasted tokens."

Every LLM has a context window — the number of tokens it can see at once. Think of it as a desk: the bigger the desk, the more you can have in front of you. But here's what the marketing doesn't tell you:

**Advertised window ≠ usable window.**

A model claiming 200K tokens is typically unreliable after ~130K. One claiming 1M is unreliable after ~400K. And "unreliable" doesn't mean gradual degradation — it means sudden cliffs in quality.

---

## 2.1 What Models Can Actually Handle (2026)

### Context Window Sizes

| Model | Window | Reliable Range | Notes |
|-------|--------|---------------|-------|
| **Claude Opus 4.6** | 1M | ~400K | Degrades slowest. Refuses rather than hallucinating |
| **Claude Sonnet 4.5** | 1M | ~400K | Beta, tier 4+ |
| **GPT-4.1** | 1M | ~400K | OpenAI's 1M entry |
| **GPT-5.2** | 400K | ~200K | December 2025 |
| **Gemini 2.5 Pro** | 1M (2M coming) | ~530K | Best at pure retrieval (99.7% NIAH at 1M) |
| **Gemini 3 Pro** | 10M | ~256K reasoning | Huge window, but reasoning collapses |
| **Llama 4 Scout** | 10M | ~256K reasoning | Open-weight. 15.6% accuracy at full length |

### The 40% Rule

Research shows consistently: **keep context under 40% of max** for reliable performance.

- 128K window → use max ~50K
- 200K window → use max ~80K
- 1M window → use max ~400K

Above 40%, you don't see gradual degradation — you see **catastrophic collapse**. One study measured F1-score dropping from 0.58 to 0.30 between 40% and 50% capacity. A 45% quality loss over just 10% more context.

---

## 2.2 Lost in the Middle

### The Problem

LLMs have a U-shaped attention curve: they handle information at the beginning and end of context well, but **lose information in the middle**. With just 20 documents (~4K tokens), accuracy drops from 75% to 55% when the answer is in the middle.

### Why It Happens

It's **architectural**, not a bug:
- **RoPE** (Rotary Position Embedding) — used in nearly all modern LLMs — has a long-range dampening effect that structurally deprioritizes middle content
- **Causal attention masks** create bias toward sequence beginnings
- Training data reinforces the pattern

### What to Do About It

Place important information **first** (system prompt, instructions) or **last** (most recent context). Never bury critical information in the middle of a long document.

---

## 2.3 Retrieval vs. Reasoning — The Critical Distinction

Models can **find** a needle in a haystack (NIAH scores are near perfect). But they **cannot reason** over distributed information in long context.

| Benchmark | What It Tests | Difficulty | Result |
|-----------|--------------|-----------|--------|
| **NIAH** | Find one fact in noise | Easy | ~100% (meaningless) |
| **RULER** | Retrieval + tracing + aggregation | Medium-Hard | Half fail at 32K |
| **NoLiMa** | Associative retrieval (not literal) | Hard | 10/12 models under 50% at 32K |
| **BABILong** | Multi-hop reasoning over distributed info | Very Hard | Models effectively use only 5-25% of window |

**Key insight:** A model with 128K context effectively uses ~10% of it (~16K tokens) for reasoning tasks. The rest is wasted tokens you're paying for.

---

## 2.4 The Solutions — Simple to Advanced

### Layer 1: What to Do FIRST

**Persistent instructions (CLAUDE.md / system prompts).** Loaded automatically every session. Zero extra cost — it's free context. This is the highest-value context engineering you can do.

**Prompt caching.** Stable prefix (system prompt, tools, instructions) cached automatically. **90% cost reduction** on cached tokens, 85% latency reduction. Key: structure prompts so stable content comes first.

**Auto-compression.** Claude Code compresses conversations automatically when context fills. Session Memory writes summaries in the background. Maintain checkpoint files that survive sessions.

### Layer 2: RAG — Retrieve Only What's Relevant

**Why RAG still beats long context:**
- **1,250x cheaper** per query than filling the entire context window
- **Better citation accuracy** — consistently wins on precise source attribution
- **Mitigates "lost in the middle"** — you send only 4-16K tokens of focused context
- **Dynamic data** — perfect for data that changes

**Chunking is the 80% factor.** (Covered in depth in Chapter 5.) Your chunking strategy matters more than your embedding model, your vector database, or your reranking approach. Get chunking right first.

**Reranking is the next step.** First retrieval gets top-20. Cross-encoder reranker reorders them to the best 3-5. Dramatically more precise than bi-encoder similarity alone.

### Layer 3: Context Compression

**LLMLingua (Microsoft):** Up to 20x compression with minimal quality loss. Reduces RAG context by 75% while improving performance by 21.4%. Open source.

**KV Cache compression:** KVzip compresses conversation memory 3-4x, doubles response speed. PagedAttention/vLLM reduces memory waste from 60-80% to under 4%.

### Layer 4: Memory Systems

| System | Approach | Score | Best For |
|--------|---------|-------|----------|
| **Mem0** | Two-phase pipeline | 66.9% | SaaS, simple integration |
| **Letta** (ex-MemGPT) | Agentic self-managed memory | 74.0% | Deep control |
| **Zep/Graphiti** | Temporal knowledge graph | 94.8% | Temporal reasoning |
| **Custom (filesystem)** | CLAUDE.md + scripts + vector DB | Competitive | Solo dev, full control |

**Key insight from Letta:** A simple filesystem-based approach can match specialized memory frameworks. CLAUDE.md + Qdrant + checkpoint scripts is actually competitive.

### Layer 5: Hierarchical Context Management

**Layered memory:**
1. **Working memory:** Current context window (fastest, smallest)
2. **Short-term:** Recent conversation history (summaries, key facts)
3. **Long-term:** Persistent facts, preferences, knowledge base (vector DB)

**Context isolation:** Split context across sub-agents. Each agent has its own context window. Prevents context pollution. Orchestrator synthesizes.

### Layer 6: Knowledge Graphs

**Microsoft GraphRAG** builds entity-relation graphs from text. Local search (DRIFT) for precise queries, global search for thematic questions. Open source.

**Zep's Graphiti** adds temporal tracking — when things happened AND when they were recorded. 94.8% on deep memory retrieval.

**Choose knowledge graphs when:** Relationships between entities matter. "When did customer X change their pickup day?"

**Avoid when:** Standard vector search answers your questions. Most questions don't need relational reasoning. Graphs add significant complexity.

---

## 2.5 Context Engineering — The New Discipline

In July 2025, Gartner declared: **"Context engineering is in, and prompt engineering is out."**

Context engineering is about designing the **minimum set of high-signal tokens** that maximizes the probability of the desired output.

### The 4 Strategies

| Strategy | What | Example |
|----------|------|---------|
| **Write** | Create context | CLAUDE.md, skill files, identity prompts |
| **Select** | Choose relevant context | Vector search, on-demand skill loading |
| **Compress** | Reduce token count | Auto-compression, session summaries |
| **Isolate** | Split across sub-agents | Parallel task agents, context isolation |

### Choose When / Avoid When

**Invest in context engineering when:** You're building systems that run repeatedly. The same context gets used across many interactions. You're paying for tokens at scale.

**Avoid over-engineering when:** You're prototyping. One-off tasks. The system might change tomorrow. Start with CLAUDE.md and prompt caching — these cover 80% of context engineering value with 5% of the effort.

---

## 2.6 The Practitioner's Context Hierarchy

```
START: "My AI responses aren't good enough"
│
├─ Is it a context problem or a capability problem?
│   ├─ Does the model have the information it needs? → Context problem
│   └─ Does it have the info but still fails? → Capability problem (try a better model)
│
├─ Context solutions (in order of effort)
│   ├─ Level 1: Free
│   │   ├─ CLAUDE.md / system prompt (always loaded, zero cost)
│   │   ├─ Prompt caching (90% cost reduction, structure stable prefix first)
│   │   └─ Auto-compression (built-in, just works)
│   │
│   ├─ Level 2: Low effort
│   │   ├─ RAG with vector DB (1,250x cheaper than context stuffing)
│   │   ├─ Better chunking (the 80% factor — get this right first)
│   │   └─ Reranking (cross-encoder on top of initial retrieval)
│   │
│   ├─ Level 3: Medium effort
│   │   ├─ Context compression (LLMLingua, 20x reduction)
│   │   ├─ Hierarchical memory (working + short-term + long-term)
│   │   └─ Context isolation (sub-agents with focused context)
│   │
│   └─ Level 4: High effort (only when justified)
│       ├─ Knowledge graphs (only for relational reasoning)
│       ├─ Specialized memory frameworks (custom > framework for most cases)
│       └─ 1M+ context stuffing (RAG is cheaper and more precise)
│
└─ The 40% Rule: Never fill more than 40% of the context window.
    Above 40% → catastrophic quality collapse, not gradual degradation.
```

---

## 2.7 Our Setup

What we currently use in Ydrasil:
- **CLAUDE.md** with advisor identity (always loaded)
- **Skill-based on-demand context loading** (only load route data when asking about routes)
- **Qdrant** with 7 collections (65K+ data points)
- **Session checkpoints** surviving context compactions
- **Hybrid search** (dense + sparse/BM25)
- **Structural chunking** (## headers, max 2000 chars)

**What we'd add next:** Cross-encoder reranking (big quality improvement, low effort). Prompt caching for API calls (90% cost reduction). LLMLingua when costs become significant.

**What can wait:** Knowledge graphs (only relevant for relational reasoning). Specialized memory frameworks (our custom approach is competitive). 1M context stuffing (RAG is 1,250x cheaper).

---

*The context window is simultaneously the most important and most misunderstood concept in applied AI. Marketing says "bigger is better." Research says "smarter is better." A 200K window with carefully curated 20K of high-signal context beats a 1M window stuffed with everything. Context engineering — not model selection — is where 80% of AI quality is determined.*

**Key sources:** Liu et al. "Lost in the Middle" (2023) · Intelligence Degradation at 40% Threshold (2026) · RULER Benchmark (NVIDIA) · NoLiMa (ICML 2025) · RAG vs Long Context — 1,250x cheaper (2025) · Anthropic Context Engineering Guide · LLMLingua (Microsoft) · Letta Memory Benchmarks · Zep/Graphiti 94.8% temporal retrieval
