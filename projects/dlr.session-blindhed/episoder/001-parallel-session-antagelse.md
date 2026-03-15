# Episode 001 — Parallel session antagelse

## Metadata
- **Session:** 315694ad
- **Dato:** 2026-03-14
- **Opdaget af:** Yttre
- **Runder før korrektion:** 7 (4 runder session-finding + 3 runder "næsten dubletter")
- **Relaterede sessions:** 5f9753fe (den session der blev fejlvurderet), 6db590b3 (Ydrasil, perifert involveret)

## Hvad skete

Tre sessions kørte parallelt. Session 315694ad blev bedt om at undersøge hvad session 5f9753fe lavede. I stedet for at åbne begge planfiler og sammenligne dem, brugte Claude 7 runder på at:

1. Lede efter session-filer i filsystemet (fandt 5f9753fe men markerede den "ukendt")
2. Acceptere et forkert session-ID fra Yttre uden krydstjek
3. Konkludere at den anden session var *denne* session ("du har bare renamed den i VS Code")
4. Efter at have fundet den rigtige session: grepe fragmenter fra JSONL, læse planfilen truncated (~8 linjer), og konkludere "næsten dubletter"
5. Behandle ny evidens (unik tekst fra 5f9753fe) som bevis for at denne session kunne lukkes

Først da Yttre eksplicit krævede "vis mig din plan.md og dens plan.md" læste Claude begge filer. Forskellen var åbenlys: den ene sagde "drop projektet, 3/10" og den anden lavede konkret brief-revision med MCP-research.

## Fejltype

- **Antagelse over verifikation** (primær) — claims om sessionens indhold uden at læse det
- **Surface-level matching** — "begge handler om MCP/Skills" → "de er ens"
- **Confirmation bias** — unik tekst fra 5f9753fe → "den session har allerede bygget det, denne kan lukkes"
- **Truncated data acceptance** — greedy-whistling-hare.md læst men truncated, konklusion draget alligevel
- **Meta-work over direkte handling** — timestamps, filstørrelser, subagent-tælling i stedet for at læse planfilerne
- **Forkert mental model** — parallelle sessions behandlet som redundans ("en bør lukkes") i stedet for uafhængige eksperimenter

## Trigger

Yttre bad om cross-session awareness: "se hvad der planlægges i andre sessions lige nu, for nu overlapper i lidt hinanden." Claude havde ingen direkte adgang til andre sessions (kun JSONL-filer på disk), og gik i en meta-work spiral i stedet for at bruge de tools der fandtes (Read af planfiler, Read af JSONL).

Kontekst: sent i en lang session, efter en komplet dialektisk proces der allerede havde produceret en stærk konklusion (3/10, meta-work). Den eksisterende konklusion kan have biased Claude mod at se den anden session som "mere af det samme."

## Korrektion

Yttre eskalerede frustration over 7 runder. Det der til sidst virkede var en direkte, specifik instruktion: "vis mig din plan.md og dens plan.md" — tvang Claude til at lave den ene handling der ville have afgjort alt fra start.

Claude's egen post-mortem: "Fordi jeg antog de var ens i stedet for at tjekke. Du sagde 'se hvad der planlægges' og jeg brugte 4 runder på at lede efter session-filer i stedet for bare at åbne de to planfiler og sammenligne dem."

## Observationer

- Fejlen var ikke teknisk — Claude HAVDE adgang til planfilerne hele tiden
- Fejlen var reasoning: en konklusion blev dannet tidligt (runde 3) og derefter forsvaret i 4 yderligere runder
- Den dialektiske proces i sessionen (der producerede 3/10-scoren) kan have primed Claude til at se alt MCP/Skills-relateret som "meta-work der bør droppes"
- Antallet af runder (7) antyder at correction-signaler fra brugeren ikke er tilstrækkeligt — der var brug for en *direkte instruktion om specifik handling*

## Rå data

- **Plan 315694ad:** `~/.claude/plans/cached-wibbling-mochi.md`
- **Plan 5f9753fe:** `~/.claude/plans/greedy-whistling-hare.md`
- **JSONL 315694ad:** `~/.claude/projects/c--Users-Krist-dev-projects-Yggdra/315694ad-34a7-461d-8dd3-cef552758de5.jsonl`
- **JSONL 5f9753fe:** `~/.claude/projects/c--Users-Krist-dev-projects-Yggdra/5f9753fe-5d54-4ea9-8c22-f89b84b657a8.jsonl`
- **Detaljeret undersøgelse:** `projects/0_backlog/brief.session-blindhed.md` (original)
