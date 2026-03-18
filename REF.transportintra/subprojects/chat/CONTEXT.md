# Chat — TiChat + YdrasilChat

Chat-funktionalitet: intern chauffør-kommunikation og AI-assistent.

## Status: PARTIAL (kode eksisterer, ikke i daglig brug)

Begge chat-moduler er implementeret men ikke færdigintegreret.

## Hvad eksisterer

- **TiChat.js** (561 linjer) — TransportIntra's native chat via checkMail API
  - Gruppechats, besked-visning, chatrum
  - Kalder checkMail endpoint (dokumenteret i API-reference)
- **ydrasilChat.js** (491 linjer) — AI chat-integration (Kristoffers tilføjelse, feb 2026)
  - Samtale med AI om rute, stops, data
  - Kontekst-aware: ved hvilken rute/stop der er aktiv

## Hvad mangler

- **Chat-preview** — notifikation om nye beskeder uden at åbne chat
- **Push-notifikationer** — chauffør-til-chauffør real-time
- **AI-kontekst** — ydrasilChat bør kende rutedata, historik, profiler
- **Offline-support** — cache beskeder når netværk mangler

## Key files

- `app/js/TiChat.js` — TI's native chat
- `app/js/ydrasilChat.js` — AI chat
- `app/js/MsgFeat.js` (429 linjer) — meddelelsessystem (relateret)

## Beslutninger

- ydrasilChat bruger Qdrant `routes` collection for kontekst
- TiChat wrapper'er TI's egen chat-API (ikke en erstatning)

## Afhængigheder

- checkMail API-endpoint (dokumenteret i API-reference)
- Qdrant for AI chat-kontekst
