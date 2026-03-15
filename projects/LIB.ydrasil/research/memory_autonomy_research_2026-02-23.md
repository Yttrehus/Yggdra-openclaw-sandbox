# Research: AI Hukommelse, Kontekstvindue & Autonomi
**Dato:** 23. februar 2026
**Bestilt af:** Kris
**Metode:** 3 parallelle research-agenter + web-søgning + YouTube-analyse + red/blue team

---

## DEL 1: Lagdelt Hukommelse — Hvad Findes?

### 1.1 Mem0 (47.8K stars) — **STÆRKESTE MATCH**
- **Hvad:** Universal memory layer. Ekstraherer "memory items" (destillerede fakta) fra samtaler
- **3 niveauer:** User memory (persistent), Session memory, Agent memory
- **Stack:** Bruger Qdrant + Anthropic (begge native supported) — **præcis vores stack**
- **Resultater:** 26% bedre accuracy, 90% lavere token-forbrug vs full-context
- **VPS:** Ja, kører på 4GB
- **MCP-server:** Findes allerede til Claude Code
- **Estimat:** 2-4 timer at integrere
- [GitHub](https://github.com/mem0ai/mem0) | [ArXiv](https://arxiv.org/abs/2504.19413)

### 1.2 LightRAG (28.5K stars) — **NÆSTE SKRIDT**
- **Hvad:** Letvægts knowledge graph bygget automatisk ved ingest
- **Dual retrieval:** Lokal (entiteter) + Global (temaer)
- **Stack:** Understøtter Qdrant native + NetworkX (in-memory graf, ingen ekstra server)
- **Vs GraphRAG:** 10x billigere, sammenlignelig nøjagtighed
- **VPS:** Ja (512MB+)
- **Claude:** Via OpenAI-compatible proxy
- **Estimat:** 1 dag at sætte op
- [GitHub](https://github.com/HKUDS/LightRAG) | [EMNLP 2025 paper](https://arxiv.org/abs/2410.05779)

### 1.3 Graphiti/Zep (23K stars) — **INTERESSANT MEN STRAMT**
- **Hvad:** Real-time temporal knowledge graph med bi-temporal model
- **Killer-feature:** Ved HVORNÅR ting skete, invaliderer forældet info automatisk
- **P95 latency:** 300ms, ingen LLM-kald ved retrieval
- **VPS:** Stramt — kræver Neo4j/Kuzu ekstra
- **Claude:** Eksplicit supported men "second class citizen" (Structured Output warnings)
- [GitHub](https://github.com/getzep/graphiti) | [ArXiv](https://arxiv.org/abs/2501.13956)

### 1.4 GraphRAG/Microsoft — **FOR DYRT**
- Suveræn til "big picture" queries, men indexering af 80K chunks = tusindvis af API-kald
- LightRAG giver 90% af værdien til 10% af omkostningen
- **Fravalg for Ydrasil**

### 1.5 Letta/MemGPT (21.2K stars) — **OVERKILL**
- Hel agent-platform med tiered memory (core/archival/recall)
- OS-metafor: context = RAM, storage = disk
- Ny V1 (feb 2026) med git-baseret versionering
- **For tungt** — Ydrasil har allerede sin agent-loop
- [GitHub](https://github.com/letta-ai/letta)

### 1.6 Cutting-edge Research
| Paper | Dato | Koncept |
|-------|------|---------|
| **MAGMA** | Jan 2026 | 4 parallelle grafer (semantic, temporal, causal, entity). 45.5% bedre reasoning |
| **A-Mem** | Feb 2025 | Zettelkasten-inspireret, auto-linking mellem memories |
| **AgeMem** | Jan 2026 | Unified framework: memory som tool-kald |
| **Memoria** | Dec 2025 | Skalerbar multi-session memory |
| **ICLR 2026 MemAgents Workshop** | Kommende | Feltet er i eksplosiv vækst |

---

## DEL 2: Kontekstvinduet — Sådan Slipper Vi Udenom

### 2.1 MIT Recursive Language Models (RLM) — Kris' video

**Paper:** "Recursive Language Models" (arXiv:2512.24601, dec 2025)
**Forfattere:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)
**Video:** Matthew Berman — "MIT Researchers DESTROY the Context Window Limit"

**Hvad det er:**
- I stedet for at proppe hele prompten i context window, gemmes den som en **ekstern variabel** i en Python REPL
- LLM'en skriver kode der **rekursivt søger** i den eksterne tekst
- Skalerer til **10M+ tokens** effektivt
- **3x billigere** end at bruge fuld context — modellen ser kun relevante uddrag

**Teknisk:**
1. Lang prompt → gemt som Python-variabel
2. LLM får adgang til REPL + søge-tools
3. LLM beslutter selv hvad der er relevant → skriver kode → kalder sig selv rekursivt
4. Resultat: selektiv kontekst-læsning i stedet for brute-force

**Benchmark:** 29%+ bedre end baselines. GPT-5 Mini: $150-275 for 6-11M tokens → RLM: $99 med bedre performance.

**HN-kritik (vigtigt!):**
- "Det er bare subagents der læser filer" — ikke arkitektonisk nyt
- Rekursionsdybde = 1 i praksis → "er det overhovedet rekursion?"
- Ingen træning/loss function — det er en **inference-strategi**, ikke en ny model
- **Men:** Den agentic del (LLM beslutter selv hvad der søges) er den reelle innovation vs. traditionel RAG

**Relevans for Ydrasil:** Vi gør allerede noget lignende med `ctx`-kommandoen (Qdrant retrieval). RLM formaliserer det. Kan implementeres som et bedre retrieval-lag.

### 2.2 Anthropics 1M Token Context (Beta)
- Claude Opus 4.6 (5. feb 2026): **1M token context window** i beta
- Standard: 200K, Enterprise: 500K, 1M for tier 4+
- Pricing: $5/M input (standard), $10/M for >200K prompts
- **Men:** Større context ≠ bedre. "Context rot" (kvalitet falder med længde) er reelt

### 2.3 Andre Tilgange

| Tilgang | Hvad | Tradeoff |
|---------|------|----------|
| **Sliding window + compaction** | Komprimér gammel kontekst, bevar ny | Tab af detaljer |
| **Hierarkisk summarization** | 4 lag: rå → session → langtid → permanent | Summarization-fejl akkumuleres |
| **MemGPT-paging** | Agent pager selv info ind/ud | Bruger "kognitiv båndbredde" på memory management |
| **Agentic RAG** | Agent styrer retrieval selv | Afhængig af agents søge-kvalitet |
| **Multi-agent** | Separate agenter med separate kontekster | Koordinations-overhead |
| **KV-cache optimering** | Stabile prompt-prefixes = 10x billigere | Kræver arkitektonisk design |

**Vigtigste indsigt:** "Context engineering" er den nye disciplin. Ikke én tilgang, men **kombination i lag**.

---

## DEL 3: Autonomi — Hvordan Gør Vi Claude Selvkørende?

### 3.1 OpenClaw (200K+ stars!)
- **Hvad:** Open-source autonom AI-agent af Peter Steinberger (Østrig)
- **Navnehistorie:** Clawdbot → Moltbot (Anthropic trademark-klage) → OpenClaw
- **Features:** Telegram/WhatsApp/Discord, fil-ops, shell, kode-sandbox, auto-PRs, Sentry
- **Steinberger joined OpenAI 14. feb 2026** — projektet → open-source foundation
- **430.000+ linjer kode** — massivt
- [GitHub](https://github.com/openclaw/openclaw) | [Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)

### 3.2 Lettere Alternativer

| Projekt | Størrelse | Platform | Relevant? |
|---------|----------|----------|-----------|
| **PicoClaw** | Enkelt binary | Telegram, Discord | **JA** — Groq Whisper, cron, kører på $10 hw |
| **Nanobot** | ~4K linjer Python | Telegram, WhatsApp | **JA** — persistent memory, sub-agents, 191MB |
| **Claude Code Scheduler** | Plugin | Claude Code | **JA** — NLP scheduling, git worktree isolation |
| **claude-flow** | 250K+ linjer | Multi-agent | For stort |

### 3.3 Claude Code Autonomi-Mønstre

**A) `claude -p` + cron** (hvad vi gør nu)
- Simpelt, virker, men ingen kontekst mellem kørsler

**B) Claude Code Scheduler** (plugin)
- `plugin marketplace add jshchnz/claude-code-scheduler`
- Natural language scheduling: "every weekday at 9am"
- Git worktree isolation (separate branches, auto-push)
- [GitHub](https://github.com/jshchnz/claude-code-scheduler)

**C) Heartbeat/Daemon** (mest relevant for os)
- Python-daemon der checker inbox/Trello/Telegram periodisk
- Spawner Claude Code sessions når der er arbejde
- Vi har allerede delene — mangler wrapperen

**D) Agent Teams** (eksperimentel)
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Lead-session koordinerer, members har eget kontekstvindue
- Delt task-liste, agent-til-agent kommunikation

### 3.4 Anthropics Officielle Memory
- **Memory Tool API** — nu GA (ikke beta). Filbaseret persistent memory du kontrollerer
- **Claude Code Auto-Memory** — projektlærdom persisteret lokalt (det vi bruger)
- **Claude Agent SDK** — Anthropic erkender Claude Code er mere end kode-tool
- [Memory Tool Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool)

---

## DEL 4: RED TEAM / BLUE TEAM ANALYSE

### 🔴 RED TEAM — Hvad er galt med denne research?

**R1. Mem0 "26% bedre accuracy" — hvad er baseline?**
- Tallet kommer fra Mem0's eget paper. Ikke uafhængigt verificeret.
- 90% lavere token-forbrug lyder for godt — sandsynligvis målt på simple use cases.
- **Risiko:** Marketing-tal der ikke holder i praksis.

**R2. LightRAG "10x billigere end GraphRAG" — æbler og appelsiner**
- LightRAG bruger NetworkX (in-memory), GraphRAG bruger fuld community-detection.
- De løser forskellige problemer: LightRAG = entity retrieval, GraphRAG = sensemaking.
- **Risiko:** Vi vælger LightRAG for prisen men mangler GraphRAG's styrke.

**R3. MIT RLM er IKKE nyt — det er agentic RAG med fancy navn**
- HN-kritikken er berettiget: rekursionsdybde 1 er ikke rekursion.
- Vi gør allerede noget lignende med `ctx` + Qdrant retrieval.
- **Risiko:** Vi tror vi mangler noget vi allerede har.

**R4. OpenClaw er 430K linjer kode — vi kan IKKE vedligeholde det**
- Steinberger forlod projektet → OpenAI. Hvem vedligeholder?
- Sikkerhedsbekymringer (CyberArk-advarsel) om brede permissions.
- **Risiko:** Dependency på abandonware.

**R5. "1M token context" løser IKKE vores problem**
- Context rot er reelt — kvalitet falder efter ~100K tokens uanset vindue.
- 1M tokens á $10/M = $10 per fuld prompt. Vores budget holder ikke.
- **Risiko:** Vi betaler for context vi ikke kan bruge effektivt.

**R6. Vi undersøgte ikke KOSTNADEN tilstrækkeligt**
- Mem0 extraction kræver LLM-kald per samtale → API-cost.
- LightRAG entity extraction ved ingest → API-cost for 80K chunks.
- **Risiko:** Migrationsomkostning er IKKE "2-4 timer" — det er timer + API-dollars.

**R7. Graphiti's "second class" Claude-support**
- "Works best with services that support Structured Output" — Claude gør det IKKE native.
- **Risiko:** Vi vælger Graphiti og opdager at Claude output-parsing fejler.

**R8. Manglende research: hvad gør ORDINARY folk?**
- Vi kiggede på frameworks og papers. Vi kiggede IKKE på hvad normale folk med en VPS og Claude Max gør.
- Reddit, HN, Discord — der er sandsynligvis simple, geniale løsninger vi overså.

### 🔵 BLUE TEAM — Hvad holder?

**B1. Mem0 + eksisterende Qdrant ER det laveste hængende frugt**
- Selv hvis "26%" er marketing, er intelligent memory extraction bedre end raw chunks.
- Vi mister intet — Qdrant forbliver. Mem0 er et lag OVEN PÅ.
- Cost: Haiku til extraction = billigt ($0.25/M input).

**B2. LightRAG med NetworkX er realistisk på vores VPS**
- NetworkX er in-memory, ingen ekstra server. 80K chunks = måske 500MB graf.
- Entity extraction kan køres incrementelt (nye chunks først).
- Giver os "multi-hop" som flat search aldrig kan.

**B3. RLM-princippet er allerede delvist implementeret**
- `ctx` + Qdrant = agentic retrieval. Vi mangler bare bedre retrieval-logik.
- Vi behøver ikke MIT's framework — princippet er det vigtige.

**B4. Heartbeat-daemon > OpenClaw for vores use case**
- 50 linjer Python der checker inbox + Trello + Telegram hvert minut.
- Spawner `claude -p` med kontekst. Simpelt, vedligeholdeligt, VORES kode.
- OpenClaw er overkill. PicoClaw/Nanobot er inspiration, ikke implementation.

**B5. Claude Code Scheduler er plug-and-play**
- Allerede bygget til Claude Code. NLP scheduling. Git worktree isolation.
- Laveste indsats for bedre autonomi.

**B6. Anthropics Memory Tool API er den "officielle" vej**
- GA, supported, dokumenteret. Ikke et tredjepartshack.
- Kan erstatte dele af vores checkpoint-system med noget mere robust.

### 🟡 EVALUERING — Var researchen grundig nok?

**Hvad vi dækkede godt:**
- ✅ Alle major memory frameworks (Mem0, LightRAG, GraphRAG, Graphiti, Letta)
- ✅ MIT RLM paper + HN-kritik (begge sider)
- ✅ Anthropics memory-landskab (Memory Tool, 1M context, Claude Code auto-memory)
- ✅ OpenClaw + alternativer + autonomi-mønstre
- ✅ Cutting-edge research (MAGMA, A-Mem, AgeMem)

**Hvad vi MANGLER:**
- ❌ **YouTube-videoen** — Tor-blokeret, kun metadata + sekundære kilder
- ❌ **Praktiske erfaringer** fra folk der bruger Mem0/LightRAG i produktion (Reddit, Discord)
- ❌ **Cost-modellering** — hvad koster det faktisk at migrere 80K chunks?
- ❌ **Benchmark på VORES data** — alle tal er fra papers, ikke fra Ydrasil-kontekst
- ❌ **Claude Code Scheduler** — ikke testet, kun beskrevet
- ❌ **Sammenligning med hvad vi ALLEREDE har** — vores Qdrant + ctx er ikke evalueret objektivt

**Fejltolkninger vi skal passe på:**
- ⚠️ "Mem0 er 2-4 timer" — sandsynligvis undervurderet (integration + re-embedding + test)
- ⚠️ "LightRAG er 1 dag" — entity extraction af 80K chunks tager tid + API-kald
- ⚠️ "OpenClaw er relevant" — det er for stort og for usikkert efter Steinbergers exit

---

## DEL 5: ANBEFALING — Prioriteret Handlingsplan

### Fase 1: I dag (0 cost, 1 time)
1. **Installer Mem0** og konfigurer med eksisterende Qdrant + Claude Haiku
2. Test med 10 samtaler fra checkpoint-loggen
3. Evaluér: giver memory extraction bedre resultater end raw chunks?

### Fase 2: Denne uge (lav cost, 1 dag)
4. **Claude Code Scheduler plugin** — installer og sæt op med daglige tasks
5. **Heartbeat-daemon** — 50 linjer Python wrapper over eksisterende scripts
6. **Anthropic Memory Tool API** — evaluér om det kan erstatte checkpoint-systemet

### Fase 3: Næste uge (moderat cost)
7. **LightRAG** med NetworkX — start med entity extraction på nyeste 5K chunks
8. Evaluér graph retrieval vs flat search på 10 test-queries
9. Beslut om fuld migration er værd at køre

### Fravalg (indtil videre)
- GraphRAG (for dyrt)
- Letta (for tungt)
- OpenClaw (for stort, usikker fremtid)
- Graphiti (Claude-support for svag)
- 1M context (for dyrt, context rot)

---

## Kilder

### Papers
- [RLM (MIT)](https://arxiv.org/abs/2512.24601) — Recursive Language Models
- [LightRAG](https://arxiv.org/abs/2410.05779) — EMNLP 2025
- [Graphiti](https://arxiv.org/abs/2501.13956) — Temporal Knowledge Graphs
- [Mem0](https://arxiv.org/abs/2504.19413) — Memory Layer for AI
- [MAGMA](https://arxiv.org/abs/2601.03236) — Multi-Graph Agentic Memory

### Frameworks
- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [LightRAG GitHub](https://github.com/HKUDS/LightRAG)
- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Claude Code Scheduler](https://github.com/jshchnz/claude-code-scheduler)

### Anthropic
- [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)
- [Memory Tool API](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool)
- [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

### Analyse
- [VentureBeat: MIT RLM](https://venturebeat.com/orchestration/mits-new-recursive-framework-lets-llms-process-10-million-tokens-without)
- [HN Discussion](https://news.ycombinator.com/item?id=46475395)
- [Matthew Berman video](https://youtu.be/huszaaJPjU8)
- [Milvus: OpenClaw Guide](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
