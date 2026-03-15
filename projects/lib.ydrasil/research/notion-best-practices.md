# Notion Best Practices for Solo Knowledge Workers

*Research rapport — 2026-03-08*

## 1. Workspace-arkitektur

**Databases er rygraden, pages er interfacet.**

- Brug **databases** til alt der skal filtreres, sorteres eller vises på flere måder. Hver vidensenhed (note, projekt, task) hører i en database.
- Brug **plain pages** til dashboards (hub-sider der embedder database-views), one-off dokumenter og uformelt indhold.
- **Relations** er power-featuren. Forbind tasks→projekter→areas→goals. Skaber en vidensgraf, ikke et arkivskab.
- **Linked Views** eliminerer duplikering. Én master-database, mange filtrerede views embedded i dashboards.
- **Dashboard-filosofi**: Ét dashboard per livsområde/projekt. Hvert dashboard trækker linked views fra relevante databases.
- **Start minimalt.** 3-5 kerne-databases (Projects, Tasks, Notes, Areas, Resources) med relations. Tilføj kompleksitet kun ved friktion.

**For Yggdra:** Projects-database (spejler 9 projekter), Tasks-database, Notes/Knowledge-database. Relations mellem alle tre. Ét dashboard per projekt + ét master "Command Center". Notion = visuelt query-lag; VPS = source of truth.

## 2. Notion Plans (2026)

| Feature | Free ($0) | Plus ($10/md) | Business ($20/md) |
|---|---|---|---|
| Pages & blocks | Unlimited | Unlimited | Unlimited |
| Fil-upload | 5 MB/fil | Unlimited | Unlimited |
| Version history | 7 dage | 30 dage | 90 dage |
| Gæster | 10 | 100 | 250 |
| Notion AI | 20 svar (trial) | 20 svar (trial) | Unlimited AI + Agents |

**Vigtigt (maj 2025-ændring):** Notion droppede $8/md AI add-on. Fuld AI er nu KUN i Business ($20/md). Free/Plus får 20 AI-svar totalt.

**Anbefaling:** Start på Free. Du har allerede Claude som AI-lag — Notion AI er redundant. Opgrader til Plus kun når 5 MB fil-grænsen generer. Overvej Business kun hvis Notion AI Agents viser unik værdi inde i workspace.

## 3. Undervurderede Features

**Formulas 2.0:**
- Kan traversere relations direkte uden rollups: `prop("Related Projects").map(p, p.prop("Status"))`
- Understøtter lokale variabler med `let`, multi-level relation traversal
- 20+ funktioner for conditional formatting, dato-matematik, tekst

**Relations + Rollups:**
- Kæd rollups på tværs: daglig tracking → ugentlig → månedlig
- Rollups: Sum, Average, Median, Min, Max, Range, Earliest/Latest, Count
- Tre vel-relaterede databases giver automatisk progress tracking

**Database Automations (native):**
- Trigger: property change eller tidsplan (daglig/ugentlig/månedlig)
- Actions: redigér properties, opret sider i andre databases, send notifikationer

**Synced Blocks:** Én blok der vises på flere sider, synkroniseret. Redigér ét sted, opdateres overalt.

**Buttons:** Custom action-knapper der opretter sider, redigerer properties, trigger automations.

## 4. Sync med VPS

**Path A: Python SDK (bedst fit)**
- `pip install notion-client` — officiel Python SDK
- Opret intern integration på notion.so/profile/integrations
- CRUD på databases og pages. Push projektstatus fra VPS til Notion
- Script i `/root/Yggdra/scripts/` triggered af hooks eller cron

**Path B: Notion MCP (til AI-agent workflows)**
- Allerede connected i Claude-setup
- Claude kan læse/skrive Notion workspace direkte i sessions

**Anbefaling:** Path A for automatisk VPS→Notion sync. Path B for interaktivt AI-arbejde.

## 5. Læringsressourcer

**YouTube (rangeret efter praktisk værdi):**
- **Thomas Frank Explains** — Største Notion-kanal (230K+). Formler, begynder→avanceret
- **August Bradley (PPV/Life OS)** — Mest systematisk tilgang. 50+ videoer
- **Red Gregory** — 200+ tutorials. Formler, dashboards, page design
- **Marie Poulin (Notion Mastery)** — Konsulent-dybde. Forstå HVORFOR
- **Notion VIP (William Nutt)** — Workspace-strategi, avanceret

**Communities:** r/Notion (Reddit), Notion Community Discord, Notion Club Discord

## 6. Anti-patterns

1. **Over-engineering dag ét.** Byg IKKE 15-database system før du har brugt Notion i en uge. Start med 2-3 databases, brug dem dagligt, tilføj ved friktion.
2. **Duplikering af eksisterende system.** Spejl IKKE alt fra VPS. Notion = view layer, ikke erstatning.
3. **Template-hamstring.** Vælg ÉN arkitektur, commit 30 dage.
4. **Prematur optimering.** Ikoner, covers, farver før systemet har indhold = prokrastination.
5. **Alt skal ind.** Notion erstatter IKKE kode, terminal eller VPS-scripts. Stærk til: dashboards, relational browsing, quick-capture. Svag til: version control, store datasets, offline.
6. **Løse sider i stedet for databases.** Alt med 5+ instanser = database fra start.
7. **Ignorer linked views.** Lav IKKE separate databases for "Active Tasks" og "Completed Tasks" — ét Tasks-database med filtrerede views.
8. **Ingen arkiv-strategi.** Brug status-property eller Archive-database til at skjule færdigt/irrelevant.
