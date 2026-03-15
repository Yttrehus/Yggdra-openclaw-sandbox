# Layer 2 Pass 2: Kildeverificering og Prioritering

**Genereret:** 2026-02-05
**Formål:** Verificere troværdighed, identificere bias, og prioritere kilder fra Pass 1

---

## METODOLOGI

Hver kilde er evalueret på:
1. **Track Record** - Hvor længe aktiv? Hvad har de bygget/publiceret?
2. **Citationsnetværk** - Hvem citerer hvem? Hub eller spoke?
3. **Bias-analyse** - Vendor bias, practitioner bias, funding?
4. **Konsensus vs. Kontrovers** - Etableret sandhed eller debatteret?
5. **Relevans for Ydrasil** - Høj/Medium/Lav baseret på vores setup (solo dev, Qdrant, Claude, dansk)

---

## AI/MEMORY KATEGORIER

---

## 1. Vektor-databaser

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **ANN-Benchmarks** (Erik Bernhardsson) | Skabt 2018, akademisk publiceret i Information Systems 2019. Erik byggede Spotify's anbefalingssystem med Annoy. | Lav - uafhængig, open source benchmark | **Høj** |
| **r/LocalLLaMA** | 615k members, ekstrem høj aktivitet | Lav - community-drevet, mange perspektiver | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Qdrant** | Rust-baseret, aktiv udvikling, SOC 2 Type II certificeret | **Medium** - promoverer egen pris/performance ratio | **Høj** |
| **Jyoti Dabass, Ph.D.** | Praktiske sammenligninger på Medium | Lav - uafhængig practitioner | Medium |
| **Hacker News** | Kritiske diskussioner, ærlige postmortems | Lav - community | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Pinecone** | Markedsleder, managed-first | **Høj** - sælger managed løsning, benchmarks favoriserer dem selv | Lav |
| **Weaviate** | Stærk hybrid search | **Høj** - fremhæver hybrid som overlegen, resource-krævende >50M vectors | Lav |
| **Milvus/Zilliz** | Industrial scale | **Høj** - enterprise-fokus, VectorDBBench er deres eget | Lav |
| **Chroma** | Developer-friendly | **Medium** - simplicity over scalability | Medium |

### Konsensus i feltet
- HNSW er den dominerende indexeringsmetode for de fleste use cases
- Hybrid search (vektor + keyword) giver bedre resultater end ren vektor
- Self-hosted vs managed er et trade-off mellem kontrol og convenience

### Kontroversielle punkter
- **Benchmark-krigen:** Hver vendor hævder at være hurtigst. ANN-Benchmarks viser at "vendor benchmarks kan være vildledende" og "afhænger af workload characteristics"
- **Throughput vs latency:** Qdrant har bedre latency (48% bedre p99), men PostgreSQL+pgvectorscale har 11.4x højere throughput
- **Skalering:** Weaviate kræver mere memory >100M vectors, Qdrant's horizontal scaling "still evolving"

### Anbefaling til Ydrasil
**Primær:** ANN-Benchmarks for objektiv performance-sammenligning. **Sekundær:** Qdrant dokumentation (vi bruger det), r/LocalLLaMA for real-world erfaringer. **Undgå:** Vendor benchmarks - de favoriserer altid sig selv.

---

## 2. RAG-arkitekturer

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Simon Willison** | 23+ års blogging, Django co-creator, Andrej Karpathy kalder ham "go-to source" | Lav - uafhængig, kritisk, praktisk fokus | **Høj** |
| **Hamel Husain** | 20+ års ML erfaring, Airbnb/GitHub, trænet 2000+ engineers inkl. OpenAI/Anthropic teams | Lav - konsulent, men O'Reilly bog bekræfter uafhængighed | **Høj** |
| **Jason Liu (jxnl)** | Instructor har 6M+ monthly downloads, citeret af OpenAI som inspiration | **Medium** - sælger kurser på Maven | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Jerry Liu** (LlamaIndex) | Forbes 30 under 30, Uber ATG/Robust Intelligence baggrund | **Høj** - CEO af RAG framework company | Medium |
| **Facebook AI Research** | Original RAG paper (2020) | Lav - akademisk | Medium |
| **Haystack (deepset)** | Production-ready pipelines | **Medium** - enterprise-fokus | Lav |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **LangChain** | Stor community, men massiv kritik | **Høj** - framework lock-in, 1+ sekund latency overhead, "dependency hell" | Lav |
| **LlamaIndex** | Dominerende RAG framework | **Høj** - kompleksitet kan overkomplicere simple use cases | Medium |

### Konsensus i feltet
- RAG er "a hack, but a powerful one" (Jerry Liu's egne ord)
- Retrieval kvalitet er vigtigere end LLM valg
- Simple RAG pipelines slår ofte komplekse for de fleste use cases

### Kontroversielle punkter
- **LangChain vs. direkte API calls:** Stærk kritik: "architectural lock-in", "bloated", teams brugte "months on rewrites to untangle"
- **Framework vs. no-framework:** Jason Liu og Simon Willison foretrækker minimale abstraktioner
- **Long-context vs. RAG:** Debat om hvorvidt 200K+ context windows gør RAG overflødig (konsensus: nej, RAG stadig nødvendig for freshness og scale)

### Anbefaling til Ydrasil
**Primær:** Simon Willison's blog (praktisk, kritisk), Hamel Husain (evals). **Sekundær:** Jason Liu for strukturerede outputs. **Undgå:** LangChain - for kompleks til solo dev setup, overhead ikke værd for vores scale.

---

## 3. Chunking-strategier

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **ACL NAACL 2025 paper** ("Is Semantic Chunking Worth the Cost?") | Peer-reviewed akademisk | Lav - rigorous cost/benefit analyse | **Høj** |
| **Chroma Research** | Recall benchmarks (op til 9% variation) | **Medium** - validerer egen database | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Firecrawl Team** | Praktiske sammenligninger 2025 | Lav - practitioner fokus | **Høj** |
| **PMC Clinical Chunking Study** | 87% adaptive vs 50% baseline | Lav - peer-reviewed | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Pinecone Learn** | Tutorials | **Høj** - promoverer Pinecone integration | Lav |
| **Amazon Science** | AutoChunker | **Høj** - AWS/Bedrock fokus | Lav |

### Konsensus i feltet
- RecursiveCharacterTextSplitter med 400-512 tokens er "solid default" (85-90% recall)
- Semantic chunking kan forbedre recall op til 9%, men med computational overhead
- "When documents are small, focused, chunking can hurt retrieval"

### Kontroversielle punkter
- **Semantic vs. fixed-size:** Semantic giver 70% accuracy boost i tests, men kræver embedding per sætning
- **Cost vs. benefit:** Er 9% recall-forbedring de ekstra API calls værd?
- **Chunk size:** 400-512 vs. 1000+ tokens - ingen definitiv konsensus

### Anbefaling til Ydrasil
**Primær:** Start med RecursiveCharacterTextSplitter (400-512 tokens). **Test:** Semantic chunking kun hvis baseline performance er utilstrækkelig. **Husk:** Vores dokumenter er ofte korte - chunking kan faktisk skade.

---

## 4. Embedding-modeller

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **MTEB Leaderboard** (HuggingFace) | 2000+ modeller, standardiseret benchmark | **Medium** - se limitations nedenfor | **Høj** |
| **Nils Reimers** (Sentence Transformers) | SBERT paper 2019, 5.2.2 release jan 2026, open source | Lav - akademisk + open source | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **BGE (BAAI)** | Open source, stærke MTEB scores | Lav - akademisk | **Høj** |
| **r/LocalLLaMA** | Praktiske diskussioner | Lav - community | **Høj** |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **OpenAI** | text-embedding-3-large | **Høj** - closed source, API dependency, pricing | Medium |
| **Cohere** | embed-v4, MTEB leader | **Høj** - sælger embedding+rerank combo | Lav |
| **Google** | Gemini Embedding | **Høj** - cloud lock-in | Lav |

### Konsensus i feltet
- Open source modeller (BGE, E5) er nu konkurrencedygtige med closed-source
- Dimensionalitet trade-off: 1536d vs 768d - minimal forskel i retrieval quality
- Multilingual modeller kræver specifik evaluering

### Kontroversielle punkter
- **MTEB limitations:** "Over-representation af STS og retrieval", "models train on benchmark tasks", "bias not addressed"
- **Top model differences:** "May not be statistically significant"
- **Open vs. closed:** Cost vs. convenience trade-off

### Anbefaling til Ydrasil
**Primær:** Sentence Transformers / BGE for open source. **Sekundær:** OpenAI embeddings hvis budget tillader. **Husk:** Test på dansk tekst specifikt - MTEB er primært engelsk.

---

## 5. Re-ranking

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **MS MARCO** (Microsoft) | Standard benchmark dataset | Lav - akademisk | Medium |
| **ColBERT paper** (Stanford NLP) | Late interaction model, peer-reviewed | Lav - akademisk | Medium |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **ZeroEntropy Team** | Comprehensive 2025 guide | Lav - practitioner | **Høj** |
| **Michael Ryaboy** | Praktisk sammenligning | Lav - practitioner | **Høj** |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Cohere Rerank** | 4.0 release, stærk performance | **Høj** - sælger reranking som "kritisk komponent", $2/1000 søgninger | Medium |
| **Jina AI** | Open-weight rerankers | **Medium** - eget ecosystem | Medium |

### Konsensus i feltet
- Reranking forbedrer retrieval kvalitet signifikant (MRR@10 > 40)
- Cross-encoders slår bi-encoders til reranking
- Cost/latency trade-off er reel

### Kontroversielle punkter
- **Nødvendighed:** Er reranking nødvendig for små datasæt?
- **LLM-based vs. dedicated:** LLM-as-reranker vs. specialized models
- **Cost-benefit:** Ekstra latency + cost vs. accuracy gain

### Anbefaling til Ydrasil
**Vurdering:** For vores scale (< 100K dokumenter) er reranking sandsynligvis overkill. **Hvis nødvendigt:** Start med open source cross-encoder før Cohere.

---

## 6. Memory Frameworks

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Charles Packer / Letta (MemGPT)** | UC Berkeley PhD, Ion Stoica advisor, $10M funding, backed by Jeff Dean/Clem Delangue | **Medium** - CEO af memory startup | **Høj** |
| **"Memory in the Age of AI Agents" survey** (Dec 2025) | Comprehensive akademisk survey | Lav - akademisk | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Leonie Monigatti** | Tilgængelige forklaringer | Lav - educator | **Høj** |
| **ICLR 2026 MemAgents Workshop** | Akademisk | Lav | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Mem0** | Graph-based memory | **Høj** - memory som separate service | Medium |
| **LangMem** | LangChain integration | **Høj** - framework lock-in | Lav |

### Konsensus i feltet
- Explicit memory management slår pure context-stuffing for lange samtaler
- Episodic memory er "missing piece" for long-term agents (Feb 2025 paper)
- Memory evaluation benchmarks er stadig "in development"

### Kontroversielle punkter
- **Kompleksitet vs. værdi:** Er memory frameworks overkill for de fleste use cases?
- **Memory architecture:** Explicit tiers vs. unified memory
- **Evaluation:** Ingen standardiserede benchmarks endnu

### Anbefaling til Ydrasil
**Primær:** MemGPT/Letta koncepter - akademisk solid, praktisk relevant. **Approach:** Implementer simple memory patterns først, undgå framework lock-in. **Husk:** Vores Qdrant setup giver allerede persistence.

---

## 7. Knowledge Management Tools

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Obsidian** | Local-first, Markdown, 1566+ plugins, aktiv udvikling 2025-2026 | Lav - fremhæver local-first | **Høj** |
| **Obsidian Forum/r/ObsidianMD** | Aktiv community | Lav - user-driven | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Notion** | All-in-one, Notion 3.0 sept 2025, offline mode aug 2025 | **Medium** - cloud-first, subscription | Medium |
| **Logseq** | Open source Roam alternative | Lav - men "mindre poleret" | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Roam Research** | Bi-directional linking pioneer | **Høj** - premium pricing ($15/mo) | Lav |

### Konsensus i feltet
- Obsidian for personal knowledge management (PKM)
- Notion for team collaboration
- "Many power users use both" - Obsidian for thinking, Notion for sharing

### Kontroversielle punkter
- **Local vs. cloud:** Privacy vs. collaboration trade-off
- **Learning curve:** Obsidian kræver Markdown kendskab
- **Plugin ecosystem:** Styrke men også maintenance-burden

### Anbefaling til Ydrasil
**Primær:** Obsidian - local-first, Markdown (vi bruger allerede .md filer), gratis. **Undgå:** Cloud-first tools for vores use case.

---

## 8. Personal AI / Second Brain

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Tiago Forte** (Building a Second Brain) | BASB book, PARA method, stort community | **Medium** - sælger kurser, "project-based bias" | Medium |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **August Bradley** (PPV) | YouTube, Notion mastery | **Medium** - Notion-fokuseret | Lav |
| **Building a Second Brain Community** | Aktiv | **Medium** - Tiago's ecosystem | Lav |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Second Brain (thesecondbrain.io)** | AI-powered | **Høj** - AI-first over structure | Lav |
| **Saner.AI** | Auto-organization | **Høj** - AI dependency, "black box" | Lav |
| **NotebookLM** | Google | **Høj** - Google ecosystem lock-in | Lav |

### Konsensus i feltet
- PARA (Projects, Areas, Resources, Archive) er udbredt framework
- "Second Brain" konceptet er mainstream, men implementeringer varierer
- AI-enhanced note-taking er i tidlig fase

### Kontroversielle punkter
- **BASB kritik:** "Project-based bias doesn't fit everyone", "too many examples, too few actionable tips"
- **Filosofisk kritik:** Feyerabend's "Against the Method" - discoveries happen contingently, not systematically
- **AI assistance:** Hjælper AI virkelig, eller skaber det dependency?

### Anbefaling til Ydrasil
**Primær:** PARA principper er nyttige, men tilpas til vores setup. **Undgå:** AI-first tools der gemmer data i cloud. **Husk:** Vi har allerede /data/, /docs/, /research/, /archive/ - det er i sig selv et second brain system.

---

## 9. Context Window Management

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **LongBench** | Long-context evaluation benchmark | Lav - akademisk | **Høj** |
| **JetBrains Research** | Efficient context management for agents | Lav - praktisk research | **Høj** |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **"Titans" paper** (Feb 2025) | Test-time memorization | Lav - akademisk | Medium |
| **RULER benchmark** | Retrieval accuracy i lange kontekster | Lav - akademisk | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Anthropic** | 200K context | **Høj** - context length som salgsargument | **Høj** (vi bruger Claude) |
| **OpenAI** | 128K GPT-4 Turbo | **Høj** - API pricing model | Medium |
| **Google** | 1M+ Gemini context | **Høj** - context som differentiator | Lav |

### Konsensus i feltet
- Længere context ≠ bedre performance (recall drops i midten af lange kontekster)
- "Lost in the middle" problem er dokumenteret
- RAG + long context er komplementære, ikke konkurrerende

### Kontroversielle punkter
- **Pris vs. RAG:** Fylder man context = høje costs, RAG = infra kompleksitet
- **"Needle in haystack":** Syntetiske tests vs. real-world performance
- **200K vs. RAG:** Debat om hvornår long context erstatter RAG

### Anbefaling til Ydrasil
**Primær:** Claude's 200K context er vores styrke - brug det strategisk. **Kombiner:** RAG for persistence + context for reasoning. **Undgå:** At fylde context blindt - prioritér relevant information.

---

## 10-15. Øvrige AI/Memory kategorier

### Hybrid Search, Knowledge Graphs, Conversational Memory, Langtids- vs Korttidshukommelse, Evaluering, Anti-patterns

**Samlet vurdering:**

| Kategori | Tier 1 Kilder | Hovedanbefaling |
|----------|--------------|-----------------|
| **Hybrid Search** | BM25 (Robertson), RRF (Cormack) - akademisk | Qdrant/Weaviate docs for implementation |
| **Knowledge Graphs** | GraphRAG (Microsoft Research) | "Poor quality on technical reports" - brug med forsigtighed |
| **Conversational Memory** | MultiWOZ, SGD benchmarks | LangGraph kun hvis nødvendigt |
| **Memory tiers** | "Position: Episodic Memory" paper (Feb 2025) | Simple tiers først, kompleksitet senere |
| **Evaluering** | RAGAS + Hamel Husain | RAGAS har bias fra LLM-as-judge |
| **Anti-patterns** | Hacker News postmortems | "80% enterprise RAG failures" - lær fra fejl |

---

## SOFTWARE ENGINEERING KATEGORIER

---

## 16. Design Principper

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Martin Fowler** | 30+ års erfaring, Refactoring book, aktiv blogging 2025-2026, skriver om LLM patterns | Lav - uafhængig thought leader | **Høj** |
| **Gang of Four** (Design Patterns) | Foundation siden 1994 | Lav - klassisk | Medium |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Kent Beck** | TDD pioneer, XP co-founder, stadig aktiv podcast jun 2025 | **Medium** - TDD advocacy | **Høj** |
| **r/programming, r/softwareengineering** | Community diskussioner | Lav | Medium |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Robert C. Martin (Uncle Bob)** | Clean Code, SOLID | **Høj** - "dogmatisk", "kontroversiel personlig adfærd", performance-kritik fra Casey Muratori | Medium |
| **Clean Coders platform** | Training | **Høj** - sælger kurser | Lav |

### Konsensus i feltet
- SOLID principper er udbredte men ikke dogmatiske
- "Refactor early and often" - bred konsensus
- TDD er "fallen out of favor" men stadig værdifuldt i kontekst

### Kontroversielle punkter
- **Clean Code kritik:** John Ousterhout (A Philosophy of Software Design) har "big differences of opinion" med Uncle Bob
- **Uncle Bob personligt:** "Planning to sue conference organizers", "sexist remarks" ifølge kritikere
- **TDD:** "Is TDD Dead?" debat fortsætter - Beck selv siger "TDD alone is not enough for excellent design"

### Anbefaling til Ydrasil
**Primær:** Martin Fowler - aktiv, nuanceret, skriver om LLM. **Sekundær:** Kent Beck for TDD koncepter. **Med forsigtighed:** Uncle Bob - tag principper, ignorer dogmatisme.

---

## 17. Arkitekturmønstre

### Tier 1 (Mest troværdige)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **InfoQ** | Høj kvalitet arkitektur artikler og talks | Lav - journalistisk | **Høj** |
| **Chris Richardson** (microservices.io) | Microservices Patterns creator | Lav - educator | Medium |

### Tier 2 (Troværdige med forbehold)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **Sam Newman** | Building Microservices | Lav - praktisk | Medium |
| **DDD Community** | Domain-Driven Design | Lav - methodology fokus | Lav |

### Tier 3 (Brug med forsigtighed)

| Kilde | Track Record | Bias | Relevans |
|-------|--------------|------|----------|
| **AWS Well-Architected** | Framework | **Høj** - AWS services | Lav |
| **Azure Architecture Center** | Patterns | **Høj** - Azure services | Lav |
| **Confluent** | Event-driven | **Høj** - Kafka-centrisk | Lav |

### Anbefaling til Ydrasil
**Primær:** InfoQ for generel arkitektur. **Husk:** Microservices er overkill for solo dev - monolith first.

---

## 18-23. Øvrige Software Engineering kategorier

### Planlægning, Testing, Solo Dev, Teknisk Gæld, Refactoring, Documentation

**Samlet vurdering:**

| Kategori | Tier 1 Kilder | Hovedanbefaling |
|----------|--------------|-----------------|
| **Planlægning** | "Mythical Man-Month" (Brooks) | Story points er "popularized" men debatteret |
| **Testing** | Kent Beck (TDD by Example), Martin Fowler (Testing Pyramid) | TDD koncepter, ikke dogme |
| **Solo Dev** | **Pieter Levels** - $3.1M/år solo, 10+ års track record, radikalt transparent | **Høj relevans** |
| **Tech Debt** | Ward Cunningham (original metafor), Martin Fowler (Quadrant) | Deliberate vs inadvertent framework |
| **Refactoring** | Martin Fowler, Michael Feathers (Legacy Code) | "Brutal Refactoring" upcoming |
| **Documentation** | Write the Docs community | Docs as Code methodology |

### Solo Developer - Særlig Opmærksomhed

**Pieter Levels** fortjener særlig omtale:
- **Track Record:** $3.1M/år, NomadList, RemoteOK, PhotoAI - alle solo
- **Bias:** Lav - radikalt åben om revenue, failures, metoder
- **Relevans for Ydrasil:** **Ekstrem høj** - vores setup er solo dev

**Andre solo dev ressourcer:**
- Marc Lou (Ship Fast) - hurtig prototyping
- Tony Dinh (TypingMind) - solo app portfolio
- Indie Hackers community - revenue sharing, building in public

---

## DATA ENGINEERING KATEGORIER

---

## 24-27. Data Lineage, Schema Design, Data Quality, ETL/ELT

### Samlet vurdering

| Kategori | Tier 1 Kilder | Hovedanbefaling |
|----------|--------------|-----------------|
| **Data Lineage** | **dbt / Tristan Handy** - 10+ år analytics engineering, aktiv newsletter siden 2015, 2025 State of AE Report | Medium relevans - vi er ikke enterprise |
| **Schema Design** | Joe Celko, Markus Winand (use-the-index-luke) | Normalization basics er nok for os |
| **Data Quality** | Great Expectations (open source) | Python-centrisk, relevant hvis vi skalerer |
| **ETL/ELT** | **Maxime Beauchemin** (Airflow creator) | Airflow er overkill, Dagster/Prefect for simpelere cases |

### dbt / Tristan Handy - Særlig Vurdering

**Credibility:** Høj - founder af analytics engineering som discipline
**Bias:** Medium - sælger dbt Cloud, men også open source dbt Core
**Relevans:** Lav for nuværende Ydrasil scale, men værd at kende koncepterne

---

## TVÆRGÅENDE KILDER - ENDELIG PRIORITERING

---

## Top 5 Kilder at Stole På

| Rang | Kilde | Hvorfor | Bias-niveau |
|------|-------|---------|-------------|
| 1 | **Simon Willison** | 23 års track record, Django co-creator, nuanceret kritik, skriver om LLM | Minimal |
| 2 | **Hamel Husain** | 2000+ engineers trænet, O'Reilly bog, praktisk fokus | Minimal |
| 3 | **Martin Fowler** | 30+ år, aktiv i 2025-2026, skriver om LLM patterns | Minimal |
| 4 | **ANN-Benchmarks** | Uafhængig, akademisk, Spotify track record | Minimal |
| 5 | **Pieter Levels** | Solo dev gold standard, radikalt transparent | Minimal |

## Top 5 Kilder at Bruge med Forsigtighed

| Rang | Kilde | Bias-advarsel |
|------|-------|---------------|
| 1 | **LangChain** | Framework lock-in, bloat, latency overhead |
| 2 | **Vendor benchmarks** (alle) | Favoriserer altid vendor |
| 3 | **Uncle Bob** | Dogmatisk, kontroversiel |
| 4 | **Cloud provider docs** (AWS/Azure/GCP) | Lock-in fokus |
| 5 | **AI-first note tools** | Cloud dependency, black box |

## Top 5 Communities

| Community | Platform | Værdi | Bias |
|-----------|----------|-------|------|
| r/LocalLLaMA | Reddit | Real-world erfaringer, open source fokus | Pro-local |
| Hacker News | news.ycombinator.com | Kritisk, ærlig | Tech elite bias |
| Indie Hackers | indiehackers.com | Solo dev erfaring | Success story bias |
| Qdrant Discord | Discord | Direkte support for vores stack | Pro-Qdrant |
| Write the Docs | Slack | Docs best practices | Docs-fokus |

---

## KONKLUSIONER FOR YDRASIL

### Hvad vi kan stole på:
1. **Uafhængige practitioners** (Simon Willison, Hamel Husain) over vendor dokumentation
2. **Akademiske benchmarks** (ANN-Benchmarks, MTEB) over vendor benchmarks
3. **Open source communities** (r/LocalLLaMA) over marketing blogs
4. **Solo dev erfaring** (Pieter Levels) over enterprise patterns

### Hvad vi skal være skeptiske overfor:
1. **Alle vendor benchmarks** - de favoriserer altid vendoren
2. **Framework complexity** - LangChain, LlamaIndex kan være overkill
3. **AI-first tools** - cloud lock-in, black box problemer
4. **Dogmatiske design principper** - context matters

### Praktiske næste skridt:
1. **Følg Simon Willison's blog** - daglig opdatering
2. **Læs Hamel Husain's eval guide** - praktisk kvalitetssikring
3. **Brug ANN-Benchmarks** - til objektiv vektor-database evaluering
4. **Implementer simpelt først** - undgå prematur framework-adoption
5. **Test på dansk tekst** - benchmarks er primært engelske

---

## KILDER TIL DENNE RAPPORT

### Web Søgninger Udført

- Simon Willison credibility: [simonwillison.net](https://simonwillison.net/2026/Jan/8/llm-predictions-for-2026/)
- Hamel Husain background: [hamel.dev](https://hamel.dev/blog/posts/evals-faq/)
- Jason Liu Instructor: [jxnl.co](https://jxnl.co/)
- Jerry Liu LlamaIndex: [LinkedIn](https://www.linkedin.com/in/jerry-liu-64390071/)
- Qdrant production use: [Qdrant benchmarks](https://qdrant.tech/benchmarks/)
- Vector DB comparison: [Firecrawl](https://www.firecrawl.dev/blog/best-vector-databases-2025)
- RAGAS limitations: [arxiv](https://arxiv.org/abs/2309.15217)
- Martin Fowler relevance: [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/martin-fowler)
- Uncle Bob criticism: [GitHub debate](https://github.com/johnousterhout/aposd-vs-clean-code)
- Tiago Forte criticism: [Medium](https://medium.com/@productivitycore/some-critical-points-on-building-a-second-brain-f86122ec8b4f)
- MemGPT/Letta: [TechCrunch](https://techcrunch.com/2024/09/23/letta-one-of-uc-berkeleys-most-anticipated-ai-startups-has-just-come-out-of-stealth/)
- LangChain criticism: [Octomind](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents)
- ANN-Benchmarks: [ann-benchmarks.com](https://ann-benchmarks.com/)
- Pieter Levels: [levels.io](https://levels.io/indie-hackers-2/)
- Cohere rerank: [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/)
- Kent Beck TDD: [TidyFirst Substack](https://tidyfirst.substack.com/p/tdd-isnt-design)
- Nils Reimers: [sbert.net](https://sbert.net/)
- MTEB limitations: [arxiv](https://arxiv.org/html/2506.21182v1)
- Obsidian vs Notion: [Productive.io](https://productive.io/blog/notion-vs-obsidian/)
- dbt Tristan Handy: [getdbt.com](https://www.getdbt.com/resources/state-of-analytics-engineering-2025)
- GraphRAG: [Microsoft Research](https://www.microsoft.com/en-us/research/project/graphrag/)
- Chip Huyen: [huyenchip.com](https://huyenchip.com/)
- Chunking strategies: [Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)

---

*Næste skridt: Layer 3 vil dykke ned i de prioriterede kilder og ekstrahere konkrete, handlingsbare insights for Ydrasil.*
