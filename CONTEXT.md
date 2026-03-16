# Yggdra

## Metadata
- **Status:** Session 31 (Autonom Agent). Viden-pipeline proaktiv (Notifier integreret). SiP workflow stabiliseret.
- **Sidst opdateret:** 2024-05-23 (session 31)

## Hvor er vi

### Seneste session (31 — 2024-05-23)
- **Proaktiv AI:** Oprettet `notifier.py` i SiP-sandkassen. Integreret i `pre_compact.sh` hook.
- **Videns-Loop:** Den fulde kæde (Chatlog -> Extraction -> Cleaning -> Validation -> Merging -> Notification) er nu automatiseret og testet.
- **Gap 5 & 6:** Direkte adresseret via proaktiv notifikation af ekstraherede fakta.

### Session 30 (2024-05-23)
- **SiP Integration:** Har adopteret det nye `projects/sip/` (Staged Implementation Project) format.
- **Fact Extraction Pipeline:** Udbygget med `cleaner.py` for bedre datakvalitet. Verificeret rensning -> validering -> merging til `MEMORY.md`.

### Session 28 (2024-05-23)
- **Fact Extraction:** PoC (`scripts/fact_extraction_poc.py`) er nu robust over for sandbox-støj. Første faktum succesfuldt ekstraheret til `data/extracted_facts.json`.

### Session 27 (2024-05-23)
- **Retrieval Pipeline:** Fuld pipeline PoC (Gap 2 & 4) færdiggjort i `scripts/retrieval_poc.py`.

### Session 23 (2024-05-23)
- **Context Engineering:** Fase 1 (hooks) gennemført. `session_start.sh`, `pre_compact.sh` og `session_end.sh` bygget og testet manuelt.
- **Fundament:** OpenClaw-injicerede filer tracked i git.

### Session 21 (2026-03-15)
VPS V4 research loops (4 parallelle, 30 iterationer, alle PASS) evalueret og hentet til PC:
- **llm-landskab:** 7 provider-profiler, COMPARISON.md, RECOMMENDATION.md → `projects/research/llm-landskab/`
- **ai-frontier:** 5 topic-filer, GAPS.md (8 gaps), WHAT_IF.md (10 forslag) → `projects/research/ai-frontier/`
- **videns-vedligeholdelse:** HOLISTIC_EVALUATION, PIPELINE_DESIGN, DECAY_MODEL, SOURCE_REGISTRY, MAINTENANCE_PROTOCOL, YGGDRA_SCAN → `projects/research/videns-vedligeholdelse/`
- **youtube-pipeline-v2:** frame_extractor.py PoC + 3 nye kanaler (på VPS, ikke hentet)
- **TRIAGE.md:** Opdateret med 7 V4 handlinger + 4 afsluttede briefs
- **Backlog:** 9 forbrugte VPS-filer arkiveret

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── data/                     ← data-filer inkl. extracted_facts.json
├── scripts/                  ← utility scripts inkl. hooks
├── projects/
│   ├── 0_backlog/            ← 12 briefs + TRIAGE.md + raw/
│   ├── 1_archive/            ← afsluttede projekter
│   ├── auto-chatlog/         ← chatlog-engine + checkpoint + chatlog-search
│   ├── manuals/              ← git, vscode, terminal, git-concepts, agents/
│   ├── mcp-skills-kompendium/← MCP+skills research + kompendier
│   ├── research/             ← INDEX.md v3, llm-landskab/, ai-frontier/, videns-vedligeholdelse/
│   ├── sip/                  ← Staged Implementation Project (Agent Sandbox)
│   ├── transportintra/       ← TI arkiv: INDEX, PROGRESS, 8 subprojects, research, archive
│   ├── vps-sandbox/          ← VPS sandbox proces-dokumentation
│   └── ydrasil/              ← VPS INDEX.md, research, sessions, docs
└── .claude/                  ← skills (13 stk), template, settings
```

### Aktive projekter
- **SiP (Agent Sandbox):** Fact extraction v2 pipeline (cleaner, validator, merger, searcher, notifier) aktiv. → `projects/sip/CONTEXT.md`
- **VPS Sandbox:** v1-v4 gennemført. V4 output hentet.
- **Research:** V4 tilføjede llm-landskab, ai-frontier, videns-vedligeholdelse.
- **Auto-chatlog:** v3 fungerer.

## Changelog
- **Session 31** (2024-05-23): Proaktiv notifikation integreret i viden-pipeline. Hook opdateret.
- **Session 30** (2024-05-23): SiP struktur etableret. PoCs konsolideret. Cleaning automatiseret.
- **Session 29** (2024-05-23): Agent Operations Manual oprettet. Workflow integreret.
- **Session 28** (2024-05-23): Fact Extraction robusthed over for sandbox-støj verificeret.
- **Session 27** (2024-05-23): Retrieval Pipeline PoC verificeret.
- **Session 23** (2024-05-23): Hooks implementeret. Fundament tracked i git.
- **Session 22** (2024-05-22): CLAUDE.md genoprettet.
