# Layer 1 Research Pass 2: AI Memory Systems & Software Engineering
## Med Abstracts og Struktureret Overblik

**Dato:** 2026-02-05
**Formål:** Anden gennemgang af Layer 1 research med fokus på nye fund fra 2025-2026, abstracts for hver kategori, og praktiske perspektiver.

---

# DEL 1: AI/MEMORY SYSTEMER

---

## 1. VEKTOR-DATABASER

**Abstract:** Vektor-databaser er specialiserede datalagringssystemer designet til at gemme, indexere og søge i høj-dimensionelle vektorer (embeddings). De er fundamentet for moderne AI-applikationer som semantic search, RAG-systemer og anbefalingsmotorer. Man vælger en vektor-database når man har brug for at finde "lignende" data baseret på betydning snarere end eksakte matches. Valget afhænger af skala (tusinder vs. milliarder vektorer), operationel kompleksitet (managed vs. self-hosted), og integration med eksisterende stack. For de fleste solo-projekter er en letvægts-løsning som Qdrant, ChromaDB eller pgvector tilstrækkelig, mens enterprise-skala kræver Milvus, Pinecone eller Weaviate.

### Qdrant
Open-source vektor-database i Rust med fokus på performance og filtered vector search. Kører lokalt eller i cloud. Ideel til mellemstore projekter med behov for metadata-filtrering.

### Pinecone
Fully-managed cloud-løsning uden operationel overhead. Premium pris men nul DevOps. Bedst for teams der vil undgå infrastruktur-administration.

### Milvus / Zilliz
Distribueret, GPU-accelereret database til milliarder af vektorer. Enterprise-grade med mange indexeringsmetoder. Overkill for små projekter.

### Weaviate
Cloud-native med stærk hybrid search og auto-vektorisering. Indbyggede moduler til at konvertere tekst/billeder til vektorer automatisk.

### ChromaDB
Letvægts, LLM-fokuseret med dyb LangChain-integration. Perfekt til prototyping og små projekter. Simpel API.

### pgvector / pgvectorscale (NYT benchmark)
PostgreSQL-extension der bringer vektor-search til eksisterende Postgres-installationer. Nye benchmarks (2025) viser pgvectorscale med 471 QPS ved 99% recall - 11.4x bedre end Qdrant på samme benchmark. Game-changer for Postgres-baserede stacks.

### LanceDB
Embedded vektor-database der kan køre direkte i applikationen. Ideel til edge-devices, offline-apps og serverless.

### Turbopuffer
Managed database brugt af Cursor, Notion og Linear. Støtter både vektor og BM25. Fokus på simplicity og performance.

### DuckDB VSS / DuckRAG (NYT)
Eksperimentel HNSW-extension til DuckDB. "DuckRAG"-arkitekturen koster ~$0.001/måned per team med per-bruger DuckDB-filer på S3. Spændende for analytics + vector workflows.

### Højere-niveau platforme (NYT 2025-2026)
Shaped, Algolia, Coveo og Bloomreach abstraherer vektor-retrieval bag end-to-end API'er med personalisering og anbefalinger out-of-the-box. Reducerer DIY-kompleksitet markant for teams uden ML-ekspertise.

---

## 2. RAG-ARKITEKTURER

**Abstract:** RAG (Retrieval-Augmented Generation) kombinerer søgning i en vidensbase med LLM-generering for at producere faktuelt forankrede svar. Det løser LLM'ers "hallucineringsproblem" ved at give dem adgang til aktuel, verificerbar information. Man bruger RAG når man vil have en AI der kan svare baseret på specifikke dokumenter, databaser eller vidensbaser snarere end kun træningsdata. Arkitekturen har udviklet sig fra simple "hent-og-indsæt" pipelines til sofistikerede modulære systemer med multi-stage retrieval, reasoning-loops og knowledge graphs. Valget af RAG-arkitektur afhænger af query-kompleksitet, vidensbasens størrelse, og krav til nøjagtighed vs. hastighed.

### Naive RAG
Simpel baseline: indexer → embed query → hent top-k → indsæt i prompt → generer. Fungerer overraskende godt som udgangspunkt. Start her.

### Advanced RAG
Tilføjer pre-retrieval (query rewriting, HyDE), forbedret retrieval (hybrid search, reranking) og post-retrieval (komprimering, filtrering). De fleste produktions-RAG-systemer.

### Modular RAG (LEGO-framework) (NYT 2026)
Bryder pipelinen op i udskiftelige moduler (retriever, reranker, generator, router). Hver komponent kan opgraderes uafhængigt. 2026-trenden: "swap, upgrade, or bypass components without rewriting the pipeline."

### GraphRAG
Kombinerer vektor-search med strukturerede knowledge graphs. Microsofts forskning viser 26-97% færre tokens. Excellent til multi-hop reasoning og komplekse relationer.

### RAPTOR
Rekursivt bygger en træstruktur af opsummeringer over dokumenter. Bevarer global kontekst som flad chunking mister. Overlegen for multi-step reasoning.

### HyDE / HyPE (NYT)
Genererer hypotetisk dokument der besvarer queryen, embedder det, og søger. HyPE (2025) optimerer per dokument med op til 42 procentpoint forbedring.

### Self-RAG
Selvrefleksiv mekanisme der beslutter hvornår retrieval er nødvendig og evaluerer kvaliteten. Reducerer hallucineringer markant.

### Agentic RAG
AI-agent der dynamisk vælger søgestrategi baseret på query-type. Mest fleksibelt men også mest komplekst.

### RAG-Fusion / MQRF-RAG (NYT)
Genererer multiple queries, kombinerer via Reciprocal Rank Fusion. MQRF-RAG (2025) viste 14.45% forbedring i precision.

### Multimodal RAG
Håndterer billeder, audio, video og tekst i ét system. Tidlig modenhed men hastigt udviklende.

### Retriever-centric vs Generator-centric (NYT taksonomi)
Nyere surveys kategoriserer RAG i retriever-centric (fokus på retrieval-kvalitet), generator-centric (fokus på LLM-optimering), hybrid (begge), og robustness-oriented (fokus på sikkerhed/pålidelighed).

---

## 3. CHUNKING-STRATEGIER

**Abstract:** Chunking er processen med at opdele dokumenter i mindre stykker til embedding og retrieval. Det er en af de mest undervurderede komponenter i RAG-systemer - forkert chunking kan ødelægge selv det bedste system. Man vælger chunking-strategi baseret på dokumenttype, query-mønstre og trade-off mellem præcision og kontekst. Små chunks giver præcis retrieval men mister kontekst; store chunks bevarer kontekst men introducerer støj. Den optimale strategi er ofte domæne-specifik og kræver eksperimentering. Nyere forskning (2025-2026) peger på semantic-first tilgange som det mest lovende, men simpel recursive splitting forbliver et stærkt baseline-valg.

### Fixed-Size Chunking
Opdeler efter fast antal tokens/tegn. Simpel baseline men ignorerer tekststruktur. Start her og optimer derfra.

### Recursive Character Splitting
Default-valg for 80% af RAG-apps. Splitter rekursivt på naturlige grænser (paragraffer → sætninger → ord). LangChains standard.

### Semantic Chunking
Splitter baseret på semantiske skift detekteret via embeddings. Optimal range: 256-512 tokens med 10-20% overlap. Vandt i sammenligning af 9 strategier.

### Max-Min Semantic Chunking (NYT 2025)
Ny metode der bruger Max-Min algoritme til at identificere semantisk kohærente segmenter. Konsistent bedre end eksisterende metoder på tværs af datasæt.

### Sidebaseret Chunking
Behandler hver dokumentside som chunk. Højeste accuracy (0.648) i NVIDIA benchmarks. Simpelt og effektivt for PDF'er.

### Agentic / LLM-baseret Chunking
LLM beslutter intelligent hvor tekst skal splittes. Dyrere men bedst for lange, komplekse dokumenter med multiple emner.

### Proposition Chunking
Opdeler i selvstændige udsagn der kan stå alene. Højere kvalitet per chunk men flere chunks total.

### Hierarchisk Chunking (Parent-Child)
Forældre-noder (stor kontekst) og børne-noder (fine detaljer). Retrieval på børne-niveau, kontekst fra forældre til LLM.

### ClusterSemanticChunker (NYT)
Bruger embeddings direkte til at komponere chunks baseret på semantisk similaritet. Research-fokuseret tilgang.

### LLMChunker (NYT)
Prompter en LLM til at udføre chunking direkte. Mest sofistikerede men dyreste tilgang.

---

## 4. EMBEDDING-MODELLER

**Abstract:** Embedding-modeller konverterer tekst til høj-dimensionelle vektorer der fanger semantisk betydning. De er kernen i vektor-søgning og RAG - kvaliteten af dine embeddings bestemmer kvaliteten af din retrieval. Man vælger embedding-model baseret på sprog, domæne, dimensionalitet, hastighed og pris. MTEB-benchmark er industristandarden for sammenligning, men overall-score skjuler nuancer - en model tunet til retrieval kan underperformere på clustering. For de fleste use cases er en mellemstør model (OpenAI small, Cohere, BGE) tilstrækkelig; specialiserede domæner kan drage fordel af finetuning eller domæne-specifikke modeller.

### OpenAI text-embedding-3-large/small
3072/1536 dimensioner, $0.13/$0.02 per million tokens. General-purpose med bred adoption. Støtter dimensionsreduktion.

### Cohere embed-v4
Højeste MTEB score (65.2), 1024 dim, $0.10 per million. Stærkt multilingual og search-optimeret. Bedste pris-performance.

### NV-Embed (NVIDIA) (NYT - MTEB rekord)
MTEB score 69.32 - ny rekord. Baseret på Llama-3.1-8B. Kraftfuld multilingual forståelse. Kører lokalt med GPU. State-of-the-art.

### Voyage AI voyage-3.5 (NYT)
Enterprise-grade semantic search. Voyage 3.5 og 3.5 Lite med excellent benchmark-performance. Domæne-tuning mulighed (voyage-code, voyage-law).

### BGE-M3 (BAAI) (NYT fremhævet)
Open-source, multilingval (1000+ sprog). Dense + sparse + multi-vector retrieval i én model. Kan køre lokalt uden API-costs. Top-valg for open-source.

### Qwen3-Embedding (NYT)
0.6B parametre, 100+ sprog. State-of-the-art for sin størrelse. Top-ranker på MTEB multi-lingual og English leaderboards.

### E5-familien (Microsoft)
e5-small: 14x hurtigere (16ms) med 100% Top-5 accuracy i tests. Exceptionel for latency-kritiske apps.

### Jina Embeddings v3
Op til 8192 tokens kontekst. Task-specific embeddings via LoRA-adaptere. Populært for lange dokumenter.

### EmbeddingGemma-300M (NYT)
Google DeepMind, kun 300M parametre. Optimeret til on-device. Rivaliserer meget større modeller. Gratis.

### Nomic Embed Text v1.5/v2 (NYT)
Fuld gennemsigtighed (træningsdata, kode). v2 er første MoE embedding-model. Matryoshka-representation (variabel dimensionalitet). Privacy-fokuseret.

---

## 5. RE-RANKING

**Abstract:** Re-ranking er et andet retrieval-pass der forbedrer præcisionen ved at score og omordne kandidat-dokumenter fra det første pass. Hvor bi-encoders (embedding-modeller) scorer dokumenter uafhængigt for hastighed, behandler re-rankers (cross-encoders) query og dokument sammen for dybere semantisk forståelse. Man bruger re-ranking når retrieval-kvalitet er kritisk og latency tillader et ekstra trin. Typisk køres re-ranking på top 50-100 kandidater. Valget står mellem hastighed (cross-encoders) og kvalitet (LLM-based), med ColBERT som interessant mellemvej der giver cross-encoder kvalitet med bi-encoder hastighed via late interaction.

### Cohere Rerank
Industristandard for managed reranking. 100+ sprog. API-baseret. Op til 48% forbedring ifølge Databricks. "Rerank 3 Nimble" for hurtigere production.

### Cross-Encoders (BGE, MXBAI)
BERT-baserede modeller der scorer query-document par via fuld cross-attention. State-of-the-art accuracy men lineær skalering med kandidat-antal.

### ColBERT / ColBERTv2
Late interaction: dokumenter som sæt af token-embeddings, similarity via max similarity per query-token. Bedre end single-vector, mere storage.

### Jina-ColBERT (NYT)
ColBERT-implementering med op til 8000 tokens kontekst. Excellent til lange dokumenter.

### SPLATE
Kombinerer SPLADE og ColBERT. ColBERTv2-performance med sparse retrieval-hastighed. Tiltalende for CPU-miljøer.

### Qwen3 Rerankers (NYT)
0.6B, 4B, 8B parametre. 100+ sprog, 32k tokens kontekst. State-of-the-art open-source.

### ZeroEntropy zerank-1
+28% NDCG@10 forbedring. Korrelerer med lavere hallucinationsrater. zerank-1-small som open-source.

### Pinecone Rerank V0 (NYT)
Cross-encoder med 0-1 relevans-scores. Højeste avg NDCG@10 på BEIR. 60% forbedring på Fever dataset vs Google Semantic Ranker.

### MonoQwen2-VL-v0.1 (NYT)
Første visuelle dokument-reranker med VLM. Fortolker billeder direkte uden OCR. Cutting-edge for multimodal.

### LLM-baseret Reranking (RankGPT)
5-8% højere accuracy men 4-6 sekunder ekstra latency. Bedst til offline/batch processing og high-stakes use cases.

---

## 6. MEMORY FRAMEWORKS

**Abstract:** Memory frameworks giver AI-systemer evnen til at huske information på tværs af interaktioner - fra tidligere samtaler til akkumuleret viden og lærte præferencer. De løser LLM'ers fundamentale statelessness-problem. Man bruger memory frameworks når man bygger assistenter der skal personaliseres over tid, agenter der lærer af erfaring, eller systemer der skal huske kontekst på tværs af sessions. Valget afhænger af use case (samtale-hukommelse vs. viden-akkumulering), deployment (managed vs. self-hosted), og integration med eksisterende stack. 2025-2026 har set en eksplosion af løsninger med Mem0, Letta og Zep som de tre mest modne.

### Mem0
Y Combinator-backed, mest produktionsklar. 26% bedre accuracy end OpenAI Memory, 91% hurtigere, 90% lavere token-forbrug. SaaS + open-source.

### Letta (MemGPT)
UC Berkeley-oprindelse, OS-inspireret memory hierarki: core → conversational → archival → external. Truly open-source. SaaS under udvikling.

### Zep / Graphiti
Temporalt knowledge graph med bi-temporal datamodel. 94.8% på DMR benchmark. Hybrid search uden LLM-kald (300ms P95). Stærkt til relationsrig data.

### Cognee
ECL-pipelines (Extract, Cognify, Load). Kombinerer vektor + graf for semantisk søgbarhed og relationer. Støtter Neo4j, FalkorDB, Kuzu.

### LangMem (LangChain)
Tre typer: semantic (fakta), procedural (how-to), episodisk (erfaringer). Finkornret kontrol i LangChain-økosystemet.

### LlamaIndex
RAG-først framework med native query engines. Rapid udvikling med high-level abstraktioner. MIT-licenseret.

### Haystack (deepset)
Production-orienteret med ~5.9ms framework overhead. Enterprise-features: monitoring, scaling, REST API.

### Microsoft Semantic Kernel
Første-klasses .NET-støtte (plus Python/Java). Dyb Azure-integration. Agent Framework (juli 2025).

### Membase (NYT)
Universal memory layer der synker kontekst på tværs af AI-tools og services.

### TeamLayer (NYT)
Persistent, delt memory på tværs af ChatGPT, Claude, Cursor og andre AI-værktøjer. Forhindrer konteksttab.

### A-MEM (Agentic Memory)
Zettelkasten-inspireret. Mindst 2x bedre end konkurrenter på Multi-Hop opgaver. Februar 2025.

---

## 7. KNOWLEDGE MANAGEMENT TOOLS

**Abstract:** Knowledge management tools hjælper med at fange, organisere og genfinde personlig og organisatorisk viden. De er fundamentet for "second brain"-konceptet - et eksternt system der udvider din hukommelse og tænkeevne. Man vælger tool baseret på arbejdsstil (outliner vs. freeform), privacy-krav (local-first vs. cloud), samarbejdsbehov (solo vs. team), og AI-integration. 2026 markerer et skifte: æraen med manuel organisering slutter, og intelligente workspaces med automatisk capture, AI-drevet linking og proaktive reviews overtager. De bedste tools kombinerer nu multimodal capture, AI intelligence og local-first privacy.

### Obsidian
Local-first Markdown, graf-baseret tænkning, 1000+ plugins. "Bases" feature (2025) giver database-funktionalitet. Mest kraftfulde PKM men kræver investering.

### Notion
All-in-one workspace med AI-integration. Enestående collaboration. Cloud-first. Dominerer team-baseret vidensstyring.

### Logseq
Open-source outliner med bidirektionelle links. Block-baseret struktur. Gratis, privacy-fokuseret.

### Tana
AI-native med "supertags" (nodetyper med egenskaber). Natural language queries. Kraftfuld men data i Tanas graf.

### Anytype (NYT)
Open-source, har erstattet mange tidligere favoritter. Forbedrer capture, connections og kontrol over digitalt liv.

### AFFiNE (NYT)
Open-source, local-first workspace der kombinerer docs, whiteboards og databases. Voksende som Notion-alternativ.

### Heptabase
Visuel note-taking med uendelige whiteboards. Ideel for visuelt tænkende. $11.99/måned.

### Capacities
Objekt-baseret med AI-drevne insights. Kombination af Notion-struktur og Obsidian-linking.

### Mem 2.0 (NYT okt 2025)
Komplet genopbygning: hurtigere, offline-støtte, voice mode. Mere agentisk AI-lag.

### Fabric (Daniel Miessler)
Open-source framework med modulære "patterns" for AI-opgaver. CLI-baseret, kan integreres i pipelines.

---

## 8. PERSONAL AI / SECOND BRAIN

**Abstract:** Personal AI er systemer der augmenterer individuel tænkning og hukommelse med AI-kapabiliteter. Det handler om at bygge en personlig vidensinfrastruktur hvor capture er automatisk, organisering usynlig, retrieval konversationel, og reviews proaktive. Man investerer i personal AI når man vil have et "eksternt sind" der husker alt man lærer, forbinder idéer på tværs af kilder, og proaktivt bringer relevant viden frem. Implementeringen spænder fra simple note-app + AI combos til fulde custom RAG-setups. 2026-trenden er AI-native second brains: automatisk ingestion af digital exhaust, on-device privacy, RAG med kilder, og proaktive insights.

### Daniel Miesslers PAI (Personal AI Infrastructure)
Omfattende system "Kai" til human augmentation. PAI v2.4 (jan 2026) med Memory System v7.0, Hook System, TELOS-mål. Open-source.

### PAIMM (Personal AI Maturity Model)
Model for at måle AI-integration i personlig workflow. Fra chatbot-bruger til fuld agent-orkestrering.

### Second Brain (Tiago Forte)
CODE-metodologi: Capture, Organize, Distill, Express. AI transformerer passivt arkiv til aktiv assistant.

### Zettelkasten-metoden
Atomiske noter forbundet via links. Inspiration for A-MEM. Skalerbar vidensstruktur.

### Khoj (NYT)
Self-hostable AI second brain. Get answers from web or docs. Build custom agents, schedule automations. Gratis.

### Quivr (NYT)
Opinionated RAG for GenAI i apps. Any LLM (GPT4, Groq, Llama), any vectorstore (PGVector, Faiss). Customizable.

### Custom RAG-setups
Qdrant/Chroma + embedding + LLM. Maksimal kontrol og tilpasning. Ydrasil er et eksempel.

### Implementeringsniveauer (NYT 2026)
**Begynder:** Eksisterende note-app + web clipper + chat model med manuelt klippede snippets.
**Mellem:** Obsidian vault + lokal vektor-store (FAISS/SQLite) + file-watcher + recursive chunking + chat interface.
**Avanceret:** Fuld custom pipeline med automatisk ingestion, on-device parsing, RAG med citater, proaktive reviews.

---

## 9. CONTEXT WINDOW MANAGEMENT

**Abstract:** Context window management handler om at maksimere værdien af LLM'ens begrænsede inputkapacitet. Selvom kontekstvinduer er vokset (100K+), falder model-performance ved lange kontekster, og costs stiger lineært. Man har brug for context management når samtaler bliver lange, dokumenter er store, eller token-budgettet er stramt. Strategierne spænder fra simple sliding windows til sofistikerede komprimeringsteknikker. Nyere forskning (2025-2026) viser at smart kompression ofte slår større vinduer for både cost og kvalitet - 5-20x kompression med bibeholdt eller forbedret accuracy er muligt med de rigtige teknikker.

### Conversation Buffer
Gem alt. Maksimal information men højt tokenforbrug. Funktionelt umulig for lange samtaler.

### Sliding Window
Behold kun de seneste N interaktioner. Simpelt og effektivt for de fleste chatbots.

### Hierarkisk Opsummering
Nylige udvekslinger ordret, ældre komprimeres til opsummeringer. Progressive kompression. Standard for produktion.

### Extractive Compression (NYT anbefaling)
Anbefalet for 80% af use cases. Sikreste, hurtigste, ofte accuracy-forbedrede. Vælg vigtige sætninger ordret.

### 5-20x Kompression (NYT benchmark)
Summarization + keyphrase extraction + semantic chunking opnår 70-94% cost savings i produktion.

### Observation Masking vs. LLM Summarization (NYT)
Masking: behold seneste 10 turns for bedste balance. Summarization: opsummer 21 turns, behold 10 i fuld form. Begge effektive.

### SUPO (Summarization-augmented Policy Optimization)
ByteDance/Stanford/CMU. End-to-end lært opsummering for RL-træning ud over faste vinduer. Cutting-edge research.

### Acon (Agent Context Optimization)
26-54% lavere peak tokens. 32-46% forbedring for små LM'er som agenter. Praktisk framework.

### Glyph (Visual-Text Compression)
Tekst renderet som billeder, behandlet af vision-LLM. 3-4x kompression standard, op til 8x ekstremt. Kreativt hack.

### Knowledge Graph Memory
Entiteter og relationer fra samtaler i graf. Struktureret kontekst syntetiseret fra grafen.

---

## 10. HYBRID SEARCH

**Abstract:** Hybrid search kombinerer keyword-matching (BM25/sparse) med semantisk similaritet (dense vectors) for at fange hvad hver metode alene misser. BM25 exceller ved eksakte matches, sjældne termer og domæne-specifikke ord; dense retrieval finder semantiske ligheder og håndterer parafraser. Man bruger hybrid search når man vil have både præcision og recall - typisk 15-30% bedre recall end enkeltmetoder. IBM-forskning (2025) viste at three-way retrieval (BM25 + dense + sparse) er optimal, og med ColBERT reranker nås NDCG 0.93. For de fleste RAG-systemer er hybrid search nu industristandard.

### BM25 + Dense Vector (Standard Hybrid)
Den basale kombination. Keyword-matching + semantisk. 15-30% bedre recall end hver alene.

### Reciprocal Rank Fusion (RRF)
Parameter-fri fusion: konverter scores til ranks, kombiner med RRF(d) = sum(1/(k+rank)). Plug-and-play, robust.

### Three-Way Hybrid (BM25 + Dense + Sparse) (NYT IBM research)
IBM-research: optimal kombination. NDCG 0.85 vs 0.72 (dense-only) vs 0.65 (sparse-only). Bevist overlegen.

### Full Pipeline (Hybrid + HyDE + Reranking)
NDCG 0.93. Den mest effektive retrieval-strategi påvist i benchmarks.

### SPLADE
Lært sparse retrieval der udvider queries/dokumenter med relaterede termer via BERT. Effektiv, kan køre på inverterede indekser.

### Learned Sparse Retrieval
Bredere kategori: SPLADE, DeepCT, COIL. Bedre end BM25 for semantik men beholder sparse effektivitet.

### Convex Combination / Weighted Fusion
Lineær interpolering med konfigurerbar vægt. Bedre end RRF med labelerede data til tuning.

### Blended RAG (NYT)
Full-text + dense + sparse outperformer alle to-vejs kombinationer. ColBERT reranker giver yderligere forbedring.

---

## 11. KNOWLEDGE GRAPHS

**Abstract:** Knowledge graphs strukturerer viden som netværk af entiteter og relationer - "Kris" er-kører "Rute 256", Rute 256 indeholder "Stop A, B, C". De muliggør reasoning over relationer som vektor-search alene ikke kan fange. Man bruger knowledge graphs når data har komplekse relationer, multi-hop queries er vigtige, eller man har brug for forklarbare svar. GraphRAG kombinerer vektor-embeddings med knowledge graphs for det bedste af begge verdener: semantisk søgning plus eksplicit relationsmodellering. Implementeringen kræver entity extraction, de-duplikering og ontologi-design - mere kompleks end ren vektor-search men med markant bedre resultater for relationsrig data.

### Neo4j
Verdens mest populære graf-database. Cypher query-sprog. Pattern matching, graf-algoritmer, vektor-search (5.x+). De facto standard.

### Graphiti (Zep)
Open-source Python framework for temporalt-bevidste knowledge graphs. Automatisk ontologi, de-duplikering. MCP-server inkluderet.

### Microsoft GraphRAG
Entity-centriske knowledge graphs med communities og LLM-opsummeringer. 26-97% færre tokens. Open-source.

### Cognee (graf-aspekt)
Triplet-ekstraktion (subjekt-relation-objekt). Overvinder RAGs begrænsninger med memory-first arkitektur.

### FalkorDB
Høj-performance, optimeret til AI/knowledge graph workloads. Hurtigere end Neo4j for visse queries. Støttet af Graphiti.

### Kuzu
Embedded graf-database (ligesom SQLite). In-process, ingen server. Ideel for lokale/embedded AI-apps.

### Entity Extraction + Resolution
LLM-baseret ekstraktion fra ustruktureret tekst. De-duplikering kritisk: "Kris", "chaufføren", "Rute 256 kører" = samme entitet. 300-320% ROI rapporteret.

### Document Parsing (NYT)
Docling, LlamaParse, Amazon Textract, Google Document AI, Azure AI Document Intelligence til struktureret ekstraktion.

### Ontologi-drevet KG Construction (NYT)
RDF-ontologier guider LLM i at skabe specifikke entitets- og relationstyper. Mere deterministisk end fri-form.

---

## 12. CONVERSATIONAL MEMORY

**Abstract:** Conversational memory giver chatbots og AI-assistenter evnen til at huske kontekst inden for og på tværs af samtaler. Det er essensen af at føles "intelligent" - en assistant der husker hvad du sagde for 5 minutter siden føles radikalt bedre end en der ikke gør. Man implementerer conversational memory baseret på samtale-længde, persistence-krav og token-budget. Simple chatbots klarer sig med sliding window; avancerede assistenter har brug for summary + buffer kombinationer eller vektor-baseret retrieval. Nyere forskning viser at LLM'er stadig har udfordringer med very long-term conversational memory (300+ turns) - state-of-the-art performer væsentligt dårligere end mennesker.

### Conversation Buffer Memory
Gem al historik. Maksimal kontekst men umulig for lange samtaler. LangChains reference-implementering.

### Conversation Buffer Window Memory
Behold seneste N interaktioner. Fleksibelt vindue. Simpelt og effektivt. Default for de fleste.

### Conversation Summary Memory
Løbende opsummering. Nyttigt for lange samtaler hvor man behøver tråden men ikke hvert ord. Afhængig af opsummerings-kvalitet.

### Conversation Summary Buffer Memory
Kombination: nylige i buffer, ældre opsummeret. Mest fleksibel. Anbefalet default for produktion.

### Entity Memory
Gemmer info om specifikke entiteter. Akkumulerer viden over samtalen. Ideel for specifikke datapunkter.

### Knowledge Graph Memory
Bygger mini knowledge graph med noder og relationer. Mest sofistikerede built-in type.

### VectorStore Retriever Memory
Gemmer som embeddings, henter kun relevante dele. Skalerbar til meget lange historikker.

### Memoria (NYT)
KG-baseret long-term memory + session-level summarization + recency-weighted retrieval. Robust, skalerbar.

### LoCoMo Dataset/Benchmark (NYT)
Very long-term conversations: 300 turns, 9K tokens, 35 sessions. LLM'er lagger stadig væsentligt bag mennesker.

---

## 13. LANGTIDS- VS. KORTTIDSHUKOMMELSE

**Abstract:** AI-agenter har brug for forskellige typer hukommelse ligesom mennesker: korttidshukommelse (working memory i kontekstvinduet) og langtidshukommelse (persistent storage). Langtidshukommelse opdeles yderligere i episodisk (specifikke oplevelser), semantisk (fakta og viden) og procedural (hvordan man gør ting). Valget af memory-arkitektur afhænger af agent-typen: personlige assistenter prioriterer episodisk, domæne-eksperter prioriterer semantisk, og workflow-automatisering prioriterer procedural. 2026-forskning fokuserer på at forene disse i sammenhængende frameworks (AgeMem, MemRL) med selvudviklende hukommelse.

### Tre typer langtidshukommelse
**Episodisk:** Præferencer, tidligere interaktioner, udfald. Vigtigst for personlige assistenter.
**Semantisk:** Domæneviden (jura, medicin, finans). Vigtigst for domæne-eksperter.
**Procedural:** Lærte rutiner, workflows. Vigtigst for automation-agenter.

### MemGPT Hierarki
OS-inspireret: core memory (kontekst) → conversational → archival (vektor-DB) → external files. Agent styrer selv hvad der er i "RAM" vs. "disk".

### AgeMem (Agentic Memory, jan 2026) (NYT)
Samler lang- og korttidshukommelse i ét framework. Eksplicit tool-baserede operationer. State-of-the-art paper.

### MemRL (jan 2026) (NYT)
Self-Evolving Agents via Runtime RL på episodisk hukommelse. Systemet bliver bedre af at bruge det. Meta-learning for hukommelse.

### MAGMA (Multi-Graph Agentic Memory, jan 2026) (NYT)
Multi-graf arkitektur for forskellige hukommelses-aspekter. Tidligt stadie men lovende.

### Redis for Agent Memory
Hurtig in-memory store for både kort- og langtidshukommelse. Fire gængse strategier. Industrielt modent.

### MongoDB + LangGraph
MongoDB Store bringer fleksibel, skalerbar langtidshukommelse til LangGraph-agenter. Enterprise-grade.

### Korttidshukommelse
Essentially working memory - kontekstvinduet. Nyttigt for umiddelbare opgaver, begrænset i scope. Som RAM: lukker du app'en, forsvinder det.

---

## 14. EVALUERING OG BENCHMARKS

**Abstract:** Evaluering måler om dit RAG-system faktisk virker - og hvordan det performer over tid. Uden systematisk evaluering deployes systemer blindt, kvalitet degraderer gradvist, og fejl opdages først af brugere. Man implementerer evaluering fra dag 1 for at etablere baselines, sammenligne ændringer, og monitorere drift. Kernemålingerne er retrieval-kvalitet (precision, recall, nDCG), generations-kvalitet (faithfulness, relevans), og end-to-end performance (correctness, latency, cost). RAGAS er de facto standard for RAG-evaluering, men har pålidelighedsbegrænsninger - kombiner med menneskelig review og multiple LLM-judges.

### RAGAS
Pionerede reference-fri RAG-evaluering. Context Precision/Recall, Faithfulness, Response Relevancy, Answer Accuracy m.fl. De facto baseline men forskellige judges er ofte uenige.

### TruLens
Open-source med feedback functions: groundedness, context relevance, coherence. LLM-as-judge grading. Dashboard til drift-monitorering.

### DeepEval
RAG-specifikke metrikker. Unit + integration tests. Bedre developer experience end RAGAS. Aktiv community.

### ARES
Syntetiske evaluerings-datasæt + adversarial stress-tests. Reducerer behov for menneskelige labels.

### Precision@k og Recall@k
Kerne retrieval-metrikker. Tilpasses ofte til statement-niveau i RAG. Begrænsning: ét relevant dokument ud af ti = kun 10% recall.

### MRR og nDCG
MRR: reciprok rank af første relevante. nDCG: ranking-kvalitet. Primary metrics i retrieval benchmarks.

### Faithfulness / Groundedness
Er svaret tro mod kilderne? Kritisk for faktuelt krævende apps. Implementeret i RAGAS, TruLens, DeepEval.

### LLM-as-Judge
Brug LLM'er til at evaluere output. Multiple judges i panel fanger flere nuancer. Bedre human alignment end single-judge.

### NoLiMa Benchmark
Performance ved forskellige kontekstlængder. Ved 32K tokens faldt 11/12 modeller under 50% af kort-kontekst performance. Kritisk indsigt.

---

## 15. ANTI-PATTERNS OG FAILURE MODES

**Abstract:** RAG-systemer fejler på forudsigelige måder - at kende disse patterns er halvdelen af at undgå dem. Fejlene spænder fra tekniske (stale embeddings, naive chunking) til sikkerhedsmæssige (context poisoning, prompt injection) til fundamentale (multi-hop reasoning failure). Man studerer anti-patterns for at designe robuste systemer fra starten og for at diagnosticere problemer i eksisterende systemer. Mange fejl er "stille" - systemet returnerer et svar, men svaret er forkert uden tydelige tegn. Systematisk evaluering og adversarial testing er de vigtigste værn. 2025-2026 har set særligt fokus på sikkerhedstrusler mod RAG-pipelines.

### Context Poisoning / Context Clash
Modstridende eller vildledende information kontaminerer ræsonnering. Selv relevant kontekst kan oversvømme i ren volumen.

### Embedding-Level Prompt Injection (NYT 2025)
"Vector Magnets": adversarial tekst optimeret til at okkupere samme embedding-region som target queries. 5 dokumenter kan manipulere 90% af svar.

### RAG Poisoning (NYT)
0.04% corpus poisoning → 98.2% attack success rate, 74.6% system failure. PoisonedRAG, CorruptRAG, Phantom angreb.

### Trust Paradox
Queries behandles som untrusted, men hentet kontekst er implicit trusted - selvom begge enters same prompt. OWASP LLM08:2025.

### Multi-Hop Reasoning Failure
RAG henter relevante fakta men mangler reasoning-forbindelser til syntese. Al nødvendig info til stede, men forkert svar.

### Lost in the Middle
Information i midten af konteksten ignoreres. Kritisk info i midten kan overses. Påvirker ranking-strategi.

### Naive Chunking
Faste 512-token vinduer bryder tabeller og semantisk kontinuitet. LLM hallucinererer relationer der ikke eksisterer.

### Cascading Failures
0.95 × 0.95 × 0.95 = 0.81 total reliability. Dit system fejler 1 ud af 5 gange. Reliability math.

### Stale Embeddings / Knowledge Drift
Embeddings reflekterer gammel information efter opdateringer. Kræver systematisk re-embedding strategi.

### Information Flooding
Store mængder tekst spreder modellens opmærksomhed. Smart compression slår større vinduer.

### Manglende Evaluering
Den største anti-pattern. De fleste RAG-systemer deployes uden systematisk evaluering.

---

# DEL 2: SOFTWARE ENGINEERING

---

## 16. DESIGN PRINCIPPER

**Abstract:** Design principper er tidstestede guidelines der hjælper med at skabe vedligeholdelig, forståelig og fleksibel software. De adresserer de fundamentale årsager til problematisk kode: for mange ansvarsområder, for tæt kobling, og skjulte afhængigheder. Man bruger principper som SOLID, KISS, DRY og YAGNI som "tensions to manage" snarere end rigide regler - hvert princip peger på et trade-off. 2026-perspektivet understreger pragmatisme: principper er ment som guides, ikke politi. Real-world systemer er rodede, og trade-offs er uundgåelige. Det vigtige er at være bevidst om hvorfor man vælger én tilgang over en anden.

### SOLID
Fem OO-principper: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. 20+ år gamle men stadig relevante.

### KISS (Keep It Simple, Stupid)
Simplicitet i design reducerer fejl og forbedrer forståelighed. Betyder ikke simplistisk kode - betyder kun så kompleks som nødvendigt.

### DRY (Don't Repeat Yourself)
Hvert stykke viden har én autoritativ repræsentation. VIGTIGT: Kan overdrives - duplikering er bedre end forkert abstraktion.

### YAGNI (You Aren't Gonna Need It)
Implementer aldrig noget før du har brug for det. Tidlig feature-building skaber bygge-, forsinkelse- og vedligeholdelsesomkostninger.

### Unix-filosofien
Programmer der gør én ting godt, arbejder sammen, og håndterer tekststrømme. MCP er direkte arving.

### Separation of Concerns
Opdel i distinkte sektioner med separate ansvarsområder. Grundlag for MVC, mikroservices, lagdelt arkitektur.

### Composition over Inheritance
Sammensæt objekter af mindre dele fremfor dybe arvehierarkier. GoF-bogen 1994. Standard i moderne frameworks.

### Principle of Least Surprise (POLA)
Systemer bør opføre sig som forventet. Du ER brugeren om 6 måneder - og du vil blive overrasket.

### Law of Demeter
Minimal viden om andre enheder. Undgå "train wreck" kode: customer.getAddress().getCity().getZipCode().

### Robustness Principle (Postels Law)
Konservativ i hvad du sender, liberal i hvad du accepterer. Balancer med: vær streng nok til at fange fejl.

---

## 17. ARKITEKTURMØNSTRE

**Abstract:** Arkitekturmønstre er højniveau-strukturer for hvordan software organiseres og kommunikerer. Valget af arkitektur har langsigtede konsekvenser for vedligeholdelse, skalering og udviklingshastighed. Man vælger arkitektur baseret på teamstørrelse, kompleksitet og vækstforventninger. 2026-trenden er markant: organisationer der rushed ind i microservices konsoliderer tilbage til enklere strukturer, og modular monolith er blevet det anbefalede udgangspunkt. Microservices køber organisatorisk fleksibilitet til prisen af operationel kompleksitet - en pris solo-udviklere sjældent har brug for at betale.

### Modulær Monolit
Én deploybar applikation med velafgrænsede moduler og klare interfaces. Shopify og GitHub bruger det. Næsten altid det rigtige valg for solo.

### Microservices (og hvorfor de ofte er forkerte)
Uafhængigt deploybare services. Introducerer enormt overhead: service discovery, distribueret tracing, netværksfejl, eventuel konsistens. Start med monolit.

### 2026-tendens: Konsolidering (NYT)
Organisationer der rushed til microservices konsoliderer tilbage. Modular monolith med selective extraction er optimal for de fleste.

### Event-Driven Architecture
Komponenter kommunikerer via hændelser snarere end direkte kald. Løs kobling, udvidelsesvenlig. Naturlig for AI-pipelines.

### Pipes and Filters
Data flyder gennem sekvens af processing-steps. Unix-inspireret. Naturligt mønster for data/AI-pipelines.

### Plugin-arkitektur
Kernesystem med udvidelsespunkter. VSCode, WordPress, Obsidian. Nyttigt for stabil kerne med hyppige eksperimenter.

### Hexagonal Architecture (Ports and Adapters)
Forretningslogik i midten, omgivet af ports og adapters. Uafhængig af infrastruktur. Testbar uden infrastruktur.

---

## 18. PLANLÆGNING OG ESTIMERING

**Abstract:** Planlægning og estimering handler om at navigere usikkerhed - at finde ud af hvad der skal bygges, hvor lang tid det tager, og hvad der kan gå galt. For solo-udviklere er dette særligt kritisk: ingen team til at dele byrden, ingen manager til at sætte deadlines. Man bruger metodikker som timeboxing, spikes og iterativ udvikling til at reducere risiko og opretholde momentum. Kerneprincippet er at indrømme usikkerhed og designe processen omkring det: byg vertikale skiver, timebox research, ship hyppigt, og lær af feedback.

### Walking Skeleton
Minimal, kørbar implementering der forbinder alle arkitekturkomponenter end-to-end. Produktionskode fra dag 1. Verificer arkitekturen tidligt.

### Vertical Slicing
Byg tynde end-to-end funktionelle skiver. Leverer værdi tidligt, afslører integrationsproblemer, giver hurtig feedback.

### Spike and Stabilize
(1) Hurtig eksplorativ implementering for at reducere usikkerhed. (2) Stabilisér med tests, fejlhåndtering, dokumentation. Perfekt for nye teknologier.

### Iterativ Udvikling
Korte cyklusser (1-2 uger) med funktionelle leverancer. Plan → implementer → test → reflektér.

### Timeboxing
Fast tidsgrænse, stop når tiden er gået. Forhindrer rabbit holes og perfektionisme. 30-120 minutter for spikes (solo).

### Spike Estimation (NYT)
Spikes bør ikke estimeres med story points. Track tid separat. Formål: reducér usikkerhed, ikke producér artefakter.

### Scope Management
Prioritér hensynsløst. MoSCoW eller simpler: "Hvad er den ene ting der gør mest forskel?" Minimalisme er strategisk fordel.

### AI-assisteret estimering (NYT 2026)
Planning faktorer nu AI-assisterede estimater og low-code prototypes ind. Hurtigere ide-validering.

---

## 19. TESTSTRATEGIER

**Abstract:** Test sikrer at kode virker som forventet og fortsætter med at virke efter ændringer. For solo-udviklere er automatiserede tests særligt vigtige - du er din egen QA, og du kan ikke manuelt teste alt efter hver ændring. Valget af teststrategi handler om at maksimere "confidence per test": integration tests giver ofte mest værdi, unit tests for kompleks logik, og smoke tests som sikkerhedsnet. 2026 bringer AI-assisteret testing der automatisk finder vigtige flows og forudsiger fejlpunkter, men fundamenterne forbliver: test de kritiske stier, catch regressions, og verifiér at systemet starter.

### Smoke Tests
Hurtige tests der verificerer at basale funktioner virker. Mest cost-effective metode til at fange grove fejl. 30 sekunder, 80% af fejl.

### Integration Tests
Tester at komponenter virker sammen. Fanger fejl i grænseflader. Ofte vigtigere end unit tests for små systemer.

### Property-Based Testing
Definér egenskaber koden bør opfylde, framework genererer tilfældige inputs. Hypothesis (Python), fast-check (JS). Effektivt til kanttilfælde.

### Test-pyramiden (og alternativer)
Klassisk: mange unit (bund), færre integration (midte), få E2E (top). "Trofæet" (Kent C. Dodds): fokusér på integration.

### Regression Testing
Hver bug-fix starter med en test der fanger buggen. Bygger gradvist testsuite af faktiske problemer. Mest værdifulde test-vane.

### AI-assisteret Testing (NYT 2026)
AI finder automatisk vigtige flows, analyserer service-interaktioner, forudsiger fejlpunkter. Hurtigere, smartere smoke tests.

---

## 20. SOLO DEVELOPER STRATEGIER

**Abstract:** Solo-udvikling har unikke udfordringer og fordele. Udfordringer: du er single point of failure for al viden, ingen code review, let at grave sig ned i rabbit holes. Fordele: ingen kommunikations-overhead, hurtig beslutningstagning, fuld kontrol. Man kompenserer for udfordringerne med disciplin: dokumentér beslutninger (ADRs), automatisér kvalitetssikring, review egen kode efter 24 timer. AI-augmented development er solo-udviklerens største force multiplier - 40-70% produktivitetsgevinster ved at restructurere workflow til AI-first.

### Framework vs. Build Your Own
Brug frameworks for kendte problemer (auth, routing, ORM), byg selv for domæne-specifik logik. Vælg frameworks med lav kobling.

### Managing Complexity Alone
Skriv ADRs, brug konsistent kodeorganisering, automatisér alt, hold teknisk gæld-liste, review egen kode efter 24 timer.

### Cognitive Load Management
Skriv ting ned, automatisér rutiner, brug checklister, hold systemer simple, sæt loft for samtidige projekter. Context switching koster 15-25 min/skift.

### AI-Augmented Development (NYT 2026)
Behandl AI som collaborator, ikke autocomplete. 40-70% produktivitetsgevinster. Prototype 3-5x hurtigere. Bevar raw skills med periodisk AI-fri kodning.

### Shipping og Scope
Ship dagligt/ugentligt. Minimum Viable Feature > MVP. "Done is better than perfect." Feature flags til at separere deploy fra release.

### Asynchronous Operations
Dokumentér workflows, brug dashboards, automatisér notifications. Dyb fokus uden interruptions.

### Version Control Best Practices (NYT)
Scan commits for at briefe AI. Paste git diffs i prompts. Robust CI: tests på hver commit, style checks, staging deploys.

### Vibe Coding (NYT 2026)
AI-augmenteret prototyping der overvinder blank page problem. GitHub Spark tillader voice-driven coding. Turn ideas into working MVPs.

---

## 21. TEKNISK GÆLD

**Abstract:** Teknisk gæld er akkumulerede kompromiser i kodebasen - hurtige løsninger, manglende tests, outdated dependencies - der gør fremtidige ændringer sværere og langsommere. Som finansiel gæld akkumuleres den med "renter" over tid. Man håndterer teknisk gæld ved at gøre den synlig (gæld-liste), prioritere baseret på impact (Quadrant Method, 80/20), og afsætte dedikeret tid til afbetaling. For solo-udviklere er kontinuerlig, inkrementel afbetaling bedre end store "cleanup sprints" - boy scout-reglen: efterlad koden bedre end du fandt den.

### Prioriteringsstrategier
Quadrant Method: klassificér efter cost-to-fix og impact. 80/20 Rule: målret de mest forstyrrende 20% af codebasen.

### Sprint Allocation
20% af sprints til gældsafbetaling, 80% til features. Holder codebasen ren uden at ofre velocity.

### Inkrementel Afbetaling
Boy scout-regel: efterlad koden bedre end du fandt den. Byg gældsbehandling ind i regulært workflow.

### Automatiserede Tools (NYT)
OpenRewrite: automatiseret refactoring fra dage til minutter. JetBrains ReSharper: automatiserede operationer.

### ROI-baseret Beslutningstagning
Mål impact af refactoring. Brug data til at beslutte baseret på langsigtet værdi.

### Eksplicit Gæld-liste
Hold en synlig liste over kendt gæld. Prioritér efter påvirkning af daglig produktivitet.

### 2026 Outlook (NYT)
75% af tech decision-makers forventer moderate-to-severe gæld-niveauer drevet af accelereret AI-adoption.

---

## 22. REFACTORING

**Abstract:** Refactoring er processen med at forbedre kodens interne struktur uden at ændre dens eksterne adfærd. Det handler om at gøre kode lettere at forstå, vedligeholde og udvide. Man refactorer når man identificerer code smells (duplikeret kode, lange metoder, store klasser) eller før man tilføjer nye features (preparatory refactoring). Nøglen er at gøre det i små, testede skridt - aldrig store "big bang" omskrivninger uden tests. AI-powered refactoring (2026) automatiserer rutine-forbedringer og foreslår sofistikerede optimeringer.

### Red-Green-Refactor
Skriv fejlende test (Red) → minimum kode til at passere (Green) → forbedre med test som sikkerhedsnet (Refactor).

### Refactoring by Abstraction
Identificér fælles funktionalitet, udtræk til abstrakt klasse/interface. Reducerer duplikering, fremmer genbrug.

### Composing / Simplifying Methods
Bryd lange metoder op, udtræk hjælpefunktioner, forenkle kompleks logik.

### Preparatory Refactoring
Rens struktur FØR nye features, så ændringer passer glat ind.

### Hvornår Refactorer
Code smells: duplikeret kode, store klasser, lange metoder, globale variable. Før ny feature. Efter test er på plads.

### Små Skridt
Refactor inkrementelt for at undgå at introducere bugs. Robust testdækning FØRST.

### AI-Powered Refactoring (NYT)
IDE'er (IntelliJ, VS Code, Eclipse) automatiserer rename, extract method, etc. AI foreslår sofistikerede optimeringer.

---

## 23. DOKUMENTATION

**Abstract:** Dokumentation er kommunikation med dit fremtidige selv og andre udviklere. Den forklarer HVORFOR kode er skrevet som den er, hvad systemet gør, og hvordan man bruger det. Man investerer i dokumentation der lever tæt på koden og vedligeholdes som del af udviklings-workflow. Architecture Decision Records (ADRs) er særligt værdifulde for solo-udviklere: om 6 måneder husker du ikke hvorfor du valgte Qdrant over Pinecone - ADR'en fortæller dig det. God dokumentation er kort, fokuseret, og svarer på "hvorfor" snarere end "hvad".

### Architecture Decision Records (ADR)
Korte dokumenter: Kontekst, Beslutning, Konsekvenser, Status. 1-2 sider. Gem i `/docs/adr/`. Append-only: gamle beslutninger superseded, aldrig ændret.

### ADR Best Practices (NYT)
Hold dem korte, fokusér på én beslutning. Meetings: 30-45 min max. Living documents med datostemplede opdateringer. Markdown i source control.

### Documentation-as-Code
Dokumentation lever med koden, vedligeholdes som kode, versioneres med koden. README, inline kommentarer (HVORFOR), genereret API-docs.

### Self-Documenting Code
Beskrivende navne, små funktioner (20-30 linjer), klar struktur, eksplicitte typer. Kommentarer forklarer HVORFOR, kode forklarer HVAD.

### Changelog og Commit-historik
Konventionelle commits (feat:, fix:, docs:, refactor:). CHANGELOG.md. Commits der forklarer HVORFOR, ikke bare HVAD.

### Mappestruktur
Klar, forudsigelig struktur. Grupper efter feature/domain. Max 3 niveauer dybde. Navne der afslører indhold.

### 2026 Challenge (NYT)
"Hidden ADR syndrome" - beslutninger dokumenteret men arkiveret og glemt. Hold dokumentation tilgængelig, søgbar, aktuel.

---

# KILDER

## AI/Memory Sources
- [LakeFS: Best Vector Databases](https://lakefs.io/blog/best-vector-databases/)
- [Shakudo: Top 9 Vector Databases 2026](https://www.shakudo.io/blog/top-9-vector-databases)
- [DataCamp: Best Vector Databases 2026](https://www.datacamp.com/blog/the-top-5-vector-databases)
- [Shaped: Vector Database Alternatives 2025](https://www.shaped.ai/blog/best-vector-database-alternatives-in-2025)
- [arXiv: RAG Comprehensive Survey](https://arxiv.org/html/2506.00054v1)
- [Meilisearch: 14 Types of RAG](https://www.meilisearch.com/blog/rag-types)
- [Techment: RAG in 2026 Enterprise AI](https://www.techment.com/blogs/rag-in-2026-enterprise-ai/)
- [Chroma Research: Evaluating Chunking](https://research.trychroma.com/evaluating-chunking)
- [Springer: Max-Min Semantic Chunking](https://link.springer.com/article/10.1007/s10791-025-09638-7)
- [Modal: MTEB Leaderboard](https://modal.com/blog/mteb-leaderboard-article)
- [OpenXCell: Best Embedding Models 2026](https://www.openxcell.com/blog/best-embedding-models/)
- [NVIDIA: NV-Embed MTEB](https://developer.nvidia.com/blog/nvidia-text-embedding-model-tops-mteb-leaderboard/)
- [Analytics Vidhya: Top Rerankers for RAG](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/)
- [Medium: Cross-Encoders, ColBERT, LLM Re-Rankers](https://medium.com/@aimichael/cross-encoders-colbert-and-llm-based-re-rankers-a-practical-guide-a23570d88548)
- [Graphlit: Survey of AI Agent Memory Frameworks](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks)
- [Medium: Letta, Mem0, Zep Comparison](https://medium.com/asymptotic-spaghetti-integration/from-beta-to-battle-tested-picking-between-letta-mem0-zep-for-ai-memory-6850ca8703d1)
- [Radiant: Second Brain Apps 2026](https://radiantapp.com/blog/best-second-brain-apps)
- [AFFiNE: Best Second Brain Apps 2026](https://affine.pro/blog/best-second-brain-apps)
- [Remio: AI Native Second Brain Guide](https://www.remio.ai/post/ai-native-second-brain-ultimate-guide)
- [GitHub: Khoj AI Second Brain](https://github.com/khoj-ai/khoj)
- [GetMaxim: Context Window Management](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- [JetBrains Research: Efficient Context Management](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)
- [Superlinked: Hybrid Search & Reranking](https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking)
- [Infiniflow: Best Hybrid Search Solution](https://infiniflow.org/blog/best-hybrid-search-solution)
- [Neo4j: Knowledge Graph Generation](https://neo4j.com/blog/developer/knowledge-graph-generation/)
- [Meilisearch: GraphRAG Guide 2026](https://www.meilisearch.com/blog/graph-rag)
- [Pinecone: Conversational Memory](https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/)
- [Snap Research: LoCoMo Dataset](https://snap-research.github.io/locomo/)
- [MarkTechPost: Memory-Driven AI Agents](https://www.marktechpost.com/2026/02/01/how-to-build-memory-driven-ai-agents-with-short-term-long-term-and-episodic-memory/)
- [RAGAS Docs: Available Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [Label Your Data: RAG Evaluation 2026](https://labelyourdata.com/articles/llm-fine-tuning/rag-evaluation)
- [MDPI: Hallucination Mitigation Review](https://www.mdpi.com/2227-7390/13/5/856)
- [InstaTunnel: RAG Poisoning](https://instatunnel.my/blog/rag-poisoning-contaminating-the-ais-source-of-truth-)

## Software Engineering Sources
- [Trio: Software Design Principles 2026](https://trio.dev/software-design-principles/)
- [Scalastic: SOLID, DRY, KISS Principles](https://scalastic.io/en/solid-dry-kiss/)
- [Milan Jovanovic: Modular Monolith](https://www.milanjovanovic.tech/modular-monolith-architecture)
- [Java Code Geeks: Microservices vs Monoliths 2026](https://www.javacodegeeks.com/2025/12/microservices-vs-monoliths-in-2026-when-each-architecture-wins.html)
- [Deep Project Manager: Spike Stories in Agile](https://deeprojectmanager.com/spike-stories-in-agile/)
- [BrowserStack: Smoke Testing 2026](https://www.browserstack.com/guide/smoke-testing)
- [Block Engineering: Testing Pyramid for AI Agents](https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents)
- [Addy Osmani: LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [CodeCondo: Solo Builders Ship Faster 2026](https://codecondo.com/solo-builders-shipping-faster-2026/)
- [Revelo: Technical Debt Prioritization](https://www.revelo.com/blog/rethinking-technical-debt-prioritizing-refactoring-vs-new-features)
- [Monday: Technical Debt Strategies](https://monday.com/blog/rnd/technical-debt/)
- [CodeSee: Code Refactoring Best Practices](https://www.codesee.io/learning-center/code-refactoring)
- [Refactoring.guru: Clean Your Code](https://refactoring.guru/refactoring)
- [AWS: ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [ADR GitHub](https://adr.github.io/)

---

*Genereret: 2026-02-05*
*Pass 2 af Layer 1 Research med fokus på nye fund 2025-2026, abstracts og praktiske perspektiver*
