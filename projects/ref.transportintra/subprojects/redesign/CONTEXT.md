# Redesign — v2 App + UI Overhaul

Ny arkitektur og nyt design til TI webapp.

## Status: PARTIAL (prototyper eksisterer)

To parallelle forsøg: v2/ (ren arkitektur) og redesign/ (UI-prototype).

## Hvad eksisterer

- **v2/** (7 filer, 2107 linjer) — ny arkitektur med store/api/map separation
  - `v2/app.js`, `v2/route-detail.js`, `v2/api.js`, `v2/store.js`, `v2/map.js`, `v2/routes.js`, `v2/sw.js`
- **redesign/** (1 fil, 1062 linjer) — standalone HTML prototype med inline CSS/JS
- **command-center/** (4 filer, 690 linjer) — dashboard + chat eksperiment

## Arkitektonisk retning

v2/ adskiller concerns: `api.js` (HTTP), `store.js` (state), `map.js` (kort), `routes.js` (data).
Nuværende app (js/) er monolitisk: Ruter.js gør alt.

## Hvad mangler

- Valg: v2/ eller redesign/ som fremtid?
- Feature-paritet med js/ (login, sortering, tidsreg)
- Konsolidering af 3 JS-versioner (js/, js.bak.20260215/, classic/js/)
- Mobiloptimering (nuværende app er jQuery Mobile)

## Key files

- `app/v2/` — ny arkitektur
- `app/redesign/` — UI-prototype
- `app/command-center/` — dashboard
- `app/classic/` — frozen backup (15/2-2026)

## Beslutninger

- Two-way door: classic/ gemt som rollback (15/2)
- v2/ bygger på moderne JS (ingen jQuery Mobile)
- Ingen beslutning endnu om v2 vs redesign som retning
