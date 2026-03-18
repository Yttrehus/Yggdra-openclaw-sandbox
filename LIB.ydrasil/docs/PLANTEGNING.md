# Plantegning: Ydrasil System

*Version 0.1 — 2026-02-03*
*Levende dokument. Opdateres løbende.*

---

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE SESSION                       │
│                   (Opus 4.5 / Sonnet)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HUKOMMELSE (hvad jeg "ved")                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ CLAUDE.md    │  │ 4 Skills     │  │ Samtale-kontekst │  │
│  │ (instruks)   │  │ (domæne-     │  │ (denne session)  │  │
│  │              │  │  viden)      │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│  ┌──────┴─────────────────┴────────────────────┴─────────┐  │
│  │              KONTEKSTVINDUE (~200k tokens)             │  │
│  │  Alt jeg kan "se" lige nu. Resten er glemt.           │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                  │
│  VÆRKTØJER (hvad jeg kan "gøre")                            │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │ Bash   │ │ Read/  │ │ Web      │ │ MCP Qdrant (×3)   │  │
│  │ (shell)│ │ Write/ │ │ Search/  │ │ ┌───────────────┐ │  │
│  │        │ │ Edit   │ │ Fetch    │ │ │ routes 40k pts│ │  │
│  │        │ │ Glob   │ │          │ │ │ conversations │ │  │
│  │        │ │ Grep   │ │          │ │ │ docs          │ │  │
│  └────────┘ └────────┘ └──────────┘ │ │ sessions 1.5k │ │  │
│                                      │ │ knowledge     │ │  │
│                                      │ └───────────────┘ │  │
│                                      └───────────────────┘  │
│  HOOKS (automatisk)                                         │
│  ┌──────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │ SessionStart │ │ SessionEnd    │ │ PreCompact        │  │
│  │ load_check-  │ │ save_check-   │ │ save_check-       │  │
│  │ point.sh     │ │ point.py      │ │ point.py          │  │
│  └──────────────┘ └───────────────┘ └───────────────────┘  │
│                                                             │
│  SLASH COMMANDS                                             │
│  ┌──────────────┐ ┌───────────────┐                        │
│  │ /context     │ │ /audit        │                        │
│  │ (Qdrant søg) │ │ (health chk)  │                        │
│  └──────────────┘ └───────────────┘                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BAGGRUNDSPROCESSER (kører uden mig)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Cron: tmux logs → Qdrant embeddings (hver time)     │   │
│  │ Cron: huskeliste scanner (hver time :30)             │   │
│  │ Cron: auto_dagbog (23:55 dagligt)                    │   │
│  │ Cron: backup (04:00 dagligt)                         │   │
│  │ Cron: weekly_audit (søndag 06:00)                    │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Docker: Traefik (SSL) → Nginx (webapp) → Qdrant     │   │
│  │ Systemd: ydrasil-webapp (3000), secondbrain-api      │   │
│  │ Manuel: api_logger.py (3003)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  DISABLED (eksisterer men kører ikke)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ youtube_monitor, source_discovery, navigator         │   │
│  │ substack_scraper (ingen cron)                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  DATAFLOWS                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Voice memo → Whisper → Fabric classify_intent →     │   │
│  │   ├→ COMMAND/HIGH → huskeliste.md                    │   │
│  │   ├→ OBS/IDEA/Q  → Qdrant conversations             │   │
│  │   └→ THOUGHT/LOW → markdown only                     │   │
│  │                                                      │   │
│  │ Webapp → dataLogger.js → api_logger.py (3003) →     │   │
│  │   → /data/api_logs/YYYY-MM-DD.jsonl                  │   │
│  │                                                      │   │
│  │ Tmux session → hourly logs → process_session_log →  │   │
│  │   → Qdrant sessions → auto_dagbog → DAGBOG.md       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  KRITISK MANGEL (identificeret 2026-02-03)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⚠ Ingen feedback-loop til brugeren                   │   │
│  │ ⚠ Systemet samler info men leverer den ikke tilbage  │   │
│  │ ⚠ Backup er aldrig restore-testet                    │   │
│  │ ⚠ Qdrant MCP fejler (vector name error)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Næste iteration bør inkludere
- Detaljeret port-map med firewall-status
- Dependency-graf (hvad afhænger af hvad)
- Failure modes (hvad sker når X dør)
- Brugerens faktiske touchpoints (hvornår/hvordan Kris interagerer)
- Cost-flow (hvad koster hvad, og hvem kalder hvem)
