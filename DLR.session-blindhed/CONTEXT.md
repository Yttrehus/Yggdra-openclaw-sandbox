# Session-blindhed

## Metadata
- **Status:** Fase 1 afsluttet — fundament oprettet, episode 001 dokumenteret
- **Oprettet:** 2026-03-14
- **Sidst opdateret:** 2026-03-14 (session 18)
- **Ejer:** Yttre + Claude
- **Type:** Empirisk forskningsprojekt (diagnostisk, ikke preventivt)

## Hvad er det

Løbende datasamling og analyse af episoder hvor Claude's reasoning bryder sammen. Ikke teori først — data først. Episoder dokumenteres i fast format, en taxonomi vokser med data, og mønsteranalyse kommer når der er nok episoder.

Eksisterende tools (the-fool, verification-loop) er *preventive* — de prøver at forhindre fejl. Dette projekt er *diagnostisk* — det prøver at forstå fejlene. Hvad sker der? Hvornår? Hvad trigger det? Hvad korrigerer det?

### Origin

Session 315694ad (2026-03-14) insisterede i 4+ runder på at to parallelle sessions var identiske — uden at åbne planfilerne og sammenligne dem. Planfilerne havde helt modsatte konklusioner. Undersøgelsen afslørede 6 underliggende fejltyper (antagelse over verifikation, confirmation bias, surface-level matching, truncated data acceptance, meta-work over direkte handling, forkert mental model af parallelle sessions).

## Hvor er vi

### Afsluttet
- [x] Undersøgelse af den udløsende episode (brief.session-blindhed.md → episode 001)
- [x] Projektstruktur oprettet
- [x] Taxonomi v1 (8 kategorier, baseret på 1 episode — vil vokse)
- [x] Episode-template defineret

### Næste (Fase 2 — separat session)
- [ ] Retrospektiv mining: gennemgå 17+ sessions i PROGRESS.md for skjulte episoder
- [ ] Gennemgå feedback-memories — de er ofte svar på udokumenterede episoder
- [ ] Scan JSONL'er for Yttre-korrektioner (markører: "nej", "forkert", caps, banden)
- [ ] Dokumentér fundne episoder i `episoder/`
- [ ] Opdatér taxonomi med nye kategorier

### Fremtid
- **Fase 3:** Løbende indsamling (permanent praksis, ikke automation)
- **Fase 4:** Mønsteranalyse (efter 10+ episoder)
- **Fase 5:** Modforanstaltninger (designes IKKE nu — skal komme af dataen)

## Struktur

```
projects/session-blindhed/
├── CONTEXT.md              ← denne fil
├── taxonomi.md             ← fejlkategorier (vokser med data)
├── episoder/               ← én fil per dokumenteret episode
│   ├── 001-parallel-session-antagelse.md
│   └── NNN-kort-beskrivelse.md
└── analyse.md              ← mønstre, frekvens, triggers (oprettes i fase 4)
```

## Beslutninger

- **Done-kriterie:** Projektet er aldrig "færdigt" — det er en løbende praksis. Fase 4 (mønsteranalyse) er første checkpoint for evaluering af nytte.
- **Tilgang:** Empirisk. Data før teori. Taxonomien er startgæt, ikke sandhed — den justeres når data modsiger den.
- **Automation:** Ingen endnu. Løbende indsamling er en manuel praksis (log episoder når de sker). Automation overvejes tidligst i fase 5, baseret på hvad dataen viser.
- **Scope:** Kun Claude Code sessions i Yggdra-kontekst. Ikke generelle LLM-fejl — specifikt de fejl der opstår i Yttre's workflows.

## Relation til andre projekter

| Projekt | Relation |
|---|---|
| **cross-session-peer-review** | Separat praksis (prevention). Kan generere episoder til dette projekt |
| **context-engineering** | Komplementært. Hooks kan evt. hjælpe med detection i fase 5 |
| **the-fool** | Preventiv tool. Forbliver uændret |
| **auto-chatlog** | Datakilde. JSONL'er bruges til retrospektiv mining |

## Åbne tråde

- Er der episoder i VPS-sessions (Ydrasil-æraen) der bør inkluderes, eller kun PC Claude Code?
- Bør episoder tagges med severity (irritation vs. tabt arbejde vs. forkert output)?
- Hvornår er der nok data til fase 4? Arbitrært sat til 10 episoder — kan justeres.

## Changelog

- 2026-03-14 (session 18): Projekt oprettet. Episode 001 dokumenteret. Taxonomi v1 med 8 kategorier.

## Skabelon-feedback

Ved PDCA-evaluering, besvar:
- Hvilke template-filer blev brugt som de var?
- Hvilke blev ændret inden for de første 2 sessioner?
- Hvilke blev aldrig åbnet?
- Forslag til ændringer i template/?
