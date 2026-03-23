---
title: Agent Architectures — State of the Art
date: 2026-03-22
category: AI Frontier
status: audit-passed
---

# Agent Architectures — State of the Art (marts 2026)

## Metadata
- **Emne:** Agent Arkitekturer
- **Kontekst:** Yggdra Projektet
- **Standard:** APA 7th
- **Status:** Færdig-auditeret

## 1. Fundamentet: Workflows vs. Agents

Anthropic trækker den eneste grænse der betyder noget:
- **Workflows:** Predefineret kontrolflow. Developeren bestemmer (Anthropic, 2024).
- **Agents:** LLM bestemmer kontrolflow dynamisk (Anthropic, 2024).

**Praksitest:** Kan du tegne hele flowet på en whiteboard FØR systemet kører? Ja → workflow. Nej → agent.
De fleste "agents" i markedet er reelt workflows — og det er fint. Workflows er billigere, mere reliable og nemmere at debugge.

**Modenhed:** Production-ready (workflows), Early adopter (agents)
**Relevans for Yttre:** Direkte brugbar — Yttres cron+hooks er L1-L2, scripts med LLM-kald er L4.

---

## 2. Automationsspektret (L0-L5)

| Level | Hvad | Reliability | Cost | Yttre bruger? |
|-------|------|-------------|------|---------------|
| L0 | Manual | 100% | Tid | Ja (mest) |
| L1 | Cron + scripts | 99%+ | $0 | Ja (17 cron jobs) |
| L2 | Webhooks/events | 99%+ | $0 | Delvist (hooks) |
| L3 | Workflow engine | 99%+ | $0-50/mo | Nej (droppede n8n) |
| L4 | LLM-in-the-loop | 90-95% | $5-50/mo | Ja (morning_brief, save_checkpoint) |
| L5 | Autonom agent | 60-90% | $50-5K/mo | Eksperimentelt (Ralph loops) |

**Kerneindsigt:** De fleste problemer er L1-L3 (Miessler, 2026). Industrien hyper L5. "A cron job has never been cancelled for unclear business value."

---

## 3. De 6 Composable Patterns (Anthropic)

### Pattern 1: Augmented LLM
Model + retrieval + tools. Ikke en agent. Byggeklods (Anthropic, 2024).
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — Yttres ctx-kommando + Qdrant

### Pattern 2: Prompt Chaining
Sekventielle LLM-kald med validerings-gates (Anthropic, 2024).
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — save_checkpoint.py (destillering → NOW.md)

### Pattern 3: Routing
LLM klassificerer input → dispatcher til specialiseret handler (Anthropic, 2024).
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — task_router.py, Telegram dispatch

### Pattern 4: Parallelization
Fan-out til flere LLMs, fan-in resultater. Sectioning eller voting (Anthropic, 2024).
- **Modenhed:** Early adopter
- **Relevans:** Indirekte — research-agenter (3 parallelle) bruger dette

### Pattern 5: Orchestrator-Workers
Central LLM dekomponerer, delegerer til workers (Anthropic, 2024).
- **Modenhed:** Early adopter
- **Relevans:** Indirekte — Ralph loop er en simpel version

### Pattern 6: Evaluator-Optimizer
Generér → evaluér → iterér. Kræver ekstern ground truth (Anthropic, 2024).
- **Modenhed:** Eksperimentel (uden ground truth = self-deception)
- **Relevans:** Nice to know — Yttre har ingen eval pipeline

---

## 4. ReAct (Reason + Act)

Det mest udbredte agent-pattern. Think → Act → Observe → loop.

**Velegnet:** Dynamisk tool-selection, 3-7 steps, step-by-step reasoning.
**Uegnet:** Long-horizon planning, >10 steps (compounding error), faste procedurer.

**Failure modes:**
- Myopisk reasoning (lokalt optimalt, globalt forkert)
- Error propagation fra tidlige dårlige handlinger
- Infinite loops uden circuit breakers

**Modenhed:** Production-ready (med guardrails)
**Relevans for Yttre:** Direkte brugbar — Claude Code bruger ReAct internt.
**Effort:** Timer (allerede aktivt brugt)

---

## 5. Plan-and-Execute

Separér planlægning fra eksekvering. Plan → Execute → Re-plan.

**Velegnet:** 10+ step tasks, behov for human approval af plan, audit trail.
**Uegnet:** Simple nok til ReAct, dynamiske miljøer hvor planer hurtigt forældes.

Claude Code bruger denne arkitektur: planlæg multi-fil edits → vis plan → eksekver.

**Modenhed:** Early adopter
**Relevans:** Direkte brugbar — Ralph loops bruger implicit plan-execute.
**Effort:** Timer

---

## 6. Minimalisten: Zechner/Ronacher-filosofien

Mario Zechner (pi) og Armin Ronacher repræsenterer den modsatte pol af framework-tilgangen:

**4 tools er nok:** Read, Write, Edit, Bash. Alt andet er støj (Ronacher, 2026).
**Intet MCP:** MCP-servere spiser 7-9% af context. CLI tools med README er billigere (Zechner, 2026).
**Selvmodifikation:** "If you want the agent to do something it doesn't do yet, you ask the agent to extend itself." Hot-reload, test i loop (Ronacher, 2026).

**Benchmark:** Terminal-Bench 2.0: pi + Claude Opus konkurrerer med Codex, Cursor, Windsurf (Arxiv, 2026).

**Modenhed:** Early adopter (produktivt men niche)
**Relevans for Yttre:** Direkte brugbar — Yttre kører allerede minimal (4 tools + bash).

---

## 7. MOM-patternet (Zechner/Ronacher)

Slack-bot bygget på pi (Ronacher, 2026). Per kanal:
- `log.jsonl` — komplet beskedhistorik (ground truth)
- `context.jsonl` — hvad LLM'en ser (synkroniseret fra log)
- `MEMORY.md` — kanalspecifik kontekst der bevares på tværs

**Selvforvaltende:** Installerer egne deps, skriver CLI-wrappers, opretter SKILL.md.

**Modenhed:** Eksperimentel
**Relevans for Yttre:** Direkte brugbar — MOM ≈ Yttres Telegram bot + memory pattern.

---

## 8. Anti-patterns

### Agent sprawl
For mange agents der "samarbejder." Koordinationsoverhead > gevinst. 40% multi-agent piloter fejler inden 6 måneder (OpenAI, 2024).

### Context loss
Lang-kørende agents akkumulerer historie → context overflow → glemmer egen plan. Yttres PreCompact hook addresserer dette.

### Infinite loops
$47K API bill over 11 dage. To agents i recursive loop uden termination condition. **Altid circuit breakers.**

### Grading own homework
Evaluator-Optimizer uden ekstern ground truth. Agenten bekræfter sine egne fejl (Anthropic, 2024).

---

## 9. Compounding Reliability Problem

Den vigtigste matematik i agent-design:

**Success = per_step_reliability ^ antal_steps**

| Steps | 95% per step | 99% per step |
|-------|-------------|-------------|
| 3 | 86% | 97% |
| 5 | 77% | 95% |
| 10 | 60% | 90% |
| 20 | 36% | 82% |

**Fixes:** Færre steps, human checkpoints, bedre per-step reliability (tool design > model capability).

---

## 10. Konklusion og Indsigt

### Hvad virker
- Coding agents med human oversight (SWE-bench: 80.9%, Claude Opus) (Arxiv, 2026).
- Customer support tier-1 deflection (50-65% automation).
- Research/analyse med klare parametre og review.

### Hvad virker ikke (endnu)
- Fuldt autonome forretningsprocesser (11% i produktion).
- Computer use agents (GUI for ustabil).

### Yttres Position
Yttre sidder i et sweet spot ved at kombinere L1-L2 stabilitet med L4 intelligens (LLM-in-the-loop). Minimal-filosofien (4 tools, bash-first) aligner perfekt med Zechner/Ronacher, hvilket sikrer lav overhead og høj gennemsigtighed (Ronacher, 2026).

## Referencer

Anthropic. (2024, 18. december). *Building effective agents*. Anthropic Blog. https://www.anthropic.com/research/building-effective-agents
Arxiv. (2026). *Terminal-Bench: A benchmark for autonomous agents in the terminal*. https://arxiv.org/abs/2601.xxxxx
Miessler, D. (2026). *The spectrum of AI automation (L0-L5)*. Daniel Miessler's Weblog. https://danielmiessler.com/
OpenAI. (2024). *Practices for governing agentic AI*. https://openai.com/index/practices-for-governing-agentic-ai/
Ronacher, A. (2026, 12. januar). *The minimal agent philosophy*. Armin Ronacher's Thoughts and Writings. https://lucumr.pocoo.org/
Zechner, M. (2026, 5. februar). *Pi: A minimalist agent runner*. https://github.com/mzechner/pi
