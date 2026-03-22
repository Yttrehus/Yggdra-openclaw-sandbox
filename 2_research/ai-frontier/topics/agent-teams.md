---
title: Agent Teams — Frameworks, Patterns & Erfaringer
date: 2026-03-22
category: AI Frontier
status: audit-passed
---

# Agent Teams — Frameworks, Patterns & Erfaringer (marts 2026)

## Metadata
- **Emne:** Multi-Agent Systemer
- **Kontekst:** Yggdra Projektet
- **Standard:** APA 7th
- **Status:** Færdig-auditeret

## 1. Hvornår Teams vs. Single Agent

**90% af use cases klares af én agent med gode tools.** Multi-agent er kun berettiget når:
- Opgaven naturligt dekomponerer i uafhængige specialiseringer.
- Perspektiv-diversitet forbedrer output (review, debate).
- Kontekstvinduet er for lille til hele opgaven.

**Multi-agent pilot failure rate:** 40% inden 6 måneder (Gartner, 2025).
**Mest udbredte failure mode:** Agents der taler i cirkler, brænder tokens uden konvergens.

---

## 2. Multi-Agent Patterns

### Orchestrator-Workers
Central agent dekomponerer, delegerer til specialiserede workers (Anthropic, 2026).
- Claude Agent SDK: parent→subagent
- CrewAI: hierarchical process med manager

### Pipeline (Sequential)
Agent A → Agent B → Agent C. Hvert trin processer output fra forrige (CrewAI, 2025).
- CrewAI sequential process
- Manus: append-only context, KV-cache optimeret

### Debate/Review
To+ agents diskuterer til konvergens eller approval.
- AutoGen: RoundRobinGroupChat, SelectorGroupChat (AutoGen, 2026)
- Evaluator-Optimizer pattern (Anthropic, 2024)

### Handoff (Routing)
Triage-agent sender samtalen videre til specialist. Kun én agent aktiv adgang ad gangen (OpenAI, 2024).
- OpenAI Swarm: transfer-funktioner
- Claude Agent SDK: subagent invocation

---

## 3. Framework-vurdering

### CrewAI — Role-Based Crews
**Stars:** ~30K | **Modenhed:** Stabil (v0.80+) (CrewAI, 2025).

**Arkitektur:** Agents med roller, goals, backstories. Crews orkestrerer. Flows wrapper til produktion.
**Memory:** 4 typer built-in (short-term, long-term, entity, contextual).
**Styrker:** Intuitiv rollemodel, rig memory, god docs.
**Svagheder:** Abstractions-overhead, role/backstory prompting brænder tokens (~30% ekstra).

---

### AutoGen (Microsoft) — Conversational Multi-Agent
**Stars:** ~40K | **Modenhed:** Pre-1.0 (v0.4) (AutoGen, 2026).

**Arkitektur:** 4 lag (Core, AgentChat, Extensions, Studio). Agent-samarbejde = gruppesamtale.
**Styrker:** Mest modne community, fleksible patterns, code execution built-in.
**Svagheder:** API churn, group chat spiral, ingen long-term memory.

---

### smolagents (Hugging Face) — Code-First
**Stars:** ~15K | **Modenhed:** Stabil (v1.x) (Hugging Face, 2025).

**Arkitektur:** Agents skriver Python i stedet for JSON tool calls. 30% færre LLM-kald.
**Styrker:** Minimalt, model-agnostisk, gratis med lokale modeller.
**Svagheder:** Code execution = sikkerhedsrisiko, basalt multi-agent.

---

### LangGraph — Graph-Based Orchestration
**Stars:** ~10K | **Modenhed:** Stabil (v0.2+) (LangChain, 2024).

**Arkitektur:** StateGraph med nodes (funktioner), conditional edges, typed state.
**Styrker:** Mest kontrol over flow, production-grade persistence, stærkt human-in-the-loop.
**Svagheder:** Stejl læringskurve (grafprogrammering).

---

### Claude Agent SDK — Anthropic's Framework
**Modenhed:** Ny (2026) (Anthropic, 2026).

**Arkitektur:** Claude Code som library. Built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch).
**Styrker:** Zero tool implementation, same capabilities som Claude Code, hooks, sessions.
**Svagheder:** Claude-only (komplet vendor lock-in).

---

## 4. Konklusion og Indsigt

### Yttres Erfaringer
Yttres multi-agent erfaringer er primært fra Ralph loops (baseret på bash og fil-stat) samt Claude Code's parent-child delegation. Erfaringer viser, at fraværet af circuit breakers kan føre til token-spild, og at file-systemet fungerer glimrende som persistent hukommelse (Manus, 2026).

### Anbefalinger
1. **Bliv på Claude SDK + bash** — intet framework giver p.t. merværdi for et solo setup.
2. **Implementér circuit breakers** på alle agent-loops (max_turns, timeout, cost cap).
3. **Adopter Manus' append-only context** — undgå at mutere state direkte i prompts for at optimere KV-cache (Manus, 2026).
4. **Undgå multi-agent frameworks** medmindre opgaven kræver parallel specialisering.

## Referencer

Anthropic. (2026). *Claude agent SDK documentation*. https://sdk.anthropic.com/
AutoGen. (2026). *AutoGen v0.4 release notes*. https://microsoft.github.io/autogen/
CrewAI. (2025). *CrewAI multi-agent flows*. https://docs.crewai.com/core-concepts/Flows/
Gartner. (2025). *Market guide for agentic AI*. https://www.gartner.com/
Hugging Face. (2025). *Smolagents: Code-first AI agents*. https://github.com/huggingface/smolagents
LangChain. (2024). *LangGraph: Orchestrating multi-agent systems*. https://langchain-ai.github.io/langgraph/
Manus. (2026). *The Manus context engineering pattern*. https://manus.ai/blog/context-engineering
OpenAI. (2024). *Swarm: Lightweight multi-agent orchestration*. https://github.com/openai/swarm
