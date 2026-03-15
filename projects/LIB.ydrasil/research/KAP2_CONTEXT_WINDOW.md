# Kapitel 2: Context Window — Problemet, Løsningerne, og Hvad Du Faktisk Skal Gøre

**Researched:** 2026-02-09 via 3 parallelle agenter (Kap 1 metodik)

---

## 2.1 Problemet i ét billede

Hver LLM har et "context window" — det antal tokens den kan se på én gang. Tænk på det som en arbejdsflade: jo større flade, jo mere du kan have foran dig. Men her er sandheden de ikke fortæller dig i marketing:

**Annonceret vindue ≠ brugbart vindue.**

En model der påstår 200K tokens er typisk upålidelig efter ~130K. En der påstår 1M er upålidelig efter ~400K. Og "upålidelig" betyder ikke gradvis forværring — det er pludselige klipper i kvalitet.

---

## 2.2 Hvad modellerne faktisk kan (februar 2026)

### Context Window Størelser

| Model | Vindue | Pålideligt område | Noter |
|-------|--------|-------------------|-------|
| **Claude Opus 4.6** | 1M | ~400K | Nyeste. Degraderer langsomst. Nægter hellere end at hallucinere |
| **Claude Sonnet 4.5** | 1M | ~400K | Beta, tier 4+ |
| **GPT-4.1** | 1M | ~400K | OpenAI's 1M-entry |
| **GPT-5.2** | 400K | ~200K | Kodename "Garlic." Dec 2025 |
| **Gemini 2.5 Pro** | 1M (2M kommer) | ~530K | Bedst på ren retrieval (99.7% NIAH ved 1M) |
| **Gemini 3 Pro** | 10M | ~256K for reasoning | Enormt vindue, men reasoning kollapser |
| **Llama 4 Scout** | 10M | ~256K for reasoning | Open-weight. 15.6% accuracy ved full length |
| **Grok 4.1 Fast** | 2M | Ukendt | 8K output cap |
| **Mistral Large 3** | 256K | ~100K | 675B MoE |
| **DeepSeek-R1** | 128K | ~50K | Reasoning model |

### 40%-Reglen

Research viser konsistent: **hold kontekst under 40% af max** for pålidelig performance.

- 128K vindue → brug max ~50K
- 200K vindue → brug max ~80K
- 1M vindue → brug max ~400K

Over 40% ser du ikke gradvis forværring — du ser **katastrofisk kollaps**. Et studie målte F1-score der faldt fra 0.58 til 0.30 mellem 40% og 50% kapacitet. Det er en 45% forringelse over bare 10% mere kontekst.

---

## 2.3 "Lost in the Middle"

### Hvad det er
LLM'er har en U-formet opmærksomhedskurve: de er gode til information i starten og slutningen af konteksten, men **mister information i midten**. Med bare 20 dokumenter (~4K tokens) falder accuracy fra 75% til 55% når informationen er i midten.

### Hvorfor det sker
Det er **arkitektonisk**, ikke bare en fejl:
- **RoPE** (Rotary Position Embedding) — bruges i næsten alle moderne LLM'er — har en langtids-dæmpningseffekt der strukturelt nedprioriterer midterindhold
- **Causal attention masks** skaber bias mod begyndelsen af sekvensen
- Træningsdata forstærker mønsteret

### Hvad det betyder for dig
Sæt vigtig information **først** (system prompt, instruktioner) eller **sidst** (seneste kontekst). Lad aldrig kritisk information ligge begravet i midten af et langt dokument.

---

## 2.4 Retrieval vs. Reasoning — Den vigtige skelnen

Modellerne kan **finde** en nål i en høstak (NIAH-scores er næsten perfekte). Men de kan **ikke ræsonnere** over spredt information i lang kontekst.

| Benchmark | Hvad det tester | Sværhedsgrad | Resultat |
|-----------|----------------|--------------|----------|
| **NIAH** | Find én fakta i støj | Let | ~100% (meningsløst) |
| **RULER** | Retrieval + tracing + aggregering | Medium-Svær | Halvdelen fejler ved 32K |
| **NoLiMa** | Associativ retrieval (ikke ordret) | Svær | 10/12 modeller under 50% ved 32K |
| **BABILong** | Multi-hop reasoning over spredt info | Meget svær | Modeller bruger effektivt kun 5-25% af vinduet |

**Nøgleindsigt:** GPT-4 bruger effektivt kun ~10% af sit 128K vindue (~16K tokens) til reasoning-opgaver. De andre 90% er spildte tokens.

---

## 2.5 Løsningerne — Fra Simpelt til Avanceret

### Lag 1: Det du skal gøre FØRST (vi gør allerede det meste)

#### CLAUDE.md / Persistente instruktioner
- Læses automatisk ved hver session
- Koster nul ekstra — det er gratis kontekst
- **Vi har det:** CLAUDE.md + 5 skill-filer + 2 slash commands

#### Prompt caching
- Stabil prefix (system prompt, tools, instruktioner) caches automatisk
- **90% prisreduktion** på cached tokens, **85% latency-reduktion**
- Anthropic: Cache write koster 1.25x, cache read koster 0.1x
- **Nøgle:** Strukturér prompts så det stabile kommer først

#### Auto-komprimering
- Claude Code komprimerer samtalen automatisk når context fyldes
- Session Memory (siden v2.0.64) skriver summaries i baggrunden
- **Vi har det:** save_checkpoint.py + MASTER_PLAN.md som overlever sessions

---

### Lag 2: RAG — Hent kun det relevante

#### Hvorfor RAG stadig vinder over lang kontekst
- **1250x billigere** per query end at fylde hele context window
- **Bedre citation accuracy** — konsistent vinder på præcis kildehenvisning
- **Mitigerer "lost in the middle"** — du sender kun 4-16K tokens af fokuseret kontekst
- **Dynamisk data** — perfekt til data der ændrer sig

#### De tre generationer af RAG

| Generation | Hvad | Eksempel |
|------------|------|---------|
| **Naive RAG** | Embed → hent top-K → generer | Vores nuværende system |
| **Advanced RAG** | Hybrid retrieval + reranking + filtrering | Vores mål |
| **Agentic RAG** | Autonom planlægning + iterativ retrieval + tool use | Fremtid |

#### Chunking — den mest undervurderede parameter
- **Fixed-size (~500 tokens)** med overlap: Simpelt, godt baseline
- **Sentence-aware:** Respekterer sætningsgrænser
- **Semantic chunking:** Grupperer efter betydning via embeddings
- **Strukturel chunking:** Respekterer headers, tabeller, kodeblokke

**Vores nuværende:** Vi chunker på `## ` headers, max 2000 chars. Det er strukturel chunking — godt valg for bøgerne.

#### Reranking — det næste skridt
Første retrieval henter top-20. Reranker reordner dem til de bedste 3-5.
- **Cross-encoder rerankers** (Cohere Rerank, bge-reranker): Scorer hvert (query, dokument) par. Meget mere præcis end bi-encoder similarity.

---

### Lag 3: Context Compression

#### LLMLingua (Microsoft)
- Op til **20x kompression** med minimal kvalitetstab
- LongLLMLingua: Forbedrer RAG performance med 21.4% med kun 1/4 af tokens
- Integreret i LangChain og LlamaIndex
- Open source: [github.com/microsoft/LLMLingua](https://github.com/microsoft/LLMLingua)

#### KV Cache compression
- **KVzip:** Komprimerer samtalehukommelse 3-4x, fordobler response-hastighed
- **PagedAttention/vLLM:** Reducerer memory waste fra 60-80% til under 4%
- **FP8 KV Cache:** Halverer memory-krav på nyere GPU'er

---

### Lag 4: Memory Systems

| System | Tilgang | Score | Tokens | Bedst til |
|--------|---------|-------|--------|-----------|
| **Mem0** | Two-phase pipeline | 66.9% | 7K | SaaS, simpel integration |
| **Letta** (ex-MemGPT) | Agentisk med self-managed memory | 74.0% | Varierer | Dyb kontrol |
| **Zep/Graphiti** | Temporal knowledge graph | 94.8% | ~600K | Tidsmæssig ræsonnering |
| **Custom (filesystem)** | CLAUDE.md + scripts | Konkurrencedygtig | Minimal | Solo dev, fuld kontrol |

**Nøgleindsigt fra Letta:** En simpel filsystem-baseret tilgang kan matche specialiserede memory-frameworks. Det vi gør med CLAUDE.md + Qdrant + save_checkpoint.py er faktisk konkurrencedygtigt.

---

### Lag 5: Hierarkisk Context Management

#### Lagdelt hukommelse
1. **Working memory:** Nuværende context window (hurtigst, mindst)
2. **Short-term:** Seneste samtalehistorik (summaries, nøglefakta)
3. **Long-term:** Persistente fakta, præferencer, videnbase (Qdrant)

#### Context Isolation
Split kontekst på tværs af sub-agenter. Hver agent har sit eget 200K context window. Forhindrer context-forurening. Orchestrator syntetiserer.

**Vores version:** Skills der loader on-demand (route-lookup, advisor, etc.) + parallelle Task agents til research.

---

### Lag 6: Knowledge Graphs

#### Microsoft GraphRAG
- Bygger entity-relation grafer fra tekst
- **Local search** (DRIFT) for præcise queries
- **Global search** for tematiske spørgsmål
- Open source: [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)

#### Zep's Graphiti
- Temporal knowledge graph — tracker hvornår ting skete OG hvornår de blev registreret
- 94.8% på Deep Memory Retrieval
- Bedst til: "Hvornår ændrede kunde X sin afhentningsdag?"

**Tradeoff:** Grafer er kraftfulde men komplekse. Brug dem kun når relationer mellem entiteter er vigtige. For de fleste spørgsmål er vector search tilstrækkeligt.

---

## 2.6 Context Engineering — Den nye disciplin

I juli 2025 erklærede Gartner: **"Context engineering is in, and prompt engineering is out."**

Context engineering handler om at designe det **mindst mulige sæt af højsignal-tokens** der maksimerer sandsynligheden for det ønskede output.

### De 4 strategier

| Strategi | Hvad | Eksempel i Ydrasil |
|----------|------|-------------------|
| **Write** | Skab kontekst | CLAUDE.md, skill-filer, advisor-identitet |
| **Select** | Vælg relevant kontekst | `ctx` søgning, skill on-demand loading |
| **Compress** | Reducer token-count | Auto-komprimering, session summaries |
| **Isolate** | Split på sub-agenter | Task agents til research, context isolation |

### Praktiske patterns

**Session persistence:**
- `claude -c` fortsætter seneste samtale
- `claude -r "abc123"` genoptager specifik session
- CLAUDE.md + NOW.md overlever alle sessions
- MASTER_PLAN.md tracker fremdrift

**Context routing:**
- Skill-filer loader kun ved relevante spørgsmål
- `ctx --advisor` søger advisor-viden
- `ctx --routes` søger rutedata
- Forskellige collections = naturlig kontekst-routing

---

## 2.7 Hvad vi gør rigtigt — og hvad vi kan forbedre

### Allerede på plads
- CLAUDE.md med advisor-identitet (altid loaded)
- Skill-baseret on-demand context loading
- Qdrant med 7 collections (65K+ datapunkter)
- Session checkpoints (save_checkpoint.py)
- Hybrid search (dense + sparse/BM25)
- Strukturel chunking (## headers)

### Næste skridt (prioriteret)
1. **Reranking** — Tilføj cross-encoder reranker efter retrieval (stor kvalitetsforbedring, lav indsats)
2. **Prompt caching** — Strukturér API-kald med stabil prefix (90% prisreduktion)
3. **LLMLingua** — Komprimer retrieved passages før de sendes til LLM (når det bliver dyrt)
4. **Embed /research/** — De 18 research-filer er ikke søgbare endnu

### Kan vente
- Knowledge graphs (kun relevant hvis vi har brug for relational reasoning)
- Specialized memory frameworks (vores custom tilgang er konkurrencedygtig)
- 1M+ context stuffing (RAG er 1250x billigere og mere præcis)

---

## 2.8 Kilder

### Context Window Limits & Benchmarks
- [Liu et al. (2023): Lost in the Middle](https://arxiv.org/abs/2307.03172) — Den originale U-kurve forskning
- [ICLR 2026: Lost in the Middle as Emergent Property](https://arxiv.org/abs/2510.10276) — Arkitektonisk forklaring
- [Du et al. (2025): Context Length Alone Hurts](https://arxiv.org/abs/2510.05381) — 13.9-85% degradering selv med perfekt retrieval
- [Intelligence Degradation in Long-Context LLMs (Jan 2026)](https://arxiv.org/abs/2601.15300) — 40% threshold opdagelse
- [Chroma Research: Context Rot (Jul 2025)](https://research.trychroma.com/context-rot) — 18 modeller testet
- [NVIDIA RULER Benchmark](https://arxiv.org/abs/2404.06654) — Halvdelen fejler ved 32K
- [NoLiMa: Beyond Literal Matching (ICML 2025)](https://arxiv.org/abs/2502.05167) — 10/12 modeller under 50%
- [BABILong Benchmark](https://arxiv.org/abs/2406.10149) — 5-25% effektiv brug

### Løsninger
- [RAG vs. Long Context (Jan 2025)](https://arxiv.org/abs/2501.01880) — RAG 1250x billigere
- [LLMLingua (Microsoft)](https://github.com/microsoft/LLMLingua) — 20x kompression
- [Agentic RAG Survey](https://arxiv.org/abs/2501.09136) — Den komplette RAG-evolution
- [Anthropic: Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — 90% prisreduktion
- [Letta Benchmarking AI Agent Memory](https://www.letta.com/blog/benchmarking-ai-agent-memory) — Simpel > fancy
- [Zep State of the Art Agent Memory](https://blog.getzep.com/state-of-the-art-agent-memory/) — 94.8% temporal retrieval
- [vLLM PagedAttention](https://arxiv.org/abs/2309.06180) — KV cache optimization

### Context Engineering
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Write/Select/Compress/Isolate
- [Gartner: Context Engineering > Prompt Engineering](https://www.flowhunt.io/blog/context-engineering/) — Paradigmeskift
- [LangChain: Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/) — Praktiske patterns
- [Claude Code Memory Management](https://code.claude.com/docs/en/memory) — CLAUDE.md, Session Memory

---

*Sidst opdateret: 2026-02-09*
