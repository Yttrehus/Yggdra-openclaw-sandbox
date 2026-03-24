# Triage — Prioriteret overblik

Sidst opdateret: 2026-03-23 (Session 35)

## V4 Handlinger (fra HOLISTIC_EVALUATION)

Prioriteret efter impact × (1/effort).

| # | Handling | Effort | Kilde | Status |
|---|---------|--------|-------|--------|
| 1 | Fix RSS feed bug (tilføj `fetch_rss_feeds()` kald i ai_intelligence.py) | 15 min | videns-vedligeholdelse | Afventer VPS sync |
| 2 | Genaktivér heartbeat.py (uncomment i crontab) | 5 min | ai-frontier GAPS P1 | **PoC OK (S35)** |
| 3 | Tilføj reranking i ctx (Cohere API efter Qdrant top-20) | 2-4 timer | ai-frontier WHAT_IF #2 | **DEPLOYED (v2.1)** |
| 4 | Pipeline health check i daily_sweep.py | 2-3 timer | videns-vedligeholdelse | **PoC OK (S34)** |
| 5 | Temporal decay i ctx (`score *= exp(-age_days/30)`) | 1-2 timer | ai-frontier GAPS P2 | **DEPLOYED (v2.1)** |
| 6 | Blog RSS feeds (Anthropic + OpenAI blog) | 2-3 timer | videns-vedligeholdelse | **PoC OK (S34)** |
| 7 | VPS→PC sync design (git eller rsync) | 4-6 timer | YGGDRA_SCAN | **Planlagt (S35 Sync-script)** |

## Aktive Projekter (Klar til eksekvering)

| Projekt | Stage | Mål | Næste Step |
|---------|-------|-----|------------|
| **04.NOTION_INTEGRATION** | BMS/PoC | Mobil-overblik via Notion MCP | Opret database i Notion |
| **07.VOICE_EXPERIENCE** | SIP/PoC | Real-time cadence og personlighed | Test latency i Groq pipeline |
| **02.BACKLOG_BURN** | BMS | Løbende backlog vedligeholdelse | Kør næste burn 2026-04-05 |

## Vedtagne Politikker & Standarder

| Dokument | Formål | Status |
|----------|--------|--------|
| `02.PEER_REVIEW_PROTOCOL.md` | Adversarial kvalitetssikring | **AKTIV** |
| `03.SCRAPING_POLICY.md` | Omkostningseffektiv scraping | **AKTIV** |
| `05.RESEARCH_KVALITET/APA_STANDARDS.md` | Epistemisk sporbarhed | **AKTIV** |

## Afsluttede / Brændte (S35 Status)
- `01.memory-architecture Fase 1` → **Gennemført**. Retrieval v2.1 er aktiv i `scripts/get_context.py`.
- `01.memory-architecture Fase 2` → **Gennemført**. Fact Extraction v2.1 integreret i `pre_compact.sh`.
- `02.context-engineering` → Hooks implementeret og dokumenteret.
- `03.automation-index` → Dokumenteret i `03.AUTOMATION_INDEX.md`.
- `project-taxonomy` → Færdiggørelse af `LIB.research` migration.

---
**Note:** Alle rå briefs er flyttet til `9_archive/briefs/`.
