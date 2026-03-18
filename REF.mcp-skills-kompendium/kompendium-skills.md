# Claude Code Skills — Kompendium

Kurateret oversigt over Claude Code skills. Kategoriseret efter funktion, med kilde og kvalitetsvurdering.

**Skills er markdown-filer** — ingen runtime-risiko, kan inspiceres og redigeres frit.

---

## Allerede installeret i Yggdra

| Skill | Kategori | Kilde | Kvalitet |
|-------|----------|-------|----------|
| **checkpoint** | Session/State | Egenudviklet | Basal (4 trin) |
| **strategic-compact** | Session/State | ECC community | God |
| **context-search** | Search/Retrieval | Egenudviklet (Qdrant) | God |
| **chatlog-search** | Search/Retrieval | Egenudviklet | God |
| **debugging-wizard** | Debugging | Jeffallan | God (5 reference-filer) |
| **the-fool** | Kritisk tænkning | Jeffallan | God |
| **verification-loop** | Kvalitetssikring | ECC community | God (multi-fase) |
| **spec-miner** | Krav/Spec | Jeffallan | God (EARS-format) |
| **mcp-builder** | Infrastruktur | Anthropic officiel | God |
| **infrastructure** | Infrastruktur | Egenudviklet | Basal |
| **new-project** | Projekt | Egenudviklet | Basal |
| **notion** | Projekt | Egenudviklet | Basal |

---

## Kategori: Planlægning & Execution

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **writing-plans** | Granulær task-nedbrydning (2-5 min per task), human checkpoints | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Delvist med PDCA/CONTEXT.md |
| **executing-plans** | Batch execution af planer med stop-points og verificering | Superpowers (obra) | Høj | Delvist med PDCA/CONTEXT.md |
| **AB Method** | Spec-driven workflow: store problemer → fokuserede missioner | [Ayoub Bensalah](https://github.com/AyoubBensworker) | Medium | Delvist med writing-plans |

---

## Kategori: Code Review & Kvalitet

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **requesting-code-review** | Pre-review checkliste, severity-baseret feedback | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Ingen |
| **receiving-code-review** | Systematisk respons på code review feedback | Superpowers (obra) | Høj | Ingen |
| **claude-git-pr-skill** | PR review med `gh` CLI, pending reviews, suggestions | [aidankinzett](https://github.com/aidankinzett/claude-git-pr-skill) | Medium | Delvist med code-review |

---

## Kategori: Testing

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **test-driven-development** | RED-GREEN-REFACTOR cyklus med anti-patterns reference | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Ingen |
| **verification-before-completion** | Verificér at implementation matcher spec før done | Superpowers (obra) | Høj | Delvist med verification-loop |

---

## Kategori: Debugging & Analyse

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **systematic-debugging** | Hypotese-drevet fejlsøgning, log-analyse | [Superpowers (obra)](https://github.com/obra/superpowers) | Medium | Overlap med debugging-wizard |
| **debugging-wizard** (installeret) | 5 reference-filer, stack trace analyse, root cause | [Jeffallan](https://github.com/Jeffallan/claude-skills) | Høj | — |

---

## Kategori: Sikkerhed

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **audit-context-building** | CodeQL/Semgrep analyse, angrebsflade-mapping, variant analysis | [Trail of Bits](https://github.com/trailofbits/skills) | Professionel | Ingen |
| **security-review** | OWASP-style review af kode | Trail of Bits | Professionel | Delvist med audit |
| **parry** | Prompt injection scanner for hooks | [Dmytro Onypko](https://github.com/nicepkg/aide) | Niche | Ingen |

---

## Kategori: Git & Workflow

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **using-git-worktrees** | Isoleret branch-arbejde i separate directories | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Ingen |
| **git-commit-conventions** | Conventional commits, semantic versioning | Diverse | Medium | Ingen |

---

## Kategori: Subagent & Orchestration

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **dispatching-parallel-agents** | Koordinér concurrent subagent workflows, merge resultater | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Ingen |

---

## Kategori: Kreativ & Ideation

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **brainstorming** | Socratic questioning, design exploration, muligheds-generering | [Superpowers (obra)](https://github.com/obra/superpowers) | Høj | Komplementær til the-fool |
| **the-fool** (installeret) | Devil's advocate, pre-mortem, red team | [Jeffallan](https://github.com/Jeffallan/claude-skills) | Høj | — |

---

## Kategori: Session & State

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **session-management** | Track åbne beslutninger, modificerede filer, uafsluttede tråde | [t0ddharris](https://github.com/t0ddharris/claude-code-skills) | Medium | Delvist med checkpoint |
| **strategic-compact** (installeret) | Kontekst-komprimering ved logiske intervaller | ECC community | God | — |
| **skill-creator** | Guide til oprettelse af nye skills | [Anthropic officiel](https://github.com/anthropics/skills) | Høj | Ingen |

---

## Kategori: Specialiseret

| Skill | Hvad den gør | Kilde | Kvalitet | Overlap |
|-------|-------------|-------|----------|---------|
| **spec-miner** (installeret) | Reverse-engineer specs fra kodebase, EARS-format | [Jeffallan](https://github.com/Jeffallan/claude-skills) | Høj | — |
| **mcp-builder** (installeret) | Guide til at bygge MCP-servere | [Anthropic officiel](https://github.com/anthropics/skills) | Høj | — |
| **firecrawl** (installeret) | Web scraping, research, crawling | Firecrawl | Høj | — |

---

## Store collections (vælg enkeltskills, ikke hele pakken)

| Collection | Antal | Kvalitet | Anbefaling |
|-----------|-------|----------|------------|
| **Superpowers (obra)** | ~14 skills | Høj, konsistent | Cherry-pick de relevante. Stærkest: writing-plans, code-review, TDD, parallel-agents |
| **Jeffallan/claude-skills** | 66 skills | Varierende | debugging-wizard, the-fool, spec-miner er allerede installeret. Resten er nichéer. |
| **VoltAgent/awesome-agent-skills** | 500+ | Varierende | Katalog, ikke pakke. Brug som opslagsliste. |
| **travisvn/awesome-claude-skills** | Kurateret liste | — | Meta-resource. Peger til andre repos. |

---

## Noter
- **Overlap-kolonne** viser om en skill duplikerer noget du allerede har. Overlap ≠ dårlig — men vær bevidst om det.
- **Kvalitet** er vurderet ud fra: antal filer, dokumentation, vedligeholdelse, og om den faktisk ændrer Claude's adfærd.
- Skills er markdown — du kan altid redigere dem til dit behov efter installation.
