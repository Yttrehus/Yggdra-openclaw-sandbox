# SYNTESE: 11 Videoer → Ydrasil Handlingsplan

## Kilder analyseret

| # | Video | Kanal | Kerneemne |
|---|-------|-------|-----------|
| 1 | Building Your Own Unified AI Assistant | Miessler | UFC, CLI-first, Skills |
| 2 | PAI v2.0 | Miessler | TELOS, 4-layer context, self-update |
| 3 | Complete Agentic RAG Build (134 min) | AI Automators | 8-modul RAG pipeline |
| 4 | GraphRAG | AI Automators | Knowledge graphs, LightRAG |
| 5 | Hybrid Retrieval | AI Automators | 9 spørgsmålstyper, retrieval engineering |
| 6 | 800+ Hours RAG in 42 min | AI Automators | 8 RAG-mønstre, progressive complexity |
| 7 | Second Brain + Claude Code + Obsidian | Cole Medin | Skills, progressive disclosure |
| 8 | More Agents = Worse (Google/MIT) | Nate B Jones | To-tier hierarki, ephemeral workers |
| 9 | Ticking Time Bomb in Codebases | Nate B Jones | Context engineering > model intelligence |
| 10 | Second Brain 2026 | Nate B Jones | 8 building blocks, 12 design principles |
| 11 | Karpathy Feels Behind | Nate B Jones | 4-level skill tree, generation vs decisioning |

---

## De 7 konsensus-principper (alle kilder enige)

**1. Filesystem > RAG for struktureret viden**
Miessler, Cole Medin, og Nate B Jones er enige: for ting med kendt struktur (config, regler, præferencer, skills) er filer overlegne. RAG er til store, ustrukturerede datasæt hvor semantisk søgning er nødvendig.

**2. Progressive Disclosure er nøglen til skalering**
Cole Medin + Miessler: Skills med 3 lag (kort beskrivelse → fuld instruktion → ekstra filer). Google/MIT-studiet: 30-50 tools er grænsen før accuracy falder. Løsning: vis kun hvad der er relevant nu.

**3. To-tier hierarki er optimalt**
Google, MIT, Cursor, Yaggi (Gastown) bekræfter uafhængigt: Planner → dumb Workers → Judge. Flat teams og 3+ niveauer fejler. Ydrasils n8n-arkitektur (AI Rute Router → sub-agents) er allerede korrekt.

**4. Context engineering > model intelligence**
Nate B Jones: "Model intelligence is commoditized. Context engineering is the differentiator." Miessler: 80% deterministic code, 20% AI. Værdien er i scaffolding, ikke i hvilken model der bruges.

**5. Design for restart, ikke perfektion**
Nate B Jones' Second Brain: Kris vil have dage hvor systemet ikke bruges. Ingen backlog-monster. Bare genoptag. Episodisk drift hvor state gemmes eksternt.

**6. Separation: Memory / Compute / Interface**
Alle kilder: Hold lagene adskilt. Memory = Qdrant + filesystem. Compute = Claude + n8n. Interface = webapp/chat/voice. Gør hvert lag udskifteligt.

**7. Start simpelt, tilføj kompleksitet kun når simpelt fejler**
RAG Masterclass: 8 mønstre i rækkefølge — gå kun op når det nuværende mønster bevisligt fejler. Cole Medin: build core loop first, then add modules.

---

## Ydrasils nuværende position

| Komponent | Status | Kilde-validering |
|-----------|--------|------------------|
| Qdrant (40.053 rutepunkter) | ✅ Korrekt | RAG til store datasæt |
| CLAUDE.md (struktureret kontekst) | ✅ Korrekt | UFC-princip fra Miessler |
| n8n (to-tier: Router → sub-agents) | ⚡ Afvikles | Erstattes af ren Python/FastAPI |
| 6-fase logging | ✅ Korrekt | Observability (Jones Level 3) |
| Continue On Fail | ✅ Korrekt | Graceful degradation |
| CHATLOG + session docs | ✅ Korrekt | Audit trail (building block 5) |
| Root Cause Analyse | ✅ Korrekt | Feedback loop (Jones Level 4) |
| Skills/Progressive Disclosure | ✅ Done | Fase 1 |
| Hybrid search (lexical+semantic) | ✅ Done | Fase 2 |
| Metadata filtering | ✅ Done | Fase 2 |
| Pattern matching (koder, IDs) | ✅ Done | Fase 2 |
| n8n → Python migration | ❌ Mangler | Fase 3 — renere, mere fleksibelt |
| PWA (installérbar app) | ❌ Mangler | Fase 4 — cross-platform |
| Navigation for lastbiler | ❌ Mangler | Fase 4 — standalone byggeklods |
| Capture point (friktionsfri input) | ❌ Mangler | Fase 5 |
| Daily digest/nudge | ❌ Mangler | Fase 5 |
| Voice-first interface | ❌ Mangler | Fase 6 |

---

## HANDLINGSPLAN: 4 Faser

### FASE 1: Kontekst-fundament (UFC + Skills) ✅ DONE

**1a. Omstrukturér til UFC-stil kontekst** ✅
- `.claude/skills/` med 6 skills (route-lookup, sync-sorting, webapp-dev, youtube-pipeline, infrastructure, data-analysis)
- CLAUDE.md slanket fra 552 → 176 linjer

**1b. Skills med Progressive Disclosure** ✅
- Hver skill: frontmatter (description + use when) → fuld instruktion

**1c. Company Glossary** ✅
- `/data/glossary.json` + `/data/glossary.md`
- Rutekoder, container-typer, status-koder, forkortelser

---

### FASE 2: Retrieval-lag (Hybrid Search) ✅ DONE

**2a. Hybrid search i Qdrant** ✅
- Re-embedded 40.053 punkter med dense (OpenAI) + sparse (BM25/fastembed) vectors
- RRF (Reciprocal Rank Fusion) kombinerer begge for bedre resultater
- Script: `embed_routes_v2.py`

**2b. Metadata filtering** ✅
- 12 payload indexes: date, weekday, year, month, rute_id_abs, postnr, bynavn, kunde, adresse, disp_status, rute_status, chf_rmrks
- Enriched metadata: date, weekday, year, month, disp_headline, chf_rmrks, sorter, rute_id_abs

**2c. Pattern matching for koder** ✅
- Regex-baseret detektion: rute_id, rutekoder, ugedage, måneder, fejlkoder, telefonnumre
- MatchText search i kunde/adresse/chf_rmrks felter

**2d. Retrieval routing** ✅
- Auto-klassificering per query: hybrid (default), filter, pattern, hybrid_filtered
- `get_context.py` v2 med --filter, --mode, --exact flags

---

### FASE 3: n8n → Python migration
*Erstat n8n workflows med ren kode — mere fleksibelt, nemmere at debugge*

**3a. TransportIntra API-klient i Python**
Direkte API-kald (auth, getRute, updateSorter). Ingen n8n mellemled. Kan bruges som library af andre scripts.

**3b. Sync Sorting som Python-script**
Google Sheets data → sammenlign med API → updateSorter. Erstatter n8n Sync Sorting workflow.

**3c. AI Rute Agent som FastAPI service**
Claude API direkte + Qdrant kontekst (get_context.py allerede bygget) + samtalehukommelse. Erstatter n8n AI Rute Router.

**3d. Skill-ificér det hele**
Hvert script bliver en Claude Code skill der kan trigges direkte.

---

### FASE 4: App-byggeklodser
*Modulære komponenter der bygges uafhængigt og samles til den endelige app*

**4a. PWA-konvertering**
Service worker + manifest → webapp kan installeres på telefon (Android + iPhone + Windows). Offline-support for kernefunktioner.

**4b. Friktionsløs chauffør-flow**
Automatisk næste-stop, swipe-gestures, minimal berøring. Chaufføren fokuserer på fysisk arbejde, app'en håndterer resten.

**4c. Navigation for lastbiler**
Selvstændig byggeklods (potentielt egen app). Idéer der adresserer lastbilchaufførers specifikke behov — et område hvor Google Maps ikke er optimalt. Kris har idéer til dette.

**4d. AI-lag i app'en**
Intelligent assistance direkte i interfacet — kontekst-bevidst, lærer over tid (arrival predictor-princippet udvidet).

---

### FASE 5: Capture + Second Brain Loop
*Friktionsfri input → AI klassificerer → daglig digest*

**5a. Drop Box (ét capture-punkt)**
Voice memo eller kort tekst fra telefon → API → AI klassificerer → gemmer. Én handling, nul beslutninger.

**5b. Sorter + Form (AI klassificering)**
4 kategorier: Rute, Idé, Person, Admin. Strukturerede felter (next action, kontekst, urgency).

**5c. Bouncer (confidence filter)**
Score 0-1. Under 0.6: log + spørg Kris. Over: fil automatisk.

**5d. Tap on Shoulder (daglig digest)**
Morgen: Top 3 handlinger. Søndag: Uge-review. Under 150 ord.

---

### FASE 6: Autonomi
*Systemet arbejder selvstændigt og rapporterer*

**6a. Voice-first interface**
Whisper (STT) + TTS. Tale ind, høre svar. Aldrig behøve skærm.

**6b. Informations-pipeline**
AI læser kuraterede kilder i baggrunden → kun guldkorn → daglig briefing.

**6c. Self-update skill**
AI monitorerer nye releases, best practices, opdaterer sig selv.

---

## Kerne-beslutning: Retrieval-strategi

```
Filesystem (UFC/Skills)     → Regler, config, skills, præferencer, glossary
                               Miessler: "File system IS the context system"

Qdrant Hybrid Search        → Rutedata (40K+ points), samtaler, knowledge
                               Vector + Sparse + Metadata + RRF

Pattern Matching (Regex)    → Rutekoder, IDs, telefonnumre, fejlkoder
                               AI Automators: "Tokenizers destroy codes"

GraphRAG/LightRAG           → SENERE. Evaluér når hybrid search fejler
                               på relationship-queries. Ikke nu.
```

---

---

## Strategisk retning (opdateret 2026-01-31)

**Vision:** En cross-platform app (PWA) der gør arbejdet mellem fysiske opgaver og TransportIntra friktionsløst. Ikke bare en webapp-klon — en intelligent chauffør-assistent.

**n8n afvikles gradvist.** n8n var en god prototype-platform, men er nu en hat på en hat. Claude kan skrive bedre kode direkte end det n8n workflows kan udtrykke.

**Byggeklods-tilgang:** Hver komponent (navigation, sync, AI-agent, capture) bygges som selvstændigt modul der kan bruges alene og samles til den endelige app. Særligt navigation for lastbiler har potentiale som standalone produkt.

**Princip:** Bevæg dig ikke for hurtigt. Byg én byggeklods ad gangen, test den i praksis, iterér.

## Én sætning

**Byg modulære byggeklodser (API-klient, PWA, navigation, AI-agent) der hver især løser ét problem godt — og som tilsammen bliver den friktionsløse chauffør-app.**
