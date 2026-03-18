# Command Center — Subproject

## Status: PROTOTYPE (system-level, ikke TI-specifikt)

## Hvad
Dashboard/overview der samler system-status for Ydrasil.
Eksisterer som fungerende prototype med frontend + backend.
**NB:** Dashboardet viser cron/health/agents — IKKE TI-data (ruter, stop, tidsreg).

## Eksisterende kode

### Frontend: `app/command-center/` — 4 filer, 690 linjer
- `index.html` (214L) — Tabler UI, dark theme, sidebar: Dashboard + Chat views
- `dashboard.js` (205L) — Henter fra `/api/dashboard/*`, viser cron-status med farvekodede badges, health checks, projekt-status, stale-filer
- `chat.js` (186L) — Chat-interface der sender til `/chat` (port 3004)
- `style.css` (85L) — Custom dark-theme styling

### Backend: `scripts/dashboard_api.py` — 441 linjer, port 3005
- 6 endpoints: ping, health, cron, projects, stale, agents, stats
- `get_cron_status()` — parser crontab, checker log-freshness
- `get_health_checks()` — Qdrant, Telegram, Trello, Google OAuth
- `get_projects()` — læser projekt-mapper og NOW.md
- `get_stats()` — cost_daily.json, episodes.jsonl

## Hvad mangler for TI-integration
- Ingen TI API-kald (getRute, getDisps4day, getTimeReg)
- Ingen rute-visning, stop-overblik, eller tidsreg-data
- Ingen kobling til TransportIntra API overhovedet

## Dokumentation
- INDEX.md (l.64-67): "dashboard-eksperiment" fra feb 2026, del af 3 app-versioner
- Redesign subproject refererer til command-center som "dashboard + chat eksperiment"
- technical_app.md bekræfter 4 filer, 690 linjer

## Vurdering
Fungerende system-dashboard, men TI-subproject-kategorisering er diskutabel.
Relevant for TI først når det udvides med TI-endpoints.
