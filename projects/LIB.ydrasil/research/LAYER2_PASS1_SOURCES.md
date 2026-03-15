# Layer 2 Pass 1: Kilder og Eksperter

**Genereret:** 2026-02-05
**Formål:** Identificere de bedste kilder, eksperter og communities for hvert research-område

---

## AI/MEMORY KATEGORIER

---

## 1. Vektor-databaser

### Vendors
- **Pinecone** - https://www.pinecone.io - Managed-first, serverless vektor-database. Exceptionel query speed og multi-region support. - *Bias: Promoverer managed løsning over self-hosted*
- **Weaviate** - https://weaviate.io - Open-source med managed option. Stærk hybrid search og modulært design. - *Bias: Fremhæver egen hybrid search som overlegen*
- **Qdrant** - https://qdrant.tech - Open-source, skrevet i Rust. Bedste free tier (1GB forever). Performance-fokuseret. - *Bias: Fokuserer på pris/performance ratio*
- **Milvus/Zilliz** - https://milvus.io - Industrial scale, billion-vector scenarier. Flest indexing strategier (IVF, HNSW, DiskANN). - *Bias: Enterprise-fokus, kompleksitet som feature*
- **Chroma** - https://www.trychroma.com - Developer-friendly, letvægts. God til prototyping. - *Bias: Simplicity over scalability*

### Practitioners
- **Jyoti Dabass, Ph.D.** - Medium - Praktisk sammenligning af vektor-databaser - Kendt for: Detaljerede tekniske sammenligninger
- **Reddit Engineering Team** - Milvus Blog - Valgte mellem Qdrant og Milvus til produktion - Kendt for: Real-world scale evaluation

### Academics
- **"Vector Database: A Systematic Overview"** - Diverse universiteter - Systematisk oversigt over vektor-database teknologier

### Communities
- **r/LocalLLaMA** - Reddit - 615k members, høj aktivitet - Diskuterer vektor-databaser i kontekst af lokale LLMs
- **Qdrant Discord** - Discord - 30,000+ members - Fokus på similarity search og praktisk brug
- **Hacker News** - news.ycombinator.com - Varierende - Kritiske diskussioner om vektor-database trade-offs

### Benchmarks
- **ANN-Benchmarks** - https://ann-benchmarks.com - Måler query speed, accuracy (recall), memory usage - Erik Bernhardsson (creator)
- **VectorDBBench** - Zilliz - Full database benchmarking inkl. database overhead
- **VIBE (Vector Index Benchmark for Embeddings)** - ArXiv 2025 - Moderne embedding datasets

---

## 2. RAG-arkitekturer

### Vendors
- **LlamaIndex** - https://www.llamaindex.ai - RAG framework, production-ready. LlamaParse, LlamaExtract. - *Bias: Kompleksitet kan overkomplicere simple use cases*
- **LangChain** - https://www.langchain.com - Chains, agents, integrations. Stor community. - *Bias: Framework lock-in, kan være bloated for simpel RAG*
- **Haystack (deepset)** - https://haystack.deepset.ai - Production-ready modular pipelines - *Bias: Enterprise-fokus*
- **LangWatch** - https://langwatch.ai - RAG observability og evaluation - *Bias: Sælger monitoring som kritisk*

### Practitioners
- **Jerry Liu** - LlamaIndex CEO - "RAG is a hack, but a powerful one" - Kendt for: Long-context RAG arkitekturer
- **Jason Liu** - jxnl.co, Instructor creator - Systematisk RAG forbedring, strukturerede outputs - Kendt for: 6M+ monthly downloads på Instructor
- **Simon Willison** - simonwillison.net - 23+ års blogging, practical LLM analysis - Kendt for: "World's top AI blogger", Django co-creator
- **Hamel Husain** - hamel.dev - LLM evals, AI product improvement - Kendt for: GitHub erfaring, 700+ engineers trænet i evals

### Academics
- **"RAGBench: Explainable Benchmark for RAG Systems"** - ArXiv - Systematisk RAG evaluation framework
- **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** - Facebook AI Research - Original RAG paper

### Communities
- **LangChain Slack** - slack.langchain.com - Aktiv - Open discussion, job sharing, agent showcases
- **LangChain Forum** - forum.langchain.com - Aktiv - Product support og tekniske spørgsmål
- **r/LangChain** - Reddit - Medium aktivitet - RAG diskussioner og troubleshooting

### Benchmarks
- **RAGAS** - https://docs.ragas.io - Faithfulness, answer relevance, context precision/recall - Open source, widely adopted
- **RAGBench** - ArXiv - Explainable RAG evaluation
- **CRAG, LegalBench-RAG, T²-RAGBench** - Diverse - Domain-specifikke RAG benchmarks

---

## 3. Chunking-strategier

### Vendors
- **Chroma Research** - https://research.trychroma.com - Evaluering af chunking strategier - *Bias: Validerer egen database*
- **Pinecone Learn** - https://www.pinecone.io/learn - Chunking tutorials og best practices - *Bias: Promoverer integration med Pinecone*
- **Amazon Science** - amazon.science - AutoChunker: Structured text chunking - *Bias: AWS/Bedrock integration*

### Practitioners
- **Plaban Nayak** - Medium/AI Forum - Semantic chunking for RAG - Kendt for: Praktiske chunking guides
- **Firecrawl Team** - firecrawl.dev - Best chunking strategies for RAG 2025 - Kendt for: Praktiske sammenligninger

### Academics
- **"Is Semantic Chunking Worth the Computational Cost?"** - ACL NAACL 2025 - Rigorous cost/benefit analyse
- **"Max-Min Semantic Chunking for RAG"** - Discover Computing Journal - Novel chunking algoritme
- **"Comparative Evaluation of Advanced Chunking for RAG in Clinical Decision Support"** - PMC - Healthcare-specifik chunking evaluation

### Communities
- **r/MachineLearning** - Reddit - Høj aktivitet - Akademisk/praktisk chunking diskussioner
- **Hacker News** - Varierende - Kritiske perspektiver på chunking overhead

### Benchmarks
- **Chroma Chunking Benchmark** - Recall across methods (op til 9% variation) - Chroma Research
- **Clinical Chunking Study** - Accuracy (87% adaptive vs 50% baseline) - PMC

---

## 4. Embedding-modeller

### Vendors
- **OpenAI** - https://openai.com - text-embedding-3-large, Matryoshka embeddings - *Bias: Closed source, API dependency*
- **Cohere** - https://cohere.com - embed-v4, MTEB leader (65.2 score) - *Bias: Sælger embedding+rerank combo*
- **Voyage AI** - https://voyageai.com - voyage-3-large (63.8 MTEB) - *Bias: Niche fokus*
- **Google** - Vertex AI - Gemini Embedding, #1 MTEB overall - *Bias: Cloud lock-in*

### Practitioners
- **Nils Reimers** - Sentence Transformers creator - Open source embeddings pioneer - Kendt for: SBERT, Sentence Transformers
- **HuggingFace Team** - huggingface.co - MTEB leaderboard maintainers - Kendt for: Demokratisering af embeddings

### Academics
- **"MTEB: Massive Text Embedding Benchmark"** - HuggingFace - 56 datasets, 8 tasks, 112 languages
- **BGE (BAAI General Embedding)** - Beijing Academy of AI - Open source embedding models
- **E5-Mistral-7B-Instruct** - Microsoft Research - Instruction-tuned embeddings

### Communities
- **HuggingFace Forums** - Høj aktivitet - Model diskussioner og troubleshooting
- **r/LocalLLaMA** - Reddit - Høj aktivitet - Open source embedding diskussioner

### Benchmarks
- **MTEB Leaderboard** - https://huggingface.co/spaces/mteb/leaderboard - 2000+ modeller evalueret - HuggingFace
- **BEIR** - Benchmark for Information Retrieval - Retrieval-specifik evaluation

---

## 5. Re-ranking

### Vendors
- **Cohere** - https://cohere.com/rerank - Rerank 4.0, 32K context, self-learning - *Bias: Sælger som kritisk komponent*
- **Jina AI** - https://jina.ai - Reranker models - *Bias: Integration med eget ecosystem*

### Practitioners
- **Michael Ryaboy** - Medium - Cross-encoders, ColBERT, LLM-based rerankers guide - Kendt for: Praktisk reranker sammenligning
- **ZeroEntropy Team** - zeroentropy.dev - Ultimate guide to reranking 2025 - Kendt for: Comprehensive comparisons

### Academics
- **"ColBERT: Efficient and Effective Passage Search"** - Stanford NLP - Late interaction model
- **"MS MARCO Passage Ranking"** - Microsoft - Reranking benchmark dataset
- **Cross-Encoder Research** - Diverse - MRR@10 > 40 på MS MARCO

### Communities
- **r/MachineLearning** - Reddit - Akademiske diskussioner
- **Hacker News** - Varierende - Praktiske erfaringer

### Benchmarks
- **MS MARCO** - Passage ranking, MRR@10 - Microsoft
- **BEIR** - Diverse retrieval tasks - Evaluerer reranking effekt

---

## 6. Memory Frameworks

### Vendors
- **Letta (MemGPT)** - https://www.letta.com - Self-editing memory, agent framework - *Bias: Promoverer memory som core feature*
- **Mem0** - https://mem0.ai - Scalable long-term memory, graph-based - *Bias: Memory som separate service*
- **LangMem** - LangChain - Long-term memory for LangChain agents - *Bias: Framework lock-in*

### Practitioners
- **Charles Packer** - MemGPT creator - LLMs as Operating Systems - Kendt for: Original MemGPT paper
- **Leonie Monigatti** - leoniemonigatti.com - Memory in AI agents explainers - Kendt for: Tilgængelige forklaringer

### Academics
- **"MemGPT: Towards LLMs as Operating Systems"** - ArXiv 2310.08560 - Foundational memory paper
- **"Memory in the Age of AI Agents: A Survey"** - ArXiv 2512.13564 - Comprehensive survey (Dec 2025)
- **"From Human Memory to AI Memory"** - ArXiv - Human/AI memory paralleller
- **ICLR 2026 Workshop: MemAgents** - Memory for LLM-Based Agentic Systems

### Communities
- **Letta Discord** - Discord - Aktiv - MemGPT/Letta specifik support
- **r/MachineLearning** - Reddit - Akademiske memory diskussioner

### Benchmarks
- **LongBench** - Long-context evaluation
- **Memory-specific evals** - Diverse papers - In-development

---

## 7. Knowledge Management Tools

### Vendors
- **Notion** - https://notion.so - Collaborative workspace, Notion AI - *Bias: Cloud-first, subscription model*
- **Obsidian** - https://obsidian.md - Local-first, Markdown, 1566+ plugins - *Bias: Kræver setup og vedligeholdelse*
- **Roam Research** - https://roamresearch.com - Bi-directional linking pioneer - *Bias: Premium pricing*
- **Logseq** - https://logseq.com - Open source Roam alternative - *Bias: Mindre poleret*

### Practitioners
- **Tiago Forte** - fortelabs.com - Building a Second Brain, PARA method - Kendt for: BASB book, produktivitets-guru
- **Nick Milo** - Linking Your Thinking - Obsidian workflows - Kendt for: LYT framework

### Academics
- **"Building a Second Brain"** - Tiago Forte - Holistic creative process methodology

### Communities
- **Obsidian Forum** - forum.obsidian.md - Høj aktivitet - Plugin diskussioner, PKM workflows
- **r/ObsidianMD** - Reddit - Aktiv - Community support
- **r/PKMS** - Reddit - Medium aktivitet - Generel PKM diskussion

### Benchmarks
- *Ingen formelle benchmarks - subjektiv preference*

---

## 8. Personal AI / Second Brain

### Vendors
- **Second Brain** - https://www.thesecondbrain.io - AI-powered visual board, chat med social media - *Bias: AI-first over structure*
- **Saner.AI** - https://www.saner.ai - AI second brain, auto-organization - *Bias: AI dependency*
- **NotebookLM** - Google - AI notebook with sources - *Bias: Google ecosystem*
- **Reflect Notes** - https://reflect.app - AI-powered networked notes - *Bias: Premium pricing*
- **Mem** - https://mem.ai - AI-powered note organization - *Bias: AI black box*

### Practitioners
- **Tiago Forte** - Building a Second Brain - Pioneer i second brain konceptet - Kendt for: PARA method
- **August Bradley** - YouTube - PPV (Pillars, Pipelines, Vaults) system - Kendt for: Notion mastery

### Academics
- **"AI Native Second Brain"** - Diverse - Emerging research area

### Communities
- **Building a Second Brain Community** - Fortelabs - Høj aktivitet - Tiago Forte's community
- **r/SecondBrain** - Reddit - Medium aktivitet - Generel diskussion

### Benchmarks
- *Ingen formelle benchmarks - brugerspecifik*

---

## 9. Context Window Management

### Vendors
- **Anthropic** - https://anthropic.com - 200K context Claude models - *Bias: Context length som feature*
- **OpenAI** - https://openai.com - 128K GPT-4 Turbo - *Bias: API pricing model*
- **Google** - Gemini 1M+ context - *Bias: Context som differentiator*

### Practitioners
- **JetBrains Research** - blog.jetbrains.com - Efficient context management for LLM agents - Kendt for: Practical research
- **Kuldeep Paul** - Medium - Context engineering for production AI agents - Kendt for: Hands-on guides

### Academics
- **"Titans: Learning to Memorize at Test Time"** - Feb 2025 - Test-time memorization
- **"Infinite Retrieval and Cascading KV Cache"** - Sliding window attention innovations
- **"Memory-Augmented Transformers: A Systematic Review"** - ArXiv - Comprehensive review

### Communities
- **r/MachineLearning** - Reddit - Høj aktivitet - Context length diskussioner
- **Hacker News** - Varierende - Performance vs cost debates

### Benchmarks
- **LongBench** - Long-context evaluation tasks
- **RULER** - Retrieval accuracy i lange kontekster
- **Epoch AI Context Window Analysis** - Tracking context window growth

---

## 10. Hybrid Search

### Vendors
- **Weaviate** - https://weaviate.io - Native hybrid search, fusion algorithms - *Bias: Hybrid som kernefunktion*
- **Elastic** - https://elastic.co - Elasticsearch hybrid capabilities - *Bias: Legacy infrastruktur*
- **OpenSearch** - https://opensearch.org - AWS-backed hybrid search - *Bias: AWS ecosystem*
- **Pinecone** - Sparse-dense hybrid support - *Bias: Managed solution*

### Practitioners
- **Syntal** - Medium - "Hybrid Search That Actually Wins" - Kendt for: 9 real-world hybrid strategies
- **Akash A Desai** - Medium/LanceDB - BM25 + semantic search med LangChain - Kendt for: Praktiske tutorials

### Academics
- **BM25 Algorithm** - Robertson et al. - Foundation for keyword search
- **RRF (Reciprocal Rank Fusion)** - Cormack et al. - Rank fusion method

### Communities
- **Elasticsearch Community** - discuss.elastic.co - Høj aktivitet - Hybrid search implementation
- **Weaviate Community** - Slack/Discord - Aktiv - Hybrid-specifik support

### Benchmarks
- **BEIR** - Retrieval benchmark inkl. hybrid evaluation
- **MS MARCO** - Hybrid retrieval evaluation

---

## 11. Knowledge Graphs

### Vendors
- **Neo4j** - https://neo4j.com - Markedsleder, GraphRAG ecosystem - *Bias: Graph database lock-in*
- **Amazon Neptune** - AWS - Managed graph database - *Bias: AWS ecosystem*
- **TigerGraph** - https://tigergraph.com - Enterprise graph analytics - *Bias: Enterprise fokus*

### Practitioners
- **Tomaz Bratanic** - Neo4j - GraphRAG tutorials og guides - Kendt for: Neo4j + LLM integration
- **LlamaIndex Team** - Knowledge graph agents - Kendt for: Text2Cypher workflows

### Academics
- **"GraphRAG: Unlocking LLM discovery on narrative private data"** - Microsoft Research - Foundation GraphRAG paper
- **"Knowledge Graphs and LLMs"** - Diverse - Integration patterns

### Communities
- **Neo4j Community** - community.neo4j.com - Høj aktivitet - Graph + AI diskussioner
- **r/GraphDB** - Reddit - Medium aktivitet

### Benchmarks
- **FB15k, WN18** - Knowledge graph completion benchmarks
- **GraphRAG-specific evals** - Microsoft - In development

---

## 12. Conversational Memory

### Vendors
- **LangGraph** - LangChain - State management, memory stores - *Bias: LangChain ecosystem*
- **Rasa** - https://rasa.com - Dialogue management - *Bias: Enterprise chatbot fokus*
- **Botpress** - https://botpress.com - Conversational AI platform - *Bias: Low-code fokus*

### Practitioners
- **Nayeem Islam** - Medium - Building AI agents that remember - Kendt for: Practical memory guides
- **JIN** - Medium/AI Monks - OpenAI conversation state management deep dive - Kendt for: Technical analysis

### Academics
- **"Long-Term Dialogue Memory"** - EmergentMind - Survey of approaches
- **SeCom (Segmented Chunks)** - Topical segmentation for conversations
- **SGMem, Mnemosyne** - Graph-based dialogue memory

### Communities
- **Rasa Community** - forum.rasa.com - Aktiv - Dialogue system diskussioner
- **LangChain Slack** - Conversational AI channels

### Benchmarks
- **MultiWOZ** - Multi-domain dialogue benchmark
- **SGD (Schema-Guided Dialogue)** - Google - Dialogue state tracking

---

## 13. Langtids- vs Korttidshukommelse

### Vendors
- **Letta** - Explicit short/long-term memory tiers - *Bias: Arkitekt-kompleksitet*
- **Mem0** - Graph-based long-term memory - *Bias: Separate service model*

### Practitioners
- **Shichun Liu et al.** - GitHub - Agent Memory Paper List maintainers - Kendt for: Comprehensive paper collection
- **MarkTechPost Team** - marktechpost.com - Memory-powered AI guides - Kendt for: Tilgængelige forklaringer

### Academics
- **"Position: Episodic Memory is the Missing Piece for Long-Term LLM Agents"** - ArXiv Feb 2025
- **"Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management"** - Jan 2026
- **"M2PA: Multi-Memory Planning Agent"** - ACL 2025 - Multi-memory for open worlds
- **"MemSearcher"** - End-to-end RL for memory management

### Communities
- **r/MachineLearning** - Reddit - Akademiske diskussioner
- **AI Safety communities** - Diverse - Memory alignment concerns

### Benchmarks
- **Memory evaluation datasets** - In active development
- **Task-specific memory tests** - Per-paper custom evals

---

## 14. Evaluering og Benchmarks

### Vendors
- **Arize AI** - https://arize.com - Phoenix, LLM observability - *Bias: Sælger monitoring platform*
- **Weights & Biases** - https://wandb.ai - ML experiment tracking - *Bias: Platform lock-in*
- **LangSmith** - LangChain - RAG/LLM tracing og evals - *Bias: LangChain ecosystem*
- **Braintrust** - https://braintrust.dev - AI evaluation platform - *Bias: Enterprise fokus*

### Practitioners
- **Hamel Husain** - hamel.dev - LLM Evals definitive guide - Kendt for: "Most knowledgeable about LLM evals"
- **Shreya Shankar** - UC Berkeley - AI evals research og kurser - Kendt for: Academic + practical bridge

### Academics
- **"RAGAS: Automated Evaluation of RAG"** - ArXiv 2309.15217 - Foundation eval framework
- **"RAGBench"** - ArXiv 2407.11005 - Explainable RAG benchmark

### Communities
- **Eval-focused Discord servers** - Diverse - Praktisk eval diskussion
- **r/MachineLearning** - Reddit - Benchmark kritik og forslag

### Benchmarks
- **RAGAS** - https://docs.ragas.io - Faithfulness, relevance, context metrics - Open source standard
- **ARES** - Automated RAG Evaluation System
- **MTEB** - Embedding evaluation
- **LangSmith Evals** - Integrated RAG evaluation

---

## 15. Anti-patterns og Failure Modes

### Vendors
- **Snorkel AI** - https://snorkel.ai - RAG failure modes documentation - *Bias: Sælger data-centric løsning*
- **vFunction** - https://vfunction.com - Technical debt + RAG complexity - *Bias: Modernization services*

### Practitioners
- **Bhagya Rana** - Medium - "10 RAG Failure Modes at Scale" - Kendt for: Production experience
- **Skylar Payne** - jxnl.co feature - "RAG Mistakes That Are Killing Your AI" - Kendt for: Brutally honest assessment
- **Kuldeep Paul** - DEV Community - "Ten Failure Modes Nobody Talks About" - Kendt for: Detection strategies

### Academics
- **Analytics Vidhya Research** - "Silent Killers of Production RAG" - 80% enterprise RAG failures framework

### Communities
- **r/MachineLearning** - Reddit - Failure case sharing
- **Hacker News** - Ærlige postmortems og kritik

### Benchmarks
- **Failure detection metrics** - Custom per-organization
- **Error taxonomy frameworks** - Analytics Vidhya 5-part framework

---

## SOFTWARE ENGINEERING KATEGORIER

---

## 16. Design Principper

### Vendors
- **Clean Coders** - https://cleancoders.com - Uncle Bob's training platform - *Bias: Dogmatisk tilgang*
- **O'Reilly** - https://www.oreilly.com - Software design books og kurser - *Bias: Traditionel publicering*

### Practitioners
- **Robert C. Martin (Uncle Bob)** - cleancoders.com - SOLID principles, Clean Code - Kendt for: Clean Code bogen, Clean Architecture
- **Martin Fowler** - martinfowler.com - Refactoring, design patterns - Kendt for: Refactoring book, Enterprise Patterns

### Academics
- **"Clean Code: A Handbook of Agile Software Craftsmanship, 2nd Edition"** - Robert Martin 2025 - Opdateret klassiker
- **"Design Patterns: Elements of Reusable Object-Oriented Software"** - Gang of Four - Foundation

### Communities
- **r/programming** - Reddit - Høj aktivitet - Design diskussioner
- **r/softwareengineering** - Reddit - Aktiv - Arkitektur og design
- **Hacker News** - Kritiske perspektiver på design dogmer

### Benchmarks
- **Code quality metrics** - Cyclomatic complexity, coupling, cohesion
- **SOLID adherence** - Static analysis tools

---

## 17. Arkitekturmønstre

### Vendors
- **Confluent** - https://confluent.io - Event-driven architecture, Kafka - *Bias: Kafka-centrisk*
- **AWS** - Well-Architected Framework - *Bias: AWS services*
- **Microsoft** - Azure Architecture Center - *Bias: Azure services*

### Practitioners
- **Chris Richardson** - microservices.io - Microservices Patterns creator - Kendt for: Pattern language for microservices
- **Sam Newman** - Building Microservices author - Kendt for: Practical microservices guidance

### Academics
- **"Software Architecture: Perspectives on an Emerging Discipline"** - Shaw & Garlan - Foundation text
- **Event-Driven Architecture patterns** - Diverse research - CQRS, Event Sourcing

### Communities
- **r/softwarearchitecture** - Reddit - Aktiv - Arkitektur diskussioner
- **InfoQ** - https://infoq.com - Høj kvalitet - Arkitektur artikler og talks
- **DDD Community** - Domain-Driven Design practitioners

### Benchmarks
- **Architecture fitness functions** - Evolutionary architecture metrics
- **System quality attributes** - Performance, scalability, maintainability

---

## 18. Planlægning og Estimering

### Vendors
- **Atlassian** - https://atlassian.com - Jira, agile tools - *Bias: Tool-centric estimering*
- **Asana** - https://asana.com - Project management - *Bias: Workflow lock-in*
- **Mountain Goat Software** - mountaingoatsoftware.com - Agile training - *Bias: Certificerings-fokus*

### Practitioners
- **Mike Cohn** - Mountain Goat Software - Story points popularizer - Kendt for: "Agile Estimating and Planning" book
- **Ron Jeffries** - ronjeffries.com - XP co-founder - Kendt for: Agile kritik og guidance

### Academics
- **"Agile Estimating and Planning"** - Mike Cohn - Definitive guide
- **"The Mythical Man-Month"** - Fred Brooks - Classic estimation wisdom

### Communities
- **r/agile** - Reddit - Aktiv - Estimation debatter
- **Scrum.org Community** - Scrum diskussioner
- **Atlassian Community** - Agile praktikere

### Benchmarks
- **Velocity tracking** - Team-specifik
- **Estimation accuracy** - Historical comparison

---

## 19. Testing Strategier

### Vendors
- **JetBrains** - https://jetbrains.com - Testing tools i IDEs - *Bias: IDE-integration*
- **Postman** - https://postman.com - API testing - *Bias: API-centrisk*
- **Cypress** - https://cypress.io - E2E testing - *Bias: Frontend fokus*

### Practitioners
- **Kent Beck** - TDD pioneer - Test-Driven Development creator - Kendt for: TDD by Example, XP
- **Martin Fowler** - Testing pyramid - Kendt for: Test kategorisering og strategi
- **Dan North** - BDD creator - Kendt for: Behavior-Driven Development

### Academics
- **"Test-Driven Development: By Example"** - Kent Beck - 20th anniversary edition 2025
- **"xUnit Test Patterns"** - Gerard Meszaros - Comprehensive testing patterns

### Communities
- **r/programming** - Reddit - Testing diskussioner
- **Ministry of Testing** - ministryoftesting.com - Testing community

### Benchmarks
- **Code coverage** - Line, branch, path coverage
- **Mutation testing** - Test quality metrics

---

## 20. Solo Developer Strategier

### Vendors
- **Indie Hackers** - https://indiehackers.com - Solo founder community - *Bias: Success story fokus*
- **MicroConf** - microconf.com - Bootstrap SaaS community - *Bias: SaaS-centrisk*

### Practitioners
- **Pieter Levels** - levels.io - Nomad List, Photo AI creator - Kendt for: $2.5M ARR solo, "ship fast"
- **Marc Lou** - marclou.com - Ship Fast creator - Kendt for: Rapid prototyping
- **Tony Dinh** - tonydinh.com - TypingMind, BlackMagic - Kendt for: Solo app portfolio

### Academics
- **"The Mom Test"** - Rob Fitzpatrick - Customer research for founders
- **"Start Small, Stay Small"** - Rob Walling - Developer entrepreneurship

### Communities
- **Indie Hackers** - indiehackers.com - Høj aktivitet - Revenue sharing, building in public
- **r/SideProject** - Reddit - Aktiv - Solo project diskussioner
- **r/startups** - Reddit - Høj aktivitet - Founder diskussioner

### Benchmarks
- **MRR (Monthly Recurring Revenue)** - Standard SaaS metric
- **Time to first dollar** - Solo founder milestone

---

## 21. Teknisk Gæld

### Vendors
- **SonarQube** - https://sonarqube.org - Code quality og tech debt tracking - *Bias: Metric-drevet*
- **CodeScene** - https://codescene.com - Behavioral code analysis - *Bias: Behavioral metrics*
- **Stepsize** - https://stepsize.com - Tech debt management - *Bias: Process-fokus*

### Practitioners
- **Martin Fowler** - martinfowler.com - Technical Debt Quadrant - Kendt for: Deliberate/inadvertent framework
- **Ward Cunningham** - Original "technical debt" metaphor creator - Kendt for: Wiki inventor, debt metaphor

### Academics
- **"Managing Technical Debt"** - Kruchten et al. - Comprehensive academic treatment
- **Technical Debt Quadrant** - Martin Fowler - Klassifikations-framework

### Communities
- **r/ExperiencedDevs** - Reddit - Aktiv - Senior dev perspektiver
- **r/softwareengineering** - Reddit - Tech debt diskussioner

### Benchmarks
- **SQALE** - Software Quality Assessment based on Lifecycle Expectations
- **Technical debt ratio** - Debt vs development time

---

## 22. Refactoring

### Vendors
- **JetBrains** - Refactoring tools i IntelliJ, PyCharm etc. - *Bias: IDE-lock-in*
- **Microsoft** - Visual Studio refactoring - *Bias: .NET fokus*

### Practitioners
- **Martin Fowler** - martinfowler.com - Refactoring catalog - Kendt for: "Refactoring" book, pattern catalog
- **Michael Feathers** - Working Effectively with Legacy Code - Kendt for: Legacy code techniques
- **Kent Beck** - Refactoring som TDD del - Kendt for: Red-Green-Refactor

### Academics
- **"Refactoring: Improving the Design of Existing Code"** - Martin Fowler - Definitive reference
- **"Working Effectively with Legacy Code"** - Michael Feathers - Legacy code Bible
- **"Brutal Refactoring"** - Michael Feathers - Upcoming (system-wide refactoring)

### Communities
- **r/programming** - Reddit - Refactoring diskussioner
- **Refactoring.com** - Martin Fowler - Catalog og ressourcer

### Benchmarks
- **Refactoring metrics** - Coupling reduction, complexity reduction
- **Test coverage pre/post** - Refactoring safety

---

## 23. Documentation

### Vendors
- **GitBook** - https://gitbook.com - Documentation platform - *Bias: Hosted løsning*
- **ReadTheDocs** - https://readthedocs.org - Open source docs hosting - *Bias: Sphinx-fokus*
- **Notion** - Documentation i workspace - *Bias: General purpose*

### Practitioners
- **Write the Docs Community** - writethedocs.org - Documentation practitioners - Kendt for: Conferences, Slack, best practices
- **Tom Johnson** - idratherbewriting.com - Technical writing blog - Kendt for: API documentation expertise

### Academics
- **"Docs as Code"** - Write the Docs - Methodology guide
- **Google Technical Writing** - developers.google.com - Free courses

### Communities
- **Write the Docs** - writethedocs.org - Høj aktivitet - Slack, meetups, conferences
- **r/technicalwriting** - Reddit - Aktiv - Tech writer community

### Benchmarks
- **Documentation coverage** - API docs completeness
- **Readability scores** - Flesch-Kincaid etc.

---

## DATA ENGINEERING KATEGORIER

---

## 24. Data Lineage og Mapping

### Vendors
- **Atlan** - https://atlan.com - Leader i Gartner Magic Quadrant 2025 - *Bias: Enterprise pricing*
- **Monte Carlo** - https://montecarlodata.com - Data observability - *Bias: Observability som primær feature*
- **dbt** - https://getdbt.com - Transformation + lineage - *Bias: SQL-centrisk*
- **Datafold** - https://datafold.com - Data diff og lineage - *Bias: CI/CD fokus*
- **Secoda** - https://secoda.co - Data catalog og lineage - *Bias: Simplicity*

### Practitioners
- **Tristan Handy** - dbt Labs CEO - Data transformation pioneer - Kendt for: Analytics engineering movement
- **Chad Sanderson** - Data contracts advocate - Kendt for: Data contracts methodology

### Academics
- **Gartner Research** - Data lineage market analysis - Critical capabilities assessment

### Communities
- **dbt Community** - community.getdbt.com - Høj aktivitet - Slack, forum
- **r/dataengineering** - Reddit - Aktiv - Lineage diskussioner

### Benchmarks
- **Gartner Critical Capabilities** - Vendor comparison
- **Lineage accuracy metrics** - Automated vs manual

---

## 25. Schema Design

### Vendors
- **DbSchema** - https://dbschema.com - Visual database design - *Bias: Tool-fokus*
- **Devart** - https://devart.com - Database tools - *Bias: Multi-DB kompleksitet*
- **Bytebase** - https://bytebase.com - Schema change management - *Bias: GitOps approach*

### Practitioners
- **Joe Celko** - SQL author - Advanced SQL og schema design - Kendt for: "SQL for Smarties" series
- **Markus Winand** - use-the-index-luke.com - SQL performance - Kendt for: Index design expertise

### Academics
- **Database normalization theory** - Codd et al. - 1NF-5NF foundations
- **Dimensional modeling** - Ralph Kimball - Data warehouse design

### Communities
- **r/Database** - Reddit - Medium aktivitet - Schema diskussioner
- **dba.stackexchange.com** - Stack Exchange - Høj kvalitet - DBA expertise

### Benchmarks
- **Normalization levels** - 1NF through 5NF compliance
- **Query performance** - Schema efficiency metrics

---

## 26. Data Quality

### Vendors
- **Great Expectations** - https://greatexpectations.io - Open source data validation - *Bias: Python-centrisk*
- **Soda** - https://soda.io - Data quality monitoring - *Bias: SodaCL YAML simplicity*
- **Monte Carlo** - Data observability platform - *Bias: Anomaly detection fokus*
- **Deequ** - Amazon/Spark - Data quality for Spark - *Bias: Spark ecosystem*

### Practitioners
- **Abe Gong** - Great Expectations founder - Data quality pioneer - Kendt for: GX framework
- **Maarten Masschelein** - Soda founder - Data quality accessibility - Kendt for: SodaCL approach
- **DataKitchen Team** - datakitchen.io - DataOps methodology - Kendt for: Data quality automation

### Academics
- **"Data Quality Assessment"** - Diverse academic work - DQ dimensions framework

### Communities
- **Great Expectations Slack** - Aktiv - GX support
- **r/dataengineering** - Reddit - Data quality diskussioner

### Benchmarks
- **Data quality dimensions** - Accuracy, completeness, consistency, timeliness
- **DQ score frameworks** - Custom per organization

---

## 27. ETL/ELT Pipelines

### Vendors
- **Apache Airflow** - https://airflow.apache.org - De facto standard orchestrator - *Bias: Complexity for simple use cases*
- **Dagster** - https://dagster.io - Asset-centric orchestration - *Bias: Ny paradigme learning curve*
- **Prefect** - https://prefect.io - Python-first orchestration - *Bias: Flexibility over structure*
- **Airbyte** - https://airbyte.com - Open source EL(T) - *Bias: Connector fokus*
- **Fivetran** - https://fivetran.com - Managed ELT - *Bias: Premium pricing*

### Practitioners
- **Maxime Beauchemin** - Airflow creator - Orchestration pioneer - Kendt for: Created Airflow at Airbnb
- **Dagster Team** - dagster.io - Software-defined assets - Kendt for: Asset-centric approach
- **Jeremiah Lowin** - Prefect CEO - Workflow orchestration - Kendt for: Prefect/Marvin

### Academics
- **"Fundamentals of Data Engineering"** - Joe Reis & Matt Housley - Comprehensive guide
- **DataOps methodology** - Diverse - Process framework

### Communities
- **Apache Airflow Slack** - Høj aktivitet - Airflow support
- **Dagster Slack** - Aktiv - Dagster community
- **r/dataengineering** - Reddit - Orchestration diskussioner

### Benchmarks
- **Pipeline reliability** - Success rate, MTTR
- **Orchestrator comparison** - Feature matrices

---

## TVÆRGÅENDE RESSOURCER

---

## Top Practitioners at Følge

| Navn | Platform | Fokusområde |
|------|----------|-------------|
| Simon Willison | simonwillison.net, Twitter | LLM praktisk brug, Django |
| Hamel Husain | hamel.dev | LLM evals, AI produkter |
| Jason Liu | jxnl.co | RAG, strukturerede outputs |
| Jerry Liu | LlamaIndex | RAG arkitekturer |
| Eugene Yan | eugeneyan.com | ML systems, recommendations |
| Chip Huyen | huyenchip.com | ML systems design |
| Lilian Weng | lilianweng.github.io | AI research (ex-OpenAI) |
| Martin Fowler | martinfowler.com | Software design, refactoring |

---

## Top Communities

| Community | Platform | Aktivitet | Fokus |
|-----------|----------|-----------|-------|
| r/LocalLLaMA | Reddit | 615k members | Open source LLMs |
| r/MachineLearning | Reddit | 3M+ members | ML generelt |
| r/dataengineering | Reddit | 300k+ members | Data pipelines |
| LangChain Slack | Slack | Høj | RAG, agents |
| Qdrant Discord | Discord | 30k+ | Vector search |
| Write the Docs | Slack + Conf | Aktiv | Documentation |
| Indie Hackers | Web | Høj | Solo founders |
| Hacker News | news.ycombinator.com | Ekstrem høj | Tech generelt |

---

## Top Benchmarks

| Benchmark | Måler | Maintainer |
|-----------|-------|------------|
| MTEB | Embedding kvalitet | HuggingFace |
| ANN-Benchmarks | Vector search performance | Erik Bernhardsson |
| RAGAS | RAG system kvalitet | Open source |
| MS MARCO | Retrieval/reranking | Microsoft |
| BEIR | Information retrieval | Diverse |
| LongBench | Long-context performance | Diverse |

---

## Næste Skridt

**Layer 2 Pass 2 bør:**
1. Dykke dybere ned i specifikke vendors' dokumentation
2. Læse nøglepapers identificeret her
3. Gennemgå practitioner blogs for konkrete implementeringsdetaljer
4. Deltage i relevante communities for real-time insights
5. Køre benchmarks på vores specifikke use case

**Prioriterede kilder at starte med:**
1. Simon Willisons blog (praktisk LLM brug)
2. Hamel Husains eval guides (kvalitetssikring)
3. LlamaIndex docs (RAG implementation)
4. Qdrant docs + Discord (vores vector DB)
5. RAGAS documentation (eval setup)
