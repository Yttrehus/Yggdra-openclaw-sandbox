# Chapter 10 Research: Visualization & Understanding -- Making AI Visible

**Purpose:** Practitioner-focused guide to visualization tools and techniques for AI systems. Not a matplotlib tutorial. Not "how to make pretty charts." The visualization decisions that reveal real insights and the ones that waste your time.
**Date:** 2026-02-09
**Target:** ~2500 words of usable material

---

## 1. Visualizing Embeddings -- Making Vector Spaces Visible

### The Problem

You have 50,000 vectors in a database. Each is 1536 dimensions. Something about your RAG system is not working -- retrievals feel off, clusters seem wrong, similar documents are not returning together. You cannot stare at a list of floating-point numbers and debug this. You need to see the space.

Dimensionality reduction projects those 1536 dimensions down to 2 or 3 that humans can perceive. Three methods dominate: PCA, t-SNE, and UMAP. They are not interchangeable.

### PCA: The Honest Baseline

PCA (Principal Component Analysis) finds the directions of maximum variance and projects data onto them. It is linear, deterministic, and fast. Run it on 100,000 points in seconds. The same input always produces the same output.

PCA preserves global structure -- the overall shape and spread of your data. It sacrifices local detail. If your embeddings have clear linear separations (e.g., two distinct document categories that differ along obvious axes), PCA will show this cleanly. If the structure is non-linear (most real embedding spaces), PCA will flatten interesting topology into mush.

**Use PCA for:** A first look. Sanity checking. Preprocessing before UMAP (reduce to 50 dimensions first, then UMAP to 2). It is the only method where distances in the projection correspond somewhat reliably to distances in the original space ([aicompetence.org, 2025](https://aicompetence.org/pca-vs-t-sne-vs-umap/)).

### t-SNE: Beautiful but Fragile

t-SNE excels at revealing local clusters. Points that are neighbors in high-dimensional space will be neighbors in the projection. The resulting plots look spectacular -- tight, well-separated clusters with clear boundaries.

The problem: t-SNE lies about everything except local neighborhoods. The distance between clusters is meaningless. The size of clusters is meaningless. Two clusters that appear far apart may be close in the original space. A large cluster is not necessarily more populated than a small one -- it may just have higher local variance. t-SNE also requires careful hyperparameter tuning. The perplexity parameter (typically 5-50) dramatically changes the result, and there is no principled way to choose it without trial and error.

t-SNE is also slow. On datasets above ~10,000 points, it becomes impractical without GPU acceleration or approximation methods.

**Choose t-SNE when:** You need to identify whether natural clusters exist in your embeddings, and you will not over-interpret inter-cluster distances.

**Avoid when:** You need to compare distances, need reproducible results (t-SNE is stochastic), or have more than ~10,000 points.

### UMAP: The Default Choice

UMAP (Uniform Manifold Approximation and Projection) is the right default for most practitioners. It is faster than t-SNE (handles millions of points), preserves both local and global structure better, and produces more stable results across runs ([biostatsquid.com, 2025](https://biostatsquid.com/pca-umap-tsne-comparison/); [Voxel51, 2025](https://voxel51.com/blog/how-to-visualize-your-data-with-dimension-reduction-techniques)).

The recommended pipeline: reduce to 50 dimensions with PCA first, then apply UMAP to get 2D coordinates. This is faster and often produces cleaner results than running UMAP directly on 1536-dimensional vectors.

**Choose UMAP when:** You need to visualize embedding spaces for debugging, exploration, or presentation. This is your default.

**Avoid when:** You need mathematically rigorous distance preservation (use PCA) or you need results that are identical across runs without setting a random seed.

### The Failure Mode Nobody Warns About

UMAP and t-SNE both create visual artifacts that look meaningful but are not. UMAP is sensitive to `n_neighbors` and `min_dist` parameters. Tune them too aggressively and continuous data fractures into discrete-looking clusters. Standard UMAP shows 5-15% variation in embedding coordinates across runs ([Nature Communications, 2024](https://www.nature.com/articles/s41467-024-45891-y)). This means a cluster boundary you see may be an artifact of that particular run.

The rule: **if a pattern disappears when you change hyperparameters or re-run with a different seed, it is not real.** Run the visualization three times with different seeds before drawing conclusions. If the clusters persist, they are probably real. If they shift or merge, you are seeing noise.

### When Embedding Visualization Actually Helps

It is genuinely useful for three things:

1. **Cluster quality auditing.** After building a RAG system, project your chunks into 2D. If chunks from the same document or topic do not cluster together, your chunking strategy is wrong.
2. **Semantic drift detection.** Embed the same queries a month apart. If the clusters have shifted, your data distribution has changed and your retrieval tuning may be stale.
3. **Retrieval gap identification.** Plot queries and retrieved documents together. Queries that land in empty regions (far from any document clusters) represent topics your knowledge base does not cover.

It is not useful for: choosing between embedding models (benchmark scores are more reliable), fine-tuning hyperparameters (use quantitative metrics), or impressing stakeholders (they will not understand what the clusters mean).

### The Tools

**Matplotlib + sklearn:** Bare minimum. `sklearn.decomposition.PCA` or `umap-learn` for reduction, `matplotlib.pyplot.scatter` for plotting. Good enough for debugging. Ugly for sharing.

**Plotly:** Interactive 2D and 3D scatter plots with hover labels. When you need to explore -- hover over a point to see which document it represents. The right choice for exploratory work.

**Nomic Atlas:** A managed platform that automates embedding, UMAP projection, and interactive exploration of large datasets. It adds automatic topic labeling, duplicate detection, and hierarchical clustering on top of visualization. If you have 50,000+ documents and want to explore them interactively without writing code, Atlas is the best option available ([atlas.nomic.ai](https://atlas.nomic.ai/); [OpenAI Cookbook, 2025](https://cookbook.openai.com/examples/third_party/visualizing_embeddings_with_atlas)). The tradeoff is vendor dependency and a cloud-first approach.

**Arize Phoenix:** Open-source, with 3D embedding visualization specifically designed for RAG debugging. Its specialized RAG view shows which retrieved chunks contributed to a response (or a hallucination). Built on OpenTelemetry, so it integrates with existing observability stacks ([phoenix.arize.com](https://phoenix.arize.com/); [Arize docs](https://docs.arize.com/phoenix)).

**Our recommendation:** Start with Plotly for exploration, Arize Phoenix for RAG debugging, Nomic Atlas for large-scale dataset understanding.

---

## 2. Visualizing LLM Behavior -- What You Can Actually See

### Token Probabilities (Logprobs)

When an LLM generates text, it computes a probability distribution over its entire vocabulary for each token position. Most APIs now expose these as log probabilities (logprobs). OpenAI, Anthropic, and Ollama (as of v0.12.11) all support this.

The practical visualization: color each token by confidence. High-probability tokens in green, low-probability in red. This reveals where the model is uncertain -- and uncertainty correlates with potential hallucination. If the model generates "The capital of France is Paris" with 99.9% confidence on "Paris," you can trust that. If it generates a specific date or number with 40% confidence, flag it for verification ([eli5 docs](https://eli5.readthedocs.io/en/latest/tutorials/explain_llm_logprobs.html); [Kedziorski, Medium, 2025](https://medium.com/@rafal.kedziorski/peek-inside-your-llm-building-a-token-probability-analyzer-with-ollamas-new-logprobs-f5d794671016)).

**Choose logprob visualization when:** You are building classification systems (use logprobs as confidence scores), debugging hallucinations in specific outputs, or building guardrails that flag low-confidence generations.

**Avoid when:** You want a general sense of "model quality" -- aggregate metrics are better for that. Also avoid treating logprobs as ground-truth calibration; models are often overconfident.

### Attention Patterns: Mostly Misleading

Attention visualizations -- heatmaps showing which tokens attend to which other tokens -- were the original "look inside the transformer" tool. They look impressive. They are mostly useless for practitioners.

The research is clear: attention patterns do not reliably explain model decisions. Serrano and Smith (2019) showed that shuffling attention weights barely changed model outputs. Jain and Wallace (2019) demonstrated that adversarial attention distributions could produce identical predictions. Recent 2025 studies confirm that attention maps are context-dependent and do not consistently provide reliable interpretive insights ([Frontiers in Computer Science, 2023](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2023.1178450/full); [HuggingFace Blog, 2025](https://huggingface.co/blog/royswastik/is-attention-interpretable)).

Wiegreffe and Pinter (2019) pushed back with "Attention is Not Not Explanation" -- arguing attention provides *some* signal when analyzed alongside other methods. Fair point. But for practitioners: if you need to understand why a model produced a specific output, look at logprobs, chain-of-thought traces, or activation patching. Do not stare at attention heatmaps.

**Choose attention visualization when:** You are doing mechanistic interpretability research on transformer internals. Almost never for application development.

**Avoid when:** You want to explain or debug a production LLM's behavior. Use tracing tools instead.

### Chain-of-Thought Traces: The Actually Useful View

The most valuable LLM visualization for practitioners is the simplest: seeing the chain of reasoning. When a model uses chain-of-thought (or when an agentic system executes multiple steps), the trace of intermediate steps is the visualization that actually helps you debug.

Tools like LangSmith and Langfuse render these as tree structures: a root call spawns child calls (retrieval, tool use, sub-prompts), each with captured inputs, outputs, latency, and token cost. When your RAG pipeline returns bad results, you click through the trace and see: was the query embedding wrong? Did the retriever return irrelevant chunks? Did the model ignore good context? The trace tells you exactly where the failure occurred.

**LangSmith** (by LangChain) is the commercial leader. Automatic tracing, dashboard visualization, performance monitoring, alerts, and an AI assistant (Polly) that analyzes traces. Tight integration with LangChain but works with any framework via API ([langchain.com/langsmith](https://www.langchain.com/langsmith/observability); [LangSmith docs](https://docs.langchain.com/langsmith/observability)).

**Langfuse** is the open-source alternative. MIT licensed, self-hostable, built on OpenTelemetry. 19,000+ GitHub stars. Acquired by ClickHouse in 2025, which suggests long-term investment in the platform. Supports LLM-as-judge evaluations with full trace visibility. If you want observability without vendor lock-in, Langfuse is the answer ([langfuse.com](https://langfuse.com/); [ClickHouse blog, 2025](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability)).

**Our recommendation:** Langfuse for self-hosted/open-source stacks. LangSmith if you are already in the LangChain ecosystem and want managed infrastructure. Arize Phoenix if embedding visualization is your primary need.

---

## 3. Interactive Dashboards for AI Systems

### Streamlit vs Gradio: The Real Decision

Both are Python frameworks for building web UIs without knowing JavaScript. The internet is full of feature-by-feature comparisons. Here is the actual decision framework:

**Gradio** is for model demos. You have a model that takes input X and produces output Y. Gradio gives you an interface for that in 10 lines of code. Built-in widgets for images, audio, video, and chat. Native Hugging Face integration. If you are publishing an ML model for others to try, Gradio is the obvious choice ([squadbase.dev, 2025](https://www.squadbase.dev/en/blog/streamlit-vs-gradio-in-2025-a-framework-comparison-for-ai-apps)).

**Streamlit** is for dashboards and applications. Multiple pages, interactive data exploration, custom layouts, integration with Plotly/Matplotlib/Altair for rich visualization. If you are building a monitoring dashboard for your RAG system -- showing retrieval quality over time, cost tracking, query patterns -- Streamlit is the right tool ([myscale.com, 2025](https://www.myscale.com/blog/streamlit-vs-gradio-ultimate-showdown-python-dashboards/)).

**Choose Gradio when:** Demo-ing a model. Building a chatbot interface. Prototyping for non-technical users. Deploying on Hugging Face Spaces.

**Choose Streamlit when:** Building operational dashboards. Exploring data interactively. Multi-page applications. Anything where the visualization is the product, not the model.

**Avoid both when:** You need production-grade applications with authentication, role-based access, or complex state management. At that point, build a real web application with FastAPI + React or similar.

### The Minimum Viable AI Dashboard

Every AI system in production needs monitoring. Here is what your first dashboard should track, in order of importance:

1. **Cost per day/week.** Track API spend. Plot it. Set an alert threshold. This is the number that surprises people -- a misconfigured loop can burn $500 in an hour.
2. **Latency distribution.** Not average latency -- the P95 and P99. If 1% of your requests take 30 seconds, your users notice.
3. **Error rate.** API failures, timeout rates, malformed responses. Track these over time to catch degradation.
4. **Usage patterns.** When do queries come in? What categories? This informs caching, scaling, and content decisions.
5. **Retrieval quality (for RAG).** Sample random queries weekly, check if retrieved chunks are relevant. This can be automated with LLM-as-judge but manual spot-checking is still irreplaceable.

Build this in Streamlit. Connect it to your logging backend (a JSON file works for small systems; PostgreSQL or ClickHouse for larger ones). This dashboard will save you money and catch failures before users report them.

---

## 4. Data Visualization for AI Projects

### Visualizing What Matters

AI projects generate data at every stage: training data distributions, embedding quality, chunk statistics, query logs, cost data, evaluation results. Most of this does not need specialized tools.

**Standard stack (use first):**
- **Matplotlib** for static charts in scripts and notebooks. Ugly defaults but complete control.
- **Seaborn** for statistical visualizations -- distribution plots, heatmaps, pair plots. Better defaults than matplotlib for data exploration.
- **Plotly** for interactive charts -- especially when exploring data or sharing with non-technical stakeholders. Hover labels, zoom, pan.

**Specialized tools (use when the standard stack is not enough):**
- **Nomic Atlas** for large-scale embedding exploration (50,000+ documents).
- **Arize Phoenix** for RAG pipeline traces and embedding debugging.
- **W&B (Weights & Biases)** for experiment tracking and training curves -- if you are fine-tuning models.

### The Visualization That Practitioners Skip

The single most valuable visualization for a RAG system is one almost nobody builds: **a histogram of chunk sizes.** Plot the character count (or token count) of every chunk in your vector database. If you see a bimodal distribution -- half your chunks are 200 tokens and half are 2000 tokens -- your chunking is inconsistent and your retrieval quality will suffer. Short chunks lose context; long chunks dilute relevance. This five-minute visualization catches a problem that takes hours to debug through retrieval testing.

Similarly: plot the distribution of similarity scores for your retrieval results. If most queries return chunks with cosine similarity between 0.78 and 0.82, your system has narrow effective range and may be missing relevant content that scores 0.75. If scores are spread from 0.3 to 0.95, your embeddings are highly discriminative -- which is good.

**Choose standard tools when:** You need a specific chart for a specific question. Most AI visualization needs are standard data visualization needs.

**Choose specialized tools when:** You need to interactively explore high-dimensional spaces, trace multi-step AI pipelines, or monitor production systems continuously.

---

## 5. AI-Powered Visualization -- When AI Makes the Charts

### Napkin AI: Concept Visualization

Napkin AI converts text into structured visuals -- flowcharts, mind maps, diagrams, infographics. Paste your notes, get a visual. It has reached 5 million users as of mid-2025 and generates clean, professional output from unstructured text ([napkin.ai](https://www.napkin.ai); [unite.ai review, 2025](https://www.unite.ai/napkin-ai-review/)).

**Where it works:** Explaining AI architectures to stakeholders. Turning meeting notes into process diagrams. Creating presentation visuals from bullet points. It is genuinely faster than building diagrams manually in PowerPoint or Lucidchart.

**Where it fails:** Anything requiring precision. Napkin AI generates template-style layouts. It cannot represent complex data relationships accurately. It cannot create a correct system architecture diagram from a description if the architecture has subtle dependencies. It is a communication tool, not an analysis tool.

**Choose Napkin AI when:** You need to communicate a concept visually and speed matters more than precision.

**Avoid when:** The visualization needs to be technically accurate (e.g., actual data flow diagrams for engineering teams).

### Claude Artifacts & ChatGPT Canvas

Both Anthropic's Claude (via Artifacts) and OpenAI's ChatGPT (via Canvas) can generate interactive visualizations from natural language descriptions. Claude Artifacts supports React components, charts via libraries like Recharts, SVG graphics, and full interactive dashboards. ChatGPT Canvas offers similar capabilities with inline code editing ([claude.ai/catalog/artifacts](https://claude.ai/catalog/artifacts); [Zapier guide, 2025](https://zapier.com/blog/how-to-use-claude-artifacts-to-visualize-data/)).

These are best understood as rapid prototyping tools. Describe the chart you want, get a working interactive version in 30 seconds. Iterate by describing changes. This is transformatively faster than writing Plotly code from scratch for one-off exploratory charts.

**Choose AI-generated visualizations when:** Prototyping. Exploring data quickly. Creating one-off charts for a specific question. Teaching someone what a visualization could look like before building the production version.

**Avoid when:** The visualization needs to be reproducible (the prompt-to-code process is not deterministic), the data is sensitive (you are sending it to an external API), or the chart will be used in a production dashboard (write real code for that).

### The Meta-Failure: AI Visualization of AI

The most dangerous application of AI-powered visualization is using AI to visualize AI system performance without understanding what the visualization shows. A model can generate a beautiful dashboard of its own performance metrics, but if the metrics are wrong -- if "retrieval accuracy" is measured incorrectly, or "confidence" is based on token probability when it should be based on factual verification -- the dashboard is worse than useless. It provides false confidence.

**The rule:** Use AI to generate the visualization code. Do not use AI to decide what to measure. The human decides what matters; the AI makes it visible.

---

## Summary: The Practitioner's Visualization Stack

| Need | Tool | When to graduate |
|------|------|-----------------|
| Quick data charts | Matplotlib / Seaborn | Never -- these are permanent |
| Interactive exploration | Plotly | When you need collaboration features |
| Embedding debugging | UMAP + Plotly | When dataset exceeds 50K points |
| Large-scale embedding exploration | Nomic Atlas | When you need persistent, shared views |
| RAG pipeline debugging | Arize Phoenix | When you need full observability |
| LLM tracing (open source) | Langfuse | When you need managed → LangSmith |
| LLM tracing (managed) | LangSmith | When you outgrow it → custom |
| Operational dashboards | Streamlit | When you need auth/roles → real web app |
| Model demos | Gradio | When you need customization → Streamlit |
| Concept diagrams | Napkin AI | When you need precision → manual tools |
| Quick prototyping | Claude Artifacts | When you need reproducibility → real code |

**The three visualizations every AI practitioner should build first:**
1. A cost-over-time chart (prevents budget surprises)
2. A chunk-size histogram (catches RAG quality issues)
3. A retrieval similarity score distribution (reveals effective retrieval range)

Everything else is optimization. Start with these three, and you will catch 80% of the problems that visualization can reveal.
