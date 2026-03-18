# TransportIntra — INDEX

Komplet guide til alt TI-materiale. Opdateret: 2026-03-14.

---

## Crown Jewels

De 5-8 vigtigste filer. Læs disse først.

| # | Fil | Linjer | Hvad | Hvornår |
|---|-----|--------|------|---------|
| 1 | `data/TRANSPORTINTRA_API_REFERENCE.md` | 519 | Komplet API-reference. Alle 8 endpoints, HAR-baseret. Dobbelt JSON-quoting dokumenteret | Når du kalder TI API, debugger responses, eller bygger ny funktionalitet |
| 2 | `data/GETRUTE_SCHEMA.md` | 316 | JSON-schema for getRute. 132 felter. rute_id -231 = rute 256 mandag | Når du parser getRute-data, bygger UI for stops, eller analyserer rutestruktur |
| 3 | `docs/TRANSPORTINTRA_PROFIL.md` | 321 | Dedikeret profil: webapp, rute 256, vision "1:1 kopi → forbedring". Dækker alle underprojekter | Når du har brug for overblik over hele TI-projektet og dets retning |
| 4 | `app/js/Ruter.js` | 1642 | Rute-visning, stop-håndtering, drag+drop sortering. Produktionskode | Når du ændrer stop-visning, sortering, eller rute-funktionalitet |
| 5 | `app/js/app.js` | 837 | App-core: boot, login, pagechange, state. jQuery Mobile SPA | Når du ændrer login-flow, navigation, eller app-initialisering |
| 6 | `projects/transport/CONTEXT.md` | — | Projekt-identitet og state. Næste: stop-beskrivelser, ikoner, GPS | Når du starter en TI-session — altid læs denne først |
| 7 | `app/js/sortProfiles.js` | 363 | Sorteringsprofiler for ruter. Kulminationen af dec→feb sorteringsrejsen | Når du ændrer sorteringslogik eller profiler |
| 8 | `data/JS_CHAUFFØRHAANDBOG.md` | — | Chaufførhåndbog fra live.transportintra.dk. Officiel dokumentation | Når du har brug for at forstå TI's tilsigtede brug |

**Abstract:** API-referencen og getRute-schemaet er fundamentet — uden dem er alt andet gætværk. Profilen giver den strategiske kontekst: hvorfor projektet eksisterer og hvor det skal hen. Ruter.js + sortProfiles.js er produktionskoden hvor sorteringsvisionen blev til virkelighed. Chaufførhåndbogen er den eneste officielle kilde til "hvordan TI er ment at virke."

---

## App-kode (app/js/ — 22 filer, 10.620 linjer)

Produktions-webapp: jQuery Mobile SPA. Boot: `db.initialise() → msgFeat.initialise() → applicationReady()`.

| Fil | Linjer | Formål |
|-----|--------|--------|
| Tidsreg.js | 1652 | Tidsregistrering — stempel ind/ud |
| Ruter.js | 1642 | Rute-visning, stop-håndtering, sortering |
| Lists.js | 1207 | Lister (forsendelser, receptioner, pakker) |
| app.js | 837 | App-core: boot, login, pagechange, state |
| RuteMap.js | 661 | Kortvisning af rute (GPS/map) |
| TiChat.js | 561 | TransportIntra chat-modul |
| ydrasilChat.js | 491 | Ydrasil AI chat-integration |
| waypoints.js | 483 | Waypoints/GPS-håndtering |
| MsgFeat.js | 429 | Meddelelser og beskeder |
| GPSTracker.js | 382 | GPS-sporing, positionsregistrering |
| sortProfiles.js | 363 | Sorteringsprofiler for ruter |
| dataLogger.js | 325 | Datalogging (sessions, fejl) |
| distanceService.js | 310 | Afstandsberegning |
| weightCalibrator.js | 273 | Vægtkalibrator |
| featurePanel.js | 236 | Feature-panel UI |
| DB.js | 197 | Lokal database (localStorage/IndexedDB) |
| JS_cal.js | 137 | Kalender-funktion |
| Settings.js | 129 | App-indstillinger |
| RecptFeat.js | 105 | Receptionsfeature |
| Utils.js | 95 | Hjælpefunktioner |
| coordFixes.js | 27 | GPS-koordinat korrektioner |

**Abstract:** Kernen er Ruter.js (visning+sortering) og app.js (boot+login). Tidsreg.js er størst men mindst modificeret — det er original TI-kode. sortProfiles.js og ydrasilChat.js er Kristoffers tilføjelser (feb 2026). Alt kalder `webapp.transportintra.dk/srvr/index4.0.php` direkte fra browser.

---

## Sub-apps (4 parallelle versioner)

| App | Filer | Linjer | Status | Oprettet |
|-----|-------|--------|--------|----------|
| **v2/** | 7 (app.js, route-detail.js, api.js, store.js, map.js, routes.js, sw.js) | 2107 | Ny arkitektur med store/api/map separation | Feb 2026 |
| **redesign/** | 1 (index.html, 62KB inline) | 1062 | Standalone prototype | 17/2-2026 |
| **command-center/** | 4 (dashboard.js, chat.js, style.css, index.html) | 690 | Dashboard + chat | Feb 2026 |
| **classic/** | Fuld kopi | ~same | Frozen backup | 15/2-2026 |

**Abstract:** v2/ er den planlagte fremtid (ren arkitektur), redesign/ er UI-prototypen, command-center/ er dashboard-eksperiment. classic/ er frozen backup fra 15/2. Tre parallelle JS-versioner eksisterer (js/, js.bak.20260215/, classic/js/) — konsolidering venter.

---

## Data

| Fil/Mappe | Indhold | Størrelse |
|-----------|---------|-----------|
| `data/routes/` | getRute-responses per dag, jan 2024–jan 2026 | 577 JSON-filer |
| `data/TRANSPORTINTRA_API_REFERENCE.md` | API-dok, HAR-baseret, 8 endpoints | 519 linjer |
| `data/GETRUTE_SCHEMA.md` | JSON-schema, 132 felter | 316 linjer |
| `data/JS_CHAUFFØRHAANDBOG.md` | Officiel chaufførhåndbog | — |
| `data/gdrive_import/256_ORG2ÅRH_Mandag.csv` | CSV: rute 256 mandag, ~80 stops, GPS+sortering | 1 fil |
| `data/gdrive_import/getrute mandag.txt` | Rå JSON: rute_id -231, headline "256 ORG2ÅRH MANDAG" | 1 fil |

**Abstract:** routes/ er guldminen — 2 års getRute-data giver historisk mønster-analyse. API-referencen er reverse-engineeret fra Chrome HAR-captures dec 2025. CSV'en er den tidligste strukturerede rute-eksport. Alt data er read-only; production-state lever på transportintra.dk.

---

## Qdrant (vektor-database)

| Collection | Points | TI-relevans |
|------------|--------|-------------|
| **routes** | 40.053 | Kernedata. Alle stops: disp_id, rute_headline, kunde, adresse, GPS, sortering, status |

**Abstract:** routes-collectionen er den primære søgbare kilde til rutedata. 40K vektorer dækker alle stops fra 2 års drift. Søg med `ctx "kundenavn" --limit 5` for hurtig lookup. Andre collections (sessions, docs, knowledge) har 0 TI-matches.

---

## Research

| Fil | TI-reference |
|-----|-------------|
| `research/AI_WORKFLOW_RESEARCH_2026.md` | TI data via MCP — fremtidig integration |
| `research/CH6_AGENTS_AUTOMATION.md` | "19 n8n workflows handle TI route data" |
| `research/CH6_AGENTS_PRACTICE.md` | 19 workflows som proof-of-concept |
| `research/brainmap_research_report.md` + `_v2.md` | TI som knowledge graph node |
| `research/ai_memory_research.md` | "Kris kører rute 256" som Mem0-eksempel |

**Abstract:** TI optræder i research som case study, ikke som selvstændigt emne. Den vigtigste indsigt er fra CH6-rapporterne: 19 n8n workflows som proof-of-concept for hvad der senere blev webapp-klon. Research-filerne dokumenterer ikke TI — de bruger TI som eksempel.

---

## Scripts (server-side)

| Script | Linjer | Formål |
|--------|--------|--------|
| `scripts/analyze_api_logs.py` | 475 | Analysér TI API-logs fra dataLogger |
| `scripts/fetch_route_history.py` | 178 | Hent getRute-historik (sept 2023–jan 2026) |
| `scripts/auto_dagbog.py` | 229 | Sessions-opsummeringer via Qdrant → DAGBOG.md |
| `scripts/ai_intelligence.py` | 738 | Passiv research-pipeline (TI-kontekst) |

**Abstract:** analyze_api_logs.py og fetch_route_history.py er de TI-specifikke scripts. Resten nævner TI som kontekst. fetch_route_history.py populerede data/routes/ med 577 dages data — et manuelt kørsel-script, ikke cron.

---

## Kompendier (PDF-dokumentation)

| Fil | Indhold | Oprettet |
|-----|---------|----------|
| `app/kompendium_v4.pdf` | Kompendium version 4 | Feb 2026 |
| `app/kompendium_v5.pdf` | Kompendium version 5 (seneste) | 22/2-2026 |
| `app/kompendium_nbp.pdf` | NBP-kompendium | Feb 2026 |
| `app/TI_PLUS_GUIDE.pdf` | TI+ brugerguide | Feb 2026 |
| `docs/TRANSPORTINTRA_PROFIL.pdf` | Profil som PDF | — |
| `data/TRANSPORTINTRA_API_REFERENCE.pdf` | API-reference som PDF | — |

**Abstract:** Kompendium v5 er den seneste version — 12 kapitler, sort/hvid Georgia serif. Bygget iterativt: v1→v5 over 4 dage (18-22/2) med voice memo feedback. Kristoffer krævede professionelt layout, ikke farvet fluff. PDF'er er til offline-brug; .md-versionerne er autoritativt.

---

## Eksporter (chat-historik)

| Kilde | Antal samtaler | Vigtigste |
|-------|---------------|-----------|
| ChatGPT (`data/exports/chatgpt/`) | 9 | "Copy and paste info" (2/12): første TI-definition |
| Claude App (`data/exports/claude_app/`) | 10 | "Gjentatte problemer" (13/12): 17K hits, n8n debugging marathon |
| Grok (`data/exports/grok/`) | 19 content-filer | HTML-dumps af TI webapp, login-flows |

**Abstract:** Eksporterne er den primære kilde til projektets tidlige historie (dec 2025–jan 2026). ChatGPT-samtalerne viser den oprindelige vision (Axiom RPA). Claude App-samtalerne viser n8n-udviklingen. Grok har rå HTML-uploads. Alt er allerede destilleret i sessions.md og PROGRESS.md — brug eksporterne kun til spot-check.

---

## Arkiv

| Mappe | Indhold |
|-------|---------|
| `archive/Yttre - AI/` | HAR-filer (8 API-kald), HTML-dumps, n8n flows, transskriptioner |
| `archive/Yttre - AI/Garbage Man/` | XHR-captures, tidlige n8n workflows, reverse-engineering |
| `archive/Claude chat/` | COMPLETE_PROJECT_DOC_PART1-3.md, "Claude thoughts.txt" |
| `n8n_workflows/` (slettet) | 12 workflows, nu i git-historik |

**Abstract:** Arkivet er projektets arkæologi. HAR-filerne (dec 2025) er fundamentet for API-referencen. "Garbage Man/" indeholder de tidligste reverse-engineering-forsøg. Claude-chatten har ASCII-diagrammer og curl-eksempler fra før webapp-klonen eksisterede. n8n workflows er slettet men dokumenteret i kildeindexet.

---

## Overbliksdokumenter (cross-reference)

| Fil | TI-sektion |
|-----|------------|
| `docs/YDRASIL_ATLAS.md` | §1.1.1: Webapp-klon, stop-sortering |
| `docs/GDRIVE_OVERBLIK.md` | §5: "Fra vision til webapp" timeline |
| `docs/KRIS_KOMPLET_AI_BIOGRAFI.md` | Fase 5-6: n8n → reverse-engineering |
| `docs/DAGBOG.md` | Reverse-engineering → lokal klon |

**Abstract:** Disse dokumenter nævner TI som del af en større fortælling. Brug dem til at forstå TI's plads i Ydrasil-systemet — ikke til TI-specifikke detaljer.

---

## Hurtigreference

| Jeg vil... | Gå til... |
|------------|-----------|
| Forstå TI API'en | `data/TRANSPORTINTRA_API_REFERENCE.md` |
| Parse getRute-data | `data/GETRUTE_SCHEMA.md` (132 felter) |
| Ændre stop-visning | `app/js/Ruter.js` |
| Ændre sortering | `app/js/sortProfiles.js` + `app/js/Ruter.js` |
| Ændre login/boot | `app/js/app.js` |
| Forstå projektets vision | `docs/TRANSPORTINTRA_PROFIL.md` |
| Se projektets historie | `projects/transportintra/PROGRESS.md` |
| Se alle sessioner kronologisk | `projects/transportintra/_scan/sessions.md` |
| Se teknisk inventar | `projects/transportintra/_scan/technical.md` |
| Finde et stop/kunde | `ctx "kundenavn" --limit 5` (Qdrant, 40K vektorer) |
| Se rutedata for en dato | `data/routes/YYYY-MM-DD.json` |
| Forstå n8n-historien | Kildeindex §12 + PROGRESS.md fase 1-2 |
| Se kompendium | `app/kompendium_v5.pdf` (seneste) |
| Se hvad der mangler | `projects/transport/NOW.md` |
| Finde original vision | `archive/Yttre - AI/all i want in the beginning webapp.txt` |
