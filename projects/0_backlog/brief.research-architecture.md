# Research Architecture

**Dato:** 2026-03-12 (opdateret 2026-03-14)
**Klar til:** Backlog — høj prioritet
**Prioritet:** Høj — fundamentalt for alt andet

## Opsummering
- Etablér formidabel research-praksis: struktur, kvalitetssikring, multi-LLM strategi
- Al eksisterende research er pre-reformation — kræver revision
- VPS sandbox-loop (6 iterationer, 2026-03-14) producerede 5 rapporter + projektdesign — kvalitetsaudit gennemført

## Origin Story
Opstod fra idé-parkering: "Research/vidensbank som separat projekt ('personligt forskningsinstitut')." Voksede i session 12 til en erkendelse af at research-arkitektur er lige så fundamental som Yggdras kernearchitektur. Praksisser, infrastruktur, planlægningsstrategier bygger alle på forskning — men hvor velkonstrureret er fundamentet? Kilder: Anthropic, OpenAI, Perplexity, forskningsinstitutter, eksperter, communities. VPS har 60+ research-filer der skal auditeres.

## VPS Sandbox Output (2026-03-14)

VPS'en kørte en semi-autonom Ralph-loop (6 iterationer) på en kopi af Yggdra-repoet. Delegation: orchestrator → researcher/architect/builder/reviewer subagents. Alt output i `/root/Yggdra/yggdra-pc/`.

### Rapporter produceret
| Rapport | Score | Brugbar til |
|---------|-------|-------------|
| yggdra-direction-analysis | 8/10 | Emergent 5-lags model, ærlig selvkritik, reelle gap-identificationer |
| context-engineering-2026 | 7.5/10 | State of the art reference. ~20% kilder kræver verifikation |
| vps-pc-convergence | 7/10 | Praktisk: separate domæner, SSH som bro, ingen sync |
| session-drift-poc | 6.5/10 | Korrekt scope, men SSH i SessionStart er anti-minimalt |
| automation-audit | 6/10 | 56 scripts inventoried, men agenten glemte `crontab -l` lokalt |
| research-architecture-report | 6/10 | Hybrid search (BM25+dense) er godt. Resten overdesignet |

### Indsigter der holder
- **Hybrid search:** BM25 + dense vectors i Qdrant løfter recall markant. Teknisk solid, men tallene (0.72→0.91) er fra uspecificerede benchmarks — tag som retningsgivende, ikke præcis
- **VPS-PC split:** VPS ejer drift/services, PC ejer development/research. SSH er broen. Ingen sync. Simpelt, matcher virkeligheden
- **5-lags model:** Epistemisk fundament → temporal kontinuitet → handlingsevne → tilgængelighed → situationsbevidsthed. Nyttig som linse, ikke som arkitektur at implementere
- **Trello-cruft:** 5+ cron jobs poller stadig Trello selvom det er droppet. Mest actionable single finding
- **Design-mønster observeret:** irritation → overdesign → konfrontation med virkelighed → radikal forenkling → working solution

### Indsigter der IKKE holder
- **"Stanford NLP 40% bedre retrieval"** — sandsynligvis halluceret kilde
- **Zettelkasten + PARA som "optimal kombination"** — én mulighed præsenteret som konklusion. Quality gates (4 stk) er overkill for solo brug
- **6-step research pipeline** — repackaged PKM-råd, mere friktion end værdi
- **BLUEPRINT.md** — en hel iteration brugt på at opsummere sit eget output
- **arXiv-papir-IDs** — plausible formater men uverificerede

### Procesproblemer
- 6 iterationer for at aktivere én JSON-fil (hooks). Revieweren fangede det, men loopet lukkede ikke
- Research spawner mere research i stedet for at bygge
- Agenten var bedre til at producere artefakter end working software
- Overconfidence i evalueringer — markerer ting som "Stærk" der er ufuldstændige

## Rå input (original brief)

**Parallel-tasks output:** ~/parallel-tasks/output-07-vidensbank-scope.md (253 linjer, dato 2026-03-10). Indeholder: problem-analyse, eksisterende assets (VPS research/, DAGBOG.md, Qdrant, lokale references/), genbrug-mønstre, arkitektur-forslag (minimum viable = distributed reference system), scope-grænse (IN/OUT), anbefaling.

**Session 12 beslutninger:**
- Research er en *praksis*, ikke bare en mappe
- Al eksisterende research er "pre-reformation" — intet har gennemgået kvalitetssikret process
- VPS research lægges i arkiv/vps efter reformation, gennemgås med ny praksis
- Multi-LLM strategi: "de rigtige LLM'er til de rigtige ting"

## Cowork Output (2026-03-10)

### Problem
~5-10 timer/mnd tabt på duplikeret research. Viden fragmenteret mellem VPS research/ (60+ filer), DAGBOG.md, lokale references/, Qdrant, og session-outputs. Søgning kræver manuelt trawl.

### Genbrug-mønstre (sorteret efter værdi)
1. **Arkitektur/workflow-beslutninger** — HØJT genbrug (mappestruktur, VPS-ops, navngivning)
2. **Tool-evalueringer** — HØJ-MEDIUM (Firecrawl vs puppeteer, Qdrant vs Postgres)
3. **Professionelle konventioner** — MEDIUM-HØJ (README-format, markdown-navngivning)
4. **AI-assistering mønstre** — MEDIUM (prompt-engineering, workflow-læring fra DAGBOG)
5. **Implementation-kode** — LAVT genbrug (bliver hurtigt stale)

### Anbefalet arkitektur: Distributed Reference System
Ingen centraliseret database — bare god organisering:
1. **Fælles reference-mappe** (`~/reference/`) symlinked fra alle projekter. Navngivning: `[domain]-[topic].md`
2. **Session-output arkiv** (`~/reference/sessions/`) med INDEX.md
3. **VPS-synk:** rsync/scp ugentligt → `~/reference/vps-research/`
4. **Søgning:** `grep -r "topic" ~/reference/` — god nok for denne volumen
5. **Index:** Hand-curated `~/reference/INDEX.md`

### Scope-grænse
**IN:** Arkitektur-beslutninger, tool-evalueringer, destillerede session-outputs, langtidslæring, VPS-knowledge.
**OUT:** Implementation-kode, rå session-noter, blog/artikler, personlige produktivitets-noter.

### Implementeringsplan
- **Fase 1:** Opret ~/reference/ med INDEX.md, symlinks, VPS rsync-job
- **Fase 2:** Seed ~10 prioriterede reference-filer fra VPS research/ + DAGBOG.md mønstre
- **Fase 3 (efter 3 mnd):** Evaluer baseret på faktisk brug. Qdrant/Wiki/Obsidian KUN hvis behov viser sig

### Action items
- [ ] Opret ~/reference/ med INDEX.md template
- [ ] Symlink fra Basic Setup/references/
- [ ] Setup VPS rsync-job (ugentligt)
- [ ] Definér naming-convention baseret på VPS research/ eksempler
- [ ] Dokumentér procedure for tilføjelse af nye filer
