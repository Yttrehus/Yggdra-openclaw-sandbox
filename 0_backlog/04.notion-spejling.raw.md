# Notion-spejling af VS Code-struktur

**Dato:** 2026-03-10 (opdateret 2026-03-15)
**Klar til:** Backlog (mangler: oprettelse af Notion-database, test af mobiltilgang)

## Opsummering
- Notion som "andet vindue" ind i projekter: mobiltilgang, Kanban, hurtige noter
- Disk forbliver master for kode-kontekst, Notion ejer overblik og mobil-noter
- Synk-script skeleton klar (Python), starter manuelt, automatiseres senere

## Origin Story
Opstod fra idé-parkering: "Notion-spejling af VS Code-struktur." Problemet: markdown-filer er kun tilgængelige i VS Code. Yttre vil se projektstatus fra telefon (på vej til arbejde, i pauser). Notion MCP allerede installeret — Claude kan læse/skrive direkte.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-05-notion-spejling.md (334 linjer, dato 2026-03-10). Indeholder: designprincipper, database-design ("Projekter" med 8 properties), views (Fokus, Alt, Arkiv), synkroniseringsmodel (disk→Notion + Notion-only noter), implementeringsplan (dag 1-4+), sync-to-notion.py skeleton, risici.

**Fra PLAN.md idé-parkering:**
> Notion-spejling af VS Code-struktur

## Cowork Output (2026-03-10)

### Designprincipper
1. Disk forbliver master for kode-kontekst (CLAUDE.md, PLAN.md, NOW.md)
2. Notion er ligeværdigt for overblik og planlægning — du *må* skrive direkte
3. Synk er en-vejs per felt (disk→Notion for status, Notion-only for mobil-noter)
4. Start simpelt, iterer baseret på brug

### Database: "Projekter" (8 properties)
Projektnavn (title), Status (select: Aktiv/Pauset/Venter/Arkiveret), Milepæl (text, fra PLAN.md), Næste step (text, fra NOW.md), Type (select: Dev/Research/Setup/Rejseselskab/Personlig), Prioritet (select: Fokus/Normal/Baggrund), Sidst opdateret (date), Noter (text, Notion-only).

### Views
- **Fokus:** Kanban grupperet på Status (dagligt overblik)
- **Alt:** Tabel med alle properties
- **Arkiv:** Filtreret Status=Arkiveret
- **Rejseselskab:** Filtreret Type=Rejseselskab

### Synkronisering
- **Disk → Notion:** Projektnavn, milepæl, status, næste step, session-noter
- **Kun Notion:** Hurtige noter fra mobil, idéer, links
- **Kun disk:** CLAUDE.md, kode, chatlogger, git-historik
- **Trigger:** Manuelt først, post-commit hook senere, evt. session-slut hook

### Implementeringsplan
- Dag 1: Opret database, ét projekt manuelt, 2-3 views, test på mobil
- Dag 2-3: Juster properties, tilføj projekter, test mobil-noter
- Dag 4+: sync-to-notion.py script (skeleton klar med parsere for PLAN.md/NOW.md/PROGRESS.md)

### Mulige udvidelser (ikke nu)
Inbox-side, Rejseselskab-database, Ugeplan/Sprint-view, Reference-side, Lærte-ting-database.

### Risici
Største risiko: properties passer ikke til virkeligheden (sandsynlighed: høj, konsekvens: lav — juster løbende). Notion-føles-ikke-nyttigt er lav risiko og koster intet at droppe.

### Notion MCP (tilføjet 2026-03-15)
Notion MCP er nu tilsluttet i Claude Code. Det ændrer implementeringsplanen:
- Database-oprettelse kan ske direkte fra Claude Code via MCP (notion-create-database)
- Sider kan oprettes/opdateres via MCP (notion-create-pages, notion-update-page)
- Synk behøver muligvis ikke et separat Python-script — Claude Code kan potentielt synke direkte via MCP-kald
- Overvej: er sync-to-notion.py stadig nødvendig, eller kan det hele køres via Claude Code + hooks?

### Action items
- [ ] Opret "Projekter" database i Notion via MCP (notion-create-database)
- [ ] Opret "Yggdra" som første projekt med ægte data
- [ ] Test mobiloplevelsen
- [ ] Evaluér: sync via MCP-kald eller separat Python-script?
