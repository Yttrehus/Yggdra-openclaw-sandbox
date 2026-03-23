# Triage — Prioriteret overblik

Sidst opdateret: 2026-03-22 (Session 34)

## V4 Handlinger (fra HOLISTIC_EVALUATION)

Prioriteret efter impact × (1/effort).

| # | Handling | Effort | Kilde | Status |
|---|---------|--------|-------|--------|
| 1 | Fix RSS feed bug (tilføj `fetch_rss_feeds()` kald i ai_intelligence.py) | 15 min | videns-vedligeholdelse | Afventer VPS sync |
| 2 | Genaktivér heartbeat.py (uncomment i crontab) | 5 min | ai-frontier GAPS P1 | Afventer VPS sync |
| 3 | Tilføj reranking i ctx (Cohere API efter Qdrant top-20) | 2-4 timer | ai-frontier WHAT_IF #2 | **PoC OK (S34)** |
| 4 | Pipeline health check i daily_sweep.py | 2-3 timer | videns-vedligeholdelse | **PoC OK (S34)** |
| 5 | Temporal decay i ctx (`score *= exp(-age_days/30)`) | 1-2 timer | ai-frontier GAPS P2 | **PoC OK (S34)** |
| 6 | Blog RSS feeds (Anthropic + OpenAI blog) | 2-3 timer | videns-vedligeholdelse | **PoC OK (S34)** |
| 7 | VPS→PC sync design (git eller rsync) | 4-6 timer | YGGDRA_SCAN | Planlagt |

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

## Afsluttede / Brændte (S34 Burn)
- `01.memory-architecture` → PoC færdig i `SIP.agent-sandbox/retrieval_v2/`.
- `02.context-engineering` → Hooks implementeret og dokumenteret.
- `03.automation-index` → Dokumenteret i `03.AUTOMATION_INDEX.md`.
- `03.webscraping-audit` → Erstattet af `03.SCRAPING_POLICY.md`.
- `04.notion-spejling` → Dokumenteret i `04.NOTION_INTEGRATION.md`.
- `06.abonnement-overblik` → Dokumenteret i `06.FINANCIAL_SNAPSHOT.md`.
- `07.voice-integration` → Erstattet af `07.VOICE_EXPERIENCE.md`.
- `project-taxonomy` → Færdiggjort med `LIB.research` migration.

---
**Note:** Alle rå briefs er flyttet til `9_archive/briefs/`.
