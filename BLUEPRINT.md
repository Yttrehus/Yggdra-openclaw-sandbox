# BLUEPRINT — Yggdra PC

**Sidst opdateret:** 2026-03-14

## Vision

Yggdra er et personligt kognitivt exoskeleton. Yttre (Kristoffer, 36, chauffør rute 256, 40% ejer rejseselskab) bygger det som selvlært udvikler via AI. Målet: det skal føles som én kontinuerlig samtale med et system der husker alt.

To instanser:
- **VPS (Ydrasil)** — modent driftsmiljø: Qdrant (84K vektorer), Docker (traefik, webapp, qdrant, tor-proxy), 17 cron jobs, TransportIntra webapp (PRODUKTION), Telegram bot, Google integrations
- **PC (Yggdra)** — dette repo: udvikler-fundament, research, context engineering, projektstruktur. 18 sessioner + et autonomt V1-loop (6 iterationer) gennemført.

## Arkitektur — 5 emergente lag

Identificeret i V1-loopets direction-analysis (`research/reports/yggdra-direction-analysis.md`):

| Lag | Funktion | Status |
|-----|----------|--------|
| 1. Epistemisk fundament | Research-praksis, vidensorganisering | Designet (research-architecture) |
| 2. Temporal kontinuitet | Session-hooks, compaction, episodisk log | **Bygget** (4 hooks aktive) |
| 3. Handlingsevne | Automation, scripts, MCP/skills | Kortlagt (automation-audit, mcp-kompendium) |
| 4. Tilgængelighed | Notion-spejling, voice, mobil | Uadresseret |
| 5. Situationsbevidsthed | Self-audit, peer review | Uadresseret |

## Filstruktur

```
yggdra-pc/
├── CONTEXT.md                 ← repo-state, sessionshistorik
├── PROGRESS.md                ← fuld narrativ (18 sessioner)
├── BLUEPRINT.md               ← denne fil (systemkontekst on demand)
├── V1/                        ← arkiveret V1-loop output (BLUEPRINT, hooks, research)
├── data/
│   └── episodes.jsonl         ← episodisk log (git-baseret)
├── scripts/
│   ├── pre_compact.sh         ← PreCompact hook
│   ├── post_session_check.sh  ← UserPromptSubmit hook
│   ├── session_start.sh       ← SessionStart hook
│   ├── session_end.sh         ← Stop hook
│   ├── ctx / get_context.py   ← Qdrant-søgning (kræver SSH tunnel)
│   └── notion_api.py          ← Notion integration
├── research/
│   ├── INDEX.md               ← 5 atomiske noter + rapportindeks
│   ├── _inbox/                ← fleeting notes
│   ├── _archive/              ← pre-reformation VPS-research
│   └── reports/               ← 5 rapporter (direction, context-eng, research-arch, automation, session-drift)
├── projects/
│   ├── 0_backlog/                 ← raw./brief./r2g. briefs + TRIAGE.md
│   ├── 1_archive/                 ← døde projekter
│   ├── BMS.auto-chatlog/          ← chatlog-engine v3, kører automatisk
│   ├── DLR.session-blindhed/      ← aktiv research
│   ├── KNB.manuals/               ← git, terminal, vscode guides
│   ├── LIB.research/              ← INDEX.md, llm-landskab/, ai-frontier/, videns-vedligeholdelse/
│   ├── LIB.ydrasil/               ← VPS-æra research+docs (~160 filer)
│   ├── REF.mcp-skills-kompendium/ ← MCP+skills opslagsværk
│   ├── REF.prompt-skabeloner/     ← templates, MINING_RESULTS
│   ├── REF.transportintra/        ← TI arkiv, API docs, 8 subprojects
│   └── REF.vps-sandbox/           ← v1-v4 historik, evaluations
├── docs/                      ← eksterne docs (Qdrant m.m.)
└── .claude/
    ├── settings.local.json    ← 4 hooks + permissions
    └── skills/                ← context-search, infrastructure, notion
```

## Aktive projekter

| Projekt | Status | Sti |
|---------|--------|-----|
| BMS.auto-chatlog | v3 fungerer (chatlog-engine, secret-redaction, subagent-abstracts) | `projects/BMS.auto-chatlog/` |
| LIB.research | V4 output: llm-landskab, ai-frontier, videns-vedligeholdelse | `projects/LIB.research/` |
| REF.vps-sandbox | v1-v4 gennemført, V5 implementering deployet | `projects/REF.vps-sandbox/` |

## Hook-system

```
SessionStart     → session_start.sh       → injicerer CONTEXT.md + seneste episoder
PreCompact       → pre_compact.sh         → skriver marker med projekt + state
UserPromptSubmit → post_session_check.sh   → tjekker marker, injicerer reminder
Stop             → session_end.sh         → logger episode til episodes.jsonl
```

Registreret i `.claude/settings.local.json`. Alle 4 scripts testet og executable. Uafhængig af VPS hooks.

## VPS-adgang

```bash
ssh root@72.62.61.51 "command"              # Kør på VPS
ssh -L 6333:localhost:6333 root@72.62.61.51  # Qdrant tunnel
ctx "query" --limit 5                        # Søg i Qdrant (via tunnel)
```

## V1-loop: Resultater (6 iterationer, 2026-03-14)

Autonomt work-loop producerede:
- 5 research-rapporter (~2200 linjer, 60+ kilder)
- 3 projekter promoveret fra backlog (research-arch, context-eng, mcp-skills)
- 4 hook-scripts bygget og testet
- research/ mappestruktur med INDEX.md (5 atomiske noter)
- Optimeret CLAUDE.md med compaction-instruktioner

Kritisk finding fra revieweren: hooks blev forsøgt aktiveret 3 gange før det lykkedes i iteration 5. Lektie: verifikation > intention.

Fuld dokumentation: `V1/LOOP_STATE.md`, `V1/DELEGATION_PLAN.md`.

## Designprincipper

- **Bash-first.** Scripts over MCP. Composable, verifiable.
- **State på disk.** Markdown/JSONL i git. Ingen database for state.
- **Progressive disclosure.** CLAUDE.md (lag 1) → BLUEPRINT.md + CONTEXT.md (lag 2) → skills (lag 3).
- **Kill conditions.** Intet nyt uden defineret betingelse for fjernelse.
- **Irritation → overdesign → simplificering → exact fit.** Kris' designcyklus.
- **Adoption over arkitektur.** Byg kun hvad der bliver brugt.

## Backlog (prioriteret)

**Høj:** research-architecture (fase 2+), context-engineering (fase 3+)
**Medium:** automation-index, notion-spejling, cross-session-peer-review
**Lavere:** pdf-skill, integrationer, visualisering, voice, abonnement-overblik, project-taxonomy, terminal-automatisering, webscraping-audit

Alle briefs: `projects/0_backlog/` (15 stk).

## Afsluttede moduler

- **M1-M3:** Git, VS Code, Terminal (SSH, WSL, Zsh, Starship)
- **M4:** Projektstruktur (~/dev/, template, /checkpoint, dotfiles-repo)
- **M5:** PC-setup (downloads, .wslconfig, JetBrains Mono) — step 12+15 venter fysisk adgang
- **REF.mcp-skills-kompendium:** Adversarial-reviewed opslagsværk (25+ MCP-servere, 20+ skills)

## Åbne spørgsmål

1. **VPS-PC konvergens:** Overtager PC VPS-funktioner? Synkroniserer de? Eller separate ansvarsområder? Ingen af de 18 sessioner eller V1-loopet har besvaret dette.
2. **Feedback-loop:** Bruger Kris faktisk det der bygges? 18 sessioner + V1-loop har produceret hooks, research, projekter — men der er ingen systematisk måling af om det giver reel værdi i daglig brug.
3. **CLAUDE.md placering:** V1-loopet skrev en optimeret CLAUDE.md der nu ligger i `V1/CLAUDE.md`. Den er ikke aktiv i roden. PC-repoet har ingen CLAUDE.md — hooks og settings virker, men den primære instruktionsfil mangler.
