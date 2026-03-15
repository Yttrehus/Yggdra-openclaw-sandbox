# Chapter 5: RAG in Production — What Actually Works

**Researched:** 2026-02-09 via web research + production reports
**Status:** Research notes (pre-chapter draft)

---

## 5.1 Why This Chapter Is Different

Most RAG guides describe the happy path: embed documents, query a vector store, generate answers. This chapter is about the *unhappy* path — what breaks, what costs more than you expected, and which "advanced techniques" are worth your time versus which are resume-driven development.

The core insight: **80% of RAG failures trace back to chunking and data quality, not retrieval algorithms or model choice.** Teams chase fancy retrieval techniques when their documents are poorly chunked. This is the Context > Capability principle applied to RAG.

---

## 5.2 RAG Evaluation — The Minimum Viable Approach

### What It Is

RAG evaluation measures whether your system (a) retrieves the right documents, (b) generates faithful answers from them, and (c) does so at acceptable cost/latency.

### The Three Metrics That Actually Matter

1. **Retrieval Precision@k** — Of the k documents retrieved, how many are relevant? Low precision = the LLM processes noise alongside signal, degrading quality and increasing cost.
2. **Faithfulness / Groundedness** — Does the generated answer stay true to retrieved context, or does it hallucinate? This is the metric users care about most.
3. **Answer Relevance** — Does the answer actually address the user's question? (A faithful answer to the wrong question is still useless.)

### Tools Landscape

| Tool | Strength | Best For |
|------|----------|----------|
| **RAGAS** | Most popular OSS. Automated metrics, synthetic test data. Now supports agentic workflows. | Teams wanting quick, standardized evals |
| **TruLens** | RAG Triad methodology (Context Relevance, Groundedness, Answer Relevance). Strong visualization. | Debugging retrieval pipelines |
| **DeepEval** | Integrates RAGAS metrics with additional custom metrics. CI/CD friendly. | Teams wanting eval in their deployment pipeline |
| **Custom evals** | 20-30 gold-standard Q&A pairs specific to your domain | Everyone — this is your minimum viable eval |

### The Minimum Viable Evaluation

Start here — not with a framework:

1. **Create 20-30 high-quality test questions** covering your most common user scenarios
2. **Manually annotate expected answers** and the documents that should be retrieved
3. **Measure retrieval hit rate** — does the right document appear in top-k?
4. **Measure faithfulness** — does the answer stick to retrieved context?
5. **Track cost per query and latency** from day one

**Critical insight:** Treat retrieval and generation as separate systems. Prove you fetch the right docs *before* you tune prompts or models. Companies often judge RAG by answer quality alone but ignore that the retriever is the actual bottleneck.

### Choose When / Avoid When

**Choose formal eval frameworks when:** You have >100 users, production traffic, or regulatory requirements. You need CI/CD gates for quality regression.

**Avoid when:** You're prototyping. 20-30 manual test cases with a spreadsheet will tell you more than RAGAS on a system you're still designing.

### Hype vs Reality: 6/10
Eval tools are real and useful, but most teams don't need the full framework. The minimum viable approach (manual test cases + retrieval hit rate) catches 80% of issues. The sophisticated metrics help at scale but are not prerequisites.

### Failure Modes
- Evaluating answer quality without checking retrieval quality separately
- Using synthetic test data before you have real user queries
- Green dashboards while precision silently degrades (the "retrieval precision crisis" — embedding drift causes gradual misalignment between query and document embeddings)

---

## 5.3 Production RAG Patterns — Which Give the Biggest Lift

### Query Transformation Techniques

**HyDE (Hypothetical Document Embeddings)**
Generates a hypothetical answer to your query, embeds *that*, and uses it for retrieval. The insight: documents retrieve documents better than questions retrieve documents.

- **Biggest lift when:** Queries are abstract or there's vocabulary mismatch between user language and document language
- **Limitation:** Improves semantic alignment, not recall. If the document isn't in your corpus, HyDE won't find it.
- **Hype vs Reality: 5/10** — Moderate improvement in specific scenarios. Not the universal fix it's sometimes pitched as.

**Multi-Query Retrieval**
Generates multiple reformulations of the user's query, retrieves for each, then merges results.

- **Real numbers:** MQRF-RAG showed 14.45% F1 improvement over single-query on FreshQA tasks. On AmbigQA, 3.75% F1 improvement over HyDE.
- **When it matters:** Ambiguous queries, multi-intent questions
- **Hype vs Reality: 7/10** — Consistently delivers measurable improvements. The extra latency is the main tradeoff.

**Practical Selection Heuristic (from production teams):**
- Very short query → HyDE
- High ambiguity → Multi-Query
- Otherwise → Simple query expansion (cheapest, often sufficient)

### Chunking Strategies

This is where most teams should spend their optimization budget.

**The data point that matters:** Naive fixed-size chunking achieves faithfulness scores of 0.47-0.51. Optimized semantic chunking achieves 0.79-0.82. That's a 60% improvement from chunking alone — larger than most retrieval technique improvements.

**Parent-Child Chunking**
Small child chunks (100-500 tokens) are embedded and searched. When a child matches, its larger parent chunk (500-2000 tokens) is returned to the LLM.

- **Choose when:** Long documents where answers are specific but context matters. Token-budget-conscious deployments.
- **Avoid when:** Short documents. Simple Q&A where small chunks suffice.
- **Production result:** Teams using hierarchical chunking report 30-40% fewer retrieval calls needed.

**Metadata Filtering**
Add structured metadata (date, document type, product version, author) and filter *before* similarity search.

- **This is the most underrated technique.** It's simple, deterministic, and dramatically improves precision for any domain with structured attributes.
- **Choose when:** Always. There's almost no scenario where metadata filtering hurts.

### Reranking

Use a cross-encoder or LLM-based reranker after initial vector retrieval to reorder results by relevance.

- **Choose when:** Your top-k retrieval is noisy (lots of semantically similar but irrelevant results)
- **Avoid when:** Your retrieval precision is already high. Adds 100-300ms latency.
- **Hype vs Reality: 7/10** — Reranking genuinely helps and is one of the highest-ROI additions to a basic RAG pipeline.

---

## 5.4 RAG + Agents — When Adding Intelligence Helps vs Hurts

### What It Is

Agentic RAG embeds autonomous agents into the retrieval pipeline. Instead of a fixed retrieve-then-generate flow, agents can: plan multi-step retrieval, decide which tools to use, iterate if initial retrieval is insufficient, and synthesize across multiple retrieval rounds.

### Where It Actually Helps

- **Multi-hop reasoning:** "What was our Q3 revenue for products launched after the merger?" requires connecting information across multiple documents. Standard RAG fails here; agents decompose the query.
- **Heterogeneous data sources:** When answers require querying a vector store + a SQL database + an API. Agents route to the right tool.
- **Underspecified queries:** When the user's question needs clarification or decomposition before retrieval makes sense.

### Where It Hurts

- **Simple lookup queries:** "What's our refund policy?" doesn't need an agent. Adding one increases latency 3-5x and cost 2-4x for zero quality gain.
- **Reliability math:** Each agent step has a failure probability. 0.95 retrieval x 0.95 reranking x 0.95 generation x 0.95 agent routing = 0.81 total reliability. Every layer compounds failure.
- **Latency-sensitive applications:** Agent deliberation adds seconds. For customer-facing chat, this can be unacceptable.

### Choose When / Avoid When

**Choose Agentic RAG when:** Questions require multi-hop reasoning across documents. You have multiple data sources (structured + unstructured). Query complexity varies widely (route simple queries to basic RAG, complex to agentic).

**Avoid when:** Most queries are simple lookups. Latency matters more than completeness. You haven't proven basic RAG works first. (The Ladder of AI Solutions applies — exhaust simpler approaches before adding agents.)

### Hype vs Reality: 5/10
The concept is sound. The production reality is that 90% of agentic RAG projects failed in production in 2024 — not because the technology is broken, but because teams underestimate compounding failure rates. Start with basic RAG. Add agents only when you have evidence that basic RAG's limitations are your actual bottleneck.

### Failure Modes
- Recursive retrieval loops (agent keeps retrieving the same documents)
- Cost explosion from uncontrolled agent iterations
- Latency spikes when agent "thinks" for multiple rounds
- Debugging difficulty — when the agent makes a bad retrieval decision, tracing why is hard

---

## 5.5 GraphRAG and Knowledge Graphs

### What It Is

Microsoft's GraphRAG builds a knowledge graph from your documents (entities, relationships, community summaries), then uses graph traversal + vector search for retrieval. The key insight: standard RAG misses relationships between entities that span multiple documents.

### Real Performance Numbers

- **The headline claim:** Accuracy on complex multi-hop questions jumped from 43% to 91% in one case study. Query costs dropped 97%.
- **The reality check:** An unbiased evaluation framework (Zeng et al., 2025 — arxiv 2506.06331) found that "performance gains are much more moderate than reported previously" and "may be caused by evaluation biases." When biases are eliminated, gains "become much more moderate or even vanish."
- **LinkedIn production result:** 28.6% reduction in resolution time — meaningful but not transformative.

### Cost Reality

Knowledge graph extraction costs 3-5x more than baseline RAG upfront. Ongoing maintenance is significant — every document update requires graph re-extraction. One comparison: GraphRAG with ArangoDB costs ~$1,825/year vs vector RAG at ~$3,650/year for 10K queries/day — but this ignores the engineering time for graph maintenance.

### Choose When / Avoid When

**Choose GraphRAG when:** Your domain is relationship-heavy (supply chains, organizational structures, legal compliance). Questions require synthesis across many documents. You need explainability (graph paths are interpretable). You have the engineering capacity to maintain the knowledge graph.

**Avoid when:** Your questions are primarily about specific document content (standard RAG handles this fine). Your corpus changes frequently (graph maintenance becomes a burden). You're optimizing prematurely — prove standard RAG is insufficient first.

### Hype vs Reality: 4/10
GraphRAG is real technology solving a real problem (multi-document synthesis). But it's dramatically over-hyped relative to the number of use cases that actually need it. Most RAG deployments don't have a "relationship reasoning" bottleneck — they have a "chunking and retrieval quality" bottleneck. Fix the basics first.

### Failure Modes
- Over-engineering: building a knowledge graph when better chunking would solve the problem
- Graph staleness: documents update but the graph doesn't
- Entity resolution errors: the graph connects the wrong entities
- Cost surprise: the upfront graph extraction LLM costs are substantial

---

## 5.6 Common Production Failures — The Demo-to-Production Gap

### The Compound Failure Problem

The reliability math that kills production RAG:
- 0.95 (retrieval) x 0.95 (reranking) x 0.95 (generation) = **0.81 total reliability**
- Your system fails 1 in 5 times. Users notice.

### The Top 5 Production Killers

**1. Chunking Is the Real Bottleneck (Not Models)**
80% of RAG failures trace to chunking. Naive fixed-size chunking: faithfulness 0.47-0.51. Semantic chunking: 0.79-0.82. Most teams skip straight to "advanced retrieval" without fixing this.

**2. Silent Quality Degradation**
After 6 months, domain language evolves. Embedding models get updated by providers. Document indexes using older embeddings become misaligned with query embeddings. Dashboards show green. Precision silently drops. You find out when a customer gets a hallucinated answer.

**3. Cost Explosion at Scale**
- Unoptimized at 100K queries/day: ~$19,460/month
- With smart routing, caching, model optimization: ~$10,460/month (46% savings)
- The trap: costs grow non-linearly. What works at 1K queries/day becomes financially unsustainable at 100K.

**4. The "Works in Demo" Pattern**
Demo: 50 clean documents, 10 test questions, controlled environment. Production: 50,000 messy documents with formatting inconsistencies, duplicates, stale content, conflicting information, and users who ask questions you never anticipated. The gap is not technical — it's about data quality and query diversity.

**5. Context Position Bias (Lost in the Middle)**
LLMs disproportionately favor information at the start and end of context windows. Stanford research: performance degrades 30%+ when relevant information is in the middle. Your retrieved documents' order matters more than you think.

### Additional Failure Modes Worth Knowing

- **Citation hallucination:** Model cites a retrieved document that doesn't actually support the claim
- **Temporal staleness:** Confidently returns outdated information without indicating age
- **Cross-document contradiction:** Retrieves conflicting documents, generates incoherent synthesis
- **Negative interference from retrieval overload:** More than 5-10 documents often shows diminishing or negative returns

---

## 5.7 The RAG Landscape 2026 — What's Commoditized, What's Still Hard

### What's Commoditized (Don't Overthink These)

**Vector databases:** Qdrant, Weaviate, Pinecone, Milvus — they all work. Performance differences are marginal for most use cases. "Most RAG failures are self-inflicted, not database-inflicted." Pick based on your ops preferences (managed vs self-hosted) and move on.

**Embedding models:** OpenAI text-embedding-3-small/large, Cohere embed-v3, Google's embedding model — all adequate. The model matters less than your chunking strategy.

**Basic RAG pipeline:** Chunk → embed → store → retrieve → generate. This is a solved problem. If this is all you need, use any framework or just call the APIs directly.

### What's Still Hard

**Evaluation and monitoring:** Knowing when your RAG system is degrading. Automated, continuous evaluation in production is still an unsolved problem for most teams.

**Multi-document synthesis:** When answers require reasoning across 5+ documents with potentially conflicting information. This is where GraphRAG and Agentic RAG promise help, but neither is mature enough to be "just plug in."

**Data quality at scale:** Keeping 50K+ documents clean, deduplicated, fresh, and properly chunked. This is an ops problem, not a tech problem, and most teams understaff it.

**Cost optimization:** The difference between naive and optimized RAG at scale is $9K/month. Caching, smart routing, adaptive retrieval — these require ongoing engineering investment.

### Framework Recommendations

| Approach | Choose When | Token Efficiency |
|----------|-------------|------------------|
| **Direct API calls** | Simple RAG, you understand the pipeline, you want full control | Best (you control everything) |
| **LlamaIndex** | Complex ingestion (messy PDFs, heterogeneous formats), retrieval quality is your bottleneck | ~1,600 tokens/query |
| **LangChain / LangGraph** | Complex agents, multi-turn state management, broad tool integration | ~2,400 tokens/query |
| **Hybrid (LlamaIndex ingestion + LangGraph orchestration)** | Enterprise systems with both complex data and complex workflows | Depends on mix |
| **Haystack** | Most token-efficient framework if that's your priority | ~1,570 tokens/query |

**The honest recommendation:** Start with direct API calls. You'll understand every part of the pipeline. Move to a framework only when you hit a specific limitation (complex document parsing, state management, tool routing) that the framework solves. The Ladder of AI Solutions applies: simplest working solution first.

### Long Context vs RAG

The elephant in the room: with Gemini 3 at 2M tokens and Claude Sonnet at 1M, do you even need RAG?

**The numbers:**
- RAG average query cost: ~$0.00008
- Long context average query cost: ~$0.10
- RAG is **1,250x cheaper** per query
- RAG latency: ~1 second. Long context: ~45 seconds for large inputs
- Long context accuracy: 99% recall at 1M tokens, BUT 30%+ degradation for information in the middle of the context (Stanford "Lost in the Middle")

**Choose long context when:** Corpus is small (<500 pages). You need the model to understand relationships across the entire document set. One-off analysis, not repeated queries. You can afford the cost.

**Choose RAG when:** Corpus is large or growing. You need citations to specific sources. Queries are frequent (cost matters). Latency matters. Data changes frequently. You need to scale.

**The synthesis:** They're complementary, not competing. Use long context for document understanding/analysis. Use RAG for production query answering at scale. Some teams use both: RAG for retrieval, then stuff retrieved chunks + query into a larger context window.

---

## 5.8 Hype vs Reality Scorecard

| Technology | Hype Level | Reality Score | Delta | Verdict |
|------------|-----------|---------------|-------|---------|
| **RAG itself** | 9/10 | 7/10 | -2 | Real and necessary. But harder in production than demos suggest. The "80% is data quality" lesson is consistently underlearned. |
| **Vector databases** | 8/10 | 6/10 | -2 | Commoditized. The database choice matters far less than your chunking and retrieval strategy. Don't agonize over Pinecone vs Qdrant. |
| **GraphRAG** | 8/10 | 4/10 | -4 | Biggest hype-reality gap. Real gains are "much more moderate than reported" per unbiased evaluation. Most teams don't have a graph-shaped problem. |
| **Agentic RAG** | 9/10 | 5/10 | -4 | Sound concept, brutal production reality. 90% failure rate in 2024 deployments. Compounding failure probability kills reliability. |
| **RAG frameworks** | 7/10 | 5/10 | -2 | Useful for complex pipelines, but add token overhead (50% more tokens for LangChain vs direct API). Many teams would be better served by understanding the pipeline directly. |
| **Long context as RAG replacement** | 7/10 | 4/10 | -3 | 1,250x more expensive per query. 30%+ accuracy degradation in middle of context. Complementary to RAG, not a replacement. |
| **Reranking** | 5/10 | 7/10 | +2 | The rare *underhyped* technique. Consistently delivers measurable improvement with modest complexity. |
| **Metadata filtering** | 3/10 | 8/10 | +5 | The most underhyped technique in the entire RAG stack. Simple, deterministic, dramatically effective. Nobody writes blog posts about it because it's boring. |

### The Pattern

The most hyped techniques (GraphRAG, Agentic RAG, long context replacement) have the biggest reality gaps. The most effective techniques (chunking optimization, metadata filtering, reranking) are boring and underhyped. This is the Scaffolding > Models principle in action: the value is in the boring plumbing, not the exciting architecture diagrams.

---

## 5.9 The Practitioner's Decision Tree

```
Q: Do you need RAG?
├─ Corpus < 500 pages, infrequent queries → Try long context first
├─ Corpus large/growing, frequent queries → Yes, build RAG
│
Q: Where to start?
├─ Step 1: Fix your chunking (semantic chunking, proper boundaries)
├─ Step 2: Add metadata filtering
├─ Step 3: Add reranking
├─ Step 4: Build 20-30 eval test cases
├─ Step 5: ONLY THEN consider advanced patterns
│
Q: Which advanced pattern?
├─ Queries are ambiguous → Multi-query retrieval
├─ Vocabulary mismatch → HyDE
├─ Multi-document synthesis needed → Evaluate GraphRAG
├─ Complex multi-step reasoning → Evaluate Agentic RAG
├─ Simple lookups at scale → Basic RAG is enough. Stop here.
```

---

## Primary Sources

- [RAGAS Paper (arxiv 2309.15217)](https://arxiv.org/abs/2309.15217) — Original evaluation framework
- [GraphRAG Unbiased Evaluation (arxiv 2506.06331)](https://arxiv.org/abs/2506.06331) — "Performance gains much more moderate than reported"
- [Agentic RAG Survey (arxiv 2501.09136)](https://arxiv.org/abs/2501.09136) — Comprehensive survey of agentic patterns
- [RAG in Production: What Actually Breaks](https://alwyns2508.medium.com/retrieval-augmented-generation-rag-in-production-what-actually-breaks-and-how-to-fix-it-5f76c94c0591) — Production failure taxonomy
- [Ten Failure Modes of RAG](https://dev.to/kuldeep_paul/ten-failure-modes-of-rag-nobody-talks-about-and-how-to-detect-them-systematically-7i4) — Systematic failure analysis
- [Retrieval Is the Bottleneck: HyDE, Query Expansion, Multi-Query](https://medium.com/@mudassar.hakim/retrieval-is-the-bottleneck-hyde-query-expansion-and-multi-query-rag-explained-for-production-c1842bed7f8a) — Production pattern comparison
- [RAG vs Long-Context LLMs Comparison](https://www.meilisearch.com/blog/rag-vs-long-context-llms) — Cost and performance data
- [Production RAG 2026: LangChain vs LlamaIndex](https://rahulkolekar.com/production-rag-in-2026-langchain-vs-llamaindex/) — Framework comparison with benchmarks
- [Six Lessons Building RAG in Production](https://towardsdatascience.com/six-lessons-learned-building-rag-systems-in-production/) — Practitioner lessons
- [Fixing RAG in 2026: Why Enterprise Search Underperforms](https://medium.com/@gokulpalanisamy/fixing-rag-in-2026-why-your-enterprise-search-underperforms-and-what-actually-works-93480190fdd0) — Enterprise perspective
- [The Retrieval Precision Crisis](https://ragaboutit.com/the-retrieval-precision-crisis-why-your-rag-metrics-are-hiding-silent-failures/) — Silent degradation patterns
- [RAG Evaluation: Complete Guide 2025](https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/) — Evaluation methodology
- [Advanced RAG Techniques (Neo4j)](https://neo4j.com/blog/genai/advanced-rag-techniques/) — Pattern taxonomy
- [Agentic RAG 2026: UK/EU Enterprise Guide](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026) — Enterprise deployment patterns

---

**Last updated:** 2026-02-09
