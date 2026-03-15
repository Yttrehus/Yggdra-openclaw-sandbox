# TransportIntra — Projektarkiv

Komplet arkiv over TI-projektet: webapp-klon af TransportIntra til rute 256 (organisk affald, Aarhus).

## Formål

Dette er et **arkiv-projekt** — en destillering af alt TI-materiale fra dec 2025 til mar 2026. Det aktive TI-projekt lever i `projects/transport/`. Her ligger historik, analyse, og struktureret overblik.

## Status

- **Sortering:** DONE (drag+drop, profiler, feb 2026)
- **Navigation:** PLANLAGT (GPS-kode eksisterer, ikke integreret)
- **Redesign:** PARTIAL (v2/ og redesign/ prototyper)
- **Chat:** PARTIAL (TiChat + ydrasilChat implementeret)

## Struktur

```
projects/transportintra/
├── CONTEXT.md          ← denne fil
├── INDEX.md            ← komplet guide, crown jewels, hurtigreference
├── PROGRESS.md         ← kronologisk narrativ dec 2025 → mar 2026
├── _scan/              ← rå scans (sessions, technical)
│   ├── sessions.md
│   ├── sessions_chatlogs.md
│   ├── sessions_exports.md
│   ├── technical.md
│   ├── technical_app.md
│   └── technical_infra.md
└── subprojects/
    ├── sorting/CONTEXT.md    — DONE: drag+drop, profiler
    ├── navigation/CONTEXT.md — PLANLAGT: GPS, waypoints, kort
    ├── redesign/CONTEXT.md   — PARTIAL: v2/, redesign/, command-center/
    └── chat/CONTEXT.md       — PARTIAL: TiChat, ydrasilChat
```

## Relation til projects/transport/

| | projects/transport/ | projects/transportintra/ |
|---|---|---|
| **Formål** | Aktivt projekt, daglig brug | Arkiv, historik, analyse |
| **CONTEXT.md** | State + næste opgaver | Overblik + subprojects |
| **Vedligeholdes** | Løbende | Sjældent |

## Key files (se INDEX.md for komplet)

- `INDEX.md` — crown jewels, kategorier, hurtigreference
- `PROGRESS.md` — 4 faser, 4 kausale kæder
- `_scan/sessions.md` — alle sessioner kronologisk
- `_scan/technical.md` — teknisk inventar

## Kildeindex

Bygget fra `projects/transport/TI_KOMPLET_KILDEINDEX.md` (519 linjer) — den autoritative kilde til alle TI-filer.

## Kill condition

Hvis INDEX.md ikke refereres i 20 sessioner → arkivér hele mappen.
