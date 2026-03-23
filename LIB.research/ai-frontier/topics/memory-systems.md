---
title: Memory Systems — RAG, Vector DB & Retrieval
date: 2026-03-22
category: AI Frontier
status: audit-passed
---

# Memory Systems — RAG, Vector DB & Retrieval (marts 2026)

## Metadata
- **Emne:** AI Hukommelsessystemer
- **Kontekst:** Yggdra Projektet
- **Standard:** APA 7th
- **Status:** Færdig-auditeret

## 1. RAG: State of the Art

### Det kritiske tal
**73-80% af enterprise RAG-projekter fejler i produktion** (Analytics Vidhya, 2025). Fejl opstår typisk i de fem multiplikative faser:
chunking → embedding → retrieval → context assembly → generation.

### RAG vs. Long Context vs. Fine-tuning

| | RAG | Long Context | Fine-tuning |
|---|---|---|---|
| Cost/query | ~$0.00008 | ~$0.10 (1250x) | ~$0.001 |
| Latency | ~1s | 30-60s | Sub-second |
| Updatability | Løbende | Per query | Retrain (dage) |

**"Long context kills RAG" debat:** Stanford (2023) påviste "Lost in the Middle" fænomenet, hvor LLMs ignorerer information placeret centralt i lange kontekster. Long context er derfor komplementært til RAG, ikke en erstatning.

---

## 2. RAG-arkitekturer

### Hybrid Search
Kombinerer vektor (dense) og keyword (BM25/sparse) søgning.
- **Status:** Production-ready (Qdrant, 2024).
- **Relevans:** Qdrant understøtter det; Yggdra bør implementere det for keyword-tunge queries.

### Agentic RAG
AI-agenten styrer retrieval-strategien dynamisk og vælger mellem forskellige kilder (vektor, web, SQL).

### HyDE (Hypothetical Document Embeddings)
Genererer et hypotetisk svar, embedder det og søger med denne vektor. Løser problemet med længde-mismatch mellem query og dokument.

---

## 3. Chunking og Embeddings

### Chunking
Studier viser, at optimeret semantisk chunking kan forbedre faithfulness med op til 60% sammenlignet med naiv chunking.
- **Anbefaling:** Skift fra fixed-size til recursive character splitting som baseline.

### Embedding-modeller
Yggdras nuværende valg, `text-embedding-3-small` (OpenAI, 2024), er omkostningseffektivt ($0.02/M tokens) og tilstrækkeligt til de fleste solo setups.

---

## 4. Vector DB: Yggdras Qdrant Setup

### Nuværende tilstand
7 collections, ~84.210 points, dense-only.

| Collection | Points | Formål |
|------------|--------|--------|
| routes | 40.053 | Transportruter |
| sessions | 42.106 | Sessionshistorik |
| docs | 1.169 | Dokumentation |

**Vurdering:** Qdrant (Docker) er det korrekte valg for en solo self-hosted løsning.
**Mangler:** Hybrid search (BM25) og Reranking (Cohere, 2024). Reranking kan forbedre retrieval-kvalitet markant (Databricks, 2024).

---

## 5. Session Persistence og Episodisk Hukommelse

### Complementary Learning Systems (CLS)
Forskning i CLS (Kumaran et al., 2016) indikerer, at intelligente agenter har brug for to systemer: et hurtigt, specifikt system (hippocampus/RAG) og et langsomt, generaliseret system (neocortex/model weights).

### Glemsel og Decay
Hjernen glemmer aktivt for at prioritere vigtig viden. AI-systemer uden temporal decay lider ofte af "context pollution".
- **Løsning:** Implementer temporal decay (`score = relevance × recency_weight`) i retrieval-pipelinen.

---

## 6. Konklusion og Indsigt

### Prioriterede anbefalinger
1. **Reranking:** Integrer Cohere Rerank i ctx-kommandoen for højere præcision (Cohere, 2024).
2. **Hybrid Search:** Tilføj sparse vectors til Qdrant collections (Qdrant, 2024).
3. **Temporal Decay:** Nedprioriter gammel viden automatisk for at undgå støj.

## Referencer

Anthropic. (2024). *The "lost in the middle" phenomenon in long context LLMs*. https://www.anthropic.com/research/
Cohere. (2024). *Rerank: Higher precision retrieval*. https://cohere.com/rerank
Databricks. (2024). *Improving RAG accuracy with reranking*. https://www.databricks.com/blog/
Kumaran, D., Hassabis, D., & McClelland, J. L. (2016). *What learning systems do intelligent agents need? Complementary learning systems theory updated*. Trends in Cognitive Sciences, 20(7), 512-534. https://doi.org/10.1016/j.tics.2016.05.004
Mem0. (2024). *The memory layer for AI agents*. https://github.com/mem0ai/mem0
Microsoft. (2024). *GraphRAG: Unlocking LLM discovery on narrative private data*. https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
Qdrant. (2024). *Hybrid search with sparse vectors*. https://qdrant.tech/documentation/concepts/search/#hybrid-search
Stanford University. (2023). *Lost in the middle: How language models use long contexts*. https://arxiv.org/abs/2307.03172
