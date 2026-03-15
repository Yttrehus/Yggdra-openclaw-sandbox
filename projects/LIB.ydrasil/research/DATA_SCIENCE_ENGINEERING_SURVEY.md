# Data Science & Data Engineering Survey for Personal AI Systems

**Dato:** 2026-02-05
**Formål:** Research survey om data science og data engineering koncepter relevante for et personligt AI-system med vektor-database og RAG.

---

## 1. Data Mapping & Lineage

**Abstract:**
Data lineage handler om at spore data fra kilde til destination - at forstå hvor data kommer fra, hvordan det transformeres undervejs, og hvor det ender. For et personligt AI-system er dette kritisk for at debugge retrieval-problemer ("hvorfor fik jeg dette resultat?"), forstå data-flow gennem pipelines, og sikre reproducerbarhed. Moderne tilgange kombinerer runtime emission, statisk parsing og system-level telemetri for komplet sporbarhed.

### OpenLineage
En åben standard for metadata og data lineage indsamling. Integrerer med moderne datatools som Apache Airflow, Spark og dbt. Selve visualiseringen og aggregeringen håndteres af værktøjer der overholder standarden (f.eks. Marquez). Ideel til at skabe et fælles sprog på tværs af forskellige pipeline-komponenter.

### Apache Atlas
Governance og metadata framework, primært brugt i Hadoop-økosystemer. Understøtter klassificering og lineage, men kan være udfordrende at implementere for ikke-Hadoop miljøer. Bedst egnet til enterprise on-prem setups snarere end personlige projekter.

### dbt Native Lineage
dbt genererer automatisk lineage for transformationslaget. Atlan og lignende værktøjer kan udtrække metadata automatisk fra dbt. For personlige projekter er dbt's indbyggede docs ofte tilstrækkeligt til at forstå transformation-flow.

### Lightweight Alternativer
For solo developers: Start med manuel dokumentation i form af flow-diagrammer eller simple markdown-filer der beskriver data-flow. Brug dbt's native docs hvis du arbejder med SQL transformationer. OpenLineage kan integreres gradvist efterhånden som kompleksiteten stiger.

---

## 2. Schema Design for AI/ML

**Abstract:**
Schema design for AI/ML handler om hvordan man strukturerer data optimalt til embeddings og retrieval. Det inkluderer valg af embedding-model, chunk-størrelse, metadata-felter og indexeringsstrategier. God schema design er fundamentet for effektiv RAG - det afgør både retrieval-kvalitet og system-performance. Konsistens på tværs af collections er afgørende for at undgå "drift" i data-kvalitet over tid.

### Embedding Model Konsistens
Brug én embedding model konsekvent for hele databasen. Populære valg inkluderer open source modeller (all-MiniLM-L6-v2, bge-small-en) eller vendor-specifikke (OpenAI text-embedding-3-small). Blanding af modeller giver inkonsistente similarity scores og forringer retrieval-kvalitet.

### Chunking Strategier
Tekst opdeles i chunks baseret på sætningsstruktur, token-grænser eller semantisk betydning. Chunk-størrelse er en afvejning: for små chunks mister kontekst, for store chunks fortynder relevans. Typisk interval er 256-1024 tokens, men optimal størrelse afhænger af use case.

### Metadata Design i Vektor Databases
Gem vektorer sammen med rig metadata: source, owner, date, region, access_level, product, version. Qdrant understøtter JSON-baserede filtre der integrerer effektivt med vektor-søgning. Design metadata-schema med fremtidige filter-behov in mente.

### Indexeringsstrategier
HNSW (Hierarchical Navigable Small World) graphs og IVF (Inverted File) indexes reducerer søgekompleksitet til logaritmisk tid. Vælg mellem cosine similarity (bedst for normaliserede text embeddings) og dot product (hurtigere, kræver normalisering). Pre-filtering vs post-filtering påvirker både hastighed og recall.

### Hybrid Search
Kombiner vektor-søgning med keyword/BM25 søgning for bedre resultater. Anbefalet pipeline: (1) filtrer på metadata, (2) kør vektor-søgning, (3) anvend keyword-søgning for at sikre eksakte termer matcher.

---

## 3. Data Quality & Validation

**Abstract:**
Data quality er ifølge dbt Labs' 2025 State of Analytics Engineering Report den største udfordring for 56% af data professionals. For AI-systemer er datakvalitet direkte korreleret med output-kvalitet - garbage in, garbage out. Validering bør ske på flere niveauer: input-validering, transformation-validering og output-validering. Moderne teams bruger ofte flere værktøjer: Pandera til udvikling, Deepchecks til model-validering, og Evidently til production monitoring.

### Great Expectations
Det mest populære bibliotek til data validering. Bedst til serious production environments med wholesale automation. Har indbygget funktionalitet der trigger actions ved validation failures. Kan være overkill for personlige projekter, men skalerer godt.

### Pandera
Stærkt valg for dataframe-validering i mixed teams. Kombinerer column-level validation med statistisk hypothesis testing. Check-systemet understøtter både simple og sofistikerede validerings-logikker. God balance mellem power og simplicity for solo developers.

### Pydantic
Fokuserer på schema validation snarere end dataframe validation. Ideel til validering af user input fra API'er eller forms. Mere fleksibel og kan bruges til non-tabular data, men kræver mere setup for dataframe-use cases. Pandantic bridger Pydantic og Pandas.

### Lightweight Validation
For solo developers: Start med simple assertions i Python scripts. Brug Pydantic for API input validation. Tilføj Pandera gradvist for kritiske dataframes. Great Expectations først når du har behov for automatiseret alerting og actions.

---

## 4. ETL/ELT Pipelines

**Abstract:**
ETL (Extract, Transform, Load) vs ELT (Extract, Load, Transform) repræsenterer to paradigmer for data pipelines. ELT er blevet dominerende med cloud data warehouses der har billig compute. For personlige AI-systemer er valget ofte mellem enterprise orchestrators (Airflow, Dagster, Prefect) og lightweight alternativer (cron + Python scripts). Nøglen er at starte simpelt og skalere kompleksiteten efterhånden som behovene vokser.

### Apache Airflow
Industri-standard for workflow orchestration. Kraftfuld DAG-baseret scheduling, men har stejl learning curve og betydelig overhead. Bedst for teams med dedikerede data engineers. Overkill for de fleste personlige projekter.

### Dagster
Bedst for data asset lineage, stærk local dev experience, og pipelines der skal opføre sig som well-tested software. Modellerer data assets native, hvilket giver bedre visibility og governance. God balance mellem power og developer experience.

### Prefect
Maximum flexibility med Python-first authoring og minimal boilerplate. Intuitivt API og god local dev story. Bedst for dynamic, event-driven workflows. Mangler native data asset modeling, hvilket kan begrænse visibility for interdependent data platforms.

### Lightweight for Solo Developers
Brug cron + Python scripts til simple pipelines. Biblioteker som Petl, Bonobo og standard Pandas er begyndervenlige. Shell scripts med cron kan håndtere overraskende komplekse ETL-flows. Opgradér til Prefect eller Dagster når pipeline-kompleksiteten kræver det.

### Praktisk Anbefaling
Start med: cron job → Python script med Pandas/Petl → logging til fil. Tilføj gradvist: error handling, retry logic, alerting. Migrér til Prefect/Dagster når du har >5 interdependente pipelines eller behov for UI-baseret monitoring.

---

## 5. Feature Engineering for Retrieval

**Abstract:**
Feature engineering for RAG-systemer handler om at udtrække og konstruere meningsfulde features fra samtalelogger, brugerinteraktioner og kontekstuel metadata for at forbedre både retrieval accuracy og generation coherence. De rigtige features kan dramatisk forbedre relevansen af retrieved documents. Moderne tilgange bruger SHAP values og feature ablation studies til at identificere de mest impactfulde signaler.

### Temporal Features
Tidsstempler muliggør recency-biased retrieval ("vis nyeste først") og time-aware relevance. Memory-systemer bruger temporal features til at prioritere nyere samtaler. Inkludér created_at, updated_at og optionally access_count/last_accessed.

### Metadata Enrichment
Tilføj kontekst som author, source, date, kategori eller andre klassifikationer. Jo rigere metadata, jo bedre filter-muligheder. Automatisk enrichment (f.eks. sentiment scores, time-of-day tags) kan give inkrementelle forbedringer i retrieval relevans.

### Entity Features
Link dokumenter til entiteter (personer, steder, organisationer, produkter). Named Entity Recognition (NER) kan automatisere denne proces. Entity features muliggør queries som "find alt om kunde X" på tværs af forskellige dokument-typer.

### Relational Features
Spor relationer mellem dokumenter (links, citations, replies-to, parent-child). Knowledge graphs kan modellere komplekse relationer. For personlige systemer: simple "related_to" arrays kan være tilstrækkeligt til at capture vigtige forbindelser.

### Feature Integration
Features kan integreres i: (1) selve embeddings (via prompt engineering), (2) ranking algorithms (boost-factors), eller (3) prompt logic (inkludér metadata i context). Test hvilken approach der virker bedst for dit use case.

---

## 6. Data Profiling

**Abstract:**
Data profiling handler om at forstå din data - distributions, outliers, missing values, mønstre og anomalier. For AI-systemer er profiling essentielt for at opdage data quality issues før de påvirker model performance. Det er også et diagnostisk værktøj til at forstå hvorfor retrieval performer som det gør. God profiling giver indsigt i "hvad er normalt" så du kan opdage "hvad er unormalt".

### YData Profiling (tidligere Pandas Profiling)
One-line EDA (Exploratory Data Analysis) der genererer omfattende HTML-rapporter. Version 4.x understøtter både Pandas og Spark DataFrames. Features inkluderer univariate/multivariate profiling, missing data identification, outlier detection, og PII håndtering. Primary drawback: performance issues med store datasets.

### Profiling Metrics
Kernemålinger inkluderer: cardinality (unikke værdier), completeness (% non-null), distribution (mean, median, percentiles), patterns (regex matches), og correlations (mellem kolonner). For vektor databases: embedding space analysis kan afsløre clustering og outliers.

### Automatiseret vs Manuel Profiling
Automatiseret profiling (YData, Great Expectations profiler) giver hurtig overview. Manuel profiling (custom queries, visualiseringer) giver dybere indsigt i specifikke issues. Kombiner begge: automatiseret til baseline, manuel til investigation.

### Lightweight Approach
For solo developers: Start med Pandas `.describe()` og `.info()`. Tilføj YData Profiling for periodiske deep-dives. Implementér simple assertions der checker for uventede distributions (f.eks. "chunk_count bør være mellem 100-10000").

---

## 7. Master Data Management (MDM)

**Abstract:**
Master Data Management handler om at skabe "golden records" - den ene, autoritative version af en entitet (kunde, produkt, lokation) på tværs af alle systemer. Entity resolution identificerer når to records repræsenterer samme real-world entitet (f.eks. "Jon Doe" og "Jonathan Doe" er samme person). For personlige AI-systemer er dette relevant for at undgå duplikerede entiteter der forvirrer retrieval og analyse.

### Entity Resolution
Kombinerer rules (eksakte matches), probabilistic methods (fuzzy matching), machine learning (trained matchers), og graph analysis (relationship patterns). AI-native MDM er mere effektiv end traditionelle rules-based approaches for komplekse datasets. For personlige projekter: start med simple rules, tilføj fuzzy matching ved behov.

### Golden Records
Den konsoliderede version af en entitet der merger attributter fra alle kilder. Survivorship rules afgør hvilken værdi der "vinder" ved konflikter (f.eks. mest recent, mest komplet, trusted source). Implementér simple survivorship: prefer verified > recent > first-seen.

### Deduplicering
Fjern duplicate records inden for samme dataset. Forskellen fra entity resolution: deduplicering = samme dataset, entity resolution = på tværs af datasets. Teknikker: exact matching, fuzzy matching (Levenshtein distance), phonetic matching (Soundex, Metaphone).

### Praktisk Implementation
For personlige systemer: (1) Definer hvad der udgør en "entitet" (kunde, lokation, etc.), (2) Implementér ID-baseret deduplicering først, (3) Tilføj fuzzy matching for navn/adresse felter, (4) Opret linking tables der mapper duplicates til canonical records.

---

## 8. Data Contracts

**Abstract:**
Data contracts er formelle aftaler mellem data producers og consumers om hvad man kan forvente af et data asset - struktur, semantik, kvalitet og SLAs. Ligesom API contracts, men for data. I en data mesh arkitektur er contracts den eneste måde at håndtere schema evolution og sikre reliability på tværs af distribuerede teams. For personlige systemer giver contracts dokumentation og guardrails mod breaking changes.

### Contract Komponenter
En data contract specificerer: (1) exact schema (felter og datatyper), (2) value ranges og constraints, (3) refresh frequency/SLA, (4) semantic meaning af felter, og (5) breaking change policy. Machine-readable format (JSON Schema, Protobuf, Avro) muliggør automatiseret validation.

### Schema Evolution
Contracts formaliserer processen for schema-ændringer. Backward-compatible changes (tilføj optional felt) vs breaking changes (fjern felt, ændre type). Semantic Versioning fungerer godt: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for documentation.

### Data Mesh Integration
I data mesh ejer domain teams deres data products og publicerer dem med contracts. Contracts sikrer at consumers kan stole på format og kvalitet. For personlige systemer: tænk på hver collection/table som et "mini data product" med implicit contract.

### Lightweight Implementation
For solo developers: (1) Dokumentér forventet schema i comments eller README, (2) Brug Pydantic models som executable contracts, (3) Implementér validation der checker mod contract ved ingest, (4) Versionér schemas explicit (schema_version felt).

---

## 9. Observability for Data

**Abstract:**
Data observability handler om at monitorere data pipelines og data assets kontinuerligt - ikke bare om de kører, men om data er korrekt, komplet og fresh. Monte Carlo definerede de 5 søjler: Freshness, Distribution, Volume, Schema og Lineage. For personlige AI-systemer giver observability early warning om problemer før de påvirker brugere ("hvorfor er mine embeddings gamle?" eller "hvorfor mangler der data?").

### Freshness
Hvor up-to-date er dine data tables? Spor hvornår tables sidst blev opdateret og sammenlign med forventet cadence. Monte Carlo kan automatisk lære thresholds efter 7-14 dages observation. Simple implementation: timestamp felt + cron job der alerter hvis data er for gammelt.

### Volume & Completeness
Completeness checker for måder data kan være null eller unpopulated. Volume giver indsigt i health af data assets - unexpected drops eller spikes indikerer problemer. Track row counts over tid og alert på anomalier.

### Distribution
Monitor for unexpected changes i data distributions. Numeric fields: mean, median, std dev shifts. Categorical fields: new categories, changed proportions. ML-baserede baselines kan automatisk detektere anomalier.

### Schema Monitoring
Track schema changes: nye kolonner, fjernede kolonner, type changes. Automatic schema detection ved ingest kan fange uventede ændringer. Alert ved breaking changes der kan påvirke downstream systems.

### Tools og Alternativer
**Enterprise:** Monte Carlo, Acceldata, Metaplane - automatisk monitoring med ML-baseret anomaly detection.
**Lightweight:** Custom scripts der logger metrics til database/file. Prometheus + Grafana for visualisering. Simple cron jobs der checker freshness og volume. Start med alerts for de mest kritiske data assets.

---

## Opsummering: Prioritering for Solo Developers

| Kategori | Start Her | Næste Skridt | Enterprise Tool |
|----------|-----------|--------------|-----------------|
| Lineage | Markdown dokumentation | dbt native docs | OpenLineage + Marquez |
| Schema | Konsistent embedding model | JSON metadata design | Formal schema registry |
| Quality | Pydantic + assertions | Pandera | Great Expectations |
| Pipelines | Cron + Python | Prefect | Airflow/Dagster |
| Features | Timestamps + source | Entity extraction | ML feature stores |
| Profiling | Pandas describe() | YData Profiling | Enterprise profilers |
| MDM | ID-based dedup | Fuzzy matching | Tamr, Profisee |
| Contracts | README + Pydantic | JSON Schema | Data Mesh tools |
| Observability | Custom alerts | Metrics dashboard | Monte Carlo |

---

## Kilder

### Data Lineage
- [9 Best Data Lineage Tools in 2026 - Atlan](https://atlan.com/data-lineage-tools/)
- [Top 5 Open Source Data Lineage Tools - Monte Carlo](https://www.montecarlodata.com/blog-open-source-data-lineage-tools/)
- [OpenLineage Blog](https://openlineage.io/blog/)
- [Data Lineage Tracking Complete Guide 2026 - Atlan](https://atlan.com/know/data-lineage-tracking/)

### Schema Design & Vector Databases
- [Vector Databases Guide: RAG Applications 2025 - DEV Community](https://dev.to/klement_gunndu_e16216829c/vector-databases-guide-rag-applications-2025-55oj)
- [Best Vector Databases for RAG 2025 - Latenode](https://latenode.com/blog/ai-frameworks-technical-infrastructure/vector-databases-embeddings/best-vector-databases-for-rag-complete-2025-comparison-guide)
- [10 Best Vector Databases for RAG Pipelines - ZenML](https://www.zenml.io/blog/vector-databases-for-rag)
- [RAG Architecture Best Practices - Schema Sauce](https://schemasauce.com/understanding-genai-rag-infrastructure-best-practices-and-common-pitfalls/)

### Data Quality & Validation
- [The Data Validation Landscape in 2025 - Arthur Turrell](https://aeturrell.com/blog/posts/the-data-validation-landscape-in-2025/)
- [Data Validation Libraries for Polars 2025 - Pointblank](https://posit-dev.github.io/pointblank/blog/validation-libs-2025/)
- [Complete Guide to Data Validation - Medium](https://medium.com/data-science-collective/stop-ml-model-failures-complete-guide-to-data-validation-with-pandera-great-expectations-dbt-d7656eeadfae)

### ETL/ELT Pipelines
- [Airflow vs Dagster vs Prefect 2026 - Bix Tech](https://bix-tech.com/airflow-vs-dagster-vs-prefect-which-workflow-orchestrator-should-you-choose-in-2026/)
- [ETL Frameworks in 2026 - Integrate.io](https://www.integrate.io/blog/etl-frameworks-in-2025-designing-robust-future-proof-data-pipelines/)
- [5 Lightweight Python Libraries for ETL - Level Up Coding](https://levelup.gitconnected.com/python-5-lightweight-libraries-that-make-etl-simple-868d4d5bd75b)
- [Cron Jobs in Data Engineering - DataCamp](https://www.datacamp.com/tutorial/cron-job-in-data-engineering)

### Feature Engineering
- [Feature Engineering for RAG System Optimization - ChatNexus](https://articles.chatnexus.io/knowledge-base/feature-engineering-for-rag-system-optimization/)
- [RAG Architectures Guide 2025 - Medium](https://medium.com/data-science-collective/rag-architectures-a-complete-guide-for-2025-daf98a2ede8c)
- [RAG Evolving in 2025 - Medium](https://medium.com/@chandinisaisri.uppuganti/retrieval-augmented-generation-rag-is-evolving-fast-heres-what-engineers-need-to-know-in-2025-708446fe555c)

### Data Profiling
- [YData Profiling Documentation](https://docs.profiling.ydata.ai/)
- [Pandas Profiling Guide - DataCamp](https://www.datacamp.com/tutorial/pandas-profiling-ydata-profiling-in-python-guide)
- [Top Data Profiling Tools 2025 - Atlan](https://atlan.com/know/data-profiling-tools/)

### Master Data Management
- [Golden Record MDM - Profisee](https://profisee.com/platform/golden-record-management/)
- [Entity Resolution Techniques - PuppyGraph](https://www.puppygraph.com/blog/entity-resolution)
- [Guide to Data Deduplication - Tamr](https://www.tamr.com/blog/guide-to-data-deduplication)

### Data Contracts
- [Data Contracts Explained 2026 - Atlan](https://atlan.com/data-contracts/)
- [Data Contracts Explained - Monte Carlo](https://www.montecarlodata.com/blog-data-contracts-explained/)
- [Schema Evolution in Data Mesh - Medium](https://medium.com/@kuhar.deepak/schema-evolution-navigating-the-data-mesh-challenge-6bc192cdd0f3)

### Data Observability
- [What Is Data Observability 2026 - Monte Carlo](https://www.montecarlodata.com/blog-what-is-data-observability/)
- [Top Data Observability Tools 2025 - Metaplane](https://www.metaplane.dev/blog/top-data-observability-tools)
- [Six Dimensions of Data Quality - Monte Carlo](https://www.montecarlodata.com/blog-monitoring-the-six-dimensions-of-data-quality-with-monte-carlo/)
