# Sorting — Drag+Drop Sortering

Sorteringssystemet: fra manuelt til automatiseret rækkefølge af stops.

## Status: DONE (feb 2026)

Kerneproblemet løst: kunder vises i den rækkefølge chaufføren kører dem.

## Hvad er bygget

- **Drag+drop** i Ruter.js — flyt stops manuelt, gem via updateRDisp
- **sortProfiles.js** (363 linjer) — gemte sorteringsprofiler per rute/dag
- **Sorteringsnr 0** = ny/ukendt kunde → behold getRute-rækkefølge (beslutning 3/1-2026)
- **Sorteringsknap** i UI — testet og verificeret i produktion

## Kausale kæder

Tilfældig rækkefølge (2/12) → n8n+Sheets sortering (13/12) → nr 0-logik (3/1) → drag+drop webapp (feb) → profiler fra Excel (15/2)

## Key files

- `app/js/sortProfiles.js` — profillogik
- `app/js/Ruter.js` — drag+drop implementation (linje ~800-1000)
- `data/gdrive_import/256_ORG2ÅRH_Mandag.csv` — profil-kilde

## Beslutninger

- Profiler fra Excel CSV, ikke API (15/2) — API har ikke sorteringsdata
- Two-way door: classic/ vs enhanced/ — reversibel (15/2)

## Mangler (nice-to-have)

- Auto-profil per ugedag (mandag ≠ tirsdag)
- Synk profiler til andre chauffører
- Historik-baseret forslag (data/routes/ har 577 dages data)
