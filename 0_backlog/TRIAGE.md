# Triage — Prioriteret overblik

Sidst opdateret: 2026-05-23 (Session 100)

## V7 Roadmap (Real-world API Integration)

Prioriteret efter teknisk afhængighed.

| ID | Handling | Estimat | Kategori | Status |
|----|----------|---------|----------|--------|
| 1 | Google OAuth2 - Fra Mock til Reel (Secret Management) | 4-6 timer | Infrastructure | Planlagt (V7.1) |
| 2 | Notion DB Init & Live Sync (VPS Deployment) | 3-4 timer | Accessibility | Planlagt (V7.1) |
| 3 | ElevenLabs SDK Integration (SSML Support) | 2-3 timer | Voice | Planlagt (V7.1) |
| 4 | Geo-Fencing Integration (Real GPS Triggers) | 4-8 timer | Context | Research (V7.2) |

## Aktive Projekter (READY for V7)

| Projekt | Stage | Mål | Næste Step |
|---------|-------|-----|------------|
| **04.NOTION_INTEGRATION** | BMS/PoC | Mobil-overblik via Notion MCP | Initialisér DB i Notion |
| **07.VOICE_EXPERIENCE** | BMS/v1.0 | Real-time cadence, pitch og personlighed | **READY (V6.4)** |
| **08.API_ACTION_LAYER** | DLR/v1.0 | Gå fra simulation til reelle API-kald | **READY (Lag 3 Simulation OK)** |
| **09.DYNAMIC_MEMORY** | BMS/Init | Implementering af Dynamic RAG | Prototyp i memory.py |
| **02.BACKLOG_BURN** | BMS | Løbende backlog vedligeholdelse | Kør næste burn 2026-05-05 |

## Vedtagne Politikker & Standarder

| Dokument | Formål | Status |
|----------|--------|--------|
| `MISSION.md` | Strategisk vision og kerne-mål | **AKTIV** |
| `02.PEER_REVIEW_PROTOCOL.md` | Adversarial kvalitetssikring | **AKTIV** |
| `03.SCRAPING_POLICY.md` | Omkostningseffektiv scraping | **AKTIV** |
| `LIB.research/05.RESEARCH_KVALITET/APA_STANDARDS.md` | Epistemisk sporbarhed | **AKTIV** |

## Afsluttede / Brændte (S35 Status)
- `MISSION.md` → Etableret som projektets fundament.
- `scripts/sync_vps_to_pc.py` → Tool v1.0 klar til drift.
- `scripts/the_last_algorithm.py` → Strategisk motor v1.0 klar.
- `01.memory-architecture Fase 1` → **Gennemført**. Retrieval v2.1 er aktiv.
- `01.memory-architecture Fase 2` → **Gennemført**. Fact Extraction v2.1 integreret.
- `project-taxonomy` → Færdiggørelse af `LIB.research` migration.

---
**Note:** Alle rå briefs er flyttet til `9_archive/briefs/`.
