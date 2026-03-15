# Chapter 6: AI Agents & Automation — Research Notes

**Researched:** 2026-02-09
**Research base:** Web search (current state 2026), production experience (Ydrasil/n8n/cron), Miessler+Nate Jones frameworks
**Purpose:** Raw material for chapter draft. Focus on Choose when / Avoid when + failure modes.

---

## 6.1 The Automation Spectrum

The biggest mistake people make with automation is reaching for the most exciting tool instead of the simplest one that works. There's a clear spectrum, and most problems sit at the boring end.

### Level 0: Manual Process
You do it yourself. Copy-paste, click buttons, run commands by hand. This is where everyone starts and where most processes should stay until they happen more than twice a week.

### Level 1: Cron + Scripts
A Python script on a cron schedule. No UI, no framework, no dependencies beyond the standard library and maybe `requests`. Runs at 04:00, does its thing, logs the result. Nobody thinks about it until it stops working — which is the highest compliment you can give infrastructure.

**Our setup:** 8 cron jobs run Ydrasil. Hourly session log processing, hourly tmux log rotation, daily backups at 04:00, daily auto-dagbog at 23:55, daily morning brief at 07:00, half-hourly huskeliste scanning, weekly system audit. Total lines of cron config: 15. Total failures in 6 weeks: 0. Cost: $0 (runs on existing VPS).

### Level 2: Webhooks + Event-Driven
Something happens, something else responds. A Telegram message arrives, a webhook fires, a script processes it. Still deterministic. Still simple. The trigger is external instead of time-based.

### Level 3: Workflow Engines (n8n, Make, Zapier)
Visual, node-based automation. Connect services, transform data, add conditional logic. The sweet spot for cross-service integration where you need more than a script but less than an agent.

**Our setup:** 19 n8n workflows handle TransportIntra route data — scanning, sorting, syncing, matching. Plus the Telegram Claude bot. Self-hosted n8n, zero per-execution costs.

### Level 4: LLM-in-the-Loop
An otherwise deterministic workflow that calls an LLM at specific decision points. The workflow handles data flow, error handling, and retries. The LLM handles ambiguity — classification, extraction, summarization. This is the hybrid pattern and it's currently the highest-reliability way to use AI in automation.

### Level 5: Autonomous Agents
The LLM drives the workflow. It decides what to do next, which tools to call, when to stop. Maximum flexibility, minimum predictability. Think Claude Code running in a tmux session with full system access.

**Our setup:** Claude Code running persistently in tmux, with Qdrant for long-term memory, MCP for tool access, hooks for governance. This is a real autonomous agent — and it works because the blast radius is constrained (one VPS, one user, recoverable state).

### The Core Insight

**Most automation problems are Level 1-3 problems.** The industry hype is at Level 5. The production reality is that Gartner predicts 40%+ of agentic AI projects will be cancelled by end of 2027 due to escalating costs, unclear business value, or inadequate risk controls. Meanwhile, a cron job has never been cancelled for unclear business value.

**Choose higher levels when:** The task requires judgment, ambiguity resolution, or natural language understanding. When the input space is too varied for deterministic rules. When the cost of a wrong decision is low and recoverable.

**Stay at lower levels when:** The process is well-defined. When reliability matters more than flexibility. When you need auditability. When the cost of failure is high. When a regex will do.

---

## 6.2 Workflow Engines vs AI Agents: The Hard Comparison

This is the comparison nobody wants to make honestly, because the answer is uncomfortable: deterministic workflows beat AI agents for most production automation.

### The Numbers

| Dimension | Workflow Engine (n8n/Make) | AI Agent (LangGraph/CrewAI) |
|-----------|---------------------------|----------------------------|
| Reliability | 99%+ (deterministic) | 60-90% (depends on task complexity) |
| Cost per execution | ~$0 (self-hosted) or $0.001 | $0.01-$3.00 (LLM API calls) |
| Debugging | Visual trace, step-by-step | Black box reasoning, hard to reproduce |
| Maintenance | Update when APIs change | Update when APIs change AND when model behavior drifts |
| Time to build | Hours (visual builder) | Days-weeks (framework learning curve) |
| Handles ambiguity | No (fails on unexpected input) | Yes (that's the whole point) |
| Auditability | Complete execution logs | Probabilistic — same input can give different output |

### n8n vs Make vs Zapier — Quick Take

**n8n:** Self-hosted, unlimited executions, developer-friendly. Best for technical users who want control. One example: 150,000+ monthly executions at ~$50/month server cost vs $600+ on Zapier. Our choice. Runs our entire route data pipeline.

**Make (formerly Integromat):** Best visual builder, good for non-technical users. Cloud-only. Per-operation pricing can spike unpredictably.

**Zapier:** Simplest to start, largest integration library. Most expensive at scale. Per-task pricing. Good for prototyping, expensive for production.

### LangGraph vs CrewAI vs n8n AI Agent Node

**LangGraph:** Low-level, maximum control. For developers who need stateful, long-running agent workflows. Steep learning curve. Use when you need precise control over agent reasoning loops.

**CrewAI:** Multi-agent orchestration with role-based agents. Enterprise features (HIPAA, SOC2). Use when you genuinely need multiple specialized agents collaborating. Most people don't — they need one agent with multiple tools.

**n8n AI Agent Node:** LangChain-powered reasoning inside the n8n visual builder. Best of both worlds for many use cases: deterministic workflow handles data flow, AI node handles the one step that needs judgment. This is the hybrid sweet spot.

### Choose When / Avoid When

**Choose a workflow engine when:**
- The process has defined steps, even with branching
- You integrate 2+ external services
- Reliability > flexibility
- Non-technical team members need to understand/maintain it
- You can enumerate the possible inputs

**Choose an AI agent when:**
- Input is natural language with high variance
- The task genuinely requires reasoning, not just routing
- Failure is cheap and recoverable (two-way door)
- The alternative is hiring a human to do boring judgment work
- You've tried the workflow approach and hit a wall

**Failure modes of workflow engines:** Brittle — break silently when APIs change. No graceful degradation. If step 3 fails, everything stops. Spaghetti workflows become unmaintainable past ~30 nodes.

**Failure modes of AI agents:** The big one: **error cascading**. One early wrong decision compounds through subsequent steps. Production analysis shows successful agents execute fewer than 10 steps before concluding or handing back to a human. The "let it figure it out" fantasy hits reality fast. Only 5% of organizations have fully integrated AI agents across operations (MLOps community survey 2025). "Agent washing" is rampant — Gartner found only 130 of thousands of vendors claiming "agentic AI" are legitimate.

---

## 6.3 LLM-in-the-Loop: The Hybrid Pattern

This is the pattern that actually works in production, and almost nobody talks about it because it's not sexy enough for a conference talk.

### The Architecture

```
[Trigger] → [Deterministic steps] → [LLM Decision Node] → [Deterministic steps] → [Output]
```

The workflow handles: data fetching, transformation, error handling, retries, logging, routing.
The LLM handles: the ONE step that requires judgment — classifying an email, extracting entities from unstructured text, deciding which template to use, summarizing a document.

### Why This Works

From the arxiv paper "Blueprint First, Model Second" (2025): The LLM is "strategically reframed as no longer the central decision-maker but is invoked as a specialized tool at specific nodes to handle complex but bounded sub-tasks." This is exactly right. The LLM is a function call, not an orchestrator.

### Implementation Patterns

**Classification node:** Input arrives → LLM classifies it into one of N categories → workflow routes based on category. Works because the output space is constrained. The LLM can only return values the workflow knows how to handle.

**Extraction node:** Unstructured data arrives → LLM extracts structured fields → workflow processes the structured data. Works because schema validation catches LLM mistakes before they propagate.

**Decision node with fallback:** LLM evaluates input → if confidence is high, proceed automatically → if low, flag for human review. This is the "ask" pattern — allow, block, or ask.

### Our Setup

The Telegram Claude bot is this pattern: n8n receives the webhook (deterministic), formats the message (deterministic), calls Claude API (LLM decision), returns the response (deterministic). The n8n workflow handles retry logic, rate limiting, and error formatting. Claude handles the actual thinking.

### Choose When / Avoid When

**Choose LLM-in-the-loop when:**
- One specific step in your workflow requires natural language understanding
- You can validate the LLM's output before acting on it
- The rest of the workflow is well-defined
- You want the reliability of a workflow with the flexibility of AI at the bottleneck

**Avoid when:**
- You can solve it with regex, keyword matching, or a lookup table (Ladder of Solutions — start at step 1)
- The LLM call adds >2 seconds of latency and speed matters
- You can't define a schema for the LLM's output
- The cost of the LLM call per execution exceeds the value of automation

**Failure modes:** LLM returns unexpected format despite schema instructions. LLM cost spikes when workflow scales (forgot to add caching). LLM model updates change behavior — your workflow worked with Sonnet 4.5 but breaks with the next version because it interprets the prompt differently.

---

## 6.4 Cron + Scripts: The Boring Technology Advantage

This section exists because the industry has a chronic case of over-engineering. The most reliable automation in Ydrasil isn't the n8n workflows or the Claude agent. It's a Python script that runs every hour and embeds session logs into Qdrant. It has never failed.

### Why Cron Wins

**Zero dependencies beyond the OS.** Cron is built into every Linux system. It doesn't need Docker, doesn't need a database, doesn't need an API key. It runs when the system is up.

**Debuggable in 30 seconds.** Check the log file. Run the script manually. Fix it. Done. No trace viewer, no execution replay, no "which node failed in the visual builder."

**Costs nothing.** No per-execution pricing. No API calls (unless the script makes them). No cloud service subscription.

**Survives everything.** Framework updates, API changes, vendor pivots — cron doesn't care. The script might need updating, but the scheduler never does.

### Our Production Evidence

Eight cron jobs, six weeks, zero scheduler failures. Total development time for all eight: roughly 4 hours. Compare to the n8n TransportIntra workflows: 19 workflows, weeks of development, multiple iterations to get data flow right.

The cron jobs do: session processing, log rotation, backups, auto-dagbog generation, morning briefs, huskeliste scanning, weekly audit. All critical infrastructure. All boring. All working.

### Choose When / Avoid When

**Choose cron + scripts when:**
- The task runs on a schedule (not event-driven)
- Single-service automation (no complex service-to-service integration)
- You're the only maintainer and you can read Python
- The task is "fetch, transform, store" — ETL pattern
- Failure recovery is "just run it again"

**Avoid when:**
- You need real-time event response (use webhooks)
- Multiple services need to coordinate (use a workflow engine)
- Non-technical people need to maintain it
- The workflow has complex branching that's clearer visually
- You need built-in retry logic with backoff (workflow engines do this natively)

**Failure modes:** Silent failure — the script crashes and nobody notices until the data is stale. Time zone confusion. Overlapping executions when a script takes longer than its interval. No built-in alerting (you have to build it yourself).

**Mitigation:** Log to a file. Check logs. Add `|| echo "FAILED" | notify` to the cron line. Keep scripts idempotent so re-running is always safe.

---

## 6.5 MCP (Model Context Protocol)

MCP is the most important infrastructure development in AI tooling since the transformer architecture, and it's also the most overhyped in terms of what it can do *today* versus what it promises.

### What It Is

A protocol that standardizes how AI models connect to external tools and data sources. Think of it as USB-C for AI — one standard interface instead of custom integrations for every tool. Released by Anthropic in late 2024, donated to the Linux Foundation (Agentic AI Foundation) in December 2025 with OpenAI and Block as co-founders.

### The 2026 Reality

**Adoption is real:** OpenAI adopted MCP across Agents SDK (March 2025). Google DeepMind confirmed support in Gemini. 97 million monthly SDK downloads across Python and TypeScript. Tens of thousands of MCP servers exist.

**Standardization is happening:** MCP is now under the Linux Foundation, not controlled by any single vendor. This matters for enterprise adoption — nobody wants to build on a protocol that one company can change unilaterally.

**But security is a serious problem.** OWASP published the MCP Top 10 vulnerabilities list. In January 2026, researchers disclosed three CVEs in Anthropic's own official Git MCP server (CVE-2025-68145, CVE-2025-68143, CVE-2025-68144) that allowed remote code execution via prompt injection. If Anthropic's own MCP servers have RCE vulnerabilities, imagine the state of random community servers.

**Tool poisoning is real.** Malicious tool descriptions can inject prompts that alter agent behavior before the agent even executes anything. This is not theoretical — it's documented and reproducible.

### Our Setup

We use MCP for context retrieval — the `ctx` command searches Qdrant and returns relevant chunks. It works because: (1) the MCP server is self-hosted and self-written, (2) it only reads from Qdrant, never writes to production systems, (3) the blast radius of a compromised context search is "Claude gets bad context" not "production database deleted."

### Choose When / Avoid When

**Choose MCP when:**
- You need to give an LLM access to external data/tools
- You want the integration to work across multiple AI platforms (Claude, GPT, Gemini)
- The tool interaction is read-heavy (lower risk)
- You can run the MCP server yourself or trust the provider

**Avoid when:**
- The MCP server has write access to critical systems and you haven't audited the code
- You're installing community MCP servers without reviewing them (supply chain risk)
- You need the tool interaction to be 100% deterministic (MCP adds the LLM's interpretation layer)
- A direct API call from a script would be simpler and more reliable

**Failure modes:** Tool poisoning via malicious descriptions. Inconsistent authentication across MCP servers (many skip OAuth). Supply chain attacks via compromised MCP packages. Over-permissioning — giving an MCP server access to everything when it only needs one capability. The "too many tools" problem — giving an agent 50 MCP tools and expecting it to reliably choose the right one (it won't).

### The Composability Promise vs Reality

MCP's vision: any AI model can use any tool through a standard protocol. Reality in 2026: this mostly works for simple read operations (search, fetch, query). For write operations with side effects, you need governance layers on top — which is exactly what companies like MidMTP (from the Miessler/Jiquan Ngiam conversation) are building. MCP gateways that proxy all MCP calls through a security layer with allow/block/ask rules.

The honest assessment: MCP is necessary infrastructure. It will become the standard. But right now, using it responsibly requires more security awareness than most teams have.

---

## 6.6 Computer Use & Browser Agents

This is the section where I'm most honest about the gap between demos and production.

### What It Is

AI agents that can see and interact with computer interfaces — clicking buttons, filling forms, navigating websites. Claude Computer Use (launched late 2024, iterating since), browser automation agents, and the newer Claude for Chrome extension (pilot phase, early 2026).

### Current State (February 2026)

**Claude for Chrome:** In controlled pilot with 1,000 Max plan users. Anthropic explicitly states it's not ready for tasks involving sensitive information. Key limitation: prompt injection attacks where malicious website content hijacks the agent's behavior. This is not a bug to be fixed — it's a fundamental architectural challenge of having an AI read and act on untrusted content.

**Claude Computer Use (API):** Available in the API. Works for constrained, well-defined desktop automation tasks. Slow (must wait for page loads, JS execution, DOM rendering). Cannot handle MFA flows. Performance degrades significantly as context windows fill up.

**Third-party browser agents (Hyperbrowser, etc.):** More specialized, sometimes more reliable for specific use cases. But all share the same fundamental limitation: the agent reads content it doesn't control, and that content can contain adversarial instructions.

### The Fundamental Problem

Browser agents read web pages. Web pages are user-generated content. User-generated content can contain prompt injections. This means **any browser agent operating on untrusted websites is inherently vulnerable to having its behavior modified by the content it reads.** This is not a solvable problem with current architectures — it's a tradeoff between capability and security.

### Choose When / Avoid When

**Choose computer/browser use when:**
- Automating internal tools with no API (legacy enterprise software)
- The target site is trusted and controlled (your own admin panel)
- The task is simple and well-defined (fill this form, click this button)
- There is human review before any consequential action
- No alternative exists (no API, no export, no webhook)

**Avoid when:**
- The task involves sensitive data (credentials, financial info, personal data)
- The agent navigates untrusted websites
- You need reliability above 95%
- Speed matters (browser automation is 10-100x slower than API calls)
- An API or direct integration exists (always prefer that)

**Failure modes:** Prompt injection from website content. Dynamic content not loading before agent acts. UI changes breaking the automation (same problem as traditional Selenium scripts, but worse because the agent can't read a diff). Cost — each browser interaction involves sending screenshots to the model, which burns tokens fast. "Laziness" — agents lose focus on complex multi-step browser tasks as context fills up.

### The Honest Assessment

Computer use is currently **demo-grade, not production-grade** for general browsing. It's production-usable for constrained internal tool automation where you control the target interface. The gap will close — but as of February 2026, if you have an API option, use the API. If you have a workflow engine integration, use that. Browser automation is the last resort, not the first choice.

---

## 6.7 Cross-Cutting Themes

### The Simplicity Principle
The Ladder of AI Solutions applies to automation too: Manual → Script → Workflow → LLM-in-loop → Agent. Start at step 1. Most people jump to step 5 because it's exciting. The right question is always: **what's the simplest solution that meets the reliability requirement?**

### Reversibility Determines Autonomy
Two-way door / one-way door framework maps directly to automation autonomy levels. If the automated action is reversible (send a Slack message, create a draft, update a spreadsheet), let the automation run unsupervised. If it's irreversible (deploy to production, send money, delete data), require human approval. This is not conservative — this is engineering.

### The Cost of Intelligence
Every LLM call in an automation costs money, adds latency, and introduces non-determinism. The question isn't "can an LLM do this?" — the question is "does this step require intelligence, or does it require reliability?" Most steps require reliability.

### Governance Is Not Optional
The MCP security conversation (Miessler + Jiquan Ngiam, Feb 2026) makes this clear: as agents get more capable, governance becomes the bottleneck, not capability. Allow/block/ask rules. Monitoring. Audit trails. Blast radius containment. This is the boring work that separates production automation from demos.

### The 40% Failure Statistic
Gartner's prediction that 40%+ of agentic AI projects will be cancelled by 2027 is not about AI being bad. It's about teams choosing Level 5 automation for Level 2 problems. The failures are architectural, not technological. The fix is not better models — it's better judgment about when to use which level.

---

## 6.8 Sources

- [Gartner: Over 40% of Agentic AI Projects Will Be Cancelled by End of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
- [The Agentic Reality Check: Why 40% of AI Projects are failing in 2026](https://dev.to/charanpool/the-agentic-reality-check-why-40-of-ai-projects-are-failing-in-2026-2ie4)
- [Why AI Agents Didn't Take Over in 2025](https://medium.com/@Micheal-Lanham/why-ai-agents-didnt-take-over-in-2025-and-what-changes-everything-in-2026-9393a5bb68e8)
- [Enterprise Process Orchestration in 2026: Stuck Between Rigid Workflows and Unpredictable AI](https://www.trektowin.com/enterprise-process-orchestration-in-2026-why-businesses-are-stuck-between-rigid-workflows-and-unpredictable-ai/)
- [Composio: Why AI Agent Pilots Fail in Production](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap)
- [7 AI Agent Failure Modes and How To Fix Them (Galileo)](https://galileo.ai/blog/agent-failure-modes-guide)
- [Blueprint First, Model Second: A Framework for Deterministic LLM Workflow](https://arxiv.org/pdf/2508.02721)
- [CrewAI vs LangGraph vs n8n: AI Agent Framework Comparison](https://www.3pillarglobal.com/insights/blog/comparison-crewai-langgraph-n8n/)
- [n8n AI Agent Orchestration Frameworks](https://blog.n8n.io/ai-agent-orchestration-frameworks/)
- [A Year of MCP: From Internal Experiment to Industry Standard (Pento)](https://www.pento.ai/blog/a-year-of-mcp-2025-review)
- [Why the Model Context Protocol Won (The New Stack)](https://thenewstack.io/why-the-model-context-protocol-won/)
- [2026: The Year for Enterprise-Ready MCP Adoption (CData)](https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption)
- [MCP Security Vulnerabilities: Prompt Injection and Tool Poisoning (Practical DevSecOps)](https://www.practical-devsecops.com/mcp-security-vulnerabilities/)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [Anthropic MCP Git Server Vulnerabilities (PointGuard)](https://www.pointguardai.com/ai-security-incidents/git-happens-mcp-flaws-open-door-to-code-execution)
- [CoSAI MCP Security White Paper (Adversa AI)](https://adversa.ai/blog/mcp-security-whitepaper-2026-cosai-top-insights/)
- [Claude for Chrome pilot (Anthropic)](https://claude.com/blog/claude-for-chrome)
- [Miessler: When to Use Skills vs Commands vs Agents](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)
- [Miessler + Jiquan Ngiam: Agent + MCP Security conversation](https://www.youtube.com/watch?v=M02kXnomB2U) (2026-02-05)
- Ydrasil production data: crontab, n8n workflows, Claude Code agent setup

---

# PART 2: Agent Architectures — What Works, What's Overhyped

**Researched:** 2026-02-09
**Research base:** 3 parallel angles — agent architectures, framework comparison, production failure analysis
**Sources:** Anthropic "Building Effective Agents," LangChain State of Agent Engineering (1,340 respondents), ICML 2024 papers, production reports, framework docs (cited inline)

---

## 6.9 What IS an Agent? (Cutting Through the Hype)

### The Definition That Actually Helps

Anthropic's "Building Effective Agents" (Dec 2024) draws the only clean line that matters:

- **Workflows:** Systems where LLMs and tools are orchestrated through **predefined code paths**. You decide the control flow. The LLM fills in the blanks.
- **Agents:** Systems where LLMs **dynamically direct their own processes and tool usage**, maintaining control over how they accomplish tasks. The LLM decides the control flow.

This distinction is architectural, not marketing. It tells you what you're signing up for:

| Property | Workflow | Agent |
|----------|----------|-------|
| Control flow | You define it | LLM decides |
| Predictability | High — same path each time | Low — path varies per input |
| Debugging | Trace the pipeline | Trace the reasoning |
| Failure mode | Broken step (local) | Cascading errors (systemic) |
| Testing | Unit test each step | Need evaluation harnesses |
| When to use | You know the steps, LLM fills in content | You can't enumerate all paths upfront |

**The practitioner's test:** Can you draw the control flow on a whiteboard before running the system? If yes, build a workflow. If no, you might need an agent. But check twice — most problems have enumerable paths once you think hard enough.

### The Spectrum (5 Points, Not a Binary)

1. **Single LLM call with tools** — Model gets tools, picks which to call. Not an agent. Claude answering "what's the weather" by calling a weather API.
2. **Prompt chain** — Sequential LLM calls, each processing previous output. Not an agent. A translation pipeline.
3. **Router + specialized paths** — LLM classifies input, routes to predefined handlers. Still a workflow. Customer service routing to billing vs. technical support.
4. **ReAct loop** — LLM reasons, acts, observes, decides next step dynamically. This is where "agent" begins. The model controls the loop.
5. **Fully autonomous agent** — Plans, executes, self-corrects, maintains memory across sessions, operates for minutes to hours without human input. Claude Code in swarm mode. The frontier.

**Our position:** Most production value in early 2026 lives at levels 2-3. Level 4 is production-viable for specific use cases. Level 5 is where demos impress and failure rates are highest.

### Choose When / Avoid When

**Choose a true agent (level 4-5) when:**
- The task has genuinely unpredictable paths (open-ended research, exploratory coding)
- Error cost is low or reversible (two-way door)
- You can afford the token cost (3-10x a workflow for the same task)
- You have evaluation infrastructure to catch failures

**Avoid agents (use workflows instead) when:**
- You can enumerate the steps upfront — most business processes
- Error cost is high or irreversible (financial transactions, customer communications)
- You need audit trails (agent reasoning is a neural net computation, not a logged decision tree)
- Token budget matters — workflow is dramatically cheaper
- You're doing it because "agents" sound impressive

**Failure mode:** The most common failure is deploying an agent where a workflow would work. Teams add autonomous reasoning because it feels sophisticated, then spend months debugging non-deterministic behavior that a 50-line pipeline would have solved.

### The Uncomfortable Numbers

- **LLM-driven agents get multi-step tasks wrong nearly 70% of the time** in simulated office environments (Composio 2025 Agent Report)
- **Only 5% of enterprise-grade generative AI systems reach production** — 95% fail during evaluation
- **Gartner projects 40% of agentic AI projects will be scrapped by 2027**
- This isn't because agents are useless — it's because teams deploy autonomous architectures for problems that need structured workflows

---

## 6.10 Anthropic's Composable Patterns — The Foundation

Before reaching for frameworks, understand the six building blocks from Anthropic's research. Listed in order of complexity — **use the simplest one that works**:

1. **Augmented LLM** — LLM + retrieval + tools + memory. The foundation.
2. **Prompt Chaining** — Sequential LLM calls. Gate each step with validation.
3. **Routing** — Classify input, send to specialized handler.
4. **Parallelization** — Run tasks simultaneously (sectioning or voting).
5. **Orchestrator-Workers** — Central LLM delegates to worker LLMs dynamically.
6. **Evaluator-Optimizer** — Iterative refinement with feedback loops.

Anthropic's key insight: "The most successful implementations weren't using complex frameworks or specialized libraries — they were building with simple, composable patterns." Start with LLM APIs directly. Many patterns are implementable in a few lines of code. If you use a framework, understand the underlying code.

**This is the Ladder of AI Solutions applied to architecture.** Prompt -> Chain -> Route -> Parallelize -> Orchestrate -> Evaluate. Most teams skip to orchestration before exhausting what chaining can do.

Frameworks that create "extra layers of abstraction that can obscure the underlying prompts and responses" are the exact thing Anthropic warns against.

---

## 6.11 Agent Architecture Pattern Catalog

### 6.11.1 ReAct (Reason + Act)

**What it is:** The model thinks out loud, chooses an action, observes the result, then thinks again. A tight loop: Thought -> Action -> Observation -> Thought.

**Choose when:**
- Tasks require dynamic tool selection (you don't know which tools are needed upfront)
- Step-by-step reasoning improves accuracy (math, code debugging, research)
- The number of steps is bounded (typically <10)

**Avoid when:**
- Tasks need long-horizon planning with dependencies between steps
- You need efficiency — ReAct is sequential, can't parallelize
- The task has a known fixed procedure (use a workflow)

**Failure modes:**
- **Myopic reasoning:** Each step optimizes locally without considering the overall goal. The agent does the obvious next thing, not the strategically right thing.
- **Error propagation:** One bad action or observation early in the loop derails all subsequent reasoning. No recovery mechanism built in.
- **Infinite loops:** The agent repeats the same action when it doesn't produce expected results. Must implement circuit breakers (max iterations).

**Production note:** ReAct is the default architecture in most frameworks (LangChain agents, OpenAI function calling loops). Works well for 3-7 step tasks. Beyond that, errors compound faster than reasoning improves.

### 6.11.2 Plan-and-Execute

**What it is:** Separate planning from execution. First, decompose the goal into a structured task list. Then execute each sub-task. Re-plan if something fails.

**Choose when:**
- Tasks have clear sub-task decomposition (project planning, multi-file code changes)
- You need human approval before execution (plan can be reviewed)
- Audit trail matters (plan is an explicit artifact)
- Tasks are long-horizon (10+ steps) — plan keeps the agent on track

**Avoid when:**
- Task is simple enough for a single ReAct loop
- Environment is highly dynamic (plan becomes stale before execution completes)
- You can't afford the overhead — planning adds 1-2 extra LLM calls upfront

**Failure modes:**
- **Plan rigidity:** Initial plan is wrong but agent follows it anyway. Solution: re-planning checkpoints.
- **Over-decomposition:** Agent breaks simple tasks into 15 sub-tasks when 3 would do. Wasted tokens, increased failure surface.
- **Planning hallucination:** Agent creates a plan with steps that reference non-existent tools or impossible actions. Validate the plan before executing.

**Production note:** This is Claude Code's architecture. It plans multi-file edits, shows you the plan, then executes. The "show the plan" step is both transparency and a human-in-the-loop gate. Most production-viable agents in 2026 use some form of Plan-and-Execute.

### 6.11.3 LATS (Language Agent Tree Search)

**What it is:** Monte Carlo Tree Search applied to LLM reasoning. Instead of committing to one path (ReAct), LATS explores multiple action paths in a tree, uses an LLM as a value function to evaluate promising branches, and backtracks from failures. Published ICML 2024 (Zhou et al.).

**Results:** GPT-4 + LATS achieves 94.4% pass@1 on HumanEval (code benchmark), beating ReAct, Reflexion, Chain-of-Thought, and Tree-of-Thought on the same model.

**Choose when:**
- Tasks where trying multiple approaches beats committing to one (code generation, puzzle solving)
- Error cost is high but computation cost is acceptable
- Environment allows state rollback (you can "undo" actions and try again)

**Avoid when:**
- Real-world tasks where you can't revert actions (sent emails, API calls, database writes)
- Token budget is limited — LATS uses **5-10x the tokens** of a single ReAct pass
- Latency matters — exploring a tree takes time
- Production systems with SLA requirements

**Failure modes:**
- **Computational explosion:** Tree grows exponentially with depth. Must limit branching factor and depth.
- **Value function hallucination:** LLM estimates which branches are promising but can be wrong — explores dead-end branches while ignoring the correct one.

**Honest assessment:** LATS is academically impressive and genuinely useful for code generation benchmarks. In production, the "can't revert real-world actions" constraint kills most use cases. Research architecture, not production — yet.

### 6.11.4 Reflexion

**What it is:** The agent attempts a task, evaluates its own output, generates verbal self-critique, stores this reflection in memory, and tries again. "Verbal reinforcement learning" (Shinn et al., 2023).

**Results:** >18% accuracy boost on MCQA tasks. Significant improvements on multi-step reasoning when combined with clear evaluation signals.

**Choose when:**
- Task has a clear success/failure signal (code passes tests, answer matches ground truth)
- Multiple attempts are acceptable (batch processing, not real-time)
- You want the agent to learn within a session (self-improvement across iterations)

**Avoid when:**
- No clear evaluation criteria — the agent can't self-evaluate without a ground truth signal
- Single-attempt tasks (real-time responses)
- The initial attempt is usually correct — reflection adds overhead without benefit on easy tasks

**Failure modes:**
- **Reflection quality dependence:** If self-critique is imprecise, it reinforces suboptimal patterns. The agent confidently repeats mistakes with slightly different wording.
- **Infinite reflection loops:** Agent reflects, tries again, gets similar result, reflects again. Must cap retry count.
- **Scalability:** Storing reflections across long sessions strains context windows.

**Honest assessment:** Reflexion is powerful when combined with concrete evaluation (unit tests, type checkers). Without external verification, the agent is grading its own homework. The combination of Reflexion + external test suite is genuinely useful for code generation.

---

## 6.12 Tool Use and Function Calling — Where Agents Touch Reality

Every architecture above depends on tool use. This is where agents interact with the world — and where they break most often.

### State of the Art (2026)

- **OpenAI:** Structured function calling with strict mode, JSON Schema validation, up to ~100 tools per call
- **Anthropic:** Tool use with integrated agentic loop, MCP for external tools
- **Google:** Function calling in Gemini, similar structured approach

All major providers support tool use. Differences are in reliability, error handling, and edge cases.

### Where Tool Use Breaks

**1. Hallucinated tool calls.** The agent invents tools that don't exist or calls real tools with fabricated parameters. The single most dangerous failure mode. One hallucinated SKU lookup cascades through pricing, inventory, and shipping systems before anyone notices. "One hallucinated fact triggers a multi-system incident" — incident response costs multiply 10x (Composio 2025).

**2. Wrong tool selection.** When multiple tools have overlapping descriptions, the model picks the wrong one. "If multiple tools have overlapping purposes or vague descriptions, models may call the wrong one" (OpenAI docs). Tool description clarity is the primary defense.

**3. Parameter fabrication.** Tool exists, but the agent fills in parameters with plausible-sounding but incorrect values. Customer ID that looks valid but doesn't exist. Date ranges off by one. Dangerous because values pass type validation.

**4. Error handling gaps.** Tool call fails (API timeout, auth error, rate limit). Without explicit error handling in the system prompt, most agents either retry infinitely or continue silently with incomplete data.

### Production Defense Patterns

| Pattern | What it does | Cost |
|---------|-------------|------|
| **Circuit breaker** | Max iteration limit, raise exception if exceeded | Low (5 lines) |
| **Strict mode** | JSON Schema validation for all tool calls | Low (schema def) |
| **Tool result validation** | Check outputs before passing to next step | Medium |
| **Confirmation gates** | Human approves destructive tool calls | Medium |
| **Prompt caching** | Avoid repaying for static system prompts | Low (API flag) |
| **Audit logging** | Log every tool call, input, and output | Medium |

**The essential insight:** Tool use reliability comes from **tool design**, not model capability. Clear descriptions, minimal overlap, explicit error messages, bounded parameter spaces. Spend 80% of your time on tool definitions, 20% on agent logic. This is Scaffolding > Models applied to function calling.

---

## 6.13 Multi-Agent Systems — When More Agents Isn't Better

### The Promise

Multiple specialized agents collaborating: a researcher finds information, a writer drafts content, a reviewer catches errors. Like a human team.

### The Reality

Research from late 2025 (VentureBeat): **"More agents isn't a reliable path to better enterprise AI systems."** For tasks requiring 10+ tools, single-agent systems outperform multi-agent by a **2-6x efficiency factor**. The reason: context fragmentation. When compute budget splits across agents, each agent has insufficient context for tool orchestration compared to a single agent with unified memory.

LangChain State of Agent Engineering survey (1,340 respondents, Dec 2025): 57.3% have agents in production. Primary use cases: customer service (26.5%), research/data analysis (24.4%), internal workflow automation (18%). These are predominantly **single-agent** deployments.

### Choose When / Avoid When

**Choose multi-agent when:**
- Tasks are genuinely parallelizable (3 independent research streams that merge)
- Agents need different system prompts or tool sets (can't fit in one context)
- You're orchestrating heterogeneous models (cheap model for classification, expensive for generation)
- The task naturally decomposes into reviewer/creator pairs with adversarial dynamics

**Avoid multi-agent when:**
- A single agent with good tools can handle the task — this is the common case
- Agents need to share state frequently (coordination overhead exceeds benefit)
- You're adding agents because "multi-agent" sounds sophisticated
- Token budget matters — multi-agent multiplies cost, not divides it

**Failure modes:**
- **Coordination overhead:** Each handoff between agents is a failure point. Information lost in translation. Context that doesn't survive handoffs.
- **Multiplied hallucination probability:** Agent A hallucinates, passes result to Agent B, which treats it as ground truth. Error multiplication, not error correction.
- **Debugging complexity:** Which agent caused the failure? Three agents = three reasoning traces to debug.
- **Cost multiplication:** Three agents use 3x tokens minimum, often more due to coordination messages.

**The "multi-agent debate" pattern** (agents argue and converge) works in specific domains: code review (write + review), fact-checking (claim + verification), adversarial red-teaming. Outside these, it's overhead.

---

## 6.14 Agent Frameworks (2026) — Production vs Demo

### The Landscape

| Framework | Philosophy | Strength | Weakness | Prod readiness |
|-----------|-----------|----------|----------|----------------|
| **LangGraph** | Stateful graphs | Precise control, persistence, human-in-loop | Steep learning curve | High — industry standard |
| **CrewAI** | Role-based teams | Intuitive multi-agent, beginner-friendly | Abstraction hides control | Medium-High |
| **AutoGen** (MS) | Agent conversations | Dynamic dialogue, research pedigree | Complex setup | Medium |
| **OpenAI Assistants** | Managed service | Zero infra, built-in tools | Vendor lock-in, opaque | Medium |
| **Claude Code** | Agentic coding | Plan-and-execute, CLAUDE.md, swarm | Specialized for dev tasks | High |
| **Raw API + tools** | DIY | Maximum control | You build everything | Highest (if you can) |

### The Honest Assessment

**LangGraph** is the right choice for custom agents in 2026. Forces you to think about state management, human-in-the-loop, and error handling because they're first-class concepts. The learning curve is the feature — it makes you design the control flow instead of hoping the LLM figures it out.

**CrewAI** is right if your mental model is "team of specialists." Reads naturally in Python. Role/goal/backstory metaphor makes design intuitive. But abstraction hides what happens under the hood. When things break, you debug through layers you didn't write.

**AutoGen** is strongest as a research platform. Multi-agent conversation model is powerful but complex. Production deployments exist but require more engineering effort than LangGraph for comparable reliability.

**Raw API calls** — Anthropic's own recommendation. "Many patterns can be implemented in a few lines of code." Frameworks that create "extra layers of abstraction that can obscure the underlying prompts and responses" are the exact thing they warn against.

### Token Efficiency Reality

Multi-agent setups carry a concrete token tax:

- **Single agent with tools:** Baseline token cost
- **Two-agent pipeline:** ~2-3x baseline (system prompts loaded twice, context passed between agents)
- **Multi-agent crew (3+):** ~3-6x baseline, non-linear scaling from coordination overhead
- **Prompt caching** mitigates cost: modern APIs charge vastly reduced rates for repeated tokens

The emerging enterprise rule: **90% of implementations should be deterministic workflows, 10% should be agents** — deployed where they truly excel (open-ended tasks with unpredictable paths).

### Choose When / Avoid When (Frameworks)

**Choose a framework when:**
- You need persistence, human-in-the-loop, or state management that's painful to build from scratch
- Multiple developers need a shared abstraction
- You want built-in observability (LangGraph + LangSmith, CrewAI dashboard)

**Avoid frameworks when:**
- Your agent is <100 lines of logic — framework overhead exceeds implementation
- You're prototyping — frameworks slow iteration
- You can't explain what the framework does under the hood — you won't debug production failures

---

## 6.15 The Autonomy Spectrum — Where to Be in 2026

### Five Levels

| Level | Description | Example | Human role | Risk |
|-------|-------------|---------|------------|------|
| **L1: Autocomplete** | Predicts next token/action | Copilot inline suggestions | Every keystroke | ~Zero |
| **L2: Copilot** | Drafts, human reviews | ChatGPT for emails, Cursor for code | Every output | Low |
| **L3: Supervised agent** | Multi-step, human approves key decisions | Claude Code (plan before execute) | Decision gates | Medium |
| **L4: Autonomous + guardrails** | Independent within boundaries | Customer service with escalation | Exceptions only | Med-High |
| **L5: Fully autonomous** | No human oversight | No reliable examples at scale yet | None | High |

### Where Practitioners Should Be (2026)

**L2-L3 is the sweet spot.** L2 (copilot) is table stakes. L3 (supervised agent) is where real leverage appears: AI does the work, you provide judgment at key gates.

L4 is viable for narrow, well-defined domains with clear escalation paths. L5 is where demos live and production failures accumulate.

**The Nate Jones frame:** L1-L3 are two-way doors — review, revert, iterate. L4-L5 are increasingly one-way — autonomous actions have consequences expensive to reverse.

### What to Automate vs What Needs Humans

**Safe to automate (L3-L4):**
- Code generation with test suites as guardrails
- Data analysis and report drafting (human reviews conclusions)
- Routine customer queries with clear resolution paths
- Monitoring, alerting, first-response triage
- Content drafting (human edits before publishing)

**Needs human-in-the-loop (L2-L3):**
- Communications with emotional or legal stakes
- Financial decisions above a threshold
- Architecture decisions (AI proposes, human decides)
- Anything touching production infrastructure
- Creative work where taste matters (AI generates options, human curates)

**Don't automate yet:**
- High-stakes decisions with insufficient training data
- Tasks where failure is invisible (silent data corruption)
- Anything where "success" can't be defined clearly enough to evaluate

### The Judgment Tax

The deeper insight: **automation doesn't eliminate human judgment, it changes where judgment is applied.** With copilots, you judge the output. With agents, you judge the architecture, the guardrails, the evaluation criteria. Judgment moves upstream — from "is this response good?" to "is this system designed to produce good responses?"

This is Miessler's "Taste as bottleneck" in action. The model is cheap. The judgment about what to automate, where to put gates, what failure rate is acceptable — that's the expensive human contribution.

---

## 6.16 Production Reality: The Numbers

From the LangChain State of Agent Engineering survey (1,340 respondents, Dec 2025):
- **57.3%** have agents in production (up from 51% YoY)
- **32%** cite quality/accuracy as top production barrier
- **89%** have implemented agent tracing/observability
- **75%+** use multiple model providers in production
- **59.8%** rely on human review for evaluation (LLM-as-judge at 53.3%)
- **Only 43%** have attempted fine-tuning — most rely on base models + RAG

From Composio 2025 Agent Report:
- **Only 5%** of enterprise-grade generative AI systems reach production
- **Three leading causes of failure:** Bad memory management ("Dumb RAG"), brittle API connectors, no event-driven architecture
- **Most production failures aren't model failures — they're context failures:** agents drowning in irrelevant information, receiving ambiguous tools, maintaining coherence across bloated histories

The meta-pattern: **the hard part isn't making agents work. It's making agents fail gracefully.** The system that hallucinates 5% of the time and catches 4.9% is production-ready. The system that hallucinates 1% but catches 0% is a time bomb.

---

## 6.17 Sources (Part 2 — Agent Architectures)

### Primary Research
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — foundational patterns document
- [LangChain: State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering) — 1,340 respondent survey, Dec 2025
- [Composio: 2025 AI Agent Report](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap) — production failure analysis
- [Zhou et al.: Language Agent Tree Search, ICML 2024](https://arxiv.org/abs/2310.04406)
- [Shinn et al.: Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [Self-Reflection in LLM Agents: Effects on Problem-Solving Performance](https://arxiv.org/abs/2405.06682)

### Framework Documentation
- [OpenAI: Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Anthropic: Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [LangGraph Tutorial: LATS](https://langchain-ai.github.io/langgraph/tutorials/lats/lats/)

### Production Analysis
- [Galileo: 7 Agent Failure Modes](https://galileo.ai/blog/agent-failure-modes-guide)
- [Inkeep: Context Engineering — Why Agents Fail](https://inkeep.com/blog/context-engineering-why-agents-fail)
- [VentureBeat: More Agents Isn't a Reliable Path](https://venturebeat.com/orchestration/research-shows-more-agents-isnt-a-reliable-path-to-better-enterprise-ai)
- [Token Cost Trap: Why Your AI Agent's ROI Breaks at Scale](https://medium.com/@klaushofenbitzer/token-cost-trap-why-your-ai-agents-roi-breaks-at-scale-and-how-to-fix-it-4e4a9f6f5b9a)
- [By AI Team: ReAct vs Plan-and-Execute for Reliability](https://byaiteam.com/blog/2025/12/09/ai-agent-planning-react-vs-plan-and-execute-for-reliability/)
- [2025 Overpromised AI Agents. 2026 Demands Agentic Engineering](https://medium.com/generative-ai-revolution-ai-native-transformation/2025-overpromised-ai-agents-2026-demands-agentic-engineering-5fbf914a9106)

### Framework Comparisons
- [DataCamp: CrewAI vs LangGraph vs AutoGen](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [DEV.to: LangGraph vs CrewAI vs AutoGen — Complete 2026 Guide](https://dev.to/pockit_tools/langgraph-vs-crewai-vs-autogen-the-complete-multi-agent-ai-orchestration-guide-for-2026-2d63)
- [Miessler: When to Use Skills vs Workflows vs Agents](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)
- [Softcery: 14 AI Agent Frameworks Compared](https://softcery.com/lab/top-14-ai-agent-frameworks-of-2025-a-founders-guide-to-building-smarter-systems)

---

**Total word count (Part 1 + Part 2):** ~5,400
**Part 2 word count:** ~2,600
**Next step:** Merge Parts 1 and 2 into a unified Chapter 6 draft, following Ch 3-5 voice and structure.
