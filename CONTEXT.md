# Yggdra

## Metadata
- **Status:** Session 23 (Owner) / Session 31 (Agent). V6 research-konsolidering gennemført. SiP Knowledge Pipeline integreret.
- **Sidst opdateret:** 2026-03-16 (session 23/31)

## Hvad er det
Personligt udvikler-fundament. Startede som "Basic Setup" (Windows-opsætning), vokset til framework for hvordan Yttre arbejder med AI og kode.

## Hvor er vi

### Seneste Agent Sessioner (22-31 — 2024-05-22/23)
- **Session 31:** Viden-pipeline proaktiv (Notifier integreret). SiP workflow stabiliseret. Den fulde kæde (Chatlog -> Extraction -> Cleaning -> Validation -> Merging -> Notification) er nu automatiseret i `pre_compact.sh`.
- **Session 30:** PoCs flyttet til `projects/sip/`. SiP struktur etableret. Fact Cleaning automatiseret.
- **Session 29:** Agent Operations Manual oprettet i `projects/manuals/agents/OPERATIONS.md`.
- **Session 28:** Fact Extraction robusthed over for sandbox-støj verificeret. Første fakta gemt i `data/extracted_facts.json`.
- **Session 27:** Retrieval Pipeline PoC (Gap 2 & 4) færdiggjort og verificeret i `projects/sip/retrieval_v2/`.
- **Session 23:** Context Engineering Fase 1 (hooks) implementeret. Scripts bygget i `scripts/`.
- **Session 22:** CLAUDE.md genoprettet. DAGBOG.md startet. Identificeret domæneopdeling (PC vs VPS).

### Seneste Owner Sessioner
#### Session 23 (2026-03-16)
V6 research-konsolidering — VPS destillater hentet, gamle filer slettet.
- **14 nye filer hentet fra VPS** → `projects/2_research/` (2 destillater, 5 standalone, 3 psykologi, 2 transport/økonomi, catalog+deep study+red team)
- **83 filer slettet fra LIB.ydrasil/research/** (91→8): absorberede memory/agent-filer, CH-kapitler (bog-projekt), duplikater, LaTeX-artefakter, forældede snapshots
- **8 filer beholdt:** 4 visualization, 2 voice, 1 notion, sources/ — understøtter aktive briefs
- **ARCHITECTURE_CONTINUOUS_MEMORY.md** slettet fra docs/ (absorberet i destillat)
- **State opdateret:** REF.vps-sandbox/CONTEXT.md (V6-sektion), TRIAGE.md (V6 afsluttet)

#### Session 22 (2026-03-15)
Backlog burn planlagt. VPS V6 deployet (7 iter: RSS+heartbeat+decay+reranking+healthcheck+feeds+inventory). PC-plan klar (8 briefs).

### Session 21 (2026-03-15)
VPS V4 research loops (4 parallelle, 30 iterationer, alle PASS) evalueret og hentet til PC:
- **llm-landskab:** 7 provider-profiler, COMPARISON.md, RECOMMENDATION.md → `projects/LIB.research/llm-landskab/`
- **ai-frontier:** 5 topic-filer, GAPS.md (8 gaps), WHAT_IF.md (10 forslag) → `projects/LIB.research/ai-frontier/`
- **videns-vedligeholdelse:** HOLISTIC_EVALUATION, PIPELINE_DESIGN, DECAY_MODEL, SOURCE_REGISTRY, MAINTENANCE_PROTOCOL, YGGDRA_SCAN → `projects/LIB.research/videns-vedligeholdelse/`
- **youtube-pipeline-v2:** frame_extractor.py PoC + 3 nye kanaler (på VPS, ikke hentet)
- **TRIAGE.md:** Opdateret med 7 V4 handlinger + 4 afsluttede briefs
- **Backlog:** 9 forbrugte VPS-filer arkiveret

### Session 20 (2026-03-14)
VPS sandbox v2 (10 iter) + v3 (6 iter) afsluttet og evalueret. Output hentet til PC:
3 nye skills (dialectic-pipeline, session-resume, sitrep), TI-projekt (INDEX+PROGRESS+8 subprojects+research+archive), research INDEX v3 (54 insights), BLUEPRINT.md, TRIAGE.md, vps-sandbox CONTEXT.md, reference-filer.

### Session 19 (2026-03-14)
VPS sandbox v2 designet og deployed. Tre projekter i Ralph loop (10 iterationer). VPS v1 kvalitetsauditeret. Prompt evalueret og justeret. Handoff fra github-workflow absorberet (prompt-skabeloner).

### Session 18 (2026-03-14)
Ydrasil-projekt startet: VPS research+docs indekseret (INDEX.md). MCP/Skills kompendium research gennemført (adversarial proces). Nye skills tilføjet (context-search, debugging-wizard, mcp-builder, spec-miner, strategic-compact, the-fool, verification-loop). Nye backlog briefs (project-taxonomy, session-blindhed). data/ og scripts/ mapper oprettet i roden. Checkpoint-skill rettet: chatlog-engine kører nu først. Underscore-prefix fjernet fra projektmapper.

### Session 17 (2026-03-14)
Skills-synlighed i VS Code: global vs projekt `.claude/skills/` afklaret — alt allerede synkroniseret i projekt-mappen. MCP/Skills kompendium opgraderet fra brief til projekt. Adversarial research-proces designet: context scout → parallel research (MCP-landskab, skills-landskab, Yggdra-behov) → steelman → red team → steelman red team → neutral evaluator.

### Session 16 (2026-03-15)
Backlog-audit: 14→11 briefs. context-engineering + session-drift-pipeline merged. webscraping-audit + terminal-automatisering → raw/. 6 briefs opdateret/skærpet (visualisering, mcp, integrationer, notion, peer-review, voice). VPS Ydrasil-æra research + docs downloaded til projects/research/ydrasil/ (89+73 filer, ~9MB). GDrive-duplikat slettet. Research-kvalitet vurderet: høj substans, men iterativt klutter (~30% duplikater fra CH-kapitler). Diskussion om prioritering: research-arkitektur → agent teams → hukommelse. Vision-briefs parkeret (transport-app, politik, LLM-uafhængighed).

### Session 15 (2026-03-14)
M5 step 11/13/14/17 gennemført: Downloads ryddet (225→2 filer), .wslconfig oprettet (8GB/4CPU), JetBrains Mono + ligaturer, quick reference. Chatlog-engine token-scanning tilføjet (heuristisk + subagent-verifikation, redact-patterns.json). M6/M7/M8 flyttet fra plan til backlog-briefs. Parallel tasks absorberet i briefs. Backlog-briefs evalueret og opdateret. "Basic Setup" referencer fjernet. architecture.R&D CONTEXT.md oprettet. Google AI samtale flyttet til architecture.R&D. Archive ryddet. Lektie: `rm` i bash bypasser papirkurven.

### Session 14 (2026-03-13)
Chatlog-engine v3: gap-sektioner, subagent-abstracts, danske datoer, secret-redaction. Sessions fra 5 projektmapper samlet i én (~2500 beskeder, 30 sessions). Checkpoint og chatlog-search integreret i auto-chatlog-projektet. Skills audit: forældede stier rettet, checkpoint/chatlog-search forenklet til pointere. Archive ryddet: journals, manuelle chatlogs, dump-scripts slettet (alt i git). Template opdateret: NOW.md+PLAN.md → CONTEXT.md. architecture.R&D fået CONTEXT.md.

### Session 13 (2026-03-13)
Manifest v4 implementeret. Tre iterationer af mappestruktur (pipeline/ → Development/ → projects/) landede på det simpleste: flad projects/-mappe, ét projekt = én mappe. ADR-terminologi og pipeline-stages droppet — erstattet af CONTEXT.md overalt med plain dansk status. Manuals og research ind under projects/. Rod reduceret til 2 mapper (projects/ + .claude/). CONTEXT.md template designet (rekursivt, skalerbart). NOW+PLAN+PROGRESS → CONTEXT.md + PROGRESS.md.

Chatlog v2 krav defineret: én fil (chatlog.md), komplet sessionsdata inkl. tænkeblokke og tool calls, session-baseret inddeling, navigationslinks. Hukommelsesarkitektur skitseret: markdown (nu) → vector DB (snart) → knowledge graph (senere). Claude Memory tilføjet til VS Code workspace.

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── data/                     ← data-filer
├── scripts/                  ← utility scripts
├── projects/
│   ├── 0_backlog/                ← raw./brief./r2g. briefs + TRIAGE.md
│   ├── 9_archive/                ← døde projekter
│   ├── BMS.auto-chatlog/         ← chatlog-engine, kører automatisk
│   ├── DLR.session-blindhed/     ← aktiv research
│   ├── KNB.manuals/              ← git, terminal, vscode guides
│   ├── 2_research/               ← V4+V6 destillater, llm-landskab/, ai-frontier/, videns-vedligeholdelse/
│   ├── LIB.ydrasil/              ← VPS-æra docs, sessions, 8 resterende research-filer
│   ├── REF.mcp-skills-kompendium/← MCP+skills opslagsværk
│   ├── REF.prompt-skabeloner/    ← templates, MINING_RESULTS
│   ├── REF.transportintra/       ← TI arkiv, API docs, 8 subprojects
│   ├── REF.vps-sandbox/          ← v1-v4 historik, evaluations
│   └── SIP.agent-sandbox/        ← Staged Implementation Project (Agent Sandbox)
└── .claude/                  ← skills (13 stk), template, settings
```

### Aktive projekter
- **SIP.agent-sandbox:** Fact extraction v2 pipeline (cleaner, validator, merger, searcher, notifier) aktiv. → `projects/SIP.agent-sandbox/CONTEXT.md`
- **REF.vps-sandbox:** v1-v6 gennemført. V6: research-konsolidering, 14 filer hentet. → `projects/REF.vps-sandbox/CONTEXT.md`
- **2_research:** V4+V6 destillater (llm-landskab, ai-frontier, videns-vedligeholdelse, memory+agents destillater). → `projects/2_research/`
- **BMS.auto-chatlog:** v3 fungerer (~3000 beskeder, 39 sessions). → `projects/BMS.auto-chatlog/CONTEXT.md`
- **REF.transportintra:** Komplet arkiv. → `projects/REF.transportintra/CONTEXT.md`

### Afsluttede moduler
- **M1-M3:** Git, VS Code, Terminal (SSH, extensions, WSL, Zsh, Starship)
- **M4:** Projektstruktur (~/dev/ layout, template, /new-project, /checkpoint, dotfiles-repo)

### Venter
- **M5 step 12, 15:** X1 Carbon (BIOS, fysisk adgang), Dev Drive (GUI/admin)

## Hvad mangler
- [x] Reformation ✅
- [x] M5 step 11 — Downloads oprydning (225→2 filer) ✅
- [x] M5 step 13 — .wslconfig (8GB RAM, 4 CPU) ✅
- [x] M5 step 14 — JetBrains Mono + Mermaid Preview ✅
- [x] M5 step 16 — Poppler verificeret ✅
- [x] M5 step 17 — Quick reference ✅
- [ ] M5 step 12 — X1 Carbon (BIOS, Lenovo Vantage, 400 MHz bug — kræver fysisk adgang)
- [ ] M5 step 15 — Dev Drive (evaluer om det giver mening, kræver GUI/admin)
- M6, M7, M8 → backlog-briefs i `projects/0_backlog/`

## Beslutninger

**Rækkefølge:** M5 rest (12, 15 — begge kræver dig) → backlog-projekter efter prioritet

**Metodik:**
- PDCA-cyklus per modul (Plan-Do-Check-Act, Deming)
- Solnedgangsklausul per implementation (succes/kalibrerings/kill-tegn, evalueringstidspunkt)
- Default: justér → omtænk → kill
- Spørg før du bygger. Diskussion færdig → bekræftelse → kode.

**Scope:** Alt der vokser ud over udvikler-fundament bliver separate projekter i `projects/`.

**State-filer:**
- CONTEXT.md (denne fil) — læses automatisk, altid aktuelt overblik
- PROGRESS.md — fuld narrativ, læses efter behov for kontekst
- Hvert projekt har sin egen CONTEXT.md (samme format, rekursivt design)

## Åbne tråde
- Prettier mangler .prettierrc
- /new-project utestet i praksis
- chatlog-search: for tidligt at evaluere

## Changelog
Komprimeret overblik. Fuld detalje i PROGRESS.md.

- **Session 23 (Owner)** (2026-03-16): V6 research-konsolidering. 14 destillater hentet fra VPS. 83 filer slettet fra LIB.ydrasil/research/ (91→8). CH-kapitler, duplikater, LaTeX, forældede snapshots fjernet. → PROGRESS.md#session-23
- **Session 31 (Agent)** (2024-05-23): Proaktiv notifikation integreret i viden-pipeline. Hook opdateret.
- **Session 30 (Agent)** (2024-05-23): SiP struktur etableret. PoCs konsolideret. Cleaning automatiseret.
- **Session 29 (Agent)** (2024-05-23): Agent Operations Manual oprettet. Workflow integreret.
- **Session 28 (Agent)** (2024-05-23): Fact Extraction robusthed over for sandbox-støj verificeret.
- **Session 27 (Agent)** (2024-05-23): Retrieval Pipeline PoC verificeret.
- **Session 22 (Owner)** (2026-03-15): Backlog burn planlagt. VPS V6 deployet (7 iter: RSS+heartbeat+decay+reranking+healthcheck+feeds+inventory). PC-plan: 8 briefs lukkes. RDY.backlog-burn.md skrevet. → PROGRESS.md#session-22
- **Session 21** (2026-03-15): VPS V4 (4 loops, 30 iter) evalueret og hentet. 19 research-filer.
- **Session 20** (2026-03-14): VPS v2+v3 evalueret, output hentet til PC. 3 skills, TI-projekt.
- **Session 19** (2026-03-14): VPS sandbox v2 deployed (3 projekter), prompt evalueret+justeret.
- **Session 18** (2026-03-14): Ydrasil-projekt startet, MCP/Skills kompendium research done, 7 skills tilføjet.
- **Session 17** (2026-03-14): Skills-synlighed afklaret, MCP/Skills kompendium brief→projekt.
- **Session 16** (2026-03-15): Backlog-audit (14→11 briefs), VPS research downloaded.
- **Session 15** (2026-03-14): M5 step 11/13/14/17 done, M6-M8→backlog, token-scanning.
- **Session 14** (2026-03-13): Chatlog-engine v3, sessions samlet, reformation done.
- **Session 13** (2026-03-13): projects/ struktur, ADR→CONTEXT.md, chatlog v2 krav.
- **Session 12** (2026-03-12): Manifest v1-v3 implementeret, 13 briefs.
- **Session 11** (2026-03-12): Fil-audit, references/ opløst.
- **Session 10** (2026-03-12): Repo→Yggdra besluttet, CONTEXT.md design.
- **Session 9** (2026-03-11): Auto-chatlog prototype, Project Reformation startet.
- **Session 8** (2026-03-10): M4 afsluttet, skills evalueret.
- **Session 7** (2026-03-10): Dotfiles-repo, skills-arkitektur revideret.
- **Session 6** (2026-03-10): Per-projekt skabelon, /checkpoint og /new-project oprettet.
- **Session 5** (2026-03-10): ~/dev/ layout, PDCA, solnedgangsklausul.
- **Session 4** (2026-03-10): "Basic Setup er ikke basic", cross-session peer review.
- **Session 3** (2026-03-10): Session-management problem, VPS research, yggdra-gold.
- **Session 1-2** (2026-03-08/09): M1-M3 done, PLAN v2, ~/dev/ oprettet.
