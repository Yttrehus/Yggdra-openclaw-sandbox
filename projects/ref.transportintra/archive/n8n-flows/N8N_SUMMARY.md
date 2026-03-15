# N8N Workflows — Summary
**Status: ARKIVERET** (slettet fra repo, mar 2026)

---

## Tidsperiode
- **Oprettet:** december 2025 (første pipeline 11/12-2025)
- **Droppet:** januar–februar 2026 (overgang til direkte API-kald)
- **Slettet fra repo:** marts 2026

---

## Workflows (komplet liste fra TI_KOMPLET_KILDEINDEX.md §12)

| Workflow | Formål |
|----------|--------|
| `TransportIntra_-_Master_Scan.json` | Scanner TI for nye ruter |
| `TransportIntra_-_HTTP_Direct.json` | Direkte HTTP til TI API |
| `TransportIntra_-_Sorter_rute_efter_tid.json` | Sorterer stops efter tid |
| `TransportIntra_-_Sorter_efter_ønske.json` | Sorterer efter brugerpræference |
| `TransportIntra_-_Scan_og_tilføj_til_sheets.json` | TI → Google Sheets |
| `TransportIntra_-_Sync_Sorting_to_API.json` | Sheets → TI (skriver tilbage) |
| `TransportIntra_-_Sync_by_Customer_Name.json` | Match på kundenavn |
| `TransportIntra_-_Tildel_match_key.json` | Match-key tildeling |
| `TransportIntra_-_Flexible_Processor.json` | Generisk processor |
| `Tool__UpdateRDisp.json` | Opdater RDisp i TI |
| `AI-TI_Tools.json` | AI-værktøjer til TI |
| `AI_Agent_-_TransportIntra.json` | AI agent for TI (inkl. "Trashy") |

---

## Kausal kæde: Hvorfor droppet

1. **6/12-2025:** MCP/Puppeteer fejler totalt → n8n opdaget som alternativ. Vendepunkt.
2. **11/12-2025:** Første pipeline virker: n8n + Airtop + Google Sheets (TI → Sheets sync).
3. **13/12-2025:** Debugging-marathon. n8n workflows til scanning, sortering, Sheets↔TI API synk. Fejlmønstre begynder at akkumulere.
4. **21/12-2025:** SQL fravalgt. n8n's begrænsninger frustrerer. Kristoffer opdager Claude Code og formulerer "rigtige apps" — ikke workflows, men kode. Frøet til webapp-klonen plantet.
5. **3/1-2026:** Sorteringslogik raffineret (nr 0 = ny kunde). Nested AI-agent "Trashy" bygget i n8n. Signal: n8n's visuelt-først-paradigme passer ikke arbejdsformen.
6. **18/1-2026:** Claude Code + n8n går i stykker samtidig (API keys, netværk, Sheets). Markerer overgangen: n8n som primært værktøj er slut. Claude Code overtager.

**Kerneproblem:** n8n krævede konstant vedligeholdelse og visuelt-først-debugging. Versionskontrol og kodegennemgang var besværligt. Direkte Python/JS API-kald var mere composable og verificerbare.

---

## Hvad erstattede dem

- **Direkte Python API-kald** til `webapp.transportintra.dk/srvr/index4.0.php`
- **webapp-klon** (feb 2026) — React/JS app med drag+drop sortering
- **scripts/** på VPS — automation via Python + cron
- Sortering: n8n-workflow → drag+drop i webapp

Evolutionen: `Axiom/Zapier → n8n → webapp-klon`

---

## Pointer Verification

Scannede filer: alle `.md` i `archive/` og `research/` under dette projekt.

### archive/n8n-flows/N8N_POINTER.md
- Ref: `TI_KOMPLET_KILDEINDEX.md sektion 12` (ingen absolut sti angivet)
- Faktisk placering: `/root/Yggdra/projects/transport/TI_KOMPLET_KILDEINDEX.md`
- Status: **BROKEN** — ikke tilgængelig lokalt i yggdra-pc repo. Eksisterer kun på VPS.

### archive/pre-reformation/DECISIONS.md
- Ingen sti-referencer fundet. Indeholder kun skabelon-struktur (auto-genereret, ingen entries).
- Status: **OK** (ingen broken pointers)

### archive/pre-reformation/PLAYBOOK.md
- Ingen absolutte sti-referencer. Nævner scripts (`session_collector_v2.py`, `playbook_updater.py`) uden stier.
- Status: **OK** (ingen verificerbare pointers)

### archive/pre-reformation/TELOS.md
- Ingen sti-referencer. Personligt filosofidokument.
- Status: **OK** (ingen pointers)

### research/api-reference.md
- Kilde: HAR-captures fra Chrome DevTools. Ingen filsti-pointers.
- Status: **OK** (selvstændigt dokument)

### research/getrute-schema.md
- Ingen sti-referencer. Selvstændigt schema-dokument.
- Status: **OK** (ingen pointers)

### Opsummering
| Fil | Pointer | Status |
|-----|---------|--------|
| N8N_POINTER.md | TI_KOMPLET_KILDEINDEX.md | VPS: `/root/Yggdra/projects/transport/TI_KOMPLET_KILDEINDEX.md` |
| DECISIONS.md | — | OK |
| PLAYBOOK.md | — | OK |
| TELOS.md | — | OK |
| research/api-reference.md | — | OK |
| research/getrute-schema.md | — | OK |
