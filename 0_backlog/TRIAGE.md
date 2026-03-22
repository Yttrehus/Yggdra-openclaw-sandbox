# Triage — Prioriteret overblik

Sidst opdateret: 2026-03-15

## V4 Handlinger (fra HOLISTIC_EVALUATION)

Prioriteret efter impact × (1/effort). Alle fra VPS V4 research loops.

| # | Handling | Effort | Kilde | Status |
|---|---------|--------|-------|--------|
| 1 | Fix RSS feed bug (tilføj `fetch_rss_feeds()` kald i ai_intelligence.py) | 15 min | videns-vedligeholdelse | Afventer VPS |
| 2 | Genaktivér heartbeat.py (uncomment i crontab) | 5 min | ai-frontier GAPS P1 | Afventer VPS |
| 3 | Tilføj reranking i ctx (Cohere API efter Qdrant top-20) | 2-4 timer | ai-frontier WHAT_IF #2 | PoC i sandkasse (S34) |
| 4 | Pipeline health check i daily_sweep.py | 2-3 timer | videns-vedligeholdelse | PoC i sandkasse (S34) |
| 5 | Temporal decay i ctx (`score *= exp(-age_days/30)`) | 1-2 timer | ai-frontier GAPS P2 | PoC i sandkasse (S34) |
| 6 | Blog RSS feeds (Anthropic + OpenAI blog) | 2-3 timer | videns-vedligeholdelse | PoC i sandkasse (S34) |
| 7 | VPS→PC sync design (git eller rsync) | 4-6 timer | YGGDRA_SCAN | Planlagt |

## Klar (research done, kan startes)

| Brief | Modenhed | Blokerer | Noter |
|-------|----------|----------|-------|
| memory-architecture | spec'd | — | Fase 1 (reranking+decay) = V4 handlinger 3+5. Samler 2500L research til arkitektur |
| context-engineering | spec'd | research-architecture (delvist) | Hooks fase 1-2 done. GAPS.md P7 (context engineering discipline) er direkte input |
| automation-index | spec'd | — | Oprettet i S34 som `0_backlog/03.AUTOMATION_INDEX.md` |
| research-architecture | spec'd | — | INDEX.md v3 hentet. V4 tilføjer 5 topic-filer + GAPS + WHAT_IF. Fase 2+ venter |

## Næste op (kræver lidt forberedelse)

| Brief | Modenhed | Blokeret af | Mangler |
|-------|----------|-------------|---------|
| notion-spejling | brief | notion MCP | Notion-database + test af mobiltilgang |
| pdf-skill | brief | — | Faktura-layout fra rejseselskab, weasyprint, Tesseract |
| abonnement-overblik | brief | — | PureGym/United Fitness, daglige udgifter, årsopgørelse 2025 |
| cross-session-peer-review | brief | — | Design for parallel session workflow |

## Kræver skærpning (scope uklart)

| Brief | Modenhed | Hvad mangler |
|-------|----------|--------------|
| integrationer | sketch | Gmail MCP done. GDrive/Calendar/Sheets scope uafklaret |
| visualisering | sketch | Scope-valg: data-viz, diagrammer, layout, eller præsentation? |
| voice-integration | sketch | Tre retninger — skal vælge én |

## Lav prioritet / parkeret

| Brief | Modenhed | One-liner |
|-------|----------|-----------|
| project-taxonomy | brief | 7-stage lifecycle præfiks. Design færdigt, kræver migration |
| work-intake | brief | Denne fil ER deliverable. Meta-brief |

## Afsluttet

| Brief | Output | Placering |
|-------|--------|-----------|
| llm-landskab | 7 profiler + COMPARISON + RECOMMENDATION | projects/2_research/llm-landskab/ |
| ai-frontier | 5 topics + GAPS + WHAT_IF | projects/2_research/ai-frontier/ |
| videns-vedligeholdelse | HOLISTIC_EVAL + PIPELINE_DESIGN + DECAY_MODEL + 3 mere | projects/2_research/videns-vedligeholdelse/ |
| youtube-pipeline-v2 | frame_extractor.py PoC + 3 nye kanaler (på VPS) | VPS: /root/Yggdra/scripts/ |
| vps-prompt-v6-consolidation | 14 destillater hentet, 40 filer slettet fra LIB.ydrasil | projects/2_research/ |

## Afhængigheder

```
research-architecture ──→ context-engineering (INDEX.md som input)
memory-architecture fase 1 ──→ V4 handlinger 3+5 (same work)
notion MCP ──→ notion-spejling
faktura-layout ──→ pdf-skill
V4 handlinger 1-2 ──→ VPS session (direkte implementering)
V4 handlinger 3-7 ──→ VPS session (kode-ændringer)
```

## Session-forslag

1. **V4 handlinger 1-2** — 20 min total, kræver VPS session, gratis value
2. **context-engineering fase 3-5** — mest modent, størst impact på dagligt arbejde
3. **V4 handlinger 3-5** — 5-8 timer, forbedrer retrieval-kvalitet markant
4. **automation-index** — quick win, men V4 dækker 80%. Vurder om det stadig er nødvendigt
