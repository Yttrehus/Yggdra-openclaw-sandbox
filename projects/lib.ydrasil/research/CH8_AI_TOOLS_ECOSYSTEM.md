# Chapter 8: AI Development Tools — What to Use for What

**Written:** 2026-02-09
**Research base:** 3 parallel agents — IDE/coding tools landscape, API/platform economics, no-code/consumer AI maturity
**Sources:** 25+ product pages, pricing comparisons, practitioner reviews, and production failure reports (cited inline)

---

## 8.1 The Tool Explosion Problem

There are now over 50 AI-powered coding tools, a dozen API providers, and countless "build an app with AI" platforms. Most practitioners respond to this in one of two ways: either they freeze (too many options, pick none) or they chase (new tool every week, master none).

Both responses are wrong.

The reality: **3-4 tools cover 90% of what any practitioner needs.** The rest is noise. This chapter identifies which 3-4 tools those are for different practitioner profiles, and — more importantly — tells you honestly where each one breaks.

The Miessler principle applies directly: **scaffolding > models (80/20).** The tool is not the bottleneck. Your ability to give it the right context is. A mediocre tool with excellent context beats a brilliant tool with vague instructions. Every time.

---

## 8.2 IDE and Coding Tools — The Real Landscape

Five names dominate: **Cursor, Claude Code, GitHub Copilot, Windsurf, and Cline.** They all use frontier models under the hood. The difference is not intelligence — it's workflow. Each tool embeds AI into your development process differently, and that difference determines when each one wins.

### Cursor

Cursor is a VS Code fork rebuilt around AI. It's the most complete AI IDE on the market: inline completions, multi-file editing (Composer), project-aware chat, and an Agent mode that can plan and execute multi-step changes across your codebase.

Its real strength is **control**. You can point it at specific files, define project rules via `.cursorrules`, and guide it through complex refactors with structured instructions. Cursor excels when you need to make coordinated changes across 10-20 files while maintaining architectural coherence. It's the tool for developers who think in systems.

**Choose Cursor when:** You're a developer working on a real codebase. Multi-file refactors. Architecture changes. You want AI that understands your project structure and follows your conventions.

**Avoid Cursor when:** You're not a developer. The value proposition depends on you understanding what Cursor is doing and steering it. Without software judgment, you'll accept broken code and not notice.

**Honest limitation:** The credit-based pricing (post-June 2025) is opaque. Pro is $20/month, but your credits deplete faster with better models. Ultra ($200/month) removes the anxiety but is expensive for casual use. The gap between "marketing pricing" and "actual cost for heavy use" is real.

**Pricing reality:** Free tier exists but is extremely limited (50 premium requests). Pro ($20/month) works for moderate use. Heavy users need Pro+ ($60) or Ultra ($200).

### Claude Code

Claude Code is fundamentally different from the others. It's not an IDE — it's a **command-line agent**. You give it a task in your terminal and it works autonomously: reads files, makes edits, runs tests, iterates on failures. No GUI, no syntax highlighting, no live preview. Just results.

This sounds limiting, but it's the opposite for a specific type of work. Claude Code excels at **autonomous multi-step tasks** — "refactor this module, update all tests, and verify everything passes." The 1M token context window (beta) means it can hold your entire codebase in memory simultaneously, something no IDE-based tool can match.

The deeper advantage: Claude Code scales to **agentic workflows**. It can run sub-agents, use tools via MCP (Model Context Protocol), and maintain persistent context across sessions. It's the tool Daniel Miessler has built his entire 77-skill Personal AI infrastructure around — not because it's the easiest, but because it's the most composable.

**Choose Claude Code when:** You think in terms of tasks, not keystrokes. You want AI that operates on your codebase autonomously. You're building pipelines, automation, or systems that involve multiple tools. You're comfortable in a terminal.

**Avoid Claude Code when:** You need visual feedback while coding. You're making small inline edits where Cursor's Tab completions are faster. You want GUI comfort.

**Honest limitation:** The learning curve is real. There's no "try it and see" — you need to invest in CLAUDE.md, skills files, and context management before it becomes powerful. It's a tool that rewards builders who build their own scaffolding around it.

**Pricing reality:** Included in Claude Pro ($20/month) but rate-limited. Max 5x ($100/month) or Max 20x ($200/month) for serious work. Alternatively, bring your own API key (pay per token). For heavy daily use, expect $100-200/month.

### GitHub Copilot

Copilot's real advantage isn't AI quality — it's **zero friction**. It lives inside VS Code, JetBrains, Neovim, and Visual Studio. You don't switch editors. You don't learn a new workflow. You just get completions and chat where you already work.

The free tier (2,000 completions + 50 premium requests/month) is genuinely useful for learning and light work. At $10/month for Pro, it's the cheapest paid option by a wide margin. And because it's GitHub-native, it understands your repos, PRs, and issues without configuration.

**Choose Copilot when:** You want AI assistance without changing your workflow. You're in a team that uses GitHub heavily. You want the lowest-friction, lowest-cost entry point. The free tier is unbeatable for students and casual developers.

**Avoid Copilot when:** You need deep multi-file refactoring or autonomous agents. Copilot's Agent mode exists but consumes premium requests quickly and isn't as capable as Cursor's Composer or Claude Code's autonomous operation. At the top end, you're paying for convenience, not capability.

**Honest limitation:** The 300 premium requests on Pro ($10/month) sounds generous until you use Agent mode or Claude/GPT-5.2 models in chat. Heavy users burn through it in a week. Pro+ ($39/month) helps but costs more than Cursor Pro while offering less.

**Pricing reality:** Free tier is real and useful. Pro ($10/month) is the best value entry point in the market. But capability ceiling is lower than Cursor or Claude Code.

### Windsurf (Now OpenAI-owned)

Windsurf was acquired by OpenAI for $3 billion in 2025. Its signature "Flow" technology maintains real-time sync between the AI and your workspace, creating what feels like pair programming rather than request-response interaction.

**Choose Windsurf when:** You want the most fluid AI coding experience. The real-time awareness is genuinely different from competitors.

**Avoid Windsurf when:** You're concerned about vendor lock-in. Post-acquisition, Windsurf's future is tied to OpenAI's strategic decisions. The credit-based pricing (starting $15/month) can be unpredictable. And the competitive moat is thin — Cursor and Copilot are adopting similar real-time features.

**The honest take:** Windsurf is good, but it's the most strategically uncertain option. Watch what OpenAI does with it before committing your workflow.

### The Verdict

For most developers in 2026: **start with Copilot Free to get comfortable with AI coding, then graduate to Cursor Pro or Claude Code depending on whether you prefer visual or terminal-first workflows.** If you're building AI systems specifically, Claude Code is unmatched. If you're a professional developer working on traditional codebases, Cursor is the most capable IDE.

---

## 8.3 AI APIs and Platforms — The Provider Question

If you're building anything beyond personal scripts, you need an API. The three that matter: **Anthropic (Claude), OpenAI (GPT), and Google (Gemini).** Open-source (via Ollama or vLLM) is the fourth option for specific cases.

### The Big Three

**Anthropic API (Claude)**
- Strengths: Best for code generation, complex reasoning, long documents (200K context standard, 1M beta). Claude Sonnet 4.5 is the price/performance sweet spot. Prompt caching reduces repeated context costs by 90%.
- Weakness: Smaller ecosystem than OpenAI. Fewer integrations, fewer tutorials, fewer community resources. If you need vision, image generation, or voice, you need a second provider.
- Pricing: Sonnet 4.5 at ~$3/$15 per million tokens (input/output). Haiku 4.5 at $0.50/$2.50 — excellent for high-volume classification and routing.

**OpenAI API (GPT)**
- Strengths: Largest ecosystem. Most third-party integrations. GPT-5.2 is competitive across all tasks. Best multimodal coverage — text, vision, voice, image generation, video (Sora). Structured outputs (JSON mode) are rock-solid.
- Weakness: More expensive at the top end. Rate limits can be frustrating on lower tiers. The rapid product churn (models deprecated, endpoints changed) means maintenance overhead.
- Pricing: GPT-5.2 at ~$5/$15 per million tokens. GPT-4o-mini at $0.15/$0.60 — the cheapest capable model in the market.

**Google AI (Gemini)**
- Strengths: Massive context window (up to 2M tokens on Gemini 3 Pro). Native Google Workspace integration. Competitive pricing. If your data lives in Google, Gemini has the lowest integration friction.
- Weakness: API stability has historically been shakier than Anthropic or OpenAI. Developer experience (docs, error messages, client libraries) lags behind. The product direction shifts frequently.
- Pricing: Aggressive — often undercutting both competitors, especially with cached prompts.

### The Vendor Lock-in Reality

Here's the uncomfortable truth: **you will be somewhat locked in, and that's acceptable.** The dream of perfectly portable LLM code is a dream. Each provider has different prompt formats, different tool calling conventions, different strength profiles. Code written for Claude's XML-style tool use doesn't transfer to OpenAI's function calling without rewriting.

The practical strategy: **Pick one primary provider. Build your core system around it. Use a second provider for specific tasks where the primary is weak.** For most practitioners, this means Claude or GPT as primary, with the other as secondary, and maybe Gemini for bulk processing where cost matters.

**Don't** build an abstraction layer that makes all providers interchangeable. That's premature optimization. You'll spend more time maintaining the abstraction than you'd save by switching providers. When — not if — you need to switch, it'll be a deliberate migration, not a config change.

### Open Source: Ollama and vLLM

**Ollama** is Docker for LLMs. One command pulls and runs a model locally. It's the right answer when: (1) you need privacy — data never leaves your machine, (2) you're experimenting and don't want to pay per token, or (3) you're running on Apple Silicon where local models perform surprisingly well.

**vLLM** is the production-grade option — 2-4x faster than Ollama for concurrent requests, built for serving models at scale. Choose it when you're running inference for multiple users, not just yourself.

**Choose local/open-source when:** Data privacy is non-negotiable (medical, legal, classified). You have predictable, high-volume workloads where API costs would be astronomical. You're fine with models that are good but not frontier-quality.

**Avoid local when:** You need frontier intelligence. The gap between the best open-source model (Llama 4, Qwen 3, DeepSeek R1) and Claude Opus or GPT-5.2 is smaller than ever but still real for complex reasoning tasks. And the total cost of ownership (GPU hardware, electricity, maintenance) often exceeds API costs for moderate usage.

---

## 8.4 No-Code / Low-Code AI Tools — The Vibe Coding Reality

The "vibe coding" phenomenon — describing what you want in natural language and getting a working app — is real. Tools like **v0 (Vercel), Bolt.new, Lovable, and Replit Agent** can generate functional web applications from a prompt. The question isn't whether they work. It's **where they stop working.**

### What They Can Actually Build

These tools excel at: landing pages, dashboards, CRUD apps, internal tools, MVPs for investor demos, and personal utilities. Lovable has the shortest learning curve (days, not weeks). Replit Agent handles full-stack (database included). v0 produces the cleanest frontend code (React/Next.js).

A non-developer can go from idea to deployed app in hours. This is genuinely transformative. The Miessler observation captures it: "It has never been possible for pretty much anyone to go from an idea to a working, beautiful application in a few minutes."

### Where They Break — The Technical Cliff

The pattern is consistent: beautiful UI, broken backend. Practitioners report:

- **Security disasters:** Apps launching with databases completely open. Anyone who finds the URL can see all user data, payment info, private records. Premium features unlockable by changing one number in the browser console.
- **The 90% trap:** More than 90% of generated apps don't work correctly on first try. They look right but break on edge cases — malformed data, network failures, concurrent users.
- **The SaaS cautionary tale:** A developer built an entire SaaS with "zero hand-written code" and celebrated publicly. Within weeks: "random things are happening, maxed out usage on API keys, people bypassing the subscription, creating random shit on db."
- **Debugging is harder, not easier:** When the AI wrote every line, debugging through unfamiliar patterns takes longer than debugging your own code.

### Choose When / Avoid When

**Use vibe coding when:** Prototyping an idea (hours, not weeks). Building internal tools with no public users. Creating personal utilities. Validating a concept before investing in real development. You understand what the tool is generating and can spot problems.

**Avoid vibe coding for:** Anything handling money, personal data, or health information. Production systems with real users. Anything where "it mostly works" isn't acceptable. And critically: avoid it if you can't read the code it generates. The tool is a power tool, not a magic wand — you still need to verify its output.

**The framework:** Vibe coding is a **two-way door** (reversible) for prototypes. It becomes a **one-way door** (dangerous) the moment you put it in front of real users with real data. The transition from prototype to production requires a developer, period.

---

## 8.5 AI for Non-Developers — The Knowledge Worker Toolkit

For professionals who don't write code — strategists, researchers, writers, managers, consultants — the relevant tools are the consumer AI platforms. Four matter. Each has a real strength.

### ChatGPT — The Swiss Army Knife

ChatGPT has the broadest capability set: text, vision, voice, image generation (DALL-E), video (Sora), web search, file analysis, and the largest plugin ecosystem. It does everything, and it does most things well.

**Choose when:** You need one subscription to cover multiple use cases. Image generation, voice conversations, and multimodal analysis. You want the largest ecosystem of integrations and tutorials.

**Avoid when:** You need deep reasoning on complex documents or code. ChatGPT is broad but not always deep. For precision work, Claude often produces better results.

**Pricing:** Free tier is usable. Go ($8/month) for casual use. Plus ($20/month) is the standard. Pro ($200/month) for unlimited frontier access.

### Claude — The Thinking Partner

Claude's strength is sustained, deep reasoning. The 200K context window means it can analyze entire documents, codebases, or research papers in one pass. The writing quality is consistently high. And Artifacts (visual outputs, code previews) make it practical for creating deliverables.

**Choose when:** You work with long documents — legal contracts, research papers, strategy documents. Writing quality matters. You need a thinking partner that maintains coherence across a 30-minute conversation. You want Claude Code access included.

**Avoid when:** You need image generation, voice interaction, or broad multimodal capabilities. Claude's focus is text-in, text-out reasoning. For everything else, you need a second tool.

**Pricing:** Free tier is limited. Pro ($20/month) is the standard. Max ($100-200/month) for heavy users who need Claude Code.

### Perplexity — The Research Engine

Perplexity is not competing with ChatGPT or Claude. It's replacing Google for knowledge workers. Every answer comes with citations. Deep Research runs dozens of searches and produces structured reports with sources. It's what search should have become.

**Choose when:** Research-heavy work. Market analysis, competitive intelligence, fact-checking, literature review. You need transparent sourcing — not just an answer, but proof of where the answer came from.

**Avoid when:** Creative work, code generation, or extended conversations. Perplexity is built for retrieval, not generation. It finds and synthesizes information; it doesn't create.

**Pricing:** Free tier (3 Deep Research/day). Pro ($20/month) for 500 Deep Research/day. The Pro upgrade has the clearest ROI in the market — if you do research daily, $20/month replaces hours of manual searching.

### Gemini — The Google Native

If your company lives in Google Workspace (Docs, Sheets, Gmail, Calendar), Gemini Advanced eliminates tool-switching friction. It reads your documents, summarizes your emails, and integrates natively where you already work.

**Choose when:** You're embedded in Google Workspace. The integration value exceeds the model quality difference.

**Avoid when:** You need standalone AI quality. Gemini's models are competitive but not the best at any single task. You're paying for integration, not intelligence.

### The Knowledge Worker Stack

The emerging pattern among effective knowledge workers: **one primary + one specialist.**

- **Writer/strategist:** Claude (primary) + Perplexity (research)
- **Generalist/manager:** ChatGPT (primary) + Perplexity (research)
- **Google-native team:** Gemini (primary) + Claude or ChatGPT (complex tasks)

Don't subscribe to all four. Pick two. Master them. The difference between a practitioner who deeply understands one AI tool and one who superficially uses five is enormous.

---

## 8.6 The Tool Selection Framework

After examining every category, a clear pattern emerges. Here's how to choose.

### The Minimum Viable AI Toolkit

**For developers:**
1. One coding assistant (Cursor or Claude Code — pick based on visual vs. terminal preference)
2. One API provider (Anthropic or OpenAI — pick based on whether you value reasoning depth or ecosystem breadth)
3. One consumer AI for non-coding tasks (Claude or ChatGPT)

**For non-developers:**
1. One primary AI assistant (Claude or ChatGPT)
2. Perplexity for research
3. That's it. Two tools. Not five.

### The "One Tool Mastered" Principle

The single most common mistake is tool-hopping. Switching from Cursor to Windsurf to Claude Code every month means you never build the muscle memory, context files, and workflows that make any tool powerful.

Here's the uncomfortable truth: **a practitioner who has spent 3 months building a sophisticated Cursor setup (custom rules, project context, refined workflows) will outperform someone who switches to a "better" tool and starts from scratch.** The scaffolding you build around a tool is worth more than the tool itself.

This is the 80/20 rule applied to tools: 80% of the value comes from your context, rules, and workflows. 20% comes from the tool's native capabilities. Switching tools resets the 80% to zero.

### Decision Heuristic

When evaluating any AI tool, ask three questions:

1. **What's my actual problem?** Not "what's the best AI tool" but "what specific task am I trying to accomplish, and where am I wasting time?"
2. **Is this a two-way or one-way door?** Trying a new tool for a side project is reversible. Migrating your team's workflow is not. Match your evaluation investment to the decision's reversibility.
3. **Am I buying capability or context?** If a tool promises to be smarter but requires you to start from scratch, you're trading 80% (accumulated context) for a marginal improvement in 20% (model capability). That's almost never worth it.

### What's Overhyped

- **"AI replaces developers."** No. AI replaces typing. Judgment — knowing what to build, how to architect it, what edge cases matter — is still human. The gap between "AI generated code" and "production-ready code" is judgment.
- **"Use the right tool for every task."** In theory, yes. In practice, tool-switching costs are real. Two tools mastered beats five tools sampled.
- **"Vibe coding is the future of software."** For prototypes, absolutely. For production, it's a shortcut to security vulnerabilities and maintenance nightmares. The Challenger disaster analogy isn't hyperbole — unreviewed AI-generated code in production is accumulating as technical debt across thousands of startups right now.
- **"Open source is always cheaper."** Total cost of ownership (hardware, maintenance, expertise) often exceeds API costs for moderate-volume use cases. Run the numbers before making ideological choices.

### What's Underhyped

- **Prompt caching.** Anthropic's prompt caching reduces input costs by 90% for repeated contexts. If you're calling an API with the same system prompt thousands of times, this changes the economics dramatically. Most practitioners don't know it exists.
- **Batch APIs.** Both Anthropic and OpenAI offer 50% discounts for non-real-time processing. If your workload isn't latency-sensitive, you're overpaying.
- **Claude Code's MCP ecosystem.** Model Context Protocol is quietly becoming the standard for connecting AI to external tools and data sources. The practitioners who invest in MCP now are building infrastructure that compounds.

---

## 8.7 Our Setup — What We Actually Use

Transparency about our own choices:

- **Primary coding tool:** Claude Code (terminal-first, autonomous operation, MCP integration)
- **Primary API:** Anthropic (Claude Sonnet 4.5 for most tasks, with OpenAI text-embedding-3-small for embeddings)
- **Consumer AI:** Claude Pro ($20/month) — writing, analysis, planning
- **Research:** Perplexity for fact-gathering, Claude for synthesis
- **No-code:** None in production. Prototypes only, never deployed to real users without code review.
- **Infrastructure:** Self-hosted (VPS + Docker), not cloud-managed AI services. Maximum control, minimum vendor lock-in.

**Why this stack:** It optimizes for depth over breadth. One primary provider (Anthropic), mastered deeply, with minimal tool-switching. The scaffolding — CLAUDE.md, skills, Qdrant memory, MCP tools — took months to build and would be lost in any migration. The tool is 20%. The scaffolding is 80%.

**What we'd change:** If we needed image generation, we'd add OpenAI API (not switch). If we needed team collaboration, we'd evaluate Cursor (not replace Claude Code). The principle is: **add capabilities, don't replace workflows.**

---

*The tool landscape will look different in six months. New tools will launch. Prices will change. Models will improve. But the meta-principles won't change: master few over sample many, scaffolding over switching, context over capability. These are structural truths about how humans work effectively with AI tools — they survive any product cycle.*
