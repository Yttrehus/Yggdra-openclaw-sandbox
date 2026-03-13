# MCP/Skills Kompendium

**Dato:** 2026-03-10
**Klar til:** Backlog (mangler: revision af output, installation af anbefalede MCPs)

## Opsummering
- Ranket oversigt over relevante MCP-servere og Claude Code skills for solo-udvikler
- Allerede installeret: Figma, Notion, Firecrawl. Anbefalet: Filesystem, Git, Postgres, Qdrant, GitHub
- Roadmap i 3 faser: fundament → data-intelligens → automatisering

## Origin Story
Opstod fra idé-parkering i PLAN.md: "MCP/Skills kompendium som separat projekt (scan mcpmarket.com top 100)." Yttre bruger Claude Code intensivt men har kun 3 MCPs installeret. En systematisk audit ville afdække hvad der findes og hvad der er relevant for en solo-udvikler med rejseselskab + VPS-infrastruktur.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-01-mcp-skills-kompendium.md (168 linjer, research-dato 2026-03-10). Indeholder: installeret/anbefalet/overvej/ikke-relevant tabeller, roadmap i 3 faser, 7 markerede antagelser, skills-råd, og kilder.

**Fra PLAN.md idé-parkering:**
> MCP/Skills kompendium som separat projekt (scan mcpmarket.com top 100)

## Cowork Output (2026-03-10)

### Allerede installeret
Figma (design-til-kode), Notion (database/dokumentadgang), Firecrawl (web scraping skill).

### Anbefalet (relevans 4-5)
- **Filesystem** (5) — grundlæggende filhåndtering
- **Git** (5) — repo-søgning, branch-management, commit-analyse
- **Postgres** (5) — direkte SQL-adgang til VPS-data (antagelse: Yggdra kører Postgres)
- **Firecrawl MCP Server** (4) — opgradér skill til server for bedre hook/cron-integration
- **GitHub** (4) — issue-triage, PR-review, kodeanalyse
- **Qdrant Vector Memory** (4) — semantisk søgning over eksisterende Qdrant-data
- **SQLite** (4) — lightweight lokale data-jobs
- **Time** (4) — timezone-konvertering for rejseselskab

### Overvej (relevans 3)
Sequential Thinking, Invoice MCP (fakturering), Odoo Accounting, Travel Planner, Fetch, Memory, Web-curl, dbhub.

### Ikke relevant
AWS Billing, QuickBooks/FreshBooks, Slack, Unity/Godot, Azure Travel Agents, CI/CD Skills, AWS Cron.

### Roadmap
1. **Fase 1 (uge 1):** Filesystem + Git + Postgres — kan arbejde med hele stacken
2. **Fase 2 (uge 2-3):** Qdrant + Firecrawl MCP — semantisk søgning + web-research
3. **Fase 3 (uge 4+):** Time + SQLite + evt. Invoice MCP — automatisering

### Antagelser at verificere
- [A1] Yggdra kører Postgres
- [A3] Ingen CI/CD setup
- [A4] TransportIntra bruger Qdrant
- [A6] Bias mod simplicity over enterprise

### Skills-råd
- Start med [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- Relevante kategorier: TDD/Debugging, Git Workflows, Database Engineering, API/REST, Markdown

### Action items
- [ ] Installér fase 1 (Filesystem, Git, Postgres) i Claude Code
- [ ] Test Notion + Postgres + Qdrant integration
- [ ] Byg hook-prototype: automatisér 1 bogholderi-task
- [ ] Verificér antagelser A1, A3, A4
