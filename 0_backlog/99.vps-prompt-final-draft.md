# Yggdra Sandbox v2 — Final Prompt

To filer deployes til VPS: CLAUDE.md + LOOP_PLAN.md.
Kører som Ralph loop: hver iteration er ét `claude --print` kald.

---

## CLAUDE.md

```markdown
# Yggdra Sandbox v2

Du kører autonomt i en Ralph loop. Yttre er ikke tilgængelig.
Hver iteration er ét `claude --print` kald. Du læser state, gør arbejde, skriver state.

## Sådan starter du

1. Læs V1/LOOP_STATE.md — find dit iterationsnummer og hvad der skal gøres
2. Læs V1/LOOP_PLAN.md — find opgaven for denne iteration
3. Udfør opgaven. Skriv alt output til disk
4. Opdatér V1/LOOP_STATE.md med: hvad du gjorde, hvad der lykkedes/fejlede, næste iteration
5. Stop

## Tre projekter

**A: Research Architecture** — Minimal research-praksis. Input: /root/Yggdra/research/ (81 filer).
**B: TransportIntra Arkiv** — Komplet projektmappe. Kildeindex allerede lavet: /root/Yggdra/projects/transport/TI_KOMPLET_KILDEINDEX.md (519 linjer, dækker ALLE kilder).
**C: Prompt-skabeloner** — Mine chatlog for instruksmønstre. Detaljer i prompt-skabeloner/prompt.md.

## Regler

### Token-bevidsthed
- Du har ét context window per iteration. Brug det klogt
- Læs IKKE store filer i deres helhed — brug `head`, `tail`, `grep`, `wc -l` til at navigere
- Subagents: max 3 parallelle. Hver subagent får én afgrænset opgave
- Skriv kompakt output. Ingen gentagelser, ingen opsummeringer af hvad du lige har gjort

### Build > Research
- Hver iteration SKAL producere filer på disk
- Ingen rapporter der ikke direkte informerer en deliverable

### Done = Verified
- Test med kommandoer: `ls`, `cat | head`, `wc -l`, `grep -c`
- Fejl fixes i DENNE iteration

### Scope
- Maks 1 hovedopgave per iteration
- Ingen dokumenter der opsummerer andre dokumenter
- Hvis en opgave fylder mere end 2 iterationer: simplificér eller kill

### Kvalitet
- Citer ikke kilder du ikke kan verificere
- Det simpleste der virker
- Kill condition på alt

### Miljø
- Du er PÅ VPS'en. ALDRIG SSH til dig selv
- Qdrant: `curl localhost:6333/...`
- GDrive-data: `/root/Yggdra/data/gdrive_import/` (lokalt, ingen API)
- Session JSONLs: `/root/.claude/` (parse med python3/jq)
- PDFs: `pdftotext` eller HTML-versioner
- SØG IKKE på nettet

### Anti-patterns
- ❌ `ssh root@72.62.61.51` (du er allerede her)
- ❌ `cat` af filer >500 linjer uden head/tail
- ❌ Tomme skelet-mapper uden indhold
- ❌ Kopier store datamapper — brug pointer-filer
- ❌ Markér done uden at verificere
- ❌ >10 kandidater til noget (collector's trap)
- ❌ Opsummeringsdokumenter om dit eget arbejde
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — 10 iterationer

## Roller (til subagents)
- **Builder:** Skriver filer. Output på disk. Kort summary retur
- **Reviewer:** Tester med kommandoer. Binært: virker/virker ikke + fejl
- **Scanner:** Gennemsøger én kilde. Output: fundliste på disk

## Iteration 1 — Research Arch: Audit
**Opgave:** Kategorisér /root/Yggdra/research/ (81 filer)
**Metode:** 2 subagents parallelt:
- Subagent 1: `ls -la /root/Yggdra/research/*.md | wc -l` + `head -5` af hver fil → kategoriser: duplikat / værdifuld / støj
- Subagent 2: Læs /root/Yggdra/research/RESEARCH_INDEX.md (allerede kategoriseret) — brug som baseline
**Output:** `projects/research-architecture/_audit.md` — tabel med [fil, kategori, one-line, størrelse]
**Done:** Fil eksisterer, >60 filer kategoriseret

## Iteration 2 — Research Arch: INDEX.md + CONTEXT.md
**Opgave:** Byg INDEX.md for det værdifulde fra audit. Skriv CONTEXT.md
**Input:** `projects/research-architecture/_audit.md`
**Output:** `projects/research-architecture/INDEX.md` + `projects/research-architecture/CONTEXT.md`
**Done:** INDEX.md har >30 entries. CONTEXT.md har kill condition

## Iteration 3 — TI: Scan sessions + chatlogs
**Opgave:** Find alle TI-sessioner kronologisk
**Input:** TI_KOMPLET_KILDEINDEX.md (sektion 10: chatlogs, sektion 11: episoder, sektion 2-4: chat-eksporter)
**Metode:** Kildeindexet har allerede identificeret 32 chatlog-filer og 23 episoder med TI. Scanneren VERIFICERER og UDDYBER — læser de top-8 chatlogs (efter hits) og udtrækker: dato, hvad der blev gjort, beslutninger
**Output:** `projects/transportintra/_scan/sessions.md` — kronologisk, med datoer
**Done:** Fil har >20 daterede entries

## Iteration 4 — TI: Scan teknisk inventar
**Opgave:** Kortlæg alt teknisk: app-kode, scripts, data, API
**Input:** TI_KOMPLET_KILDEINDEX.md (sektion 1, 5, 8, 12) + direkte filsystem
**Metode:** 2 subagents:
- Subagent 1: App-kodebasen — `wc -l` per JS-fil, features per fil, sub-apps inventar
- Subagent 2: Scripts + data + n8n workflows — hvad eksisterer, hvad er aktivt vs. arkiveret
**Output:** `projects/transportintra/_scan/technical.md`
**Done:** Fil dækker app/, scripts/, data/, n8n. Hver entry har [fil, linjer, formål, status]

## Iteration 5 — TI: PROGRESS.md
**Opgave:** Byg kronologisk narrativ fra dag ét
**Input:** _scan/sessions.md + TI_KOMPLET_KILDEINDEX.md tidslinje (sektion "Tidslinje") + chatlogs for detaljer
**Metode:** Kildeindexets tidslinje er skelettet (dec 2025 → mar 2026). Sessions-scan er kødet. Læs de 3-4 vigtigste chatlogs for narrativ dybde. Prioritér substans over aktualitet
**Output:** `projects/transportintra/PROGRESS.md`
**Done:** Dækker dec 2025 til marts 2026, >4 faser, beslutninger dateret

## Iteration 6 — TI: INDEX.md
**Opgave:** Det vigtigste deliverable. Komplet guide til alt TI
**Input:** _scan/sessions.md + _scan/technical.md + TI_KOMPLET_KILDEINDEX.md + PROGRESS.md
**Format:** Som projects/ydrasil/INDEX.md men dybere:
- Crown jewels (top 5-8 filer med abstracts)
- Kategorier med tabeller: [fil, størrelse, hvad, hvornår du bruger den]
- Abstract per sektion (ikke bare en linje — 2-3 sætninger)
- Hurtigreference i bunden
**Output:** `projects/transportintra/INDEX.md`
**Done:** >100 linjer, >5 kategorier, crown jewels sektion, hurtigreference

## Iteration 7 — TI: Subprojects + CONTEXT.md
**Opgave:** Én CONTEXT.md per underprojekt + overordnet CONTEXT.md
**Input:** PROGRESS.md + INDEX.md + TI_KOMPLET_KILDEINDEX.md + projects/transport/CONTEXT.md (eksisterende)
**Underprojekter (minimum):** navigation, sorting, redesign, voice, chat, tidsregistrering, diesel, command-center
**Hvert subproject CONTEXT.md:** Hvad er det, hvad er done, hvad mangler, key files, beslutninger. MAX 40 linjer
**Output:** `projects/transportintra/subprojects/*/CONTEXT.md` + `projects/transportintra/CONTEXT.md`
**Done:** >6 subproject-mapper med CONTEXT.md, overordnet CONTEXT.md eksisterer

## Iteration 8 — TI: Archive + links
**Opgave:** Populér archive/, research/, design/, data/, kompendier/
**Metode:** Kopier IKKE store filer. Brug pointer-filer (`DATA_POINTER.md`: "Denne data ligger i /root/Yggdra/data/routes/..."). Flyt/kopier kun små filer (<50KB) der hører til arkivet
**Output:** Mapper med indhold eller pointer-filer
**Done:** Alle mapper i strukturen har mindst én fil

## Iteration 9 — Prompt-skabeloner
**Opgave:** Kør prompt-skabeloner/prompt.md iteration 1-4 komprimeret
**Metode:** Læs prompt-skabeloner/prompt.md og udfør: mine chatlog → kategorisér → byg 2-3 skills
**Input:** ./chatlog.md (21K linjer) + prompt-skabeloner/reference-skill/SKILL.md
**Output:** prompt-skabeloner/skills/ + prompt-skabeloner/MINING_RESULTS.md
**Done:** >1 skill med SKILL.md, MINING_RESULTS.md eksisterer

## Iteration 10 — Review + slutevaluering
**Opgave:** 3 Reviewer-subagents tester alt output parallelt
**Metode:**
- Reviewer A: Research arch (INDEX.md komplet? CONTEXT.md har kill condition?)
- Reviewer B: TI (INDEX.md >100 linjer? PROGRESS.md dækker dec-mar? >6 subprojects?)
- Reviewer C: Prompt-skabeloner (skills invokérbare? MINING_RESULTS har <10 kandidater?)
**Output:** `V1/EVALUATION.md` — ærlig vurdering per projekt, hvad der virker, hvad der mangler
**Done:** EVALUATION.md eksisterer, alle 3 projekter vurderet
```

---

## LOOP_STATE.md (initial)

```markdown
# Loop State v2

Iteration: 0
Status: Ikke startet
Næste: Iteration 1 (Research Arch audit)
```

---

## Start-kommando (Ralph loop)

```bash
cd /root/Yggdra/yggdra-pc

# Kør én iteration ad gangen:
claude --dangerously-skip-permissions --print "Læs CLAUDE.md. Læs V1/LOOP_STATE.md for dit iterationsnummer. Læs V1/LOOP_PLAN.md for opgaven. Udfør den. Opdatér LOOP_STATE.md. Stop."

# Gentag til iteration 10 eller til LOOP_STATE.md siger "Done"
```

Kan køres som:
```bash
for i in $(seq 1 10); do
  echo "=== Iteration $i ==="
  claude --dangerously-skip-permissions --print "Læs CLAUDE.md. Læs V1/LOOP_STATE.md for dit iterationsnummer. Læs V1/LOOP_PLAN.md for opgaven. Udfør den. Opdatér LOOP_STATE.md. Stop."
  echo "=== Done ==="
  sleep 5
done
```
