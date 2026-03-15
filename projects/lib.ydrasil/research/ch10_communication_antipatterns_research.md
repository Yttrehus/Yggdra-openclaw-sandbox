# Chapter 10 Research: Communication Anti-Patterns, Stakeholder Understanding & The Visualization Hype

**Purpose:** Raw research for the "making AI visible" chapter. Save practitioners from building dashboards nobody uses, giving demos that set false expectations, and communicating AI capabilities in ways that guarantee disappointment.
**Date:** 2026-02-09
**Target:** ~2500 words of usable material

---

## 1. The Understanding Gap

The most dangerous sentence in AI communication is "the AI understands." It does not understand. It processes tokens, predicts likely continuations, and produces outputs that pattern-match against training data. But the word "understands" makes stakeholders believe something categorically different is happening -- something closer to a junior employee reading a document and grasping its implications. That belief is where most AI project failures begin.

### The Anthropomorphism Tax

Every time you say "the model thinks," "the AI learned," or "it knows the answer," you are paying an invisible tax. You are importing expectations from human cognition -- that the system has memory, judgment, common sense, the ability to recognize when it is wrong. These expectations compound. A manager who hears "the AI understands our customer data" will eventually ask why it did not flag an obvious anomaly. A client who hears "it learned from your documents" will expect it to synthesize information the way a human analyst would. When the system fails at these very reasonable expectations, trust collapses. Not gradually -- suddenly.

IBM Watson for Oncology is the canonical example. After Watson won Jeopardy! in 2011, IBM announced it would become an AI doctor, with commercial healthcare products in 18-24 months. The demo was spectacular. The Jeopardy! performance created an expectation of "understanding." MD Anderson Cancer Center invested $62 million in a Watson partnership. The result: Watson's treatment recommendations were inconsistent with local clinical practices, relied on U.S.-centric guidelines that did not translate internationally, and in some documented cases provided unsafe recommendations. IBM Watson Health ultimately recorded what analysts described as an 80% failure rate in healthcare applications. The entire Watson Health division was sold off in 2022 ([IEEE Spectrum](https://spectrum.ieee.org/how-ibm-watson-overpromised-and-underdelivered-on-ai-health-care), [Henricodolfing.com](https://www.henricodolfing.com/2024/12/case-study-ibm-watson-for-oncology-failure.html)).

The failure was not primarily technical. It was communicative. IBM told hospitals that Watson "understood" cancer. It did not.

### The "95% Accurate" Trap

When someone tells you an AI system is "95% accurate," your first question should be: "Accurate at what?" Your second should be: "Measured on what data?"

Amazon's internal AI recruiting tool reportedly performed well on aggregate accuracy metrics. It screened resumes and rated candidates one to five stars. But it had learned from ten years of resumes submitted to Amazon -- a dataset dominated by men. The system systematically downgraded resumes containing the word "women's" (as in "women's rugby team") and penalized graduates of women's colleges. The bias was invisible in the top-line accuracy number because the metric measured prediction of "who Amazon historically hired," not "who would be the best candidate" ([MIT Technology Review](https://www.technologyreview.com/2018/10/10/139858/amazon-ditched-ai-recruitment-software-because-it-was-biased-against-women/), [ACLU](https://www.aclu.org/news/womens-rights/why-amazons-automated-hiring-tool-discriminated-against)).

This is the accuracy trap: a model can be statistically accurate while being functionally wrong. In imbalanced datasets -- which describes most real-world data -- a model that simply predicts the majority class can achieve 95%+ accuracy while being useless for the task it was built to perform. A cancer screening model that says "no cancer" for every patient would be 99% accurate if 99% of patients are cancer-free. The 1% it misses are the only patients that matter.

### How to Communicate Honestly

**Choose when to use precise language:** Always. Replace "the AI understands" with "the AI matches patterns in." Replace "it learned" with "it was trained on." Replace "95% accurate" with "it gives a correct answer on 95 out of 100 test cases from this specific dataset, with these known limitations."

**Avoid when:** Never. There is no situation where anthropomorphizing AI to stakeholders produces better long-term outcomes. The short-term "wow" always becomes long-term disappointment.

---

## 2. Dashboard Anti-Patterns

### The Executive Dashboard Trap

A 2026 survey by Demand Gen Report found that two-thirds of respondents say their dashboards regularly show "success" that fails to translate into revenue. Organizations using 11-25 marketing tools report nearly 90% unclear ROI ([Martech Edge](https://martechedge.com/news/the-2026-state-of-performance-marketing-report-how-inflated-signals-ai-noise-and-disconnected-tools-are-derailing-b2b-growth)). The dashboards look great. The business outcomes do not.

AI dashboards inherit all the sins of analytics dashboards and add new ones. Here are the vanity metrics that plague AI projects:

**Total queries served.** This tells you nothing. A chatbot that gives wrong answers to 10,000 questions per day is not better than one that correctly answers 500. Volume is not value.

**Model version / parameter count.** "We upgraded to GPT-4o" is not a metric. Unless you can show that the upgrade changed a business outcome, it is resume-driven development disguised as a status update.

**Uptime percentage.** 99.9% uptime on a system that nobody uses is not an achievement. Uptime is a hygiene factor, not a success metric.

**Average response time.** Fast wrong answers are not better than slow correct ones. Latency matters only after you have established that the outputs are good.

### What Actually Matters

The metrics that inform decisions are harder to build dashboards for, which is why most teams avoid them:

- **Task completion rate:** Of users who started an interaction with the AI, how many accomplished what they came to do?
- **Fallback / escalation rate:** How often does the AI fail to handle a request and hand off to a human? Is this rate improving or worsening?
- **Cost per successful outcome:** Not cost per query. Cost per query that actually solved a problem.
- **Error severity distribution:** Not "how many errors" but "how bad were the errors." A hallucinated citation in a research summary is different from a hallucinated drug dosage in a medical system.

A Federal News Network analysis of government AI adoption argued that responsible AI measurement requires four things: workflow improvement (did the AI reduce time-to-decision?), accuracy on the actual task, user trust calibration, and cost efficiency -- not surface-level activity counts ([Federal News Network](https://federalnewsnetwork.com/commentary/2025/12/beyond-vanity-metrics-rethinking-ai-impact-in-government/)).

### Visualization Lies

**Cherry-picked examples.** Every AI demo deck includes the three best outputs. Nobody shows the output where the model confidently hallucinated a customer's name, misclassified a critical ticket, or produced valid-looking but factually wrong analysis. If your dashboard has a "sample outputs" section with only impressive examples, it is lying by omission.

**Survivorship bias in reported metrics.** If you only measure users who completed a workflow, you miss everyone who abandoned it because the AI output was useless. Survivorship bias in data science means analyzing only entities that "survived" a selection filter while ignoring failures -- producing inflated conclusions and overly optimistic inferences ([kasadara.com](https://kasadara.com/2025/07/28/seeing-whats-missing-survivorship-bias-in-data-science/)).

**Accuracy on test sets vs production.** Research on AI scientist systems found that favorable outcomes are cherry-picked from experiments, creating post-hoc selection bias identical to training on test sets ([arXiv](https://arxiv.org/html/2509.08713v1)). If your dashboard reports accuracy from a held-out test set but you have never measured accuracy on live production data, the number is aspirational, not operational.

---

## 3. Communicating Uncertainty

### The Calibration Problem

A model that says it is 90% confident should be correct 90% of the time. That is calibration. Most models are not calibrated. Research on miscalibrated AI confidence found that presenting confidence scores facilitates appropriate user trust only when the confidence is well-calibrated -- but many models exhibit systematic overconfidence, reporting high confidence on outputs that are frequently wrong ([Understanding Miscalibrated AI Confidence](https://arxiv.org/html/2402.07632v4)).

This creates a toxic dynamic: users learn to trust confidence scores, the scores are wrong, and the users make worse decisions than they would have without the AI. Worse, they blame themselves ("the AI said 90%, I should have trusted it") rather than the system.

### When to Show Uncertainty

**Choose when to show confidence scores:** When users have the domain knowledge to interpret them, when the scores are calibrated against real data, and when showing uncertainty changes what the user would do. A radiologist seeing "85% confidence of malignancy" will order different follow-up tests than "99% confidence." The score changes behavior.

**Avoid when:** The user has no decision framework for interpreting confidence. Telling a customer service agent that the AI is "73% confident" about a ticket classification gives them nothing actionable. They will either trust it or not. The percentage adds noise, not signal.

A 2025 study on AI-assisted decision making found that communicating two distinct types of uncertainty -- fundamental uncertainty (the prediction itself) and model uncertainty (how confident the model is in that prediction) -- increased appropriate adherence to AI recommendations ([Foroughifar et al., SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5468868)). But this only worked when users understood what both types meant. Without that understanding, more information produced more confusion.

### The Practical Minimum

For most AI practitioner contexts, uncertainty communication does not require probability distributions or Bayesian credible intervals. It requires three things:

1. **A traffic light.** Green: the AI is confident and historically reliable on this type of input. Yellow: the AI produced an answer but has been unreliable on similar inputs. Red: the AI does not have enough information or this is outside its training distribution.
2. **A clear fallback.** When the light is yellow or red, what should the user do? "Ask a human" is a valid fallback. "Ignore and proceed" is not.
3. **Tracked calibration.** Periodically check: when the system says green, is it actually right? If green means right 95% of the time, that is calibrated. If green means right 60% of the time, your traffic light is broken.

---

## 4. The Demo Problem

### Why Demos Always Lie

Google's Gemini launch in December 2023 is the textbook case. Google released a video titled "Hands-on with Gemini: Interacting with multimodal AI" showing the model responding in real-time to voice commands and visual inputs. It looked magical -- the AI appeared to see drawings, identify objects, and respond conversationally. The video went viral.

Then came the correction: the demo was not conducted in real time. Voice prompts were dubbed afterward. The "interactions" used still image frames and text prompts, not the live voice and video shown in the video. Google admitted the video demonstrated "what the multimodal user experiences built with Gemini could look like" rather than what Gemini could actually do at that moment ([TechCrunch](https://techcrunch.com/2023/12/07/googles-best-gemini-demo-was-faked/), [TechRadar](https://www.techradar.com/computing/artificial-intelligence/that-mind-blowing-gemini-ai-demo-was-staged-google-admits)).

Google is not uniquely dishonest. Every AI demo has the same structural problem: the demo environment does not match the production environment. Demo inputs are curated to avoid edge cases. Demo outputs are selected from multiple runs. Latency is hidden by editing. Error handling is nonexistent because errors are prevented by input selection. The demo shows the ceiling of the system. Production shows the floor.

### The Wow-to-Meh Pipeline

The pattern is consistent across the industry. A 2025 analysis of agentic AI deployment found that while 60-70% of enterprises experimented with agentic AI, only 15-20% deployed agents in production ([Arion Research](https://www.arionresearch.com/blog/the-state-of-agentic-ai-in-2025-a-year-end-reality-check)). A WOW24-7 study found that 75.7% of organizations prioritized AI investment while 48.6% simultaneously reported struggling with implementation ([WOW24-7 / PR Newswire](https://www.prnewswire.com/news-releases/new-wow24-7-study-reveals-75-7-of-organizations-prioritize-ai-investment-despite-nearly-half-struggling-with-implementation-302645960.html)).

The failure sequence is predictable:

1. **Impressive demo** -- controlled inputs, curated outputs, enthusiastic presenter
2. **Executive buy-in** -- budget approved based on demo expectations
3. **Development** -- team discovers that the 5% failure rate on the 96th request is a dealbreaker for production
4. **Underwhelming pilot** -- real users with real data get inconsistent results
5. **Stakeholder disappointment** -- "this looked so much better in the demo"
6. **Project killed or deprioritized** -- organizational trust in AI damaged for the next proposal

### How to Give an Honest Demo

**Show the failure cases first.** Lead with "here is what the system cannot do" before showing what it can. This sets expectations correctly and builds trust.

**Use live inputs.** Let the audience provide inputs. If the system breaks on someone's question, that is useful information, not a disaster. A demo that survives real inputs is worth ten curated showcases.

**State the production gap explicitly.** "This demo runs on a single-tenant instance with no rate limiting. In production with 500 concurrent users, latency will be 3-5x higher and we expect a 5-8% error rate on edge cases."

---

## 5. Visualization Tools: Hype vs Reality Scorecard

| Tool | What It Promises | What It Actually Delivers | Hype Score | Reality Score | Verdict |
|------|-----------------|--------------------------|------------|---------------|---------|
| **Streamlit** | Build data apps in pure Python | Genuinely delivers for internal tools and prototypes. Clean API, fast iteration. Falls apart at scale -- no real auth, state management is painful, performance degrades with concurrent users. | 7/10 | 7/10 | **Use it.** Best tool for internal dashboards and quick demos. Do not ship it to customers as your production frontend. |
| **Gradio** | ML demos in minutes | Does exactly what it says for model demos. Built-in widgets for images, audio, video. Hugging Face integration is seamless. UI customization is limited -- everything looks like a Gradio app. | 6/10 | 7/10 | **Use it** for model demos and internal testing. Do not pretend it is a product. |
| **Weights & Biases** | Experiment tracking and model evaluation | The best experiment tracking tool available. Logging, comparison, hyperparameter sweeps -- all genuinely useful. The collaboration features and reports are oversold. Most teams use 20% of the features. | 8/10 | 6/10 | **Use the tracking.** Ignore the "AI platform" marketing. You need experiment logging, not a "system of record for ML." |
| **TensorBoard** | Training visualization | Was essential in 2018-2022. Now feels dated. The embedding projector is interesting for five minutes, then you close it and never open it again. Tightly coupled to TensorFlow. Rendering is slow with large datasets. | 5/10 | 4/10 | **Skip it** unless you are deep in the TensorFlow ecosystem and need training curves. Weights & Biases does everything TensorBoard does, better. |
| **Napkin AI** | Text to professional visuals | Genuinely fast for turning structured text into flowcharts and diagrams. Five million users as of 2025. Useful for presentations and documentation. Limited: struggles with vague or abstract content, outputs can look template-heavy ([max-productive.ai](https://max-productive.ai/ai-tools/napkin-ai/)). | 7/10 | 6/10 | **Use it** for quick diagrams in presentations. Do not use it as your primary visualization tool for data analysis. |
| **Claude Artifacts** | Interactive visualizations from conversation | Underrated. Can produce working React components, SVG graphics, Mermaid diagrams, and interactive data visualizations in seconds. Limitation: generated in conversation, so reproducibility depends on prompt consistency ([Anthropic](https://support.claude.com/en/articles/11649427-use-artifacts-to-visualize-and-create-ai-apps-without-ever-writing-a-line-of-code)). | 5/10 | 7/10 | **Use it** for one-off explorations and quick prototypes. The publish feature makes sharing trivially easy. Best ratio of effort-to-output for non-recurring visualizations. |
| **LangSmith** | LLM observability and tracing | If you use LangChain, LangSmith is the path of least resistance: set one environment variable and tracing works. The vendor lock-in is the cost -- tight coupling to LangChain means switching frameworks later is painful. Open-source alternatives like Langfuse provide 80% of the value without the lock-in. Free tier is 5,000 traces/month. | 8/10 | 5/10 | **Use Langfuse** instead unless you are committed to LangChain long-term. LangSmith's value proposition is convenience within one ecosystem, not excellence. |
| **Embedding Projectors** | Visualize high-dimensional spaces | Beautiful for screenshots and conference talks. Practically useless for actual debugging or understanding. You look at a t-SNE plot, see clusters, say "huh," and move on. The plot tells you clusters exist. It does not tell you what to do about them. Slow rendering, limited to ~1500 points before the browser struggles. | 6/10 | 2/10 | **Skip it.** If you need to understand your embeddings, compute quantitative metrics (cosine similarity distributions, cluster purity scores). A number you can act on beats a pretty plot you cannot. |

---

## 6. The "Good Enough" Principle

### When print() Beats a Dashboard

Most AI practitioners do not need a dashboard. They need a log file they can grep.

This is not a joke. For a solo practitioner or a team of three, the overhead of building, maintaining, and updating a Streamlit dashboard exceeds the value it provides. A `print()` statement that logs input, output, latency, and cost to a JSON file gives you everything you need for debugging. A spreadsheet that tracks daily cost, error count, and task completion rate gives you everything you need for monitoring.

The instinct to build a dashboard comes from two places: the desire to look professional ("we have a dashboard") and the engineer's instinct to automate observation before there is anything worth observing. Both are premature optimization.

### The Minimum Viable Approach

**For your own understanding:**
- `print()` + JSON log file. Grep when you need to investigate.
- A spreadsheet updated daily with: total cost, total queries, error count, one qualitative note about the worst failure you observed.
- A weekly 15-minute review where you look at the spreadsheet, read three random outputs, and decide if anything needs fixing.

**For stakeholder communication:**
- A screenshot of a real output with an annotation explaining what it did and why it matters. This takes five minutes and communicates more than any dashboard.
- A monthly one-page summary: what the AI did this month, what it failed at, what you changed, what it costs. Bullet points, not graphs.
- A live demo (honest, with real inputs) once per quarter.

**For when you actually need a dashboard:**
- You have 5+ people who need to monitor the system daily.
- You have SLAs tied to specific metrics that must be tracked in real time.
- Stakeholders have asked for specific metrics repeatedly and you have confirmed they will actually look at them.

If none of these conditions are true, do not build a dashboard. The time you save goes directly into making the AI system better -- which is the thing the dashboard was supposed to measure anyway.

### The Real Understanding That Matters

Miessler's framework applies here directly: scaffolding matters more than models, and context matters more than capability. The same is true for visualization. The understanding that matters most is not your manager's understanding of your AI system. It is *your* understanding of where the system fails, why it fails, and what to do about it. A `tail -f` on your log file while you run test cases teaches you more about your system in thirty minutes than any dashboard will in a month.

The best AI practitioners do not have the prettiest monitoring setups. They have the deepest intuition for when their system is lying. That intuition comes from reading outputs, not from reading graphs.

---

## Summary: The Communication Hierarchy

1. **Understand your own system first.** Logs, manual inspection, reading raw outputs. No tools required.
2. **Communicate honestly to stakeholders.** Plain language, failure cases included, uncertainty stated. A screenshot with an annotation beats a dashboard.
3. **Build lightweight monitoring.** A spreadsheet and a log file. Graduate to Streamlit or Gradio when the pain of not having a dashboard is real, not theoretical.
4. **Never build a dashboard to prove you are doing AI.** If the AI system is useful, the results speak louder than any visualization. If it is not useful, no dashboard will fix that.

The gap between what AI systems do and what people think they do is not a visualization problem. It is a communication problem. And the solution to a communication problem is almost never more software.
