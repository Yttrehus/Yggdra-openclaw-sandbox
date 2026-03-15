# Chapter 1: Research Methodology — How to Actually Know Things

> "An anecdote is not evidence. One source is an opinion. Two sources are an indication. Three independent sources are evidence."

You can't build a good knowledge base with bad method. And most AI users research wrong: they ask one question, get one answer, and believe they've "researched" it. That's reading the back cover of one book and thinking you understand the subject.

Real research with AI is different. It's systematic, multi-perspective, and verified. This chapter describes the method used to build every other chapter in this book — and the method you should use for any serious AI-assisted research.

---

## 1.1 The 5 Research Layers

Structured research follows a progression from broad to deep:

### Layer 1: Broad Survey — "What exists?"

Map the landscape. Who are the players? What are the key concepts? Where's the debate?

**Method:** 3-5 parallel web searches with different angles. Read official documentation + independent reviews. Note names, frameworks, key terms.

**Output:** A list of topics, players, and open questions.

**Failure mode:** Stopping here. Layer 1 gives overview but no depth. Most AI-generated "research" is Layer 1 — surface coverage that sounds authoritative but hasn't been verified or pressure-tested.

### Layer 2: Sources & Experts — "Who actually knows?"

Find the primary sources. Not blog posts *about* the topic, but people who *built* the thing.

**Method:** Identify 3-5 key practitioners per topic. Find their primary sources: talks, papers, docs, GitHub repos. Categorize: academic vs. practical, vendor vs. independent.

**Output:** A curated source list with credibility assessment.

**Principle: Source triangulation** — If 3 independent experts say the same thing, it's probably true. If only one says it, it's an opinion.

### Layer 3: Deep Research — "What's actually true?"

Go deep. Read primary sources. Understand nuances.

**Method: Triple Perspective** — For each topic, run 3 parallel research agents:

1. **Neutral Agent** — "Explain this objectively. What are the facts?"
2. **Blue Team (Advocate)** — "Argue FOR this. What are the strengths? When is it the best solution?"
3. **Red Team (Critic)** — "Argue AGAINST this. What are the weaknesses? When does it fail?"

No single perspective gives the full picture. Blue Team catches strengths you overlook. Red Team catches traps you don't consider. Neutral ensures the factual foundation.

**Output:** A balanced analysis with strengths, weaknesses, and use cases.

### Layer 4: Assessment — "What does this mean for ME?"

Translate abstract knowledge to your concrete situation.

**Method:**
- What's my current state? (What do I have now?)
- What's my desired state? (What do I want to achieve?)
- Which tradeoffs are acceptable? (Cost, complexity, vendor lock-in)
- Is this a two-way door? (Can I reverse it?)

**Output:** A decision matrix with concrete recommendations.

### Layer 5: Distillation — "What's the usable essence?"

Boil everything down to knowledge you can actually use.

**Method:**
- Write as if explaining to yourself in 6 months
- Remove everything that's "nice to know" but not "need to know"
- Preserve concrete examples and action steps
- Embed in a searchable system (Qdrant, notes, whatever you use)

**Output:** A chapter in your handbook. Clear, concrete, action-oriented.

---

## 1.2 Multi-Agent Research Patterns

### Pattern 1: Parallel Survey (Layer 1-2)

```
Orchestrator (you/Claude)
├── Agent A: Web search angle 1
├── Agent B: Web search angle 2
├── Agent C: Web search angle 3
└── Agent D: Official documentation
    ↓
Synthesis: Combine results, remove duplicates, identify gaps
```

**Choose when:** Starting a new topic and need broad overview fast.

### Pattern 2: Triple Perspective (Layer 3)

```
Orchestrator
├── Neutral Agent: "Explain X objectively"
├── Blue Team Agent: "Argue FOR X"
└── Red Team Agent: "Argue AGAINST X"
    ↓
Synthesis: Balanced analysis with strengths, weaknesses, use cases
```

**Choose when:** You need to understand a topic in depth and avoid bias.

### Pattern 3: Angle-Based Research (Layer 3-5)

This is the pattern that evolved through writing this book. Instead of neutral/blue/red, give each agent a **specific angle:**

```
Orchestrator
├── Agent 1: Architecture & technical foundations
├── Agent 2: Production patterns & practical implementation
└── Agent 3: Anti-patterns, failures & what goes wrong
    ↓
Synthesis: Chapter combining all three perspectives
```

**Choose when:** Building actionable content. The anti-patterns agent consistently produces the strongest material — real incidents with sources, production failures, honest limitations. This is the pattern used for Chapters 5-10.

**Key lesson:** Sharp, opinionated prompts ("Focus on failures and what to avoid. Include real incidents with sources.") produce dramatically better output than broad prompts ("Research everything about X").

### Pattern 4: Source Verification (Layer 2-3)

```
Research Agent finds claim P
├── Verification Agent 1: Check P against source A
├── Verification Agent 2: Check P against source B
└── Verification Agent 3: Check P against official docs
    ↓
Confidence score: Confirmed by 3/3, 2/3, or 1/3 sources
```

**Choose when:** Something sounds too good (or too bad) to be true.

---

## 1.3 Verification Principles

### AI Hallucinates. Always.

This is not a question of whether the model is good enough. Even the best models invent facts. Therefore:

**Rule 1: Triangulation.** A claim is only verified when 3 independent sources confirm it. One source = anecdote. Two = indication. Three = evidence.

**Rule 2: Primary sources over secondary.** Official documentation > blog post > AI-generated answer. Always go to the source.

**Rule 3: Check dates.** AI knowledge has cutoff dates. Technology changes. Something true in 2024 may be outdated in 2026.

**Rule 4: Red team your own output.** When you have a conclusion, explicitly ask: "What's wrong with this analysis? What's missing? Where are my blind spots?"

**Rule 5: Confidence scoring.** For each key claim:
- **High (3/3 sources):** Fact, act on it
- **Medium (2/3 sources):** Probable, verify when implementing
- **Low (1/3 or AI-generated):** Hypothesis, needs further research

---

## 1.4 Token Economics

Research costs tokens. Be aware:

| Pattern | Token usage | Estimated cost |
|---------|-------------|----------------|
| Single question | ~2K tokens | ~$0.01 |
| Parallel survey (4 agents) | ~40K tokens | ~$0.30 |
| Triple perspective | ~30K tokens | ~$0.20 |
| Full deep research (Layer 1-5) | ~200K tokens | ~$1-3 |
| Book distillation (like this book) | ~500K+ tokens | ~$5-15 |

**Rule of thumb:** Deep research on one topic costs $1-3. A complete handbook costs $10-30. That's nothing compared to the value of actually understanding something.

---

## 1.5 Anti-Patterns — What NOT to Do

1. **One-shot research** — Ask one question, accept the answer. You get shallow knowledge with potential errors.

2. **Echo chamber** — Use only one model or source. You inherit its biases.

3. **Volume over depth** — 50 surface searches don't beat 5 deep ones. Quality > quantity.

4. **No verification** — "Claude said it, so it's true." No.

5. **Research without distillation** — 100 pages of raw notes are useless. Always distill.

6. **Perfectionism** — Waiting for "complete" research. Research is iterative. Start, publish, revise.

7. **Broad fundamentals prompts** — "Research everything about prompt engineering" drowns agents in material. Sharp angles deliver: "Research prompt engineering anti-patterns and production failures."

---

## 1.6 What We Learned Building This Book

This methodology was tested across 10 chapters, 30 research agents, and ~50,000 words of output. Key findings:

**3 agents with different angles > 3 agents with different sources.** Architecture, production patterns, and failures as angles produce comprehensive coverage. Three agents doing the same thing from different sources produce redundant output.

**~2,500 words per agent is the sweet spot.** Enough for depth, not so much they pad. Tell agents to "write findings progressively" — agents that try to read everything before writing get stuck.

**Kill stuck agents after 10 minutes.** If no file has been written, the agent is consuming rather than producing. Use available data and move on.

**The anti-patterns agent is always strongest.** Real incidents, real sources, real consequences. "What goes wrong" is inherently more valuable than "what features exist."

**Total time per chapter: ~15-20 minutes.** Launch 3 agents (~4-5 min each), read research files, synthesize into ~400-line chapter, commit.

---

## 1.7 Our Research Workflow

The concrete workflow used in Ydrasil:

1. **Define the question precisely.** Not "tell me about LLMs" but "Which LLM is best for code generation in February 2026, and why?"
2. **Launch parallel agents.** 3 agents with specific angles, ~2,500 word target each, "Choose when / Avoid when" structure.
3. **Read all research files.** Look for convergence, contradictions, and gaps.
4. **Synthesize.** Write the chapter combining all perspectives. ~400 lines, opinionated, with decision tree at end.
5. **Verify key claims.** Cross-check impressive numbers against primary sources.
6. **Commit and embed.** Version control + searchable knowledge base.
7. **Review.** Read your output next day. Missing anything? Anything wrong?

---

*The method is the product. Bad method produces confident-sounding garbage. Good method produces knowledge you can trust and act on. Every other chapter in this book was built with this methodology — and the methodology itself was refined by building those chapters.*

**Key sources:** Anthropic "Building Effective Agents" · Anthropic Multi-Agent Research System (90% improvement) · Google Agent Threshold Research (45% single-agent accuracy) · Nate Jones: Context > Capability · Daniel Miessler: Current → Desired State
