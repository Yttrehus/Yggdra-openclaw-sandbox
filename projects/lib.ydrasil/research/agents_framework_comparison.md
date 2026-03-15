# Multi-Agent Framework Comparison

**Researched:** 2026-03-08
**Purpose:** Comprehensive comparison of the six leading multi-agent frameworks. Companion to CH6_AGENTS_AUTOMATION.md.
**Method:** Official docs, GitHub repos, web research. Code examples verified against current APIs.

---

## 1. CrewAI — Role-Based Crew Orchestration

**GitHub:** [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) (~30K stars)
**Philosophy:** Teams of role-playing agents that collaborate like a human crew. You define who each agent is, what they do, and how they work together.

### Architecture

CrewAI uses a dual-model architecture:

- **Crews** — teams of autonomous agents with roles, goals, and backstories. The crew is the unit of orchestration.
- **Flows** — event-driven pipelines for production deployments. Flows can contain Crews as nodes, enabling granular control over multi-step processes.

The mental model is organizational: you are staffing a team. Each agent has a role ("Research Analyst"), a goal ("Find comprehensive data on X"), and optionally a backstory that shapes its behavior.

### Key Abstractions

| Abstraction | What it does |
|---|---|
| **Agent** | Autonomous unit with role, goal, backstory, tools, and optional memory |
| **Task** | A unit of work with description, expected output, and assigned agent |
| **Crew** | Orchestrates agents + tasks. Defines process (sequential or hierarchical) |
| **Process** | Execution model: `sequential` (waterfall) or `hierarchical` (manager delegates) |
| **Flow** | Production wrapper: event-driven, supports state, branching, error handling |

### Communication Model

Agents communicate through task delegation. When `allow_delegation=True`, an agent can hand off subtasks to other agents in the crew. In hierarchical mode, a manager agent automatically distributes work. There is no direct agent-to-agent messaging — coordination happens through the crew's process.

### Memory

Four memory types built in:
- **Short-term** — conversation context within a task
- **Long-term** — persistent across crew executions (stored in SQLite/ChromaDB)
- **Entity memory** — tracks entities mentioned across interactions
- **Contextual memory** — combines all three for richer context

Enable with `memory=True` on the Crew. Context window overflow is handled via `respect_context_window=True` which auto-summarizes.

### Code Example

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Senior Research Analyst",
    goal="Find comprehensive information about AI frameworks",
    backstory="You are an experienced tech analyst with deep knowledge of AI.",
    tools=[SerperDevTool()],
    memory=True,
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, accurate technical documentation",
    backstory="You excel at making complex topics accessible.",
)

research_task = Task(
    description="Research the top 5 multi-agent frameworks in 2026",
    expected_output="A detailed report with pros, cons, and code examples",
    agent=researcher,
)

write_task = Task(
    description="Write a comparison document based on the research",
    expected_output="A polished markdown document",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=True,
)

result = crew.kickoff()
```

### Pros
- Intuitive role-based mental model — easy to explain to non-technical stakeholders
- Rich memory system out of the box
- Good documentation and active community
- Flows add production-grade control without abandoning the crew metaphor
- 200+ pre-built tool integrations

### Cons
- Abstraction overhead — simple tasks feel over-engineered
- Role/backstory prompting burns tokens (each agent carries its persona in every call)
- Debugging multi-agent interactions is opaque
- Hierarchical process adds a manager agent = extra LLM calls = extra cost
- Lock-in to CrewAI's abstractions — harder to drop down to raw API calls

### When to Use
Business process automation where tasks map to human roles. Content pipelines, research workflows, report generation. Teams that think in org charts.

### When NOT to Use
Simple single-agent tasks. Latency-sensitive applications. When you need fine-grained control over every LLM call. Budget-constrained projects (role overhead adds ~30% token cost).

### Approximate Cost
A 4-agent crew running a research + writing pipeline: ~$0.15–0.50 per run with GPT-4o. Memory and delegation add overhead. Hierarchical mode roughly doubles the cost vs. sequential.

---

## 2. AutoGen (Microsoft) — Conversational Multi-Agent System

**GitHub:** [microsoft/autogen](https://github.com/microsoft/autogen) (~40K stars)
**Philosophy:** Agents are participants in a conversation. Multi-agent coordination is modeled as group chat.

### Architecture

AutoGen v0.4 is built in four layers:

1. **Core** — event-driven runtime for scalable multi-agent systems. Async message passing, pluggable components.
2. **AgentChat** — high-level API for conversational single and multi-agent apps.
3. **Extensions** — integrations with external services (OpenAI, Azure, databases).
4. **Studio** — web UI for no-code prototyping.

The key insight is that agent collaboration is a conversation. Agents send messages to each other, respond, and reach conclusions through dialogue — the same way humans coordinate in a group chat.

Note: Microsoft has announced the **Microsoft Agent Framework** (targeting 1.0 GA in Q1 2026), which merges AutoGen with Semantic Kernel for enterprise use. AutoGen remains the open-source core.

### Key Abstractions

| Abstraction | What it does |
|---|---|
| **AssistantAgent** | LLM-powered agent with tools and system message |
| **UserProxyAgent** | Represents a human; can auto-execute code |
| **RoundRobinGroupChat** | Agents take turns speaking |
| **SelectorGroupChat** | An LLM selects which agent speaks next |
| **Swarm** | Hierarchical agent coordination pattern |
| **GraphFlow** | Graph-based workflow for complex orchestration |
| **Termination** | Conditions to end conversations (max messages, text match, token limit) |

### Communication Model

Asynchronous message passing. Agents communicate through a shared conversation thread. In group chat, a selector (LLM or round-robin) determines who speaks next. Supports both event-driven and request/response patterns. Cross-language interop (Python + .NET) via the Core layer.

### Memory/Persistence

- State serialization for checkpointing and resuming conversations
- OpenTelemetry integration for tracing and observability
- No built-in long-term memory — you manage persistence externally
- Session state can be saved and loaded for long-running workflows

### Code Example

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

model = OpenAIChatCompletionClient(model="gpt-4o")

analyst = AssistantAgent(
    "analyst",
    model_client=model,
    system_message="You analyze data and provide insights.",
)

critic = AssistantAgent(
    "critic",
    model_client=model,
    system_message="You review analysis for errors and biases. Say APPROVE when satisfied.",
)

termination = TextMentionTermination("APPROVE")
team = RoundRobinGroupChat([analyst, critic], termination_condition=termination)

async def main():
    result = await team.run(task="Analyze the impact of multi-agent frameworks on developer productivity.")
    print(result)

asyncio.run(main())
```

### Pros
- Most mature multi-agent framework (largest community, most production deployments)
- Flexible conversation patterns (round-robin, selector, swarm, graph)
- Code execution built in (UserProxyAgent can run Python in sandboxed environments)
- Strong enterprise backing (Microsoft, Azure integration)
- Cross-language support (Python + .NET)

### Cons
- API churn — v0.2 to v0.4 was a breaking rewrite; migration to Microsoft Agent Framework is ongoing
- Complexity creep — simple tasks require understanding the agent/team/termination stack
- Group chat can spiral (agents talking to each other without converging)
- No built-in long-term memory
- Heavy dependency tree

### When to Use
Multi-agent debate/review workflows. Code generation with execution. Enterprise environments already on Azure/Microsoft stack. Research projects needing flexible agent topologies.

### When NOT to Use
Simple single-agent tasks. When API stability matters (still pre-1.0). Resource-constrained environments. When you need lightweight, dependency-free agents.

### Approximate Cost
A 2-agent review loop typically runs 4–8 turns: ~$0.10–0.30 per task with GPT-4o. Group chats with 3+ agents can escalate quickly if termination conditions are loose — budget $0.50–2.00 for complex multi-turn debates.

---

## 3. Swarm (OpenAI) — Lightweight Handoffs

**GitHub:** [openai/swarm](https://github.com/openai/swarm) (~20K stars)
**Philosophy:** The simplest possible multi-agent pattern. Agents are functions with instructions. Coordination is a handoff.

### Architecture

Swarm is ~500 lines of code wrapping the Chat Completions API. It is stateless between calls — you pass the full message history each time. The entire execution model is:

1. Get completion from current agent
2. Execute tool calls, append results
3. If a tool returns another agent → switch to that agent
4. Repeat until no more tool calls
5. Return

That is the entire framework. No event bus, no orchestrator, no group chat. Just agents handing conversations to other agents.

**Important:** Swarm is explicitly experimental/educational. OpenAI has released the **OpenAI Agents SDK** as the production successor. Swarm is not maintained for production use.

### Key Abstractions

| Abstraction | What it does |
|---|---|
| **Agent** | Name + instructions (system prompt) + functions (tools) |
| **Handoff** | A function that returns another Agent, transferring the conversation |
| **Swarm client** | Thin wrapper around Chat Completions that manages the agent loop |
| **Context variables** | Mutable dict passed through the conversation for state |

### Communication Model

Sequential handoff. Only one agent is active at a time. When an agent's function returns another agent, control transfers. No parallel agents, no group chat, no broadcast. The conversation is a baton relay.

### Memory/Persistence

None. Swarm is stateless. You pass messages in, you get messages out. If you want persistence, you store the message history yourself.

### Code Example

```python
from swarm import Swarm, Agent

client = Swarm()

def transfer_to_support():
    """Transfer to the support agent."""
    return support_agent

def transfer_to_sales():
    """Transfer to the sales agent."""
    return sales_agent

triage_agent = Agent(
    name="Triage",
    instructions="Determine if the user needs support or sales. Transfer accordingly.",
    functions=[transfer_to_support, transfer_to_sales],
)

support_agent = Agent(
    name="Support",
    instructions="Help users with technical issues. Be concise and helpful.",
)

sales_agent = Agent(
    name="Sales",
    instructions="Help users with pricing and purchasing decisions.",
)

response = client.run(
    agent=triage_agent,
    messages=[{"role": "user", "content": "My account is locked"}],
)
print(response.messages[-1]["content"])
```

### Pros
- Dead simple — you can read the entire source code in 20 minutes
- No dependencies beyond the OpenAI SDK
- Perfect for learning multi-agent patterns
- Handoff model maps well to customer service / routing use cases
- Easy to test (stateless = deterministic given same inputs)

### Cons
- Experimental only — not production-ready, not maintained
- No memory, no persistence, no streaming (in original)
- OpenAI models only
- No parallel agents — strictly sequential
- Superseded by OpenAI Agents SDK

### When to Use
Learning multi-agent concepts. Prototyping routing/triage workflows. When you want to understand what "multi-agent" actually means without framework overhead.

### When NOT to Use
Production systems. Anything requiring persistence, memory, or complex orchestration. When you need non-OpenAI models. Anything beyond simple routing patterns.

### Approximate Cost
Minimal framework overhead — cost is just the Chat Completions API calls. A triage + specialist flow: ~$0.02–0.08 per interaction with GPT-4o-mini, ~$0.05–0.20 with GPT-4o.

---

## 4. smolagents (Hugging Face) — Code-First Agents

**GitHub:** [huggingface/smolagents](https://github.com/huggingface/smolagents) (~15K stars)
**Philosophy:** Agents should write code, not JSON. The simplest possible agent library: ~1,000 lines of core logic.

### Architecture

smolagents takes a radical stance: instead of agents emitting JSON tool calls that a framework parses and executes, agents write Python code directly. The LLM generates `result = search_tool("query")` as actual Python, which is then executed in a sandboxed environment.

This "code agent" approach reduces steps and LLM calls by ~30% compared to JSON tool-calling on complex benchmarks, because code naturally supports composition (nesting function calls), control flow (loops, conditionals), and variable reuse.

The library is the successor to `transformers.agents` and is intentionally minimal — no orchestration layer, no workflow engine, no enterprise features. Just agents that think in code.

### Key Abstractions

| Abstraction | What it does |
|---|---|
| **CodeAgent** | Writes and executes Python code to accomplish tasks |
| **ToolCallingAgent** | Traditional JSON-based tool calling (fallback for models that struggle with code) |
| **Tool** | A Python function with name, description, and typed inputs. Shareable via Hub |
| **Model** | LLM backend: InferenceClientModel (HF), LiteLLMModel (OpenAI/Anthropic), TransformersModel (local) |
| **ManagedAgent** | Wraps an agent to be used as a tool by another agent (multi-agent) |

### Communication Model

Multi-agent support via `ManagedAgent`: you wrap one agent and give it to another as a tool. The parent agent calls the child agent like any other tool. No group chat, no handoffs — it is hierarchical delegation through function calls.

### Memory/Persistence

- Conversation history within a run (agent sees its previous steps)
- No built-in long-term memory
- No session persistence
- State resets between runs

### Code Example

```python
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool, ManagedAgent

model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

search_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
)

managed_search = ManagedAgent(
    agent=search_agent,
    name="search_expert",
    description="Searches the web and returns relevant information.",
)

orchestrator = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_search],
)

result = orchestrator.run("Compare the latest multi-agent frameworks and summarize findings.")
print(result)
```

### Pros
- Minimal and readable — you can understand the entire library in an afternoon
- Code agents are genuinely more efficient than JSON tool-calling
- Model-agnostic: local models (Ollama, Transformers), cloud APIs, HF Inference
- Hub integration for sharing tools and agents
- Sandboxed execution (E2B, Modal, Docker, Pyodide)
- Free if using open models on your own hardware

### Cons
- Code execution is a security surface — sandboxing is essential
- Multi-agent is basic (hierarchical only, no peer-to-peer)
- No persistence, no memory, no sessions
- Smaller community than CrewAI or AutoGen
- Code generation quality depends heavily on the model (small models struggle)
- No built-in observability or tracing

### When to Use
Research and experimentation. When you want open-source models (no vendor lock-in). Data analysis and computation tasks where code is the natural output. When you value simplicity over features.

### When NOT to Use
Production systems needing persistence and observability. Complex multi-agent coordination (debates, reviews). Enterprise environments requiring audit trails. When security review of code execution is a concern.

### Approximate Cost
Free with local/open models. With cloud APIs: ~$0.02–0.10 per task (code agents use fewer tokens than tool-calling agents). HF Inference API has a free tier for many models.

---

## 5. LangGraph — Graph-Based Agent Orchestration (Summary)

**GitHub:** [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) (~10K stars)
**Philosophy:** Agent workflows are directed graphs with typed state, conditional edges, and checkpointing.

### Key Points

LangGraph models agents as **nodes** in a **StateGraph**. State flows through the graph, each node reads and updates it, and **conditional edges** determine routing. This gives you explicit control over execution flow — no magic, no implicit coordination.

| Aspect | Details |
|---|---|
| **Core abstraction** | `StateGraph` with nodes (functions) and edges (routing logic) |
| **State** | Typed dict (TypedDict or Pydantic) shared across all nodes |
| **Persistence** | Built-in checkpointing — pause, resume, fork, replay |
| **Human-in-the-loop** | First-class interrupt points for approval/editing |
| **Multi-agent** | Agents as subgraphs, supervisor patterns, message passing |
| **Streaming** | Token-level and node-level streaming |
| **Platform** | LangGraph Platform for deployment (managed infra) |

**Pros:** Most control over execution flow. Production-grade persistence. Strong human-in-the-loop support. Battle-tested at scale.

**Cons:** Steep learning curve (graph programming is not intuitive). Tied to LangChain ecosystem. Verbose for simple tasks. LangGraph Platform adds cost ($X/month for managed hosting).

**Best for:** Complex, stateful workflows with branching logic, human approval steps, and production persistence requirements. Deep dive covered separately.

**Approximate cost:** Framework is free. LLM costs same as raw API. LangGraph Platform pricing varies.

---

## 6. Claude Agent SDK — Anthropic's Agent Framework

**Docs:** [platform.claude.com/docs/en/agent-sdk](https://platform.claude.com/docs/en/agent-sdk/overview)
**GitHub:** [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
**Philosophy:** Give your code the same autonomous capabilities as Claude Code. Built-in tools, not DIY.

### Architecture

The Claude Agent SDK is fundamentally different from the other frameworks: instead of providing abstractions for orchestrating LLM calls, it gives you Claude Code as a library. The agent comes with built-in tools (file reading, code editing, bash execution, web search, web fetch) — you do not implement tool execution. You send a prompt, and the agent autonomously reads files, runs commands, edits code, and reports back.

This is opinionated by design. You are not building an agent from primitives. You are deploying an agent that already knows how to operate in a codebase.

### Key Abstractions

| Abstraction | What it does |
|---|---|
| **`query()`** | The main entry point. Send a prompt, get a stream of messages back |
| **Built-in tools** | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion |
| **Hooks** | Callbacks at lifecycle points: PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd |
| **Subagents** | Specialized agents defined with their own prompt and tools, invoked via the `Agent` tool |
| **Sessions** | Persistent context — resume or fork conversations with full history |
| **Skills** | Markdown files (`.claude/skills/`) that add domain knowledge |
| **MCP servers** | Connect to external systems via Model Context Protocol |

### Communication Model

Parent-child delegation via subagents. The main agent can spawn specialized subagents (defined with `AgentDefinition`) that run with their own tools and instructions, then report back. No peer-to-peer communication, no group chat. The orchestration is implicit — Claude decides when to delegate based on the prompt and available agents.

### Memory/Persistence

- **Sessions** — full conversation history, resumable and forkable
- **CLAUDE.md** — project-level persistent instructions (loaded automatically)
- **Skills** — domain knowledge in markdown, loaded on demand
- No vector store or long-term memory built in (but can connect via MCP)

### Code Example

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "security-reviewer": AgentDefinition(
                    description="Security expert that reviews code for vulnerabilities.",
                    prompt="Analyze code for security issues: injection, auth bypass, data exposure.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### Pros
- Zero tool implementation — built-in tools work immediately
- Same capabilities as Claude Code (proven in production)
- Hooks provide governance without complexity
- Sessions enable multi-turn workflows with full context
- MCP integration for extensibility
- Available in Python and TypeScript
- Permission system for controlling agent capabilities

### Cons
- Claude-only — no model choice, complete vendor lock-in to Anthropic
- Opinionated — you get Claude Code's agent loop, not your own
- Cost: Claude API pricing applies (Sonnet ~$3/$15 per 1M tokens in/out)
- Multi-agent is parent-child only (no peer coordination)
- Newer than alternatives — smaller ecosystem, fewer examples
- Requires Claude Code subscription or API key

### When to Use
Codebase-aware automation (CI/CD, code review, refactoring). When you want an agent that works out of the box without tool implementation. Teams already using Claude Code. Production pipelines where built-in file/command tools are the core requirement.

### When NOT to Use
When you need model flexibility. Budget-constrained projects (Claude API is not cheap). Complex multi-agent coordination beyond parent-child delegation. When you want to control the agent loop yourself.

### Approximate Cost
Claude Sonnet: ~$0.10–0.50 per agent task (depending on file reading, tool calls). Claude Opus: ~$0.50–3.00 per complex task. Subagents multiply the cost. A code review agent reading 10 files and running grep: ~$0.15–0.30 with Sonnet.

---

## Comparison Table

| Dimension | CrewAI | AutoGen | Swarm | smolagents | LangGraph | Claude Agent SDK |
|---|---|---|---|---|---|---|
| **Maturity** | Stable (v0.80+) | Pre-1.0 (v0.4) | Experimental | Stable (v1.x) | Stable (v0.2+) | New (2026) |
| **Complexity** | Medium | High | Very Low | Low | High | Low |
| **Multi-agent** | Role-based crews | Group chat, graph | Sequential handoff | Hierarchical | Graph-based | Parent-child subagents |
| **Memory** | 4 types built-in | External only | None | None | Checkpointing | Sessions + CLAUDE.md |
| **Model lock-in** | No (any LLM) | No (any LLM) | OpenAI only | No (any LLM) | No (any LLM) | Anthropic only |
| **Tool implementation** | You provide | You provide | You provide | You provide | You provide | Built-in |
| **Persistence** | SQLite/ChromaDB | Serialization | None | None | Checkpointing | Session resume |
| **Cost per task** | $0.15–0.50 | $0.10–2.00 | $0.02–0.20 | $0.00–0.10 | Same as raw API | $0.10–3.00 |
| **Lines of core code** | ~10K+ | ~30K+ | ~500 | ~1,000 | ~15K+ | N/A (closed) |
| **Best for** | Business workflows | Research, enterprise | Learning, prototyping | Open-source, research | Complex stateful flows | Codebase automation |
| **Worst for** | Simple tasks | Stability-critical | Production | Enterprise | Quick prototypes | Budget-constrained |

## Honest Assessment

**If you are building a production multi-agent system today** (March 2026), the honest answer is: most tasks do not need multi-agent frameworks. A single agent with good tools handles 90% of use cases. The remaining 10% splits between:

- **LangGraph** if you need fine-grained control, persistence, and human-in-the-loop
- **CrewAI** if your workflow maps to roles and you want the fastest path to a working prototype
- **Claude Agent SDK** if your task is codebase-oriented and you want zero tool setup
- **AutoGen** if you are in the Microsoft ecosystem and need cross-language support
- **smolagents** if you want open models and minimal dependencies
- **Swarm** if you want to understand the concepts before committing to a framework

The most common failure mode across all frameworks is the same: agents talking to each other in circles, burning tokens without converging. Every framework handles this differently (termination conditions, max turns, human interrupts), but none solve it fully. Budget alerts and hard token limits are not optional — they are essential.
