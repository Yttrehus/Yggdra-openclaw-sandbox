# Ydrasil Pre-Deep Research Report
## AI Memory Systems, Software Engineering & Data Engineering

**Version:** 1.0
**Dato:** 2026-02-05
**Forfatter:** Claude (Opus 4.5) i samarbejde med Kris
**Status:** Layer 1-2 afsluttet. Layer 3 (deep research) afventer.

---

# Indledning

## Formål

Dette dokument samler al research fra Layer 1 (bred survey) og Layer 2 (kildeverificering) i ét struktureret forskningsdokument. Formålet er at give et solidt fundament før vi går i dybden med Layer 3.

Dokumentet besvarer tre spørgsmål:
1. **Hvad findes der?** (Layer 1)
2. **Hvem ved noget om det?** (Layer 2)
3. **Hvem kan vi stole på?** (Layer 2)

## Læsevejledning

**Til Kris:**

Dette dokument er langt. Du behøver ikke læse det hele på én gang. Her er min anbefaling:

1. **Start med Kapitel 8: Konklusion** (side ~50)
   - Det er den kondenserede version af alt
   - 5 minutter at læse
   - Giver dig overblikket

2. **Læs derefter de kategorier der interesserer dig mest**
   - Hvis du vil bygge hukommelse: Kapitel 2 (Memory Systems)
   - Hvis du vil forstå kilder: Kapitel 7 (Kildeverificering)
   - Hvis du vil kode bedre: Kapitel 4 (Software Engineering)

3. **Brug dokumentet som opslagsværk**
   - Når du støder på et begreb (f.eks. "ColBERT"), søg i dokumentet
   - Hver sektion har et abstract der forklarer hvad det er

**Formatering:**
- **Fed tekst** = vigtige begreber
- *Kursiv* = citater eller fremhævelser
- `Monospace` = tekniske termer eller kode
- > Indrykning = citater fra kilder
- Tabeller = sammenligninger og overblik

**Forkortelser:**
- RAG = Retrieval-Augmented Generation
- LLM = Large Language Model
- DB = Database
- API = Application Programming Interface
- MTEB = Massive Text Embedding Benchmark

---

# Kapitel 1: Vektor-Databaser

## 1.1 Abstract

Vektor-databaser gemmer og søger i høj-dimensionelle vektorer (embeddings). De er fundamentet for moderne AI: semantic search, RAG-systemer, anbefalingsmotorer. Man vælger vektor-database når man vil finde "lignende" data baseret på *betydning* snarere end eksakte matches.

**Hvornår relevant:** Når du har tekst, billeder eller andet indhold der skal gøres søgbart baseret på mening, ikke keywords.

**For Ydrasil:** Vi bruger Qdrant. Det var et godt valg - open source, self-hosted, ingen vendor lock-in.

## 1.2 Hovedaktører

### Qdrant (vores valg)
Open-source vektor-database skrevet i Rust. Fokuserer på performance og filtered vector search. Kører lokalt eller i cloud.

**Styrker:** Hurtig, gratis, god dokumentation, aktiv udvikling.
**Svagheder:** Horizontal scaling "still evolving", throughput kan være lavere end alternativer ved høj concurrency.

### Pinecone
Managed (hosted) vektor-database. Ingen infrastruktur at vedligeholde.

**Styrker:** Nul DevOps, hurtig at komme i gang.
**Svagheder:** Premium pris, vendor lock-in, benchmarks favoriserer sig selv.

### Milvus / Zilliz
Distribueret database til milliarder af vektorer. GPU-acceleration.

**Styrker:** Massiv skala, mange indexeringsmetoder.
**Svagheder:** Overkill for små projekter, kompleks at administrere.

### Weaviate
Cloud-native med hybrid search og auto-vektorisering.

**Styrker:** Hybrid search (vektor + keyword), auto-embedding.
**Svagheder:** Ressourcekrævende over 50M vektorer.

### ChromaDB
Letvægts, LLM-fokuseret med LangChain-integration.

**Styrker:** Simpel API, perfekt til prototyping.
**Svagheder:** Ikke til produktion ved stor skala.

### pgvector / pgvectorscale
PostgreSQL-extension. Vektor-search i eksisterende Postgres.

**Styrker:** Nye benchmarks viser 11.4x højere throughput end Qdrant.
**Svagheder:** Kræver Postgres-kendskab.

## 1.3 Konsensus i Feltet

- **HNSW** er den dominerende indexeringsmetode
- **Hybrid search** (vektor + keyword) giver bedre resultater end ren vektor
- Self-hosted vs. managed er trade-off mellem kontrol og convenience

## 1.4 Kontroverser

- **Benchmark-krigen:** Hver vendor hævder at være hurtigst. ANN-Benchmarks er den eneste uafhængige kilde.
- **Throughput vs. latency:** Qdrant har bedre latency, men pgvectorscale har højere throughput.

## 1.5 Kilder

| Kilde | Type | Troværdighed | URL |
|-------|------|--------------|-----|
| ANN-Benchmarks | Benchmark | Høj | ann-benchmarks.com |
| Qdrant Docs | Vendor | Medium | qdrant.tech |
| r/LocalLLaMA | Community | Høj | reddit.com/r/LocalLLaMA |

---

# Kapitel 2: Memory Systems

## 2.1 Abstract

Memory systems giver AI evnen til at huske på tværs af interaktioner. Det løser LLM'ers fundamentale problem: de er stateless. Hver samtale starter fra nul.

**Hvornår relevant:** Når din AI skal huske præferencer, tidligere samtaler, akkumuleret viden, eller lærte rutiner.

**For Ydrasil:** Dette er kernen i projektet. Vi bygger "Claudes hjerne".

## 2.2 RAG-Arkitekturer

### 2.2.1 Hvad er RAG?

RAG (Retrieval-Augmented Generation) kombinerer søgning med generering. I stedet for at LLM'en svarer fra hukommelse, henter den først relevant information fra en vidensbase.

```
Query → Søg i database → Hent relevante dokumenter → Indsæt i prompt → LLM genererer svar
```

### 2.2.2 RAG-Varianter

| Variant | Beskrivelse | Kompleksitet |
|---------|-------------|--------------|
| **Naive RAG** | Simpel: embed → search → generate | Lav |
| **Advanced RAG** | + query rewriting, reranking, filtrering | Medium |
| **Modular RAG** | Udskiftelige komponenter ("LEGO") | Medium |
| **GraphRAG** | + knowledge graphs | Høj |
| **Agentic RAG** | AI vælger selv søgestrategi | Høj |

**Anbefaling:** Start med Naive RAG. Optimer kun når nødvendigt.

### 2.2.3 Kilder

| Kilde | Type | Troværdighed |
|-------|------|--------------|
| Simon Willison | Practitioner | Høj |
| Hamel Husain | Practitioner | Høj |
| Facebook AI Research (original RAG paper) | Academic | Høj |
| LangChain | Vendor | Lav (framework lock-in) |

## 2.3 Chunking-Strategier

### 2.3.1 Hvad er chunking?

Chunking er at opdele dokumenter i mindre stykker til embedding. Det er *undervurderet* - forkert chunking kan ødelægge selv det bedste system.

### 2.3.2 Strategier

| Strategi | Beskrivelse | Hvornår |
|----------|-------------|---------|
| **Fixed-size** | Fast antal tokens | Baseline |
| **Recursive** | Split på naturlige grænser | 80% af cases |
| **Semantic** | Split baseret på betydningsskift | Komplekse docs |
| **Agentic** | LLM beslutter hvor | Dyre dokumenter |

**Konsensus:** RecursiveCharacterTextSplitter med 400-512 tokens er "solid default" (85-90% recall).

**Kontrovers:** Semantic chunking giver 9% bedre recall, men koster ekstra API calls. Er det det værd?

## 2.4 Embedding-Modeller

### 2.4.1 Hvad er embeddings?

Embeddings konverterer tekst til tal-vektorer der fanger betydning. "Hund" og "kat" ligger tæt; "hund" og "bil" ligger langt fra hinanden.

### 2.4.2 Modeller

| Model | Dimensioner | Pris | MTEB Score |
|-------|-------------|------|------------|
| OpenAI text-embedding-3-small | 1536 | $0.02/M tokens | ~62 |
| OpenAI text-embedding-3-large | 3072 | $0.13/M tokens | ~64 |
| Cohere embed-v4 | 1024 | $0.10/M tokens | 65.2 |
| BGE-M3 (open source) | 1024 | Gratis | ~64 |
| NV-Embed (NVIDIA) | - | Lokal | 69.32 (rekord) |

**Anbefaling:** BGE-M3 for open source. OpenAI hvis budget tillader.

**Advarsel:** MTEB er primært engelsk. Test på dansk tekst specifikt.

## 2.5 Re-ranking

### 2.5.1 Hvad er reranking?

Reranking er et andet pass der forbedrer resultater. Første pass henter 50-100 kandidater hurtigt; reranking scorer dem nøjagtigt.

### 2.5.2 Metoder

| Metode | Beskrivelse | Hastighed |
|--------|-------------|-----------|
| **Cross-encoders** | Scorer query+dokument par | Langsom |
| **ColBERT** | Late interaction | Medium |
| **LLM-based** | GPT som judge | Meget langsom |
| **Cohere Rerank** | API-baseret | Hurtig |

**Vurdering for Ydrasil:** Ved vores scale (<100K dokumenter) er reranking sandsynligvis overkill.

## 2.6 Memory Frameworks

### 2.6.1 Aktører

| Framework | Beskrivelse | Bias |
|-----------|-------------|------|
| **Letta (MemGPT)** | OS-inspireret memory hierarki | Medium - startup |
| **Mem0** | Graph-baseret long-term memory | Høj - separate service |
| **LangMem** | LangChain integration | Høj - framework lock-in |

### 2.6.2 MemGPT Konceptet

MemGPT behandler memory som et operativsystem:
- **Core memory** = RAM (i kontekstvinduet)
- **Archival memory** = Disk (vektor-database)

Agenten styrer selv hvad der er hvor.

**Anbefaling:** MemGPT koncepter er akademisk solide. Implementer simple patterns først, undgå framework lock-in.

### 2.6.3 Daniel Miesslers PAI (Personal AI Infrastructure)

Daniel Miessler er security expert, Fabric creator, og ophavsmand til PAI-konceptet. Han er Ydrasils primære forbillede.

**PAI v2.4 (jan 2026) komponenter:**
- **Memory System v7.0:** Struktureret hukommelse (fabric patterns, markdown, vektorer)
- **TELOS:** Formål, mål, værdier (vores TELOS er direkte inspireret)
- **Hook System:** Automatiske workflows trigger ved events
- **Skills System:** Modulære capabilities (vores `.claude/skills/`)
- **Fabric:** CLI-baserede AI patterns (vi bruger `classify_intent`)

**Filosofi:** "System design is more important than model intelligence"

**Relevans:** Miessler er *arkitekten* bag den tilgang vi følger. PAI Blueprint er vores reference-arkitektur.

**Kilder:**
- `docs/PAI_BLUEPRINT.md`
- `data/intelligence_sources.json` (monitorer hans GitHub og podcast)
- danielmiessler.com, github.com/danielmiessler/fabric

### 2.6.4 Nate B. Jones' Memory-Arkitektur

Nate B. Jones (ex-Amazon Prime Video Head of Product, 127K+ YouTube) har beskrevet en memory-arkitektur der matcher Ydrasils setup præcist:

**Hans formel:** `compression + markdown files + agentic systems`

**Nøglekoncepter:**
- **Intent Gap:** Agenter fejler ikke på capabilities men på intent. Løsning: eksternaliseret intent-dokument (vores TELOS)
- **Context Engineering vs. Domain Memory:** "Domain memory er biblioteket. Context engineering er hvad der ligger på skrivebordet." (vores Qdrant + fokuseret retrieval)
- **Attention Drowning:** Selv 100K+ context windows degraderer når fyldt. Løsning: fokuseret hentning (vores `ctx` kommando)

**Relevans:** Jones beskriver præcis den arkitektur vi allerede har bygget. Vi er foran kurven.

**Kilder:**
- `docs/NATE_JONES_ANALYSE.md` (30 videoer analyseret)
- `research/NATE_JONES_5_VIDEOER_2026-02.md`
- `data/substack/natesnewsletter/` (nyhedsbrev)

## 2.7 Kilder (Memory Systems)

| Kilde | Type | Troværdighed | Relevans |
|-------|------|--------------|----------|
| Charles Packer (Letta) | Academic/Vendor | Høj | Høj |
| "Memory in the Age of AI Agents" (Dec 2025) | Academic | Høj | Høj |
| Leonie Monigatti | Educator | Høj | Høj |
| ICLR 2026 MemAgents Workshop | Academic | Høj | Medium |

---

# Kapitel 3: Context & Hybrid Search

## 3.1 Context Window Management

### 3.1.1 Abstract

Context window management handler om at maksimere værdien af LLM'ens begrænsede input. Selvom vinduer er vokset (200K+), falder performance ved lange kontekster, og costs stiger.

### 3.1.2 Strategier

| Strategi | Beskrivelse |
|----------|-------------|
| **Buffer** | Gem alt (umuligt for lange samtaler) |
| **Sliding window** | Behold seneste N interaktioner |
| **Hierarkisk opsummering** | Ældre = opsummeret, nyere = ordret |
| **Extractive compression** | Vælg vigtige sætninger ordret |

**Konsensus:** "Lost in the middle" - information i midten af konteksten ignoreres.

**Anbefaling:** Claude's 200K er vores styrke. Brug RAG for persistence + context for reasoning.

## 3.2 Hybrid Search

### 3.2.1 Abstract

Hybrid search kombinerer keyword-matching (BM25) med semantisk søgning (vektorer). BM25 finder eksakte matches; vektorer finder betydningsligheder.

### 3.2.2 Metoder

| Metode | Beskrivelse |
|--------|-------------|
| **BM25 + Dense** | Standard kombination |
| **RRF (Reciprocal Rank Fusion)** | Kombiner rankings uden parametre |
| **Three-way** | BM25 + dense + sparse (IBM research) |

**Konsensus:** Hybrid search forbedrer recall 15-30% over enkeltmetoder.

**IBM Research:** Three-way retrieval + ColBERT reranker når NDCG 0.93.

---

# Kapitel 4: Software Engineering

## 4.1 Abstract

Software engineering principper sikrer at kode er vedligeholdelig, forståelig og robust. For solo-udviklere er dette særligt vigtigt - du er din egen QA, code reviewer, og arkitekt.

## 4.2 Design Principper

### 4.2.1 SOLID

| Princip | Betydning |
|---------|-----------|
| **S**ingle Responsibility | Én klasse, ét ansvar |
| **O**pen/Closed | Åben for udvidelse, lukket for ændring |
| **L**iskov Substitution | Subtyper skal kunne erstatte basetyper |
| **I**nterface Segregation | Mange små interfaces > ét stort |
| **D**ependency Inversion | Afhæng af abstraktioner, ikke implementeringer |

### 4.2.2 KISS, DRY, YAGNI

- **KISS** (Keep It Simple): Simplicitet reducerer fejl
- **DRY** (Don't Repeat Yourself): Én autoritativ repræsentation
- **YAGNI** (You Aren't Gonna Need It): Implementer kun når nødvendigt

**Advarsel:** DRY kan overdrives. Duplikering er bedre end forkert abstraktion.

### 4.2.3 Kilder

| Kilde | Type | Troværdighed | Advarsel |
|-------|------|--------------|----------|
| Martin Fowler | Practitioner | Høj | - |
| Kent Beck | Practitioner | Høj | TDD advocacy |
| Robert C. Martin (Uncle Bob) | Practitioner | Medium | Dogmatisk, kontroversiel |

## 4.3 Arkitekturmønstre

### 4.3.1 Modulær Monolit

Én deploybar applikation med velafgrænsede moduler. Shopify og GitHub bruger det.

**For Ydrasil:** Dette er det rigtige valg. Microservices er overkill for solo dev.

### 4.3.2 2026-Trend

> "Organisationer der rushed til microservices konsoliderer tilbage til enklere strukturer."

## 4.4 Solo Developer Strategier

### 4.4.1 Pieter Levels

$3.1M/år som solo developer. NomadList, RemoteOK, PhotoAI.

**Principper:**
- Ship fast
- Simpel tech stack
- Building in public
- Radikalt transparent om failures

**Relevans for Ydrasil:** Ekstrem høj.

### 4.4.2 Praktiske Tips

- **Automatisér kvalitetssikring** (du har ingen code reviewer)
- **Dokumentér beslutninger** (ADRs - du glemmer hvorfor om 6 måneder)
- **Review egen kode efter 24 timer** (friske øjne)
- **Context switching koster 15-25 min/skift**

## 4.5 Teknisk Gæld

### 4.5.1 Definition

Akkumulerede kompromiser der gør fremtidige ændringer sværere. Som finansiel gæld: akkumuleres med "renter".

### 4.5.2 Håndtering

| Strategi | Beskrivelse |
|----------|-------------|
| **80/20 Rule** | Målret de mest forstyrrende 20% |
| **Boy Scout Rule** | Efterlad koden bedre end du fandt den |
| **20% allocation** | 20% af tid til gæld, 80% til features |

---

# Kapitel 5: Data Engineering

## 5.1 Abstract

Data engineering handler om at flytte, transformere og kvalitetssikre data. For AI-systemer er det fundamentet - garbage in, garbage out.

## 5.2 Data Quality

### 5.2.1 Dimensioner

| Dimension | Beskrivelse |
|-----------|-------------|
| **Accuracy** | Er data korrekt? |
| **Completeness** | Mangler der felter? |
| **Consistency** | Er formatet ensartet? |
| **Timeliness** | Er data opdateret? |

### 5.2.2 Tools

| Tool | Beskrivelse | Relevans |
|------|-------------|----------|
| Great Expectations | Open source validation | Medium |
| Pydantic | Python type validation | Høj |
| Soda | Data quality monitoring | Lav |

## 5.3 Schema Design

### 5.3.1 For Ydrasil

Vores Qdrant collections bruger forskellige payload-felter (`embed_text`, `content`, `document`). Dette er teknisk gæld.

**Anbefaling:** Standardisér til ét felt-navn på tværs af alle collections.

## 5.4 ETL/ELT Pipelines

### 5.4.1 Tools

| Tool | Beskrivelse | Relevans |
|------|-------------|----------|
| Airflow | De facto standard | Overkill |
| Dagster | Asset-centric | Medium |
| Prefect | Python-first | Medium |
| cron + Python | Simpel | Høj |

**Anbefaling for Ydrasil:** cron + Python scripts. Vi har ikke brug for enterprise orchestration.

---

# Kapitel 6: Knowledge Management

## 6.1 Abstract

Knowledge management tools hjælper med at fange, organisere og genfinde viden. "Second brain" - et eksternt system der udvider din hukommelse.

## 6.2 Tools

### 6.2.1 Obsidian (anbefalet)

Local-first, Markdown, 1566+ plugins. Gratis.

**Styrker:** Du ejer dine data, fungerer offline, massivt plugin-ecosystem.
**Svagheder:** Kræver setup og Markdown-kendskab.

**For Ydrasil:** Vi bruger allerede .md filer. Obsidian er naturlig integration.

### 6.2.2 Notion

All-in-one workspace. Cloud-first.

**Styrker:** Poleret UI, god til teams.
**Svagheder:** Cloud dependency, subscription.

### 6.2.3 Logseq

Open source outliner. Block-baseret.

**Styrker:** Gratis, privacy-fokuseret.
**Svagheder:** Mindre poleret end Obsidian.

## 6.3 Metodikker

### 6.3.1 PARA (Tiago Forte)

- **P**rojects: Aktive projekter med deadline
- **A**reas: Løbende ansvarsområder
- **R**esources: Emner af interesse
- **A**rchive: Inaktivt materiale

**Vores struktur:** `/app/`, `/data/`, `/docs/`, `/research/`, `/archive/` - det er i sig selv et second brain.

### 6.3.2 Zettelkasten

Atomiske noter forbundet via links. Inspiration for MemGPT.

---

# Kapitel 7: Kildeverificering

## 7.1 Abstract

Ikke alle kilder er lige troværdige. Vendors sælger produkter, practitioners har personlige perspektiver, academics kan være teoretiske. Dette kapitel rangerer kilderne.

## 7.2 Top 8 Kilder at Stole På

| Rang | Kilde | Hvorfor |
|------|-------|---------|
| 1 | **Daniel Miessler** | Security expert, Fabric creator, PAI (Personal AI Infrastructure), Unsupervised Learning podcast |
| 2 | **Simon Willison** | 23 års track record, Django co-creator, minimal bias |
| 3 | **Hamel Husain** | 2000+ engineers trænet, O'Reilly bog |
| 4 | **Nate B. Jones** | Ex-Amazon Prime Video Head of Product, AI-strateg, 127K+ YouTube |
| 5 | **Martin Fowler** | 30+ år, skriver om LLM patterns |
| 6 | **ANN-Benchmarks** | Uafhængig akademisk benchmark |
| 7 | **Pieter Levels** | Solo dev gold standard, radikalt transparent |
| 8 | **AI Automators** | YouTube kanal (RAG tutorials, n8n workflows, praktiske implementeringer) |

## 7.3 Top 5 Kilder at Bruge med Forsigtighed

| Rang | Kilde | Advarsel |
|------|-------|----------|
| 1 | **LangChain** | Framework lock-in, bloat, 1+ sek latency |
| 2 | **Vendor benchmarks** | Favoriserer altid sig selv |
| 3 | **Uncle Bob** | Dogmatisk, kontroversiel |
| 4 | **Cloud provider docs** | Lock-in fokus |
| 5 | **AI-first note tools** | Cloud dependency |

## 7.4 Bias-Typer

| Type | Eksempel | Risiko |
|------|----------|--------|
| **Vendor** | Pinecone siger managed er bedst | Sælger produkt |
| **Practitioner** | Én persons erfaring | Ikke generaliserbar |
| **Academic** | Teoretisk paper | Ikke praktisk |
| **Framework** | LangChain docs | Lock-in |

## 7.5 Verificeringsmetode

For hver kilde spurgte vi:
1. **Track record:** Hvor længe aktiv? Hvad har de bygget?
2. **Citationsnetværk:** Hvem citerer hvem?
3. **Bias:** Hvad sælger de? Hvad er deres incitament?
4. **Relevans:** Høj/Medium/Lav for Ydrasil

---

# Kapitel 8: Konklusion

## 8.1 Hvad Vi Lærte

### 8.1.1 AI/Memory

1. **Qdrant var et godt valg** - open source, self-hosted, ingen lock-in
2. **Start med Naive RAG** - kompleksitet kun når nødvendigt
3. **Chunking er undervurderet** - 400-512 tokens er god default
4. **BGE-M3 for embeddings** - open source, konkurrencedygtig
5. **Reranking er overkill** for vores scale
6. **MemGPT koncepter er solide** - implementer simple patterns først

### 8.1.2 Software Engineering

1. **Modulær monolit** - microservices er overkill for solo
2. **Pieter Levels' tilgang** - ship fast, simpel stack
3. **Martin Fowler over Uncle Bob** - nuanceret over dogmatisk
4. **ADRs** - dokumentér beslutninger, du glemmer hvorfor

### 8.1.3 Data Engineering

1. **cron + Python** - enterprise orchestration er overkill
2. **Standardisér schema** - vores payload-felter er teknisk gæld
3. **Pydantic for validation** - simpelt, effektivt

## 8.2 Hvem Vi Stoler På

| Område | Primær Kilde |
|--------|--------------|
| PAI/Fabric/Philosophy | Daniel Miessler |
| RAG/LLM | Simon Willison |
| Evals | Hamel Husain |
| AI Agents & Memory | Nate B. Jones |
| RAG Tutorials (praktisk) | AI Automators (YouTube) |
| Software design | Martin Fowler |
| Vector DB benchmarks | ANN-Benchmarks |
| Solo dev | Pieter Levels |

## 8.3 Hvad Vi Undgår

1. **LangChain** - framework lock-in
2. **Vendor benchmarks** - biased
3. **AI-first note tools** - cloud lock-in
4. **Prematur optimering** - simpelt først

## 8.4 Næste Skridt

| Prioritet | Handling |
|-----------|----------|
| 1 | Vælg 5-7 kategorier til Layer 3 |
| 2 | Læs Simon Willison's blog |
| 3 | Standardisér Qdrant payload-felter |
| 4 | Implementer simple memory patterns |

---

# Litteraturliste

## Akademiske Papers

1. Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Facebook AI Research.*

2. Packer, C. et al. (2023). "MemGPT: Towards LLMs as Operating Systems." *arXiv:2310.08560.*

3. "Memory in the Age of AI Agents: A Survey." (Dec 2025). *arXiv:2512.13564.*

4. "Is Semantic Chunking Worth the Computational Cost?" (2025). *ACL NAACL 2025.*

5. Muennighoff, N. et al. (2022). "MTEB: Massive Text Embedding Benchmark." *HuggingFace.*

6. Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *SBERT.*

7. Khattab, O. & Zaharia, M. (2020). "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction." *Stanford NLP.*

8. "RAGBench: Explainable Benchmark for RAG Systems." (2024). *arXiv:2407.11005.*

## Bøger

9. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code.* 2nd Edition.

10. Beck, K. (2022). *Test-Driven Development: By Example.* 20th Anniversary Edition.

11. Feathers, M. (2004). *Working Effectively with Legacy Code.*

12. Forte, T. (2022). *Building a Second Brain.*

13. Martin, R.C. (2025). *Clean Code: A Handbook of Agile Software Craftsmanship.* 2nd Edition.

14. Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering.*

## Blogs & Online Resources

15. Miessler, D. (2026). "Personal AI Infrastructure (PAI) v2.4." *danielmiessler.com* — Security expert, Fabric creator, Unsupervised Learning podcast. Ophavsmand til PAI-konceptet, TELOS framework, og Fabric patterns.

16. Miessler, D. (2023-2026). "Fabric: Open Source Framework for Augmenting Humans with AI." *github.com/danielmiessler/fabric*

17. Willison, S. (2026). "LLM Predictions for 2026." *simonwillison.net*

18. Husain, H. (2025). "The LLM Evals FAQ." *hamel.dev*

19. Jones, N.B. (2026). "AI News & Strategy Daily." *YouTube (127K+ subscribers)* — Ex-Amazon Prime Video Head of Product. Videoer om AI agents, memory arkitektur, intent gap.

20. AI Automators. (2026). "AI Automators YouTube." *YouTube* — RAG tutorials, n8n workflows, praktiske implementeringer.

21. Liu, J. (2025). "Instructor Documentation." *jxnl.co*

22. Levels, P. (2025). "Indie Hackers Podcast." *levels.io*

23. Fowler, M. (2025). "Technical Debt Quadrant." *martinfowler.com*

## Benchmarks & Leaderboards

20. "ANN-Benchmarks." *ann-benchmarks.com*

21. "MTEB Leaderboard." *huggingface.co/spaces/mteb/leaderboard*

22. "RAGAS Documentation." *docs.ragas.io*

23. "MS MARCO Passage Ranking." *microsoft.com/en-us/research*

## Vendor Documentation

24. "Qdrant Documentation." *qdrant.tech/documentation*

25. "OpenAI Embeddings Guide." *platform.openai.com*

26. "Cohere Rerank Documentation." *cohere.com/rerank*

## Communities

27. r/LocalLLaMA. *reddit.com/r/LocalLLaMA*

28. r/MachineLearning. *reddit.com/r/MachineLearning*

29. Hacker News. *news.ycombinator.com*

30. Write the Docs. *writethedocs.org*

---

# Appendix A: Ordliste

| Term | Definition |
|------|------------|
| **Embedding** | Vektor-repræsentation af tekst der fanger semantisk betydning |
| **RAG** | Retrieval-Augmented Generation - kombiner søgning med LLM |
| **Chunking** | Opdeling af dokumenter i mindre stykker |
| **Reranking** | Andet pass der forbedrer søgeresultater |
| **HNSW** | Hierarchical Navigable Small World - indexeringsmetode |
| **BM25** | Best Matching 25 - klassisk keyword-søgning |
| **Cross-encoder** | Model der scorer query og dokument sammen |
| **Bi-encoder** | Model der embedder query og dokument separat |
| **MTEB** | Massive Text Embedding Benchmark |
| **ADR** | Architecture Decision Record |
| **PARA** | Projects, Areas, Resources, Archive |

---

# Appendix B: Ydrasil-Specifik Kontekst

## Nuværende Setup

| Komponent | Valg |
|-----------|------|
| Vector DB | Qdrant (self-hosted) |
| LLM | Claude (Anthropic) |
| Embedding | OpenAI text-embedding-3-small |
| Hosting | Hostinger VPS |
| Klassificering | Fabric patterns |

## Collections i Qdrant

| Collection | Antal vektorer | Formål |
|------------|----------------|--------|
| routes | 40,000 | Rutedata |
| sessions | 13,500 | Samtalehistorik |
| knowledge | 246 | Manualer |
| docs | 164 | Projektdokumentation |
| conversations | 81 | Strukturerede samtaler |

## Teknisk Gæld

1. **Payload-felter ikke standardiserede** - `embed_text`, `content`, `document`
2. **Ingen systematisk evaluering** af retrieval-kvalitet
3. **Chunking ikke optimeret** til vores dokumenttyper

---

*Dokumentet er genereret 2026-02-05 og repræsenterer status efter Layer 1-2 research.*

*Næste version vil inkludere Layer 3 (deep research med Blue/Red team perspektiver).*
