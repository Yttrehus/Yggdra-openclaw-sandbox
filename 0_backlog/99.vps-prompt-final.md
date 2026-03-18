# VPS Sandbox v2 — Final

Tre filer deployes: CLAUDE.md, V1/LOOP_PLAN.md, V1/LOOP_STATE.md.
Ralph loop: hver iteration er ét `claude --print` kald med timeout.

---

## CLAUDE.md

```markdown
# Yggdra Sandbox v2

Du kører autonomt i en Ralph loop. Yttre er ikke tilgængelig.
Hver iteration er ét `claude --print` kald. Du får dit iterationsnummer som input.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten. Brug det — stol ikke på LOOP_STATE alene
2. Læs V1/LOOP_STATE.md — check ## Blokkere. Hvis noget er blokeret: skriv BLOCKED i state og stop
3. Læs den relevante iteration i V1/LOOP_PLAN.md (grep dit nummer)
4. VALIDÉR INPUT: Check at filer fra forrige iteration eksisterer og er >10 linjer. Hvis ikke: skriv BLOCKED i state og stop
5. Udfør opgaven. Skriv alt output til disk
6. Verificér dit eget output med kommandoer (ls, wc -l, head)
7. Opdatér V1/LOOP_STATE.md (se format nedenfor)
8. Stop

## LOOP_STATE format

Hold LOOP_STATE.md kompakt. Max-struktur:
```
# Loop State v2
## Blokkere
(ingen / liste af uløste problemer)

## Filregister
(kumulativ liste af alle producerede filer med fulde stier)

## Iteration [N-1] (seneste)
Opgave: ...
Output-filer: ...
Done-kriterie: ... → PASS/FAIL
Fejl: ...

## Iteration [N-2] (forrige)
(samme format — slet alt ældre end N-2)

## Næste: Iteration N
(fra LOOP_PLAN)
```
SLET iterationer ældre end de seneste 2. Filregisteret er kumulativt.

## Tre projekter

**A: Research Architecture** — Minimal research-praksis. Input: /root/Yggdra/research/ (81 filer).
**B: TransportIntra Arkiv** — Komplet projektmappe. Kildeindex: /root/Yggdra/projects/transport/TI_KOMPLET_KILDEINDEX.md (519 linjer, dækker ALLE kilder). Alt TI-output i `projects/transportintra/`. Rør IKKE `projects/transport/`.
**C: Prompt-skabeloner** — Mine chatlog for instruksmønstre. Detaljer i prompt-skabeloner/prompt.md.

## Regler

### Token-bevidsthed
- Læs ALDRIG filer >500 linjer i helhed. Brug head, tail, grep, sed -n 'X,Yp'
- Max 3 parallelle subagents. Hver subagent skriver til sin EGEN fil (aldrig samme)
- Skriv kompakt. Ingen gentagelser, ingen opsummeringer af hvad du lige har gjort

### Kronologisk sammenhæng
- Vigtigere end kategorisering. Alle deliverables skal vise hvordan ting udviklede sig over tid
- Gammel viden (dec 2025) kan være mere værdifuld end nyere. Substans > aktualitet
- Spor kausale kæder: beslutning A → konsekvens B → ny tilgang C
- TI_KOMPLET_KILDEINDEX.md har en tidslinje (sektion "Tidslinje") — brug den som skelet, uddyb med kilder

### Build > Research
- Hver iteration SKAL producere filer på disk
- Ingen rapporter der ikke direkte informerer en deliverable

### Done = Verified
- Test med kommandoer: ls, cat | head, wc -l, grep -c
- Spot-check 2 tilfældige entries ved at trace dem til kilden
- Fejl fixes i DENNE iteration

### Scope
- Maks 1 hovedopgave per iteration
- Ingen dokumenter der opsummerer andre dokumenter
- >2 iterationer på én opgave: simplificér eller kill

### Kvalitet
- Citer ikke kilder du ikke kan verificere
- Det simpleste der virker
- Kill condition på alt

### Miljø
- Du er PÅ VPS'en. ALDRIG `ssh root@72.62.61.51`
- Qdrant: `curl localhost:6333/...`
- GDrive-data: `/root/Yggdra/data/gdrive_import/` (lokalt, INGEN GDrive API)
- Session JSONLs: `/root/.claude/` (parse med python3/jq)
- PDFs: pdftotext eller HTML-versioner
- SØG IKKE på nettet

### Anti-patterns
- ❌ ssh til dig selv
- ❌ cat filer >500 linjer uden head/tail/grep
- ❌ Tomme skelet-mapper uden indhold
- ❌ Kopier store datamapper — brug pointer-filer
- ❌ Markér done uden at verificere
- ❌ >10 kandidater til noget (collector's trap)
- ❌ Opsummeringsdokumenter om dit eget arbejde
- ❌ Re-scan hvad TI_KOMPLET_KILDEINDEX.md allerede dækker
- ❌ Subagents der skriver til samme fil
- ❌ Læs chatlog.md (21K linjer) i sin helhed — brug grep til at finde sektioner
```

---

## V1/LOOP_PLAN.md

```markdown
# Loop Plan — 10 iterationer

## Roller (til subagents)
- **Builder:** Skriver filer. Output på disk. Kort summary retur
- **Reviewer:** Tester med kommandoer. Binært: virker/virker ikke + fejl
- **Scanner:** Gennemsøger én kilde. Output: fundliste på EGEN fil (aldrig delt med anden subagent)

---

## Iteration 1 — Research Arch: Audit
**Opgave:** Kategorisér /root/Yggdra/research/ (81 filer)
**Metode:** 2 subagents:
- Sub A → `projects/research-architecture/_audit_index.md`: Læs RESEARCH_INDEX.md (allerede kategoriseret), brug som baseline
- Sub B → `projects/research-architecture/_audit_sizes.md`: `find /root/Yggdra/research/ -name '*.md' -exec wc -l {} + | sort -rn | head -40` + `head -3` af de 20 største
- Orchestrator merger til `projects/research-architecture/_audit.md`
**Output:** `projects/research-architecture/_audit.md` — tabel [fil, kategori, one-line, linjer]
**Done:** Filen eksisterer, >60 filer kategoriseret, `wc -l _audit.md` > 80

## Iteration 2 — Research Arch: INDEX + CONTEXT
**Opgave:** Byg INDEX.md + CONTEXT.md fra audit
**Input:** `projects/research-architecture/_audit.md`
**Output:**
- `projects/research-architecture/INDEX.md` — crown jewels, kategorier, "hvornår du bruger den"
- `projects/research-architecture/CONTEXT.md` — med kill condition ("hvis INDEX.md ikke bruges i 20 sessioner, slet projektet")
**Done:** INDEX.md >80 linjer, >5 kategorier. CONTEXT.md har kill condition

## Iteration 3 — TI: Scan sessions
**Opgave:** Find alle TI-sessioner kronologisk
**Input:** TI_KOMPLET_KILDEINDEX.md (sektion 2-4: chat-eksporter, sektion 10: chatlogs, sektion 11: episoder)
**Metode:** Kildeindexet har ALLEREDE identificeret alt. Scan VERIFICERER og UDDYBER:
- Sub A → `projects/transportintra/_scan/sessions_chatlogs.md`: De 5 chatlogs med flest hits (2026-02-08: 168, 2026-02-15: 55, 2026-02-19: 24, 2026-02-18: 21, 2026-02-21: 17). Brug `grep -n 'transportintra\|TI\|rute 256\|sortering' /root/Yggdra/data/chatlogs/YYYY-MM-DD.md | head -30` per fil, derefter `sed -n 'X,+30p'` for kontekst. Udtyæk: dato, hvad der blev gjort, beslutninger
- Sub B → `projects/transportintra/_scan/sessions_exports.md`: ChatGPT, Claude App, Grok samtalerne fra kildeindexet sektion 2-4. Læs de 3 vigtigste (Copy and paste info, Gjentatte problemer, Google sheets workflow) med `head -200` + `grep`
- Orchestrator merger kronologisk til `projects/transportintra/_scan/sessions.md`
**Output:** `projects/transportintra/_scan/sessions.md` — kronologisk, med datoer, beslutninger
**Done:** >20 daterede entries, dækker dec 2025 til mar 2026

## Iteration 4 — TI: Scan teknisk
**Opgave:** Kortlæg teknisk inventar
**Input:** TI_KOMPLET_KILDEINDEX.md (sektion 1, 5, 8, 12) + filsystemet
**Metode:** 2 subagents:
- Sub A → `projects/transportintra/_scan/technical_app.md`: `find /root/Yggdra/app/ -name '*.js' -exec wc -l {} + | sort -rn | head -30` (KUN top 30, IKKE alle). Sub-apps: `ls -la app/classic/ app/v2/ app/redesign/ app/command-center/ app/mindmap/`. Features fra featurePanel.js (head -50)
- Sub B → `projects/transportintra/_scan/technical_infra.md`: Scripts (7 TI-scripts fra kildeindex), n8n workflows (sektion 12), data/ (routes stats: `ls data/routes/ | wc -l`, `ls data/routes/ | head -5 && ls data/routes/ | tail -5`), API reference (head -30), Docker (fra kildeindexet sektion "Docker/Infrastructure")
- Orchestrator merger til `projects/transportintra/_scan/technical.md`
**Output:** `projects/transportintra/_scan/technical.md`
**Done:** Dækker app/, scripts/, data/, n8n, Docker. Hver entry har [fil, linjer, formål, status]

## Iteration 5 — TI: PROGRESS.md
**Opgave:** Kronologisk narrativ fra dag ét. IKKE en event-liste — en historie
**Input:** _scan/sessions.md + TI_KOMPLET_KILDEINDEX.md tidslinje + _scan/sessions_chatlogs.md for detaljer
**Instruks:** Kildeindexets tidslinje (4 linjer) er skelettet. sessions.md er kødet. Byg en narrativ der fortæller:
- Dec 2025: Hvad var visionen? Hvad var frustrationen? Hvordan startede det?
- Jan 2026: Hvad gik galt med n8n? Hvad førte til skiftet?
- Feb 2026: Hvordan blev webapp-klonen til? Hvad var gennembruddet?
- Mar 2026: Hvorfor stoppede arbejdet? Hvad venter?
Spor 3-4 kausale kæder end-to-end (f.eks.: n8n-frustration → API reverse-engineering → lokal webapp → sortering → profiles)
**Output:** `projects/transportintra/PROGRESS.md`
**Done:** >100 linjer, 4 faser, beslutninger dateret, mindst 2 kausale kæder tydeligt sporet

## Iteration 6 — TI: INDEX.md
**Opgave:** Komplet guide til alt TI. Det vigtigste deliverable
**Input:** _scan/sessions.md + _scan/technical.md + TI_KOMPLET_KILDEINDEX.md + PROGRESS.md
**Format — som projects/ydrasil/INDEX.md:**
- Crown jewels (top 5-8 filer): tabel med [fil, størrelse, hvad, hvornår du bruger den]. Abstract: 2-3 sætninger, ikke bare filbeskrivelse — hvad er KEY INSIGHT
- Kategorier (app-kode, data, research, design, scripts, kompendier, eksporter, arkiv): tabeller med entries
- Abstracts per sektion: 2-3 sætninger der forklarer sektionens værdi, ikke bare indhold
- Hurtigreference i bunden: "Jeg vil..." → "Gå til..."
- Kronologisk dimension: nævn i abstracts HVORNÅR ting blev lavet og HVORFOR
**Output:** `projects/transportintra/INDEX.md`
**Done:** >150 linjer, >6 kategorier, crown jewels med abstracts, hurtigreference

## Iteration 7 — TI: Top 4 subprojects + CONTEXT.md
**Opgave:** CONTEXT.md for de 4 vigtigste underprojekter + overordnet CONTEXT.md
**Input:** PROGRESS.md + INDEX.md + TI_KOMPLET_KILDEINDEX.md + /root/Yggdra/projects/transport/CONTEXT.md
**De 4 vigtigste (baseret på aktivitet i kildeindex):**
1. `subprojects/sorting/` — drag+drop, profiles, prioritering (DONE: Feb 2026)
2. `subprojects/navigation/` — GPS tracker, waypoints, lastbil-nav (PLANLAGT)
3. `subprojects/redesign/` — v2 app, UI overhaul, mockups (PARTIAL: redesign/ + v2/ eksisterer)
4. `subprojects/chat/` — TiChat, ydrasilChat (PARTIAL: kode eksisterer)
Yderligere subprojects kan tilføjes i senere iterationer
**Hvert CONTEXT.md:** Max 40 linjer. Hvad er det, hvad er done, hvad mangler, key files (med stier), beslutninger
**Overordnet:** `projects/transportintra/CONTEXT.md` — samlet state, hvad er TI, hvad er done, hvad mangler, link til subprojects
**Output:** 5 CONTEXT.md filer (4 subprojects + 1 overordnet)
**Done:** Alle 5 filer eksisterer og er >15 linjer. Overordnet CONTEXT.md linker til subprojects

## Iteration 8 — TI: Archive + links + resterende subprojects
**Opgave:** Populér archive/, research/, design/, data/, kompendier/, scripts/. Opret stubs for resterende subprojects
**Metode:** Kopier ALDRIG store filer. Brug pointer-filer (DATA_POINTER.md: "Denne data ligger i /root/Yggdra/data/routes/...")
- `archive/pre-reformation/`: Kopier brain/TELOS.md, PLAYBOOK.md, DECISIONS.md fra /root/transportintra-universe/brain/ (små filer)
- `archive/n8n-flows/`: Pointer til sektion 12 i kildeindexet + noter om hvilke workflows der eksisterede
- `research/api-reference.md`: Kopier /root/Yggdra/data/TRANSPORTINTRA_API_REFERENCE.md (13.5K)
- `research/getrute-schema.md`: Kopier /root/Yggdra/data/GETRUTE_SCHEMA.md (8.5K)
- `design/`: Pointer til app/redesign/, mockups, UI_ELEMENTS.md
- `data/DATA_POINTER.md`: Stier til routes/, api_logs/, episodes.jsonl
- `kompendier/`: Pointer til PDFs i data/inbox/ og app/*.pdf
- `scripts/SCRIPTS_POINTER.md`: Stier til de 7 TI-scripts
- Resterende subprojects (voice, tidsreg, diesel, command-center): CONTEXT.md stubs, max 15 linjer, marker som "Stub — uddybes ved aktivering"
**Output:** Mapper med filer eller pointer-filer
**Done:** `find projects/transportintra/ -type f | wc -l` > 20

## Iteration 9 — Prompt-skabeloner
**Opgave:** Mine chatlog + byg 1-2 skills
**Input:** ./chatlog.md (21K linjer). Reference: prompt-skabeloner/reference-skill/SKILL.md
**Metode — ALDRIG læs chatlog.md i helhed:**
- `grep -n 'hvad tænker du\|gør.*skarpere\|kør.*fool\|red team\|adversarial\|brief.*projekt\|session.*koordin\|checkpoint' chatlog.md | wc -l` for frekvens
- `grep -n -B2 -A10 'MØNSTER' chatlog.md | head -60` for kontekst per mønster
- Vælg de 2 mest frekvente/komplekse. Byg 1-2 skills i prompt-skabeloner/skills/
- Skriv MINING_RESULTS.md med max 8 kandidater + frekvens + "skill vs. one-liner" vurdering
**Output:** prompt-skabeloner/MINING_RESULTS.md + prompt-skabeloner/skills/ (1-2 skills med SKILL.md)
**Done:** MINING_RESULTS.md eksisterer med <10 kandidater. Mindst 1 skill med SKILL.md

## Iteration 10 — Review + slutevaluering
**Opgave:** 3 Reviewer-subagents tester alt output
**Metode:**
- Reviewer A → V1/review_research.md: Research arch INDEX.md >80 linjer? >5 kategorier? CONTEXT.md har kill condition? Spot-check 2 entries
- Reviewer B → V1/review_ti.md: TI INDEX.md >150 linjer? PROGRESS.md dækker dec-mar med kausale kæder? >4 subprojects med >15 linjer? Spot-check 3 entries i INDEX.md mod kildeindex
- Reviewer C → V1/review_skills.md: Skills invokérbare? MINING_RESULTS <10 kandidater? Collector's trap check
- Orchestrator samler til V1/EVALUATION.md — ærlig vurdering, hvad virker, hvad mangler, hvad er næste iteration (til Yttre)
**Output:** V1/EVALUATION.md
**Done:** EVALUATION.md eksisterer, alle 3 projekter vurderet
```

---

## V1/LOOP_STATE.md (initial)

```markdown
# Loop State v2

## Blokkere
(ingen)

## Filregister
(tomt — fyldes efterhånden)

## Næste: Iteration 1
Research Arch audit af 81 filer
```

---

## Start-kommando

```bash
cd /root/Yggdra/yggdra-pc

for i in $(seq 1 10); do
  echo "=== Iteration $i === $(date)"

  # Check for blokkere
  if grep -q "BLOCKED\|FAILED" V1/LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED: blocker fundet ==="
    cat V1/LOOP_STATE.md | head -10
    break
  fi

  # Kør med 10 min timeout
  timeout 600 claude --dangerously-skip-permissions --print \
    "Du er iteration $i af 10. Følg CLAUDE.md boot-sekvens. Udfør din opgave fra V1/LOOP_PLAN.md iteration $i. Opdatér V1/LOOP_STATE.md. Stop når du er færdig."

  # Check at state blev opdateret
  if ! grep -q "Iteration $i" V1/LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi

  echo "=== Iteration $i done === $(date)"
  sleep 10
done

echo "=== Loop færdig ==="
cat V1/LOOP_STATE.md
```

---

## Review fra telefon

```bash
# Quick status
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/V1/LOOP_STATE.md"

# Evaluering (efter iteration 10)
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/V1/EVALUATION.md"

# TI INDEX (det vigtigste)
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/projects/transportintra/INDEX.md"

# Filtal
ssh root@72.62.61.51 "find /root/Yggdra/yggdra-pc/projects/transportintra/ -type f | wc -l"
ssh root@72.62.61.51 "find /root/Yggdra/yggdra-pc/projects/research-architecture/ -type f | wc -l"
ssh root@72.62.61.51 "ls /root/Yggdra/yggdra-pc/prompt-skabeloner/skills/ 2>/dev/null"
```
