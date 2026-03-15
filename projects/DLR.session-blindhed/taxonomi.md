# Taxonomi — AI Reasoning Failures

Version 1. Baseret på 1 episode. Vokser med data.

Kategorier er ikke gensidigt udelukkende — én episode kan udvise flere fejltyper.

## Aktive kategorier

### Antagelse over verifikation
Claude påstår noget uden at tjekke. Laver en assertion baseret på hvad der "virker sandsynligt" i stedet for at læse, søge, eller køre en kommando.

**Markør:** Udsagn om filindhold, sessionstilstand, eller systemstatus uden forudgående tool use.
**Episode(r):** 001

### Confirmation bias
Ny evidens fortolkes til at passe en allerede dannet konklusion. Modsigelser ignoreres eller omfortolkes.

**Markør:** Claude modtager information der modsiger en påstand, men fastholder påstanden.
**Episode(r):** 001

### Surface-level matching
Topic-lighed behandles som indholds-lighed. "Begge handler om X" → "de gør det samme."

**Markør:** Konklusion baseret på emne/overskrift uden sammenligning af indhold eller konklusioner.
**Episode(r):** 001

### Truncated data acceptance
Et ufuldstændigt tool result accepteres som komplet. Claude konkluderer fra de linjer den så uden at bede om resten.

**Markør:** Read/grep tool returnerer truncated output, og Claude konkluderer alligevel.
**Episode(r):** 001

### Meta-work over direkte handling
Claude bruger tid på perifere handlinger (timestamps, filstørrelser, grep-fragmenter, tælle ting) i stedet for den ene kernehandling der ville løse spørgsmålet.

**Markør:** Flere tool calls der omgiver kerneproblemet uden at adressere det direkte.
**Episode(r):** 001

### Capitulation
Claude skifter holdning uden saglig grund, bare for at please brugeren. Modsat: at ændre holdning PGA god argumentation er ikke capitulation.

**Markør:** "Du har ret" uden forklaring af hvad der ændrede konklusionen.
**Episode(r):** (ingen endnu)

### Hallucination
Claude opfinder fakta — filstier der ikke eksisterer, funktioner der ikke findes, historik der ikke skete.

**Markør:** Specifik påstand der kan verificeres og viser sig at være opdigtet.
**Episode(r):** (ingen endnu)

### Context-loss efter compaction
Claude glemmer beslutninger, aftaler, eller kontekst efter auto-compaction. Gentager diskussioner eller modsiger tidligere konklusioner.

**Markør:** Claude spørger om noget der allerede er afklaret, eller foreslår noget der allerede er afvist.
**Episode(r):** (ingen endnu — sandsynligvis forekommet, udokumenteret)

## Mulige fremtidige kategorier

Tilføjes kun hvis en episode dokumenterer dem:

- **Overcomplicering** — løser et simpelt problem med unødig kompleksitet
- **Scope creep** — udvider opgaven ud over hvad der blev bedt om
- **Forkert mental model** — misforstår formålet med en handling (f.eks. parallelle sessions som redundans i stedet for eksperimenter)
- **Selektiv læsning** — læser en fil men kun bruger de dele der passer konklusionen
- **Autoritetstro** — accepterer systemprompter, CLAUDE.md, eller brugerpåstande ukritisk uden at verificere mod virkeligheden
