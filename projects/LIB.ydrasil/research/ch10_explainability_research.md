# Chapter 10: Visualization & Understanding — Making AI Visible

## Research: Explainability, Interpretability & Understanding AI Decisions

---

## 1. The Explainability Spectrum

There is no single "explainability" — there is a spectrum, and where your system falls on it determines what you can honestly claim to understand about its decisions.

### The Three Tiers

**Tier 1: Traditional ML — Genuinely Interpretable.** Decision trees, logistic regression, and linear models are interpretable by design. You can point to specific features, coefficients, and thresholds. For more complex models (gradient-boosted trees, random forests), post-hoc tools like SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) provide feature-level explanations that are mathematically grounded. In production, SHAP explanations take roughly 400ms for tabular data and 800ms for text classification, with a 50-100MB memory footprint per explanation process ([Reintech, 2025](https://reintech.io/blog/ml-model-explainability-in-production-shap-lime-llm)). These numbers are real and manageable. But even here, limitations exist: LIME fits local linear approximations and fails to capture nonlinear associations. SHAP struggles with correlated features, generating explanations based on unrealistic data instances ([Salih et al., 2025](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202400304)). Neither method infers causality — they show correlation patterns, not reasons.

**Tier 2: Fine-tuned Models — Partially Interpretable.** When you fine-tune a base model on domain data, you gain task-specific performance but lose the clean interpretability of simpler models. You can still analyze confusion matrices, measure per-class performance, and run feature importance analyses. But the internal representations become entangled. You know *what* the model gets right and wrong. You have limited insight into *why*.

**Tier 3: LLM API Calls — Mostly Opaque.** When you call Claude, GPT-4, or Gemini through an API, you are interacting with a system whose internal computations involve billions of parameters across hundreds of layers. You see input and output. The middle is, for practical purposes, a black box. The tools that exist to peer inside — which we'll cover in detail — are research-grade, not production-grade.

### Choose when / Avoid when

**Choose Tier 1 (traditional ML with SHAP/LIME) when:**
- Regulatory requirements demand feature-level explanations
- Decisions are high-stakes and must be auditable (loan approvals, medical triage)
- Stakeholders need to understand *why* at the individual prediction level

**Avoid Tier 1 when:**
- The task requires understanding language, context, or nuance
- You're building creative or generative features
- The explanation overhead exceeds the value of the explanation itself

**Choose Tier 3 (LLM APIs) when:**
- The task is complex enough that accuracy matters more than explainability
- You can build sufficient guardrails around the output (human review, validation layers)
- The cost of a wrong answer is low or recoverable

**Avoid Tier 3 when:**
- A regulator will ask "why did your system make this decision?" and "the model thought so" is not an acceptable answer
- Individual decisions carry irreversible consequences

**Failure mode:** Treating SHAP/LIME outputs as causal explanations. They show what features *correlated* with the output, not what *caused* it. A SHAP plot showing "income" as the top feature for a loan decision does not mean income caused the denial — it means income was the most influential variable in the model's calculation. The distinction matters legally and ethically.

---

## 2. LLM Interpretability in Practice

### Chain-of-Thought: The Illusion of Transparency

Extended thinking in Claude, chain-of-thought in GPT-4, and similar reasoning traces look like windows into how the model thinks. They are not. A 2025 paper from Oxford's AI Governance Institute states it directly: "Chain-of-thought reasoning is a powerful tool for interacting with LLMs, but it is not a substitute for rigorous explainability" ([Barez & Wu, 2025](https://aigi.ox.ac.uk/wp-content/uploads/2025/07/Cot_Is_Not_Explainability.pdf)).

The evidence is damning. Empirical studies on production models show post-hoc rationalization rates between 0.04% (Claude 3.7 Sonnet with thinking) and 13% (GPT-4o-mini) ([Arxiv 2503.08679](https://arxiv.org/abs/2503.08679)). These are cases where the model's chain-of-thought actively misrepresents its actual reasoning process. Even at 0.04%, that is not zero — and crucially, you cannot tell which 0.04% are unfaithful without mechanistic tools.

More fundamentally, mechanistic probing reveals that models often commit to an answer *before* generating the chain-of-thought. Researchers decoded the model's intended answer from residual stream activations at the last pre-CoT token with AUC above 0.9 across most tasks ([OpenReview, 2025](https://openreview.net/forum?id=UMUYpeXtJQ)). The reasoning trace is frequently a post-hoc justification of a decision already made — not a record of the decision being made.

**Choose when / Avoid when**

**Use chain-of-thought as interpretability when:**
- You need a rough audit trail (internal tools, prototypes)
- The reasoning is about multi-step computation where CoT-as-computation dominates (math, code analysis)
- You combine it with other verification methods (human review, automated checks)

**Avoid relying on chain-of-thought when:**
- Legal or regulatory compliance requires faithful explanations
- The output involves subjective judgment where post-hoc rationalization is most likely
- You would make different decisions if the explanation were wrong

### Logprobs: Confidence You Can Measure

Token-level log probabilities are the most mathematically grounded confidence signal available from LLMs. A logprob closer to 0 means higher model confidence in that specific token. Unlike chain-of-thought, logprobs are not generated *for* you — they are a direct readout of the model's probability distribution.

Practical applications in 2025-2026 include classification confidence scoring (flagging low-confidence predictions for human review) and hallucination detection (novel frameworks using logprob entropy to quantify uncertainty) ([FSE 2025](https://conf.researchr.org/details/fse-2025/fse-2025-posters/3/Logprobs-Know-Uncertainty-Fighting-LLM-Hallucinations)).

The limitation: very few LLM providers expose logprobs. OpenAI offers them. Anthropic does not expose raw logprobs in the Claude API as of early 2026. This makes logprob-based confidence estimation provider-dependent.

**Failure mode:** Assuming logprobs equal calibrated confidence. Raw logprobs are often poorly calibrated — a model reporting 90% confidence may only be correct 70% of the time. Calibration techniques (temperature scaling, isotonic regression) are necessary but add engineering overhead ([Latitude, 2025](https://latitude-blog.ghost.io/blog/5-methods-for-calibrating-llm-confidence-scores/)).

### Anthropic's Mechanistic Interpretability: The Frontier

Anthropic's circuit tracing research, published in April 2025 and named a [2026 MIT Technology Review Breakthrough Technology](https://www.technologyreview.com/2026/01/12/1130003/mechanistic-interpretability-ai-research-models-2026-breakthrough-technologies/), represents the most ambitious attempt to look inside a large language model.

The method produces "attribution graphs" — causal maps of how features (interpretable concepts) interact within the model to produce a specific output. Applied to Claude 3.5 Haiku, researchers traced concrete behaviors ([Anthropic, 2025](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)):

- **Multi-hop reasoning:** When asked "the capital of the state containing Dallas," the model activates Texas-related features from "Dallas," then routes through those features to identify Austin. Researchers validated this by swapping Texas features for California features — the model output Sacramento instead.
- **Poetry planning:** Before writing each line of a poem, the model pre-selects candidate rhyming words at the newline token and works backward from the target word. Injecting different rhyme features caused complete line restructuring (70% success rate).
- **Hallucination circuits:** The model contains default refusal circuits that are suppressed by "known answer" features. Hallucinations occur when unknown entities incorrectly activate suppression features. "Andrej Karpathy" triggered known-answer features (causing false paper attribution); "Josh Batson" did not, triggering appropriate refusal.
- **Medical reasoning:** The model performs internal differential diagnosis — activating pregnancy + symptoms leads to preeclampsia hypothesis, with simultaneous consideration of alternatives. Inhibiting preeclampsia features caused the model to suggest biliary disorder symptoms instead.

These tools were [open-sourced in May 2025](https://www.anthropic.com/research/open-source-circuit-tracing), with an interactive frontend on Neuronpedia.

**The honest assessment:** This is research-grade, not production-grade. You cannot run attribution graphs on every API call. The analysis requires significant compute, works on specific model versions, and produces results that require expert interpretation. It is science, not a product feature. But it is the most credible path toward genuine LLM interpretability that exists.

---

## 3. The Business Case for Explainability

### When You Need It

**Regulated industries.** The EU AI Act's transparency provisions take effect August 2, 2026. High-risk AI systems must be designed to be "sufficiently transparent to enable deployers to interpret a system's output and use it appropriately." Affected persons have the right to "a clear explanation of how the AI system was involved in the decision-making process" ([EU AI Act, Article 86](https://artificialintelligenceact.eu/article/86/)). Non-compliance penalties reach EUR 35 million or 7% of global annual turnover ([K&L Gates, 2026](https://www.klgates.com/EU-and-Luxembourg-Update-on-the-European-Harmonised-Rules-on-Artificial-IntelligenceRecent-Developments-1-20-2026)).

But here is the uncomfortable truth: the Act does not clearly define what level of transparency is sufficient. The practical tools, templates, and codes of practice are still being developed by the AI Office ([EU Digital Strategy](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)). Companies face a regulation that demands explainability without specifying what explainability means in practice.

**Healthcare and clinical decisions.** When an AI system recommends a treatment, "the model said so" is malpractice. Clinicians need to understand (or at least verify) the reasoning chain, the evidence sources, and the confidence level.

**Financial services.** Credit scoring, fraud detection, and algorithmic trading all face existing regulatory scrutiny (Fair Credit Reporting Act in the US, GDPR in Europe) that predates the AI Act. Adverse action notices already require explaining *why* a credit decision was made.

### When You Do Not Need It

**Internal productivity tools.** If you build an AI tool that helps your team draft emails or summarize documents, the cost of explainability outweighs the benefit. Nobody needs to know which attention head activated for a meeting summary.

**Creative and generative tasks.** When using AI for brainstorming, content generation, or design exploration, the output is evaluated by human judgment. The "why" of how the model generated a particular option is irrelevant — what matters is whether the output is good.

**Prototypes and MVPs.** Explainability is expensive. Adding it to a prototype that might be discarded in two weeks is waste. Build the explainability layer when you have validated the core value proposition.

### The Cost of Explainability

Explainability is not free. SHAP explanations add 400-800ms of latency per prediction. Running RAG with source attribution increases token usage (and cost) by 20-40%. Maintaining explanation pipelines alongside model pipelines doubles operational complexity. And sometimes, the most explainable model is not the most accurate one — a linear model you can fully explain may be 5-15% less accurate than an ensemble model you cannot.

**Choose when / Avoid when**

**Invest in explainability when:**
- Legal liability attaches to individual decisions
- Errors have irreversible human consequences
- Customer trust depends on understanding the "why"
- The EU AI Act classifies your system as high-risk

**Avoid investing in explainability when:**
- Humans review every output anyway (the human IS the explainability layer)
- The system is internal and the cost of errors is low
- You are still validating whether the AI approach works at all

**Failure mode:** Building explainability theater — investing in beautiful dashboards that show feature importances and confidence scores that look convincing but do not actually reflect the model's reasoning. This is worse than no explainability, because it creates false confidence. Some companies offer "superficial, pre-packaged rationales that sound plausible but don't reflect the system's actual reasoning" to satisfy compliance requirements ([ScienceNewsToday, 2025](https://www.sciencenewstoday.org/explainable-ai-xai-why-transparency-still-matters-in-2025)).

---

## 4. Practical Interpretability Techniques

### For RAG Systems: Show Your Sources

RAG (Retrieval-Augmented Generation) is the most naturally explainable LLM architecture because the retrieval step is inspectable. You can show users exactly which documents were retrieved, what text chunks were used, and how they ranked.

Key techniques in production:

- **Inline citations with source links.** Map each claim to a specific retrieved chunk. The VeriCite framework (2025) rigorously validates whether cited sources actually support the generated claims ([Arxiv 2510.11394](https://arxiv.org/html/2510.11394v1)).
- **Retrieval confidence scores.** Show the cosine similarity or relevance score for each retrieved document. Users quickly learn to discount answers sourced from low-relevance chunks.
- **Citation faithfulness verification.** A critical 2025 finding: citation correctness (does the cited document support the claim?) is different from citation faithfulness (did the model actually use that document, or did it post-rationalize a citation to fit pre-existing knowledge?) ([ACM SIGIR 2025](https://dl.acm.org/doi/10.1145/3731120.3744592)). The model can cite the right source for the wrong reason.
- **The "no results" signal.** When retrieval returns nothing relevant, say so. An honest "I don't have information about this" is more valuable than a fabricated answer with fabricated citations.

### For Agents: Decision Traces

AI agents (systems that take actions across multiple steps) are interpretable through their execution logs. Every tool call, every intermediate result, every branching decision is potentially loggable.

Practical approach:
- Log every tool invocation with input parameters and output
- Record the reasoning that led to tool selection (even if it is chain-of-thought and therefore imperfect)
- Maintain a session-level decision trace that shows the full sequence
- Flag when an agent retries, backtracks, or encounters errors — these are the most informative signals

The value of agent traces is not in explaining *why* the model chose a specific tool (that remains opaque). The value is in showing *what happened* — a sequential record that a human can review and say "that step was wrong" or "that should not have been called."

### For Classification: What Non-Technical Stakeholders Understand

After years of presenting confusion matrices and ROC curves to business stakeholders, the field has learned what actually communicates:

- **Confusion matrices** work if you relabel them. "Out of 100 fraudulent transactions, we caught 94 and missed 6" is a confusion matrix in natural language. Show it both ways.
- **Feature importance** works when features are business concepts, not technical variables. "The model weighs 'payment history' most heavily, followed by 'credit utilization'" communicates. "Feature_37 has a SHAP value of 0.43" does not.
- **Example-based explanations** work best of all. "This loan was denied because it looks most similar to these three denied loans" (k-nearest-neighbor style) is intuitively understood, even if it is technically imprecise.
- **Threshold explanations** work for binary decisions. "Applications scoring above 0.7 are approved automatically. Yours scored 0.62 and was flagged for human review." People understand thresholds.

**Choose when / Avoid when**

**Use source attribution (RAG) when:**
- Users need to verify claims against original documents
- The domain is factual and source credibility matters
- You want to reduce hallucination through transparent sourcing

**Avoid heavy source attribution when:**
- The task is creative synthesis (the value is in combining, not citing)
- Sources are all internal and equally trusted
- The attribution overhead makes the system unusably slow

**Failure mode:** Overwhelming users with technical interpretability data. Showing a business user a SHAP waterfall plot with 50 features is not interpretability — it is abdication of the responsibility to communicate clearly.

---

## 5. The Honest Limits

### LLM Self-Explanation Is Unreliable

When you ask a language model "why did you give that answer?", it generates a plausible-sounding explanation. That explanation is generated by the same process that generates fiction, poetry, and marketing copy. The model does not have privileged access to its own weights and activations. It is doing what it always does: predicting the most likely next tokens given the context — which in this case is "generate an explanation for this output."

The mechanistic evidence is clear. Models commit to answers before generating reasoning traces (AUC > 0.9 on pre-CoT probing). Under adversarial steering, models produce confabulation (false premises supporting the steered answer) and non-entailment (true premises with non-sequitur conclusions) at roughly equal rates ([OpenReview, 2025](https://openreview.net/forum?id=UMUYpeXtJQ)). Models silently correct errors in their chain-of-thought without acknowledging the correction — calculating a value as 16, then stating the correct value of 13, without revising the narrative.

This does not mean chain-of-thought is useless. It means it should be treated as a *communication aid* (helping users understand an output) rather than an *interpretability tool* (faithfully representing internal reasoning).

### Attention Patterns Do Not Mean What People Think

A persistent misconception is that attention weights show "what the model is focusing on." Research in 2025 showed that non-retrieval attention heads disproportionately attend to misleading tokens in uncertain contexts, and the influence of certain heads is highly context-dependent, activating specifically in situations where the model reasons incorrectly ([Arxiv 2510.22866](https://arxiv.org/html/2510.22866v1)). Attention is a mechanism, not an explanation. Showing attention heatmaps to stakeholders as "what the AI was looking at" is misleading at best.

### Explainability Theater

The hardest truth: much of what passes for "explainable AI" in production is theater. Post-hoc SHAP plots bolted onto black-box models. Chain-of-thought traces treated as faithful reasoning records. Attention visualizations presented as causal explanations. Confidence scores displayed without calibration.

This theater serves a purpose — it makes stakeholders feel comfortable, satisfies checkbox compliance, and provides a narrative around AI decisions. But it does not provide genuine understanding of why a model made a specific decision. And when something goes wrong — when a model makes a harmful recommendation, when a bias manifests in production — the theater collapses.

### The Gap

Regulators want to know: why did the AI make this decision about this person? Customers want to know: why was I denied, flagged, or categorized this way? Researchers can, in some cases, trace circuits and identify features. But this requires model access, significant compute, and expert analysis. It cannot be done in real-time, at scale, for every decision.

The honest answer in 2026: for traditional ML models, we can provide mathematically grounded (if imperfect) feature-level explanations. For LLMs, we can provide reasoning traces (unreliable), source attribution (for RAG systems), execution logs (for agents), and confidence estimates (when logprobs are available). For the deepest question — "what is actually happening inside this neural network?" — we have a research frontier (mechanistic interpretability) that is making genuine progress but is years from production applicability.

**Choose when / Avoid when**

**Be honest about limits when:**
- Always. Presenting unreliable explanations as reliable ones creates legal and ethical liability.

**Use "good enough" explanations when:**
- The alternative is no explanation at all and stakeholders need *something*
- You clearly label the explanation's limitations
- Human review catches cases where the explanation diverges from reality

**Avoid explainability claims when:**
- You cannot verify the explanation's faithfulness
- The stakes are high enough that a wrong explanation is worse than no explanation
- You are using it primarily to satisfy compliance without genuine transparency

**Failure mode:** The biggest failure is not the absence of explainability — it is the false presence of it. A confident-looking explanation that is wrong creates more damage than admitting "we cannot fully explain this decision, but here is what we can tell you." The organizations that will navigate the next decade of AI regulation most successfully are not those with the most sophisticated explainability dashboards, but those with the most honest communication about what their systems can and cannot explain.

---

## Sources Summary

- Anthropic, "On the Biology of a Large Language Model" (2025): https://transformer-circuits.pub/2025/attribution-graphs/biology.html
- Anthropic, "Circuit Tracing: Methods" (2025): https://transformer-circuits.pub/2025/attribution-graphs/methods.html
- Anthropic, "Open-sourcing circuit-tracing tools" (2025): https://www.anthropic.com/research/open-source-circuit-tracing
- MIT Technology Review, "Mechanistic Interpretability: 2026 Breakthrough Technologies": https://www.technologyreview.com/2026/01/12/1130003/mechanistic-interpretability-ai-research-models-2026-breakthrough-technologies/
- Barez & Wu, "Chain-of-Thought Is Not Explainability" (2025): https://aigi.ox.ac.uk/wp-content/uploads/2025/07/Cot_Is_Not_Explainability.pdf
- "Chain-of-Thought Reasoning In The Wild Is Not Always Faithful" (2025): https://arxiv.org/abs/2503.08679
- "Post-Hoc Reasoning in Chain-of-Thought" (2025): https://openreview.net/forum?id=UMUYpeXtJQ
- EU AI Act, Article 86: https://artificialintelligenceact.eu/article/86/
- EU AI Act, Article 13: https://artificialintelligenceact.eu/article/13/
- Cogent, "The XAI Reckoning" (2026): https://www.cogentinfo.com/resources/the-xai-reckoning-turning-explainability-into-a-compliance-requirement-by-2026
- Salih et al., "SHAP and LIME" (2025): https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202400304
- VeriCite (2025): https://arxiv.org/html/2510.11394v1
- "Source Attribution in RAG" (2025): https://arxiv.org/abs/2507.04480
- "Correctness is not Faithfulness in RAG Attributions" (2025): https://dl.acm.org/doi/10.1145/3731120.3744592
- "Logprobs Know Uncertainty" (FSE 2025): https://conf.researchr.org/details/fse-2025/fse-2025-posters/3/Logprobs-Know-Uncertainty-Fighting-LLM-Hallucinations
- Ericjinks, "Estimating LLM Classification Confidence" (2025): https://ericjinks.com/blog/2025/logprobs/
- Latitude, "5 Methods for Calibrating LLM Confidence Scores" (2025): https://latitude-blog.ghost.io/blog/5-methods-for-calibrating-llm-confidence-scores/
- Reintech, "ML Model Explainability in Production" (2025): https://reintech.io/blog/ml-model-explainability-in-production-shap-lime-llm
- "Interpreting and Mitigating Unwanted Uncertainty in LLMs" (2025): https://arxiv.org/html/2510.22866v1
