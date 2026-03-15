# Ydrasil

## Metadata
- **Status:** Aktivt — setup + VPS session pipeline
- **Oprettet:** 2026-03-15
- **Sidst opdateret:** 2026-03-15
- **Ejer:** Yttre + Claude

## Hvad er det
Forfaderens hukommelse. Giver PC Claude adgang til VPS Claudes fulde historie — sessions, research, Qdrant. To sjæle, ét overblik. Ikke et kuraterings-projekt — et reference library med søgbar adgang.

## Indhold

### Lokalt (dette projekt)
- **research/** — 157 filer: 10-kapitel AI handbook, agent research, memory research, HOW_TO_BUILD_AGENTS (104K crown jewel)
- **docs/** — 73 filer: DAGBOG, biografi, audits, TransportIntra, TELOS, YDRASIL_ATLAS

### VPS (72.62.61.51)
- **127 Claude Code sessions** — jan-feb 2026 (Ydrasil-æraen)
- **9 projekter** med CONTEXT.md: transport, assistent, rejse, bogføring, forskning, arkitektur, automation, notion, research-architecture
- **60+ Python scripts** — embeddings, automation, ops
- **Qdrant** — 7 collections, 84K vektorer (knowledge, advisor_brain, docs, routes, sessions, conversations, miessler_bible)

## Hvor er vi
- Projekt oprettet, filer flyttet fra projects/research/ydrasil/
- VPS sessions skal downloades og køres gennem chatlog-engine
- Qdrant-adgang fra PC skal sættes op (VPS guide klar)
- INDEX.md skal bygges

## Hvad mangler
- [ ] Download VPS sessions + kør chatlog-engine → vps-chatlog.md
- [ ] Qdrant setup fra PC (SSH tunnel + ctx)
- [ ] INDEX.md med alle datakilder

## Beslutninger
- **Ingen batch-kuratering** — filer kurateres on-demand når andre projekter refererer dem (Fool pre-mortem + socratisk analyse viste at batch-kuratering staller)
- **Sessions > research-filer** — den reelle viden sidder i samtalehistorik, ikke i statiske docs
- **Qdrant > INDEX.md** — semantisk søgning slår flad markdown-liste
- **Subagent-data later** — 781 subagent JSONL-filer processeres kun hvis der er behov

## Åbne tråde
- chatlog-engine.js skal have --input-dir/--output flags
- -root-Ydrasil og -root-Yggdra på VPS er identiske (127=127) — kun download fra én
- 3 sessions i -root/ (uden projekt) — skal med

## Changelog
- 2026-03-15: Projekt oprettet. Flyttet fra projects/research/ydrasil/. Plan godkendt efter Fool-analyse.
