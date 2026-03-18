# Memory Architecture

**Dato:** 2026-03-15
**Status:** Backlog — høj prioritet
**Modenhed:** spec'd (research done, arkitektur-beslutninger klar)

## Opsummering
Samler arkitekturen for hvordan Ydrasil husker på tværs af sessioner, projekter og tid. Tre ben: **memory layer** (fact extraction + decay), **retrieval-kvalitet** (hybrid search + reranking), **personlig viden** (voice→Qdrant pipeline). Researchen er grundig (2500+ linjer i 6+ filer) — dette brief destillerer beslutningerne.

## Problem Statement
Yttre har allerede infrastrukturen (Qdrant, ctx, CLAUDE.md, episodes.jsonl, hooks). Men:
1. **Ingen fact extraction** — sessioner producerer episoder ("hvad skete"), men ikke fakta ("hvad vi ved"). MEMORY.md fyldes manuelt.
2. **Retrieval er naivt** — dense-only search, ingen reranking, ingen temporal awareness. Gammel info scorer lige højt som ny.
3. **Personlig viden mangler** — Qdrant indeholder rutedata og sessionslogger, men ikke holdninger, beslutninger, relationer, livserfaring.

## Hvad det IKKE er
- Ikke Mem0/LightRAG/Letta installation — de er evalueret og fravalgt som helhedsløsninger (for tungt/umodent). Principperne bruges, ikke frameworks.
- Ikke context-engineering (det dækker session-hooks og CLAUDE.md). Dette dækker hvad der huskes og hentes *mellem* sessions.
- Ikke research-architecture (det dækker research-praksis). Dette dækker al viden, ikke kun research.

## Hvad der allerede virker
| Komponent | Status |
|-----------|--------|
| Qdrant (7 collections, 84K points) | Kører, dense-only |
| ctx-kommando (semantisk søgning) | Kører |
| episodes.jsonl (3-5 linjer/session) | Kører (VPS) |
| NOW.md + load_checkpoint.sh | Kører (VPS) |
| CLAUDE.md + MEMORY.md | Kører (PC) |
| Groq Whisper (voice transkription) | Kører (VPS) |
| save_checkpoint.py (pre-compact) | Kører (VPS) |

## Faser

### Fase 1: Retrieval-kvalitet (Timer, VPS)
Laveste indsats, højeste impact. Forbedrer alt der allerede bruger ctx.

1. **Reranking i ctx** — Cohere Rerank API efter Qdrant top-20 → returner top-5. ~5 linjer kode, $1/1K queries.
2. **Temporal decay** — `score *= exp(-age_days/30)` i ctx. Nyere > ældre. ~3 linjer.
3. **Query expansion** — HyDE: generér hypotetisk svar → embed → søg. Ét ekstra LLM-kald per query.

**Succes-tegn:** ctx returnerer mærkbart bedre resultater på 10 test-queries vs. baseline.
**Kill-tegn:** Ingen forskel efter 2 ugers brug.

### Fase 2: Fact extraction (Dage, VPS)
Mem0-princippet uden Mem0: extract facts fra sessioner automatisk.

1. **Extract-script** — Efter session: send episode til Claude Haiku → udtræk fakta, holdninger, beslutninger, relationer → gem som strukturerede Qdrant-punkter med metadata (type, dato, kilde, confidence).
2. **Dedup** — Før insert: søg om fakta allerede eksisterer → opdatér i stedet for duplikér.
3. **Ny collection: `knowledge_extracted`** — Adskilt fra sessions/routes. Querybar via ctx.

**Pris:** ~$0.01-0.05/session (Haiku extraction). ~50 linjer Python.
**Succes-tegn:** Efter 20 sessioner kan ctx besvare "hvad synes Yttre om X?" fra extraherede fakta.
**Kill-tegn:** Extraherede fakta er for generiske/upræcise til at være nyttige.

### Fase 3: Hybrid search (Dage, VPS)
Tilføj BM25 sparse vectors til Qdrant. Kræver re-ingest.

1. **Sparse vector config** i relevante collections (sessions, knowledge, docs).
2. **BM25 tokenizer** ved ingest.
3. **Reciprocal Rank Fusion** i ctx: 0.7 dense + 0.3 sparse.

**Effort:** 1-2 dage (re-ingest 84K points). ~$2-5 embedding cost.
**Succes-tegn:** Keyword-tunge queries ("rute 256 organisk") finder præcist.
**Kill-tegn:** Dense-only performer lige godt på test-queries.

### Fase 4: Personlig viden pipeline (Dage, VPS)
Voice memos → struktureret viden. Bygger på Groq Whisper (allerede kører).

1. **process_voice_memo.py** — Transkript → Claude Haiku → atomare noter (Zettelkasten-stil) → embed i `personal` collection.
2. **Metadata:** type (fact/opinion/episode/decision/relation), dato, personer, emne, kilde.
3. **Daglig digest** — Cron kl. 23: saml dagens nye memories → generer kort opsummering.

**Pris:** ~$2-4/måned (50-100 memos).
**Succes-tegn:** ctx kan besvare personlige spørgsmål ("hvad sagde Lars om ruteændringen?").
**Kill-tegn:** Yttre bruger ikke voice memos nok til at pipeline giver mening.

## Tradeoffs og fravalg

| Fravalg | Begrundelse |
|---------|-------------|
| Mem0 (framework) | 50 linjer Python giver 80% af værdien. Undgår dependency. |
| LightRAG / knowledge graph | Svagt evidensgrundlag, paper trukket fra ICLR. Hybrid search giver 80% af multi-hop. |
| Letta/MemGPT | Overkill for 1 bruger. OS-metaforen er god — vi tager koncepterne, ikke koden. |
| Graphiti/Zep | Kræver Neo4j, Claude er "second class citizen". |
| 1M context | $10/prompt, context rot efter ~100K. Bedre retrieval slår større vindue. |

## Afhængigheder
```
Fase 1-2: Uafhængige, kan startes nu
Fase 3: Kræver VPS session (re-ingest)
Fase 4: Kræver Groq Whisper pipeline (allerede kører)
context-engineering (hooks) → komplementært, ikke blokerende
```

## Rå input (research-kilder)
- `ydrasil/research/ai_memory_research.md` (619L) — Memory framework survey
- `ydrasil/research/memory_bridge_research.md` (674L) — Human↔AI bro, voice pipeline design
- `ydrasil/research/memory_autonomy_research_2026-02-23.md` (~307L) — Mem0/LightRAG red/blue team
- `ydrasil/research/context_window_workarounds_2026.md` (~436L) — Compaction, summarization patterns
- `research/ai-frontier/topics/memory-systems.md` — RAG, hybrid search, knowledge graphs, episodisk hukommelse
- `research/ai-frontier/GAPS.md` — 6 gaps inkl. hybrid search, reranking, temporal decay, fact extraction
- `0_backlog/brief.context-engineering.md` — Session-kontinuitet (komplementær)
- `0_backlog/brief.research-architecture.md` — Research-praksis (komplementær)

## Kill condition
Hvis fase 1 (reranking + temporal decay) ikke giver mærkbar forbedring efter 2 uger, er resten tvivlsom — revurdér hele briefen.
