# Tidsregistrering — Subproject

## Status: EKSISTERENDE (umodificeret TI-klon, ikke et udviklingsprojekt)

## Hvad
Fuldt fungerende tidsregistrering via TI API. Original kode, ikke modificeret.

## Eksisterende kode

### Tidsreg.js — 1652 linjer, produktion
- Konstruktør: `function Tidsreg()` med state (timereg, veh_hist, errors, wrkHrs, vehicles)
- UI-knapper: Start, Pause, Andet, Addon, Slut, Approve, Reason, Remark, Cancel, Ok
- Forvogn/trailer-håndtering (vognChanged, parkering)
- Metoder: `show()`, `yesterday()`, `tomorrow()`, `setDate()`, `getState()`
- GPS-integration: START_DAG → `startRouteRecording()`, SLUT_DAG → `stopRouteRecording()` (l.1231-1241)

### API: `getTimeReg`
- Params: `action="getTimeReg"`, `getLists=true`, `date` (ISO), `key`, `version`
- Response: ~40 KB med tidsregistreringer + lister
- Kaldt fra `Tidsreg.setState()` i Tidsreg.js:133
- Dokumenteret i `data/TRANSPORTINTRA_API_REFERENCE.md:87-101`

## Session-referencer
Ingen session-diskussioner om tidsreg-ændringer.
INDEX.md (l.54): "Tidsreg.js er størst men mindst modificeret — det er original TI-kode."

## Vurdering
Fuldt fungerende produktionskode. Ingen ændringer diskuteret eller planlagt.
Subproject-stub er unødvendig — tidsreg er færdig kode, ikke et udviklingsprojekt.
Genaktivér kun hvis forbedringer (UI, eksport, kørselsgodtgørelse) bliver aktuelle.
