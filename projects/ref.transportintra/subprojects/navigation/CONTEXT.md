# Navigation — GPS Tracker + Waypoints

GPS-baseret navigation tilpasset lastbilkørsel og affaldsindsamling.

## Status: PLANLAGT (fundament eksisterer)

Kode er skrevet men ikke integreret i daglig brug.

## Hvad eksisterer

- **GPSTracker.js** (382 linjer) — positionsregistrering via regGPSPos API
- **waypoints.js** (483 linjer) — waypoint-håndtering
- **RuteMap.js** (661 linjer) — kortvisning af rute (Leaflet/map)
- **distanceService.js** (310 linjer) — afstandsberegning mellem stops

## Hvad mangler

- **GPS-override** — lastbil-GPS vs. telefon-GPS (præcision)
- **Køretidsforudsigelse** — estimeret tid per stop baseret på historik
- **Trafikdata** — integration med trafik-API
- **AI-ruter** — optimeret rækkefølge baseret på GPS + trafik
- **Åbningstider** — kunder med tidsvinduer
- **Turn-by-turn** — navigation tilpasset lastbil (højde, bredde, vendeplads)

## Key files

- `app/js/GPSTracker.js` — GPS core
- `app/js/waypoints.js` — waypoint-logik
- `app/js/RuteMap.js` — kortvisning
- `app/js/distanceService.js` — afstandsberegning
- Qdrant `routes` collection — 40K stops med GPS-koordinater

## Beslutninger

- Endnu ingen. Afventer prioritering vs. stop-beskrivelser og ikoner.

## Afhængigheder

- GPS-data kræver kørsel i produktion for at teste
- Lastbil-specifikke ruter kræver ekstern tjeneste (Google/HERE/OSRM)
