# AI Arkitektur - Roadmap & Læringsnoter

Mål: Effektivt agentic workflow hvor den rigtige opgave gives til den rigtige LLM, med god datainfrastruktur under.

---

## Nuværende setup

| Komponent | Model | Pris | Rolle |
|-----------|-------|------|-------|
| Claude Code (CLI) | Opus 4.5 | Dyrest | Alt: kode, debug, research, UI |
| AI Rute Router (n8n) | Sonnet 4.5 | Medium | Chat-agent for ruteforespørgsler |

**Problem:** Opus bruges til alt, inkl. simple ændringer der kunne klares af Haiku/Sonnet.

---

## Ønsket arkitektur (agentic workflow)

```
Bruger (chat/Telegram) → Router Agent (billig, hurtig)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         Kode-agent      Data-agent      Rute-agent
         (Opus/Sonnet)   (Haiku/Sonnet)  (Sonnet)
              │               │               │
              ▼               ▼               ▼
         Filer/Git       Vector DB /     TransportIntra
                         RAG system      API
```

### Principper
- **Router first:** En billig model (Haiku) vurderer opgaven og sender til rette agent
- **Specialisering:** Hver agent har specifikke tools og kontekst
- **Mindste nødvendige model:** Simple lookups → Haiku. Kodning → Sonnet/Opus. Arkitektur → Opus.
- **Kontekst-effektivitet:** Agents får kun den data de behøver (via RAG/tools)

### Claude Skills
- **Hvad:** Genanvendelige prompt-skabeloner med tools, der kan aktiveres i Claude Code
- **Relevans:** Kunne bruges til at standardisere opgavetyper (f.eks. "webapp-ændring", "data-analyse", "n8n workflow")
- **TODO:** Undersøg hvordan Skills defineres, deles, og integreres med agentic workflows

### Sub-agent modeller (hvornår hvilken)

| Opgavetype | Model | Begrundelse |
|------------|-------|-------------|
| Routing/klassificering | Haiku | Billig, hurtig, nok til intent detection |
| Data lookup/formatering | Haiku | Struktureret output, ingen kreativitet nødvendig |
| Kodeændringer (simple) | Sonnet | God til fokuserede edits |
| Kodeændringer (komplekse) | Opus | Arkitektur, multi-fil, debugging |
| Analyse/planning | Opus | Kræver dyb forståelse |
| Bruger-chat (dansk) | Sonnet | God balance mellem kvalitet og pris |

---

## Datainfrastruktur

### Nuværende data
- 577 JSON-filer med rutedata (2 år, 40.053 stops)
- Google Sheets (planlægning)
- n8n Data Tables (cached sorting data)
- TransportIntra API (live data)

### Vector Database (RAG)

**Hvad er det:** Database der gemmer data som matematiske vektorer (embeddings), så man kan søge efter semantisk lighed i stedet for nøjagtig match.

**Relevans for os:**
- Søg i 2 års rutedata: "Hvornår var vi sidst på Grenåvej 42?"
- Find lignende stops/ruter baseret på indhold, ikke bare ID
- Hurtig kontekst-injektion til AI agents

**Muligheder:**

| System | Type | Fordele | Ulemper |
|--------|------|---------|---------|
| ChromaDB | Self-hosted | Simpelt, Python, gratis | Begrænset skalering |
| Qdrant | Self-hosted | Hurtigt, REST API, gratis | Mere setup |
| Pinecone | Cloud | Managed, skalerer | Koster penge |
| pgvector | PostgreSQL ext. | Integreret med eksisterende DB | Kræver PostgreSQL |
| Supabase | Cloud/self | pgvector + auth + API | Mere end vi behøver |

**Anbefaling:** Start med Qdrant (Docker container på VPS'en). REST API, let at integrere med n8n.

### Datakategorisering

Vores data kan struktureres i lag:

1. **Rå data** - JSON fra API (det vi har nu)
2. **Struktureret** - Normaliseret i database (stops, ruter, kunder, adresser)
3. **Embeddings** - Vektor-repræsentationer til semantisk søgning
4. **Aggregeret** - Statistik, mønstre, typisk rækkefølge per rute/dag

### RAG-systemer (Retrieval Augmented Generation)

**Princip:** I stedet for at give AI'en alle data, hent kun det relevante baseret på spørgsmålet.

**Typer:**

| Type | Beskrivelse | Brug |
|------|-------------|------|
| Naive RAG | Embed → søg → injicer i prompt | Simple spørgsmål |
| Hybrid RAG | Vektor + keyword søgning kombineret | Bedre precision |
| Agentic RAG | Agent beslutter hvad der skal søges, iterativt | Komplekse spørgsmål |
| Graph RAG | Vidensgrafer + vektorer | Relationer mellem entiteter |

**For os:** Start med Hybrid RAG (vektor + keyword). Agentic RAG som næste skridt.

---

## Ting jeg vil blive klogere på

- [ ] Præcis hvordan Kris' daglige workflow ser ud (morgen til aften)
- [ ] Hvilke beslutninger træffer Kris manuelt, som data kunne hjælpe med?
- [ ] Hvor meget koster nuværende Opus-forbrug per måned?
- [ ] n8n's sub-workflow agent capabilities (kan n8n selv route til sub-agents?)
- [ ] Claude Skills format og distribution (custom slash commands?)
- [ ] Optimal chunk-størrelse for rutedata embeddings
- [ ] Hvordan Google Sheets-data synkroniseres i praksis (frekvens, trigger)

---

## PAI Blueprint

Se `/docs/PAI_BLUEPRINT.md` for den fulde blueprint inspireret af Daniel Miesslers PAI v2.
Lag-model: Kerneværdier → Kognitiv arkitektur → Context systems → Skills → Workflows/Agents.

## Næste skridt (prioriteret)

1. ✅ **Dokumentér** - Dagbog, CHATLOG, docs i gang
2. ⏳ **TELOS** - Skriv kerneværdier og mål (fundamentet for PAI)
3. ✅ **Prototype** - Qdrant på VPS med rutedata embeddings (40.053 punkter!)
4. **Første Skill** - RuteManagement med SKILL.md
5. ⏳ **Router** - Simpel intent-classifier der sender til rette agent

---

## Status (2026-01-28)

### Hvad virker nu
- ✅ Qdrant vector DB kører (localhost:6333)
- ✅ 40.053 rute-punkter embedded
- ✅ 31 samtale-punkter embedded
- ✅ search.py - søg i collections
- ✅ get_context.py - hent formateret kontekst
- ✅ token_tracker.py - log og analysér forbrug
- ✅ CHATLOG.md - komplet samtalehistorik

### Næste implementation
- [x] Task router - klassificér intent og anbefal model
- [x] Automatisk kontekst-injektion via Qdrant
- [ ] n8n workflow med billig pre-processor

---

## Reference: Gastown (steveyegge)

Multi-agent orchestration system. Relevant når vi skalerer til flere agents.

**Koncepter vi kan bruge:**
- **Beads** - Git-backed work items (strukturerede issues)
- **Formulas** - TOML-baserede genanvendelige workflows
- **Mailboxes** - Persistent kommunikation mellem agents
- **Hooks** - Git worktree-based state persistering

**Vores simple ækvivalenter:**
| Gastown | Ydrasil |
|---------|---------|
| Beads | CHATLOG + Qdrant conversations |
| Mayor | Claude Code (mig) |
| Polecats | Fremtidige sub-agents |
| Hooks | CLAUDE.md + docs/ |

**Hvornår relevant:** Når vi har 3+ agents der skal koordineres.

Link: https://github.com/steveyegge/gastown
