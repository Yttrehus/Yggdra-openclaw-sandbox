# AI Long-Term Memory for LLM-Agenter: Forskningsrapport

**Dato:** 2026-02-16
**Formaal:** Kortlaegning af state-of-the-art memory-loesninger for LLM-baserede agenter der skal huske paa tvaers af sessioner.
**Kontekst:** Ydrasil-setup med 1 bruger, VPS 4GB RAM, Qdrant vector DB, Claude API.

---

## Indhold

1. [Overblik og Taxonomi](#1-overblik-og-taxonomi)
2. [MemGPT / Letta](#2-memgpt--letta)
3. [Mem0](#3-mem0)
4. [Zep](#4-zep)
5. [Cognee](#5-cognee)
6. [A-MEM (Agentic Memory)](#6-a-mem-agentic-memory)
7. [LangChain/LangGraph Memory](#7-langchainlanggraph-memory)
8. [CrewAI Memory](#8-crewai-memory)
9. [Nyeste Papers (2024-2026)](#9-nyeste-papers-2024-2026)
10. [Praktiske Production Patterns](#10-praktiske-production-patterns)
11. [Context Window Management](#11-context-window-management)
12. [Sammenligning og Anbefaling](#12-sammenligning-og-anbefaling)

---

## 1. Overblik og Taxonomi

Den nyeste forskning (arXiv 2512.13564, januar 2026) foreslaar en tredimensionel taxonomi for agent-memory:

**Memory-former:**
- **Token-level memory** -- information gemt som tekst-tokens i kontekst
- **Parametric memory** -- information lagret i modellens vaegter (fine-tuning)
- **Latent memory** -- kompakte repraesentationer (embeddings, vektorer)

**Memory-funktioner:**
- **Factual memory** -- viden og fakta ("Kris koerer rute 256")
- **Experiential memory** -- indsigter og faerdigheder ("Naar Kris spoerger X, mener han Y")
- **Working memory** -- aktiv kontekststyring (hvad er relevant lige nu)

**Memory-dynamik:**
- **Formation** -- ekstraktion af information fra interaktioner
- **Evolution** -- konsolidering, opdatering, og glemsel over tid
- **Retrieval** -- adgang til gemt information naar den er relevant

Den gamle opdeling "short-term vs long-term" er utilstraekkelig for moderne agent-systemer. Det vigtige er samspillet mellem HVAD der huskes, HVORDAN det lagres, og HVORNAAR det hentes.

---

## 2. MemGPT / Letta

**Kilde:** [Letta docs](https://docs.letta.com/concepts/memgpt/) | [GitHub](https://github.com/letta-ai/letta) | [Paper](https://www.leoniemonigatti.com/papers/memgpt.html)

### Arkitektur

MemGPT behandler LLM'ens context window som en operativsystem-lignende memory-hierarki:

- **Core Memory (in-context)** -- analog til RAM. Altid synlig for modellen. Indeholder bruger-profil og system-instruktioner. Agenten kan selv redigere dette.
- **Recall Memory (out-of-context)** -- analog til disk. Fuld konversationshistorik gemt eksternt. Soegbar via function calls.
- **Archival Memory (out-of-context)** -- analog til ekstern storage. Vector database (Chroma, pgvector, etc.). Ubegreanset kapacitet.

Kernekonceptet: Agenten har **self-editing memory tools** -- den kan selv beslutte hvad der skal flyttes ind og ud af context window. Den "pager" information ind og ud ligesom et OS pager data mellem RAM og disk.

### Status 2025-2026

- MemGPT open-source er omdoebt til **Letta** (september 2024)
- Letta V1 arkitektur (2025): Afskaffer "heartbeats" og `send_message` tool, bruger native reasoning
- Ny feature: **Context Repositories** -- git-baseret versionering af memory
- **Conversations API** -- delt memory paa tvaers af parallelle bruger-interaktioner
- **Letta Code** -- memory-first coding agent som benchmark

### Fordele
- Elegant OS-analogi der skalerer godt konceptuelt
- Agenten styrer selv sin memory (self-managing)
- Open-source med aktiv udvikling
- Understotter flere vector DB backends

### Begraensninger
- Memory-operationer bruger LLM-kald (koster tokens)
- Kompleks arkitektur -- meget overhead for simpel brug
- Kraever Docker for self-hosting
- 4GB RAM VPS: Tight men muligt med Docker (serveren selv er Python, memory er i DB)

### Passer det til Ydrasil?
- **Delvist.** Letta er designet til multi-user, multi-agent scenarier. For 1 bruger + 1 agent er det overkill. Men koncepterne (core memory + archival memory) er vaerdifulde at kopiere. Qdrant understoeettes som archival backend.

### Pris
- Open-source (self-hosted): Gratis
- LLM-kald til memory-operationer: Ekstra tokens per session
- Hosted Letta platform: Pricing ikke offentlig

---

## 3. Mem0

**Kilde:** [mem0.ai](https://mem0.ai/) | [GitHub](https://github.com/mem0ai/mem0) | [Paper: arXiv 2504.19413](https://arxiv.org/abs/2504.19413) | [Qdrant integration](https://qdrant.tech/documentation/frameworks/mem0/)

### Arkitektur

Mem0 er en **memory orchestration layer** der sidder mellem AI-agenter og storage:

**To faser:**
1. **Extraction Phase** -- indsamler tre kontekstkilder: seneste udveksling, rullende summary, og nyeste beskeder. En LLM udtraekker kandidat-memories.
2. **Update Phase** -- intelligente operationer: tilfoej ny memory, opdater eksisterende, slet foraaldet, behold uaendret. Forhindrer bloat via automatisk filtrering og decay-mekanismer.

**Memory-typer:**
- Episodic (hvad skete)
- Semantic (hvad ved vi)
- Procedural (hvordan goer vi)
- Associative (hvad haenger sammen)

### Qdrant Integration (direkte relevant!)

```python
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "memories",
            "host": "localhost",
            "port": 6333,
        }
    }
}

m = Memory.from_config(config)
m.add("Kris koerer rute 256 organisk affald i Aarhus", user_id="kris")
results = m.search("hvilken rute koerer Kris?", user_id="kris")
```

Qdrant er **default** vector store i Mem0.

### Performance
- 26% forbedring i LLM-as-a-Judge metric vs OpenAI baseline
- 91% lavere p95 latency
- 90%+ token-besparelse via memory compression

### Fordele
- Direkte Qdrant-integration (vi har allerede Qdrant koerende)
- Simpelt API -- `add()`, `search()`, `update()`
- Open-source version tilgaengelig
- Automatisk memory-deduplicering og decay
- Understotter Python og JavaScript

### Begraensninger
- Kraever LLM-kald for memory extraction (ekstra tokens)
- Open-source version har faerre features end hosted platform
- Graph memory (knowledge graph) kun i hosted version
- Kraever OpenAI eller kompatibelt LLM endpoint til extraction

### Passer det til Ydrasil?
- **Ja, staerk kandidat.** Mem0 + Qdrant er naesten plug-and-play med vores setup. Simpelt API, lav overhead, og memory-extraction kan bruge Claude API. Perfekt til 1-bruger scenario.

### Pris
- Open-source: Gratis (+ LLM token-forbrug til extraction)
- Hosted platform: Fra $49/mdr (Pro) til enterprise
- Self-hosted estimat: ~$0.01-0.05 per memory-operation (LLM tokens)

---

## 4. Zep

**Kilde:** [getzep.com](https://www.getzep.com/) | [Paper: arXiv 2501.13956](https://arxiv.org/abs/2501.13956) | [Blog](https://blog.getzep.com/state-of-the-art-agent-memory/)

### Arkitektur

Zep bruger en **temporal knowledge graph** arkitektur via sin kerne-engine **Graphiti**:

- **Graphiti** -- temporally-aware knowledge graph engine
- Syntetiserer baade ustruktureret konversationsdata og struktureret forretningsdata
- Opretholder historiske relationer -- forstaar hvordan information aendrer sig over tid
- Entiteter, relationer og fakta med tidsmaerker

**Kerne-flow:**
1. Agent/bruger-interaktion fanges
2. Graphiti ekstraher entiteter og relationer
3. Temporal knowledge graph opdateres (ikke bare append -- sammenfletter og opdaterer)
4. Retrieval via graph-traversal + semantisk soegning

### Performance
- 18.5% accuracy-forbedring over baseline
- 90% latency-reduktion
- Under 2% af baseline token-forbrug
- Overlaegen i cross-session information synthesis

### Fordele
- Knowledge graph giver bedre relational reasoning end ren vektor-soegning
- Temporal awareness -- forstaar at fakta aendrer sig over tid
- State-of-the-art paa DMR (Deep Memory Retrieval) benchmark
- Integrerer med AWS Neptune, OpenSearch

### Begraensninger
- Kraever graph database (Neo4j eller Neptune) -- ekstra infrastruktur
- Mere kompleks setup end Mem0
- Hosted version er primary -- self-hosted kode tilgaengelig men tungt
- 4GB RAM VPS: Neo4j alene kraever ~1-2GB RAM -- tight med Qdrant ogsaa

### Passer det til Ydrasil?
- **Nej, for tungt.** Graph database kraever mere RAM end vi har. Konceptet (temporal knowledge graph) er vaerdifuldt, men implementeringen er for ressourcekraevende til en 4GB VPS der allerede koerer Qdrant + webapp.

### Pris
- Open-source Graphiti: Gratis
- Zep Cloud: Pricing ikke offentligt tilgaengelig
- Self-hosted: Gratis software, men kraever ekstra infra (graph DB)

---

## 5. Cognee

**Kilde:** [cognee.ai](https://www.cognee.ai/) | [GitHub](https://github.com/topoteretes/cognee)

### Arkitektur

Cognee er en **ECL (Extract, Cognify, Load) pipeline** der transformerer raa data til knowledge graphs:

1. **Extract** -- indlaeser fra 30+ datakilder
2. **Cognify** -- genererer embeddings og bygger knowledge graph ("memify")
3. **Load** -- gemmer i vektor DB + graph DB

Retrieval kombinerer tidsfiltre, graph-traversal og vektor-similaritet.

### Fordele
- Open-source (6000+ GitHub stars)
- Stoettter mange datakilder
- Knowledge graph + vektor-soegning hybrid
- Simpelt API (5-6 linjer kode)
- MCP-server tilgaengelig

### Begraensninger
- Tidlig version (v0.3, v1.0 paa vej)
- Kraever graph database for fuld funktionalitet
- Mindre moden end Mem0 og Letta
- Dokumentation under udvikling

### Passer det til Ydrasil?
- **Nej, for tidligt.** Cognee er lovende men endnu ikke moden nok til production. Graph DB-kravet goer det ogsaa for tungt til vores VPS.

### Pris
- Open-source: Gratis
- Cogwit (hosted): Beta, pricing ukendt

---

## 6. A-MEM (Agentic Memory)

**Kilde:** [arXiv 2502.12110](https://arxiv.org/abs/2502.12110) | [GitHub](https://github.com/agiresearch/A-mem) | NeurIPS 2025

### Arkitektur

A-MEM er inspireret af **Zettelkasten-metoden** -- atomiske noter med fleksible links:

1. Naar en ny memory tilfojes, genereres en **struktureret note** med kontekst, keywords og tags
2. Systemet analyserer historiske memories for at finde relevante forbindelser
3. Links etableres hvor meningsfulde ligheder findes
4. **Memory evolution** -- nye memories kan trigger opdateringer af eksisterende memories
5. Selvorganiserende vidensnetvaerk der kontinuerligt forfiner sig

### Fordele
- Elegant design inspireret af bevist vidensstyring (Zettelkasten)
- Dynamisk selvorganisering -- ingen rigid struktur
- State-of-the-art performance paa 6 foundation models
- NeurIPS 2025 paper -- akademisk valideret
- Open-source kode tilgaengelig

### Begraensninger
- Forskningsprojekt -- ikke production-ready framework
- Kraever LLM-kald for hvert memory-link (dyre operationer)
- Ingen managed service
- Integration med eksisterende systemer kraever arbejde

### Passer det til Ydrasil?
- **Som inspiration, ja.** Zettelkasten-tilgangen til agent-memory er elegant og passer godt til vores "second brain" koncept. Kan implementeres manuelt ovenpaa Qdrant med metadata-links.

### Pris
- Open-source: Gratis (+ LLM tokens for memory operations)

---

## 7. LangChain/LangGraph Memory

**Kilde:** [LangChain docs](https://python.langchain.com/docs/versions/migrating_memory/) | [LangGraph](https://python.langchain.com/docs/versions/migrating_memory/conversation_buffer_memory/)

### Status 2025

- `ConversationBufferMemory` er **deprecated** fra LangChain v0.3.1
- Erstattet af **LangGraph checkpointing system**
- To strategier: **Message Buffering** (behold sidste K beskeder) og **Summarization** (erstat aeldre historik med summary)

### Arkitektur

LangGraph bruger checkpointers til state management:
- `InMemorySaver` -- til udvikling
- `SqliteSaver` -- persistent storage
- `PostgresSaver` -- production
- Support for multiple threads og "time travel" (gaa tilbage til tidligere state)

### Fordele
- Tightly integreret med LangChain/LangGraph oekosystemet
- Simpel state management
- Veldokumenteret med migrations-guide

### Begraensninger
- Bundet til LangChain-oekosystemet
- Mere fokuseret paa session-state end aedte long-term memory
- Ingen avanceret memory extraction eller knowledge graph
- Ikke Claude-optimeret

### Passer det til Ydrasil?
- **Nej.** Vi bruger Claude API direkte, ikke LangChain. LangGraph's patterns (buffering + summarization) er dog vaerdifulde at implementere selv.

---

## 8. CrewAI Memory

**Kilde:** [CrewAI docs](https://docs.crewai.com/en/concepts/memory) | [Qdrant integration](https://qdrant.tech/documentation/frameworks/crewai/)

### Arkitektur

Tre built-in memory-typer:
1. **Short-Term Memory** -- ChromaDB + RAG, current session context
2. **Long-Term Memory** -- SQLite3, task-resultater paa tvaers af sessioner
3. **Entity Memory** -- RAG for entiteter (personer, steder, koncepter)

Plus support for eksterne memory-providers (Mem0, etc.).

### Fordele
- Simpelt at aktivere (`memory=True`)
- Understotter Qdrant som vektor-backend
- God til multi-agent workflows

### Begraensninger
- Designet til CrewAI multi-agent framework
- ChromaDB som default (ikke Qdrant)
- Basalt memory-system uden avancerede features

### Passer det til Ydrasil?
- **Nej.** Vi koerer ikke CrewAI. Men tredelingen short/long/entity er et godt pattern at adaptere.

---

## 9. Nyeste Papers (2024-2026)

### Centrale Papers

| Paper | Dato | Hovedbidrag |
|-------|------|-------------|
| [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) | Jan 2026 | Omfattende survey, 3D-taxonomi (form/funktion/dynamik) |
| [A-MEM: Agentic Memory](https://arxiv.org/abs/2502.12110) | Feb 2025 | Zettelkasten-inspireret selvorganiserende memory, NeurIPS 2025 |
| [Mem0 Paper](https://arxiv.org/abs/2504.19413) | Apr 2025 | Production-ready memory layer, extraction + update pipeline |
| [Zep: Temporal Knowledge Graph](https://arxiv.org/abs/2501.13956) | Jan 2025 | Graphiti engine, temporal-aware knowledge graph |
| [Agentic Memory (AgeMem)](https://arxiv.org/abs/2601.01885) | Jan 2026 | Unified STM/LTM management via tool-based actions |
| [Graph-based Agent Memory](https://arxiv.org/html/2602.05665) | Feb 2026 | Taxonomy af graf-baseret memory, teknikker og applikationer |
| [Survey on Memory Mechanism](https://arxiv.org/abs/2404.13501) | Apr 2024 | Survey af memory-mekanismer for LLM-baserede agenter |
| [From Human Memory to AI Memory](https://arxiv.org/abs/2504.15965) | Apr 2025 | 8-kvadrant klassifikation (objekt/form/tid) |

### Noegle-indsigter fra forskningen

1. **Memory er en foersteklasses primitiv** -- ikke en add-on men central for agent-design
2. **Statiske taxonomier fejler** -- memory kraever dynamiske, kontekst-afhaengige strategier
3. **Self-managing memory vinder** -- agenten skal selv kunne beslutte hvad der gemmes/slettes
4. **Temporal awareness er kritisk** -- fakta aendrer sig over tid, memory-systemer maa tracke det
5. **Hybrid tilgange dominerer** -- kombination af vektor-soegning + struktureret data + summarization

---

## 10. Praktiske Production Patterns

### Pattern 1: Dual-Layer Architecture (2025-2026 standard)

```
HOT PATH (in-context):
  - Seneste beskeder (raa)
  - Komprimeret graf-state / summary
  - Bruger-profil + praeferenceer

COLD PATH (ekstern retrieval):
  - Qdrant vektor-soegning for semantisk match
  - Historisk konversationsdata
  - Domaeneviden (ruter, kunder, etc.)

MEMORY NODE (efter hvert turn):
  - Beslut hvad der skal gemmes
  - Opdater bruger-profil
  - Decay/slet irrelevant data
```

### Pattern 2: Summarization Chain

```python
# Pseudokode
if token_count(conversation) > THRESHOLD:
    summary = llm.summarize(older_messages)
    conversation = [system_prompt, summary, recent_messages]
```

Teknikker:
- **Threshold-baseret** -- komprimer naar tokens overstiger X
- **Importance scoring** -- vaegt elementer efter sandsynlig fremtidig relevans
- **Decay** -- reduceer gradvist aeldere memories' indflydelse

### Pattern 3: Memory Hierarchy

```
Tier 1: Core Identity (altid i context)
  - Bruger-profil, praeferenceer, noegle-fakta
  - ~500-1000 tokens

Tier 2: Session Context (current session)
  - Nylige beskeder, aktuel opgave
  - ~2000-5000 tokens

Tier 3: Retrieved Context (on-demand)
  - Qdrant-soegning baseret paa query
  - ~1000-3000 tokens per retrieval

Tier 4: Archival (sjelden tilgaaet)
  - Fuld historik, gamle sessioner
  - Kun hentet ved eksplicit behov
```

### Pattern 4: Knowledge Graph Lite

I stedet for fuld Neo4j, brug Qdrant metadata til relationer:

```python
# Gem memory med struktureret metadata
qdrant.upsert(
    collection="memories",
    points=[{
        "id": uuid4(),
        "vector": embed("Kris foretraekker dansk"),
        "payload": {
            "type": "preference",
            "entity": "kris",
            "fact": "foretraekker dansk",
            "confidence": 0.95,
            "created": "2026-02-16",
            "last_accessed": "2026-02-16",
            "related_ids": ["uuid-of-related-memory"],
            "tags": ["sprog", "praeference"]
        }
    }]
)
```

### Pattern 5: Anthropic's Context Engineering

Fra [Anthropic's officielle guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

1. **Just-in-Time Loading** -- behold lette identifikatorer (filstier, queries) og load data dynamisk via tool calls
2. **Compaction** -- summariser konversationshistorik naar context-graensen naermer sig, bevar arkitektur-beslutninger og kritiske detaljer
3. **Structured Note-Taking** -- agenten vedligeholder ekstern memory (NOTES.md, memory tools)
4. **Sub-Agent Architecture** -- specialiserede agenter med rene context windows, returnerer komprimerede summaries

---

## 11. Context Window Management

### Noegletal for 200K Token Windows

- **Effektiv graense:** ~130K tokens (performance dropper markant herefter)
- **Reserveer 15-20%** til response-generering og sikkerhedsmargin
- **Optimal operationszone:** 80-100K tokens for bedste kvalitet
- **"Lost in the middle"** problem: Information midt i lang kontekst huskes daaerligst

### Teknikker

**1. Context Compression**
- Fjern fyldord og gentagelser
- Brug kompakte repraesentationer
- Summary af aeldre dele, fuldt detaljeniveau for nylige dele

**2. Token Caching**
- Claude API supporterer prompt caching
- Cachede tokens er 10x billigere
- Stabil system prompt + dynamisk bruger-kontekst = optimal caching

**3. Semantic Chunking**
- Del information i semantisk meningsfulde chunks
- Hent kun relevante chunks via Qdrant
- ~500 tokens per chunk er god balance (vi bruger allerede dette)

**4. Tiered Context Loading**
```
Altid i context:     System prompt + core memory (~2K tokens)
Sessionsspecifikt:   Seneste samtale + opgave (~5K tokens)
On-demand retrieval: Qdrant-soegning (~2K tokens per kald)
Reserve:             Response generation (~20K tokens)
```

**5. Sliding Window med Summary**
- Behold de seneste N beskeder verbatim
- Summariser aeldre beskeder til kompakt form
- Behold noegle-beslutninger og fakta permanent

---

## 12. Sammenligning og Anbefaling

### Sammenligningsmatrix

| Loesning | Qdrant-support | RAM-krav | Kompleksitet | Production-ready | Passer til Ydrasil |
|----------|---------------|----------|-------------|-----------------|-------------------|
| **Mem0** | Ja (default) | Lav (~200MB) | Lav | Ja | **Ja** |
| Letta/MemGPT | Ja (archival) | Medium (~500MB) | Hoej | Ja | Delvist |
| Zep/Graphiti | Nej (graph DB) | Hoej (2GB+) | Hoej | Ja | Nej |
| Cognee | Delvist | Hoej | Medium | Beta | Nej |
| A-MEM | Custom | Lav | Medium | Nej (research) | Som inspiration |
| LangGraph | Nej | Lav | Medium | Ja | Nej (wrong stack) |
| CrewAI | Ja | Medium | Lav | Ja | Nej (wrong stack) |

### Anbefaling for Ydrasil

**Primaer anbefaling: Mem0 Open Source + Qdrant**

Begrundelse:
1. **Vi har allerede Qdrant koerende** -- Mem0 bruger Qdrant som default vector store
2. **Simpelt API** -- `add()`, `search()`, `update()` er alt vi behoever
3. **Lav resource-overhead** -- Python library, ikke en separat server
4. **Memory extraction** kan bruge Claude API (vi betaler allerede for det)
5. **Automatisk deduplicering og decay** -- loser memory bloat problemet
6. **1-bruger scenario** -- Mem0 er perfekt dimensioneret

**Sekundaer anbefaling: DIY Memory Layer**

Hvis Mem0 er for meget overhead, kan vi bygge et letvaeegts-system selv:

```python
# Simpelt memory-system ovenpaa eksisterende Qdrant
class YdrasilMemory:
    def __init__(self, qdrant_client, collection="memories"):
        self.client = qdrant_client
        self.collection = collection

    def remember(self, fact, metadata=None):
        """Gem en ny memory med embedding"""
        vector = embed(fact)
        self.client.upsert(self.collection, points=[{
            "id": str(uuid4()),
            "vector": vector,
            "payload": {
                "text": fact,
                "type": metadata.get("type", "general"),
                "created": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
                "access_count": 0,
                **metadata
            }
        }])

    def recall(self, query, limit=5):
        """Hent relevante memories"""
        vector = embed(query)
        results = self.client.search(self.collection, vector, limit=limit)
        # Opdater access_count og last_accessed
        for r in results:
            self._touch(r.id)
        return results

    def forget(self, threshold_days=90):
        """Slet memories der ikke er tilgaaet i X dage"""
        # Decay-mekanisme
        pass
```

### Konkret Handlingsplan

**Fase 1 (nu):** Fortsaet med nuvaerende system (CLAUDE.md + Qdrant RAG + session logs). Det virker.

**Fase 2 (naar behov opstaar):** Installer Mem0 open-source:
```bash
pip install mem0ai
# Konfigurer med eksisterende Qdrant
# Tilfoej memory extraction til session-pipeline
```

**Fase 3 (optimering):** Implementer context engineering patterns:
- Tiered context loading i system prompt
- Compaction af lange sessioner
- Structured core memory der altid er i context

### Estimeret Kostnad

| Komponent | Maanedlig pris |
|-----------|---------------|
| Qdrant (allerede koerende) | $0 |
| Mem0 open-source | $0 |
| Claude API tokens til memory extraction | ~$1-5 (estimat: 100-500 memory ops/mdr) |
| **Total** | **$1-5/mdr ekstra** |

---

## Kilder

### Akademiske Papers
- [Memory in the Age of AI Agents (2026)](https://arxiv.org/abs/2512.13564)
- [A-MEM: Agentic Memory for LLM Agents (2025)](https://arxiv.org/abs/2502.12110)
- [Mem0: Building Production-Ready AI Agents (2025)](https://arxiv.org/abs/2504.19413)
- [Zep: Temporal Knowledge Graph Architecture (2025)](https://arxiv.org/abs/2501.13956)
- [Agentic Memory: Unified LTM and STM (2026)](https://arxiv.org/abs/2601.01885)
- [Graph-based Agent Memory (2026)](https://arxiv.org/html/2602.05665)
- [Survey on Memory Mechanism (2024)](https://arxiv.org/abs/2404.13501)
- [From Human Memory to AI Memory (2025)](https://arxiv.org/abs/2504.15965)

### Platforms og Frameworks
- [Letta (MemGPT)](https://www.letta.com/) | [GitHub](https://github.com/letta-ai/letta) | [Docs](https://docs.letta.com/concepts/memgpt/)
- [Mem0](https://mem0.ai/) | [GitHub](https://github.com/mem0ai/mem0) | [Qdrant integration](https://qdrant.tech/documentation/frameworks/mem0/)
- [Zep / Graphiti](https://www.getzep.com/) | [Paper](https://arxiv.org/abs/2501.13956)
- [Cognee](https://www.cognee.ai/) | [GitHub](https://github.com/topoteretes/cognee)
- [LangGraph Memory Migration](https://python.langchain.com/docs/versions/migrating_memory/)
- [CrewAI Memory](https://docs.crewai.com/en/concepts/memory)

### Guides og Best Practices
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Letta: Agent Memory Blog](https://www.letta.com/blog/agent-memory)
- [Mem0: AI Memory Layer Guide](https://mem0.ai/blog/ai-memory-layer-guide)
- [Context Engineering: Mastering the 200K Token Era](https://amirteymoori.com/context-engineering-mastering-the-200k-token-era/)
- [LLM Context Management Guide](https://eval.16x.engineer/blog/llm-context-management-guide)
