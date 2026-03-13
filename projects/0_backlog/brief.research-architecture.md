# Research Architecture

**Dato:** 2026-03-12
**Klar til:** Backlog — høj prioritet post-reformation
**Prioritet:** Høj — fundamentalt for alt andet

## Opsummering
- Etablér formidabel research-praksis: struktur, kvalitetssikring, multi-LLM strategi
- Al eksisterende research er pre-reformation og ligger i research/_ARC/ — kræver revision
- research/ mappen ER dette projekts hjem. research/_ARC/ er input til den nye praksis

## Origin Story
Opstod fra idé-parkering: "Research/vidensbank som separat projekt ('personligt forskningsinstitut')." Voksede i session 12 til en erkendelse af at research-arkitektur er lige så fundamental som Yggdras kernearchitektur. Praksisser, infrastruktur, planlægningsstrategier bygger alle på forskning — men hvor velkonstrureret er fundamentet? Kilder: Anthropic, OpenAI, Perplexity, forskningsinstitutter, eksperter, communities. VPS har 60+ research-filer der skal auditeres efter reformation.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-07-vidensbank-scope.md (253 linjer, dato 2026-03-10). Indeholder: problem-analyse, eksisterende assets (VPS research/, DAGBOG.md, Qdrant, lokale references/), genbrug-mønstre, arkitektur-forslag (minimum viable = distributed reference system), scope-grænse (IN/OUT), anbefaling.

**Session 12 beslutninger:**
- Research er en *praksis*, ikke bare en mappe
- Al eksisterende research er "pre-reformation" — intet har gennemgået kvalitetssikret process
- VPS research lægges i arkiv/vps efter reformation, gennemgås med ny praksis
- Multi-LLM strategi: "de rigtige LLM'er til de rigtige ting"

**Fra PLAN.md idé-parkering:**
> Research/vidensbank som separat projekt ("personligt forskningsinstitut")

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
- **Fase 1 (denne uge):** Opret ~/reference/ med INDEX.md, symlinks, VPS rsync-job
- **Fase 2 (denne måned):** Seed ~10 prioriterede reference-filer fra VPS research/ + DAGBOG.md mønstre
- **Fase 3 (efter 3 mnd):** Evaluer baseret på faktisk brug. Qdrant/Wiki/Obsidian KUN hvis behov viser sig

### Action items
- [ ] Opret ~/reference/ med INDEX.md template
- [ ] Symlink fra Basic Setup/references/
- [ ] Setup VPS rsync-job (ugentligt)
- [ ] Definér naming-convention baseret på VPS research/ eksempler
- [ ] Dokumentér procedure for tilføjelse af nye filer
