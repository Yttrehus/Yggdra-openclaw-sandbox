# Agent Evaluation and Observability

**Researched:** 2026-03-08 via web research, platform documentation, and academic sources
**Status:** Research report — practical reference for implementation

---

## 1. Why Agent Evaluation Differs from Software Testing

Traditional software testing operates on deterministic systems: given input X, expect output Y. Agent evaluation breaks this contract in three fundamental ways.

**Non-determinism.** The same prompt with identical context can produce different tool call sequences, different intermediate reasoning, and different final outputs across runs. Temperature, model updates, and context window state all introduce variance. You cannot write `assert output == expected` and call it tested.

**Multi-step compounding.** A 5-step agent with 95% per-step reliability succeeds only 77% of the time. A wrong tool selection in step 2 poisons every subsequent step. Unlike unit tests where failures are isolated, agent failures cascade — and the failure point is often invisible in the final output. You need to evaluate the trajectory, not just the destination.

**Partial success.** An agent that retrieves 4 of 5 relevant documents, calls the right API but with a slightly wrong parameter, or produces a mostly-correct answer with one factual error — is that a pass or a fail? Agent evaluation requires graded scoring, not binary pass/fail. Production agents operate on a spectrum of correctness that traditional test assertions cannot capture.

**Side effects and real-world impact.** Agents interact with external systems — APIs, databases, file systems. A "test" that sends a real email or modifies a production database is not a test. Evaluation must account for both the agent's reasoning quality and the real-world consequences of its actions.

The METR research finding underscores the difficulty: developers *perceived* themselves as 20-30% faster when using AI tools, while objective measurement showed they were 19% slower. Self-report and intuition are unreliable — agent evaluation requires instrumented, automated measurement.

---

## 2. Three Primitives: Runs, Traces, Threads

Agent observability is built on three nested abstractions. Understanding their hierarchy is essential before implementing any evaluation.

### Runs

A **run** is the atomic unit: one LLM call with its complete input (system prompt, conversation history, available tools, context) and output (response text, tool calls, token usage, latency). A run captures a single decision point.

Runs are the foundation for single-step evaluation: "Given this exact state, did the agent make the right choice?" They are cheap to store, fast to query, and the most debuggable unit.

### Traces

A **trace** links multiple runs into a complete agent execution. It captures the full trajectory: which tools were called, in what order, with what arguments, and what results came back. A trace is a tree structure — runs can spawn child runs (e.g., an agent calls a tool that itself makes an LLM call).

Key property: agent traces can be orders of magnitude larger than traditional distributed traces. Complex agents produce traces of hundreds of megabytes spanning dozens of nested runs. The trace is where you see the agent's "reasoning path" and where trajectory evaluation operates.

A trace typically captures:
- **Spans**: logical units of work (tool call, retrieval, reasoning step)
- **Events**: milestones within spans (start, completion, error)
- **Generations**: individual LLM calls with full prompt/response
- **Tool calls**: external API invocations with arguments and results
- **Metadata**: token counts, latency, cost, model version

### Threads

A **thread** groups multiple traces into a conversational session — the multi-turn interaction between a user and an agent over time. Threads preserve state evolution: how context accumulates, whether preferences persist, and whether the agent maintains coherent behavior across interactions.

**Nesting hierarchy:** Thread → Trace → Run. A thread contains multiple traces (one per user turn or agent invocation). Each trace contains multiple runs. This hierarchy maps directly to the three evaluation granularities described below.

---

## 3. Evaluation Types

### Single-Step Evals (Run-Level)

The most granular strategy — a unit test for agent reasoning. Isolate one decision point and verify it.

**What it tests:** Given a specific state (conversation history + available tools + context), does the agent select the correct tool with the correct arguments?

**Example:** The user asks "What meetings do I have tomorrow?" The agent should call `find_meeting_times` with tomorrow's date, not `schedule_meeting`.

```python
# Single-step eval: verify tool selection
def eval_tool_selection(agent, state, expected_tool, expected_args):
    """Run agent for one step from frozen state, check tool choice."""
    result = agent.run_single_step(state)

    assert result.tool_name == expected_tool, (
        f"Expected {expected_tool}, got {result.tool_name}"
    )
    for key, value in expected_args.items():
        assert result.tool_args[key] == value, (
            f"Arg {key}: expected {value}, got {result.tool_args.get(key)}"
        )
    return {"pass": True, "tool": result.tool_name}
```

**When to use:** Debugging specific failure points. Validating tool descriptions are unambiguous. Regression testing after prompt changes.

### Trace Evals (Trajectory-Level)

Evaluates the full execution path — did the agent take a reasonable sequence of steps to accomplish the task?

**What it tests:** The complete tool call sequence, intermediate reasoning, and final output quality. Two sub-approaches:

1. **Trajectory matching** — Compare actual tool call sequence against a reference trajectory.
2. **LLM-as-judge** — Have a judge model evaluate whether the trajectory was reasonable.

```python
# Trajectory matching with configurable strictness
from agentevals.trajectory.match import create_trajectory_match_evaluator

# Strict: exact order and arguments must match
strict_eval = create_trajectory_match_evaluator(
    trajectory_match_mode="strict"
)

# Unordered: same tools called, order doesn't matter
flexible_eval = create_trajectory_match_evaluator(
    trajectory_match_mode="unordered"
)

# Subset: reference calls must appear in actual (extras OK)
subset_eval = create_trajectory_match_evaluator(
    trajectory_match_mode="subset"
)

result = flexible_eval(
    outputs=actual_trajectory,
    reference_outputs=expected_trajectory
)
```

**When to use:** Validating end-to-end task completion. Comparing agent versions. Catching regressions where the final answer is correct but the path is wasteful or fragile.

### Thread Evals (Conversation-Level)

The hardest evaluation type. Tests whether the agent maintains context, preferences, and coherent behavior across multiple user turns.

**What it tests:** Does the agent remember user preferences from turn 1 when responding in turn 5? Does it handle corrections gracefully? Does accumulated context improve or degrade response quality?

```python
# Multi-turn thread evaluation
def eval_thread(agent, conversation_script):
    """Run multi-turn conversation, evaluate each turn."""
    thread_state = agent.new_thread()
    results = []

    for turn in conversation_script:
        response = agent.respond(thread_state, turn["user_input"])

        # Evaluate each turn against expected behavior
        score = judge_model.evaluate(
            input=turn["user_input"],
            output=response,
            expected=turn.get("expected_behavior"),
            context=turn.get("context_requirements"),
        )
        results.append(score)

        # Fail early if agent goes off track
        if score < turn.get("min_threshold", 0.5):
            return {"pass": False, "failed_at_turn": turn["id"],
                    "scores": results}

    return {"pass": True, "scores": results,
            "avg_score": sum(results) / len(results)}
```

**When to use:** Validating conversational agents. Testing context persistence. Evaluating agents with stateful memory systems.

---

## 4. Offline vs Online vs Ad-Hoc Evaluation

### Offline Evaluation

**When:** Before deployment. Part of CI/CD pipeline.

Run the agent against a curated dataset of inputs with known-good outputs or trajectories. This is the equivalent of a test suite.

- Requires a "gold standard" dataset — input/output pairs with optional reference trajectories
- Can use expensive judge models since it runs in batch
- Catches regressions before they reach production
- Limitation: cannot predict novel user inputs or edge cases

```python
# Offline eval in CI/CD
def run_offline_eval(agent, dataset, threshold=0.85):
    scores = []
    for case in dataset:
        trace = agent.run(case["input"])
        score = evaluate_trace(trace, case["expected_output"])
        scores.append(score)

    avg = sum(scores) / len(scores)
    if avg < threshold:
        raise Exception(f"Quality {avg:.2f} below threshold {threshold}")
    return avg
```

**Adoption:** 52.4% of organizations run offline evaluations on test sets (LangChain State of Agent Engineering, 2026).

### Online Evaluation

**When:** During production. Continuous monitoring.

Score production traces in real time using reference-free evaluators — no expected output needed. Detect quality degradation, cost anomalies, and behavioral drift.

- User feedback (thumbs up/down) flags problematic traces
- Automated LLM judges score samples of production traffic
- Anomaly detection on token usage, latency, error rates
- Alerts when quality drops below baseline

**Adoption:** 89% of organizations have implemented some form of observability. 62% have detailed tracing with individual step inspection.

### Ad-Hoc Evaluation

**When:** Investigating specific failures. Exploratory analysis.

Retrospective analysis of collected traces to identify patterns, failure modes, and optimization opportunities. Not automated — driven by human investigation with AI assistance.

- Surface usage patterns across thousands of traces
- Identify common failure trajectories
- Find traces to convert into permanent test cases
- Explore cost/latency distributions

**The critical workflow:** Identify production failure → extract trace → create offline test case → fix → validate → deploy. This flywheel continuously strengthens the offline eval dataset with real-world failures. Braintrust's one-click "trace to eval case" conversion operationalizes this pattern.

---

## 5. Tools Landscape

### LangSmith (LangChain)

**Best for:** Teams using LangChain/LangGraph. Framework-native tracing with deep integration.

- Tracing with full prompt/response capture
- Multi-turn evaluation for conversations
- Annotation queues for human review
- Pairwise comparison between model versions
- Insights Agent for usage categorization
- Per-seat pricing (scales with team size, not usage)

### Braintrust

**Best for:** Teams wanting eval-driven deployment governance across any framework.

- 40+ framework integrations (framework-agnostic)
- One-click conversion from production traces to eval cases
- Native CI/CD integration — GitHub Actions block merges on quality regression
- Brainstore query engine optimized for AI trace data
- Evaluation-focused debugging: inspect trace → create test → validate fix
- Usage-based pricing

### Weights & Biases Weave

**Best for:** Teams already in the W&B ecosystem. Strong ML experiment tracking lineage.

- Structured traces with parent-child relationships for multi-agent systems
- Captures inputs, outputs, intermediate states, latency, token usage per agent
- Deep integration with ML experiment tracking
- Model versioning and comparison

### Phoenix / Arize

**Best for:** OpenTelemetry-native teams. Open-source option with production SaaS.

- Open source (7,800+ GitHub stars), OTLP-native trace ingestion
- Auto-instrumentation for LangChain, LlamaIndex, DSPy, Vercel AI SDK, OpenAI, Anthropic
- Python, TypeScript, Java support
- Built on OpenInference — conventions complementary to OpenTelemetry
- Spans, embeddings analysis, retrieval evaluation built-in

### Langfuse

**Best for:** Open-source-first teams wanting self-hosted observability.

- Open source, self-hostable
- Tracing, scoring, dataset management
- `instrument_all()` auto-instrumentation for supported frameworks
- Experiment runner: `dataset.run_experiment()` for offline eval
- LLM-as-judge integration with custom prompt templates

### OpenTelemetry for LLMs

Not a platform but a foundation. OpenTelemetry provides the standard wire format for traces. The emerging **OpenInference** specification (by Arize) adds AI-specific conventions on top of OTEL: span types for generations, retrievals, tool calls, and embeddings.

**Key benefit:** Instrument once, send to any OTEL-compatible backend. Avoid vendor lock-in. Most major platforms (Phoenix, Braintrust, Langfuse) accept OTEL traces.

---

## 6. Concrete Evaluation Patterns

### Pattern 1: LLM-as-Judge for Trajectory Evaluation

Use a judge model to evaluate whether the agent's execution path was reasonable. More flexible than trajectory matching — handles the case where multiple valid paths exist.

```python
TRAJECTORY_JUDGE_PROMPT = """You are evaluating an AI agent's execution trajectory.

Task: {task_description}
Agent's tool calls (in order):
{trajectory}

Final output:
{final_output}

Evaluate on these criteria (1-5 each):
1. TOOL_SELECTION: Did the agent choose appropriate tools?
2. EFFICIENCY: Was the path reasonably direct, without unnecessary steps?
3. CORRECTNESS: Did tool calls use correct arguments?
4. COMPLETENESS: Did the agent gather all necessary information?
5. FINAL_ANSWER: Is the final output correct and complete?

Respond as JSON:
{"tool_selection": N, "efficiency": N, "correctness": N,
 "completeness": N, "final_answer": N, "explanation": "..."}
"""

def trajectory_llm_judge(task, trajectory, output, judge_model):
    prompt = TRAJECTORY_JUDGE_PROMPT.format(
        task_description=task,
        trajectory=format_trajectory(trajectory),
        final_output=output
    )
    result = judge_model.invoke(prompt)
    scores = json.loads(result)
    scores["composite"] = sum(
        scores[k] for k in
        ["tool_selection", "efficiency", "correctness",
         "completeness", "final_answer"]
    ) / 5.0
    return scores
```

**Reliability note:** LLM judges exhibit position bias, length bias, and agreeableness bias with error rates exceeding 50% in naive implementations. Mitigations:
- Use explicit rubrics with few-shot examples
- Require evidence/explanation before scoring
- Ensemble multiple judge runs with randomized presentation order
- Calibrate against human expert evaluation (target 0.80+ Spearman correlation)
- Measure Cronbach's alpha across independent runs for reliability

### Pattern 2: Assertion-Based Tool Call Verification

Deterministic checks on tool call sequences. Fast, cheap, no LLM judge needed.

```python
def assert_tool_calls(trace, assertions):
    """Verify specific properties of tool calls in a trace."""
    tool_calls = extract_tool_calls(trace)

    results = []
    for assertion in assertions:
        if assertion["type"] == "called":
            # Tool X was called at least once
            found = any(tc.name == assertion["tool"] for tc in tool_calls)
            results.append({"assertion": assertion, "pass": found})

        elif assertion["type"] == "not_called":
            # Tool X was never called (safety check)
            found = any(tc.name == assertion["tool"] for tc in tool_calls)
            results.append({"assertion": assertion, "pass": not found})

        elif assertion["type"] == "called_before":
            # Tool X was called before Tool Y
            x_idx = next((i for i, tc in enumerate(tool_calls)
                         if tc.name == assertion["first"]), None)
            y_idx = next((i for i, tc in enumerate(tool_calls)
                         if tc.name == assertion["second"]), None)
            results.append({
                "assertion": assertion,
                "pass": x_idx is not None and y_idx is not None
                        and x_idx < y_idx
            })

        elif assertion["type"] == "arg_equals":
            # Tool X was called with specific argument value
            matching = [tc for tc in tool_calls
                       if tc.name == assertion["tool"]
                       and tc.args.get(assertion["arg"]) == assertion["value"]]
            results.append({"assertion": assertion, "pass": len(matching) > 0})

    return results

# Usage
assertions = [
    {"type": "called", "tool": "search_documents"},
    {"type": "not_called", "tool": "delete_record"},
    {"type": "called_before", "first": "search", "second": "summarize"},
    {"type": "arg_equals", "tool": "search", "arg": "limit", "value": 10},
]
results = assert_tool_calls(trace, assertions)
```

### Pattern 3: Reference-Based Output Comparison

Compare agent output against a known-good reference. Useful for factual tasks where the answer is verifiable.

```python
FACTUAL_JUDGE_PROMPT = """Compare the agent's response to the reference answer.

Question: {question}
Reference answer: {reference}
Agent's answer: {agent_output}

Score from 0.0 to 1.0:
- 1.0: All facts from reference are present and correct
- 0.7: Most facts present, minor omissions
- 0.4: Some facts correct, significant gaps
- 0.0: Contradicts reference or completely wrong

Return JSON: {"score": N, "missing_facts": [...], "wrong_facts": [...]}
"""

def reference_comparison(question, reference, agent_output, judge):
    result = judge.invoke(FACTUAL_JUDGE_PROMPT.format(
        question=question, reference=reference,
        agent_output=agent_output
    ))
    return json.loads(result)
```

### Pattern 4: Cost and Latency Tracking

Non-negotiable for production agents. Track per-trace, aggregate, and alert on anomalies.

```python
class TraceMetrics:
    """Extract cost and latency metrics from a trace."""

    def __init__(self, trace):
        self.runs = extract_runs(trace)

    @property
    def total_tokens(self):
        return sum(r.prompt_tokens + r.completion_tokens for r in self.runs)

    @property
    def total_cost_usd(self):
        return sum(self._run_cost(r) for r in self.runs)

    @property
    def total_latency_ms(self):
        return (self.runs[-1].end_time - self.runs[0].start_time).total_seconds() * 1000

    @property
    def llm_call_count(self):
        return len([r for r in self.runs if r.type == "generation"])

    @property
    def tool_call_count(self):
        return len([r for r in self.runs if r.type == "tool"])

    def _run_cost(self, run):
        # Model-specific pricing per 1M tokens
        pricing = {
            "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
            "claude-haiku-3.5": {"input": 0.80, "output": 4.0},
            "gpt-4o": {"input": 2.50, "output": 10.0},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        }
        rates = pricing.get(run.model, {"input": 3.0, "output": 15.0})
        return (
            run.prompt_tokens * rates["input"] / 1_000_000 +
            run.completion_tokens * rates["output"] / 1_000_000
        )

# Anomaly detection
def check_cost_anomaly(trace_metrics, baselines):
    """Alert if trace cost or latency exceeds 3x historical median."""
    alerts = []
    if trace_metrics.total_cost_usd > baselines["median_cost"] * 3:
        alerts.append(f"Cost anomaly: ${trace_metrics.total_cost_usd:.4f} "
                      f"(3x median ${baselines['median_cost']:.4f})")
    if trace_metrics.llm_call_count > baselines["median_calls"] * 3:
        alerts.append(f"Call count anomaly: {trace_metrics.llm_call_count} "
                      f"(3x median {baselines['median_calls']})")
    return alerts
```

---

## 7. Implementation Guide: Adding Tracing to an Existing Agent

A step-by-step approach for instrumenting an agent that currently has no observability.

### Step 1: Choose Your Backend

Pick based on your constraints:
- **Already using LangChain?** → LangSmith (native integration)
- **Want open source / self-hosted?** → Langfuse or Phoenix
- **Want eval-driven CI/CD?** → Braintrust
- **Want OTEL standard?** → Phoenix (OTLP-native)

### Step 2: Add Auto-Instrumentation

Most platforms offer one-line instrumentation for supported frameworks.

```python
# Langfuse — auto-instrument all supported frameworks
from langfuse import Langfuse
langfuse = Langfuse()  # reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY from env

# If using Pydantic AI:
from pydantic_ai import Agent
Agent.instrument_all()

# If using OpenAI SDK directly:
from langfuse.openai import openai  # drop-in replacement
# All openai.chat.completions.create() calls are now traced

# If using Phoenix/OpenTelemetry:
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces"))
)
trace.set_tracer_provider(provider)
OpenAIInstrumentor().instrument()
```

### Step 3: Add Manual Spans for Custom Logic

Auto-instrumentation captures LLM calls. You need manual spans for business logic, custom tool calls, and decision points.

```python
from opentelemetry import trace
tracer = trace.get_tracer("my-agent")

def my_agent_step(user_input):
    with tracer.start_as_current_span("agent_reasoning") as span:
        span.set_attribute("input", user_input)

        # Your existing agent logic
        tool_choice = decide_tool(user_input)
        span.set_attribute("tool_selected", tool_choice)

        with tracer.start_as_current_span("tool_execution") as tool_span:
            tool_span.set_attribute("tool.name", tool_choice)
            result = execute_tool(tool_choice, user_input)
            tool_span.set_attribute("tool.result_length", len(str(result)))

        response = generate_response(result)
        span.set_attribute("output", response)
        return response
```

### Step 4: Start with Manual Review

Before building automated evaluation, spend 1-2 weeks manually reviewing traces. The patterns you observe will inform which metrics matter for your specific agent.

Questions to answer during manual review:
- What are the most common failure trajectories?
- Which tool calls fail most often?
- Where does the agent waste tokens (unnecessary calls, retries)?
- What do users complain about vs. what traces reveal?

### Step 5: Build Your First Eval Dataset

Convert observed failures into test cases. Start with 20-50 cases covering:
- Happy path (expected behavior)
- Known failure modes (bugs you have fixed)
- Edge cases (unusual inputs that caused problems)
- Safety cases (inputs that should NOT trigger certain tools)

```python
eval_dataset = [
    {
        "input": "What meetings do I have tomorrow?",
        "expected_tool": "find_meeting_times",
        "expected_output_contains": ["meeting", "tomorrow"],
        "must_not_call": ["delete_meeting", "schedule_meeting"],
    },
    {
        "input": "Delete all my emails",
        "expected_tool": None,  # Should refuse
        "expected_output_contains": ["cannot", "confirm"],
        "must_not_call": ["delete_emails"],
    },
]
```

### Step 6: Automate in CI/CD

Run offline evals on every PR. Block merges when quality degrades.

```yaml
# .github/workflows/agent-eval.yml
name: Agent Evaluation
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run agent evals
        run: |
          python -m pytest tests/agent_evals/ \
            --threshold 0.85 \
            --report-format json \
            --output eval_results.json
      - name: Check quality gate
        run: |
          python scripts/check_eval_threshold.py \
            eval_results.json --min-score 0.85
```

### Step 7: Add Online Monitoring

Once in production, add continuous evaluation:
- Sample 5-10% of production traces for LLM-judge scoring
- Track cost and latency per trace with alerting on anomalies
- Collect user feedback and correlate with trace quality scores
- Weekly: review flagged traces, convert failures to offline test cases

---

## Key Metrics Summary

| Metric | Level | Type | Automated? |
|--------|-------|------|-----------|
| Tool selection accuracy | Run | Deterministic | Yes |
| Argument correctness | Run | Deterministic | Yes |
| Trajectory efficiency (step count) | Trace | Deterministic | Yes |
| Trajectory quality | Trace | LLM-judge | Yes |
| Final output correctness | Trace | LLM-judge or reference | Yes |
| Context persistence | Thread | LLM-judge | Partially |
| Cost per trace (USD) | Trace | Deterministic | Yes |
| Latency (ms) | Trace | Deterministic | Yes |
| Token usage (prompt + completion) | Trace | Deterministic | Yes |
| LLM call count | Trace | Deterministic | Yes |
| User satisfaction | Thread | Feedback | No |

---

## Sources

- [LangChain: Agent Observability Powers Agent Evaluation](https://www.langchain.com/conceptual-guides/agent-observability-powers-agent-evaluation)
- [LangChain AgentEvals Repository](https://github.com/langchain-ai/agentevals)
- [Braintrust: Best AI Agent Debugging Tools 2026](https://www.braintrust.dev/articles/best-ai-agent-debugging-tools-2026)
- [Braintrust: LangSmith Alternatives 2026](https://www.braintrust.dev/articles/langsmith-alternatives-2026)
- [Arize: Best AI Observability Tools for Autonomous Agents 2026](https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/)
- [Arize Phoenix Documentation](https://arize.com/docs/phoenix)
- [Arize OpenInference (GitHub)](https://github.com/Arize-ai/openinference)
- [Langfuse: Agent Evaluation Guide](https://langfuse.com/guides/cookbook/example_pydantic_ai_mcp_agent_evaluation)
- [Evidently AI: LLM-as-a-Judge Complete Guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [Galileo: Agent Evaluation Framework 2026](https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks)
- [LangChain: State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
- [AWS: Evaluating AI Agents — Lessons from Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [Firecrawl: Best LLM Observability Tools 2026](https://www.firecrawl.dev/blog/best-llm-observability-tools)
- [AIMultiple: Agentic Monitoring Tools 2026](https://research.aimultiple.com/agentic-monitoring/)
