# Claude Code Best Practices — Samlet Research Rapport

**Dato:** 2026-02-01
**Kilder:** Anthropic officiel docs, Shrivu Shankar (blog.sshh.io), YK/CS Dojo, rag-cli, awesome-claude-code, HumanLayer
**Format:** De anbefaler X → Vi gør Y → Anbefalet handling

---

## HOVEDKONKLUSION

Alle kilder peger på det samme: **context window er den vigtigste ressource.** Alt der fylder unødigt i CLAUDE.md, sessions eller komprimering koster kvalitet. Vores største problem er at CLAUDE.md er for lang (~189 linjer) med en voksende Session Log der ikke hjælper nye sessioner.

---

## 1. CLAUDE.md LÆNGDE OG INDHOLD

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | "Keep it concise. For each line, ask: Would removing this cause Claude to make mistakes? If not, cut it." |
| **Shrivu** | 13KB max for professionel monorepo. Start småt, dokumenter kun fejl Claude laver. |
| **HumanLayer** | Under 60 linjer ideelt. LLM'er kan følge ~150-200 instruktioner total, system prompt bruger allerede ~50. |
| **YK** | Start CLAUDE.md tomt. Tilføj kun entries når du gentager instruktioner. |

### Vi gør

188 linjer. Session Log fylder ~50 linjer og vokser for hver session. Indeholder historisk data der ikke forhindrer fejl.

### Anbefalet handling

1. **Flyt Session Log** ud af CLAUDE.md til `/docs/SESSION_LOG.md` — referer med én linje
2. **Fjern n8n-referencen** ("AFVIKLET") — Claude behøver ikke vide om afviklede systemer
3. **Fjern CHATLOG.md-referencen** — deprecated og unødig
4. **Mål:** Under 100 linjer

---

## 2. SESSION LOG vs. CHECKPOINT

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | Brug `/clear` + `--continue`/`--resume` mellem sessioner. Kontekst bør være frisk. |
| **Shrivu** | "Document & Clear" — dump fremskridt til .md, clear, start ny session der læser .md. |
| **YK** | "Handoff-dokumenter" — struktureret HANDOFF.md med: hvad er gjort, hvad fejlede, præcist næste skridt. |

### Vi gør

`NOW.md` checkpoint via hooks (SessionEnd, PreCompact). Automatisk genereret med seneste 20 beskeder + tasks. Session Log i CLAUDE.md som vokser permanent.

### Anbefalet handling

1. **Behold NOW.md** checkpoint — matcher "Document & Clear" mønsteret
2. **Flyt Session Log** ud — den er historik, ikke operationel kontekst
3. **Overvej struktureret HANDOFF.md** format i NOW.md: "Gjort / Fejlet / Næste skridt"

---

## 3. HOOKS vs. CLAUDE.md REGLER

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." |
| **Shrivu** | Undgå block-at-write hooks på Edit/Write. Tjek resultater ved commit-tidspunktet. |
| **Anthropic** | Claude kan skrive hooks for dig: "Write a hook that runs eslint after every file edit." |

### Vi gør

3 hooks: SessionStart (load checkpoint), SessionEnd (save checkpoint), PreCompact (save checkpoint). Dokumentationskrav i CLAUDE.md er advisory (kan ignoreres).

### Anbefalet handling

1. **Konverter kritiske CLAUDE.md-regler til hooks** — f.eks. infrastruktur-dokumentation
2. **Undgå write-level hooks** — Shrivu advarer eksplicit mod dette
3. **Behold nuværende hooks** — de matcher best practice perfekt

---

## 4. SKILLS ARKITEKTUR

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | Skills for "domain knowledge that is only relevant sometimes." Brug `disable-model-invocation: true` for workflow-skills. |
| **Shrivu** | Skills > MCP for de fleste use cases. Pitch "hvorfor og hvornår" i CLAUDE.md, ikke bare "hvad." |
| **HumanLayer** | `agent_docs/` mønster — separate filer Claude vælger efter behov. |

### Vi gør

5 skills (route-lookup, webapp-dev, youtube-pipeline, infrastructure, data-analysis). 4 af 5 er forældede (audit fandt dette).

### Anbefalet handling

1. **Opdater skills** til aktuel tilstand (allerede på huskelisten)
2. **Reducer til 3-4 skills** — færre at vedligeholde
3. **Tilføj YAML frontmatter** med `name:` og `description:` (Anthropic format)
4. **Overvej workflow-skills** med `disable-model-invocation: true` (f.eks. `/audit`, `/deploy-check`)

---

## 5. SLASH COMMANDS

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | `.claude/commands/` med markdown-filer. Støtter `$ARGUMENTS`, `$1`, `$2`. |
| **rag-cli** | Slash commands for RAG: `/search`, `/rag-enable`, `/rag-disable`. |
| **Shrivu** | "Long lists of complex custom commands signal broken tooling." Hold det minimalt. |

### Vi gør

Ingen slash commands overhovedet.

### Anbefalet handling

1. **Opret 2-3 simple commands** — ikke flere:
   - `/context` → kør `get_context.py` med argument
   - `/audit` → kør system-audit
2. **Undgå at overdesigne** — Shrivu advarer mod for mange
3. **Brug workflow-skills i stedet** for komplekse flows

---

## 6. SUBAGENTS

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | Custom subagents i `.claude/agents/`. Brug til code review, security audit. Writer/Reviewer mønster. |
| **Shrivu** | Undgå custom subagents. "CC can natively split up the context via its Task(...) tool." Fokuser på kontekst, ikke sub-agents. |

### Vi gør

Ingen custom subagents.

### Anbefalet handling

1. **Vent med custom subagents** — Shrivu (mest erfaren bruger) advarer mod det
2. **Brug den indbyggede Task tool** i stedet — den håndterer delegation automatisk
3. **Overvej kun** en `security-reviewer` agent når vi har git (til pre-commit review)

---

## 7. KONTEKST-HÅNDTERING

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | "Run /clear between unrelated tasks." Brug `/compact <instructions>` for kontrolleret komprimering. |
| **Shrivu** | Undgå `/compact` — "Avoid due to opacity and poor optimization." Brug `/clear` + `/catchup` i stedet. |
| **YK** | Kør `/context` midt i session for at overvåge token-forbrug. |

### Vi gør

Auto-compaction via system. Ingen komprimerings-instruktioner. Ingen `/clear` rutine.

### Anbefalet handling

1. **Tilføj compaction-instruktion** til CLAUDE.md: "When compacting, preserve: modified files list, current task, test commands"
2. **Brug `/clear`** aktivt mellem urelaterede opgaver
3. **Anthropic og Shrivu er uenige** om `/compact` — vores situation (lang-kørende sessions) favoriserer `/clear` over `/compact`

---

## 8. VERIFIKATION

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | "This is the single highest-leverage thing you can do." Inkluder tests, screenshots, expected outputs. |
| **YK** | "Double check everything and make a verification table." |
| **Shrivu** | Multi-layered programmatic verification. |

### Vi gør

Ingen verifikations-instruktioner i CLAUDE.md. Ingen test-suite. Manuel verifikation.

### Anbefalet handling

1. **Tilføj verifikations-standard** til CLAUDE.md: "Efter ændringer, kør relevant test eller demonstrer at det virker"
2. **Dette er den største manglende brik** ifølge Anthropic

---

## 9. RAG / SØGNING

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **rag-cli** | Hybrid search: 70% semantisk + 30% keyword. Cross-encoder reranking. Auto-enhancement for alle queries. |
| **Shrivu** | "Context indirection" — agenter handler på kontekst via scripting UDEN at loade massive filer. |
| **HumanLayer** | Prefer pointers to copies. Progressive disclosure. |

### Vi gør

Ren semantisk søgning via Qdrant. Manuel `get_context.py` kald. `/docs/` ikke embeddet i Qdrant.

### Anbefalet handling

1. **Embed `/docs/` i Qdrant** (allerede på huskelisten) — sparer tokens
2. **Tilføj keyword-komponent** til søgning (hybrid search)
3. **Overvej auto-enhancement** via hook — kald get_context.py automatisk ved relevante spørgsmål

---

## 10. BASH WRAPPER PATTERN

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Shrivu** | "If your CLI commands are complex and verbose, write a simple bash wrapper with a clear, intuitive API and document that." |
| **Anthropic** | Dokumenter custom tools med usage examples. |

### Vi gør

Langt bash-kald i CLAUDE.md: `source /root/Ydrasil/scripts/venv/bin/activate && python3 /root/Ydrasil/scripts/get_context.py "SPØRGSMÅLET HER" --limit 5`

### Anbefalet handling

1. **Lav bash wrapper** — f.eks. `ctx "spørgsmål"` i stedet for den lange kommando
2. **Dokumenter kun wrapperen** i CLAUDE.md

---

## 11. SIKKERHED

### De anbefaler

| Kilde | Anbefaling |
|-------|-----------|
| **Anthropic** | "Do not include sensitive information, API keys, credentials in CLAUDE.md." |
| **Shrivu (kommentarer)** | Prompt injection via usynlig tekst i skills er en reel trussel. |
| **Anthropic** | Brug sandboxing (`/sandbox`) for isolation. |

### Vi gør

Credentials i separat CREDENTIALS.md (ikke i CLAUDE.md). Token-reference i CLAUDE.md ("Token i CREDENTIALS.md"). Ingen sandboxing.

### Anbefalet handling

1. **Fjern credentials-reference** fra CLAUDE.md ("Token i CREDENTIALS.md" → unødigt)
2. **Vær opmærksom på skill injection** når vi opdaterer skills
3. **Git + .gitignore** for credentials (når git er sat op)

---

## 12. FEJLMØNSTRE AT UNDGÅ

Alle kilder nævner disse:

| Fejlmønster | Kilde | Relevant for os? |
|-------------|-------|-----------------|
| Overfyldt CLAUDE.md | Alle | **Ja** — Session Log vokser |
| Kitchen sink session | Anthropic | **Ja** — vi blander ofte opgaver |
| Gentagne korrektioner uden /clear | Anthropic | Muligvis |
| For mange slash commands | Shrivu | Nej (vi har ingen) |
| Custom subagents der "gatekeep" kontekst | Shrivu | Nej (vi har ingen) |
| Ikke at komprimere proaktivt | YK | **Ja** — ingen compaction-strategi |
| Task-specifik guidance i CLAUDE.md | HumanLayer | **Ja** — noget niche-indhold |

---

## PRIORITERET HANDLINGSLISTE

### Gør nu (højeste effekt, laveste indsats)

| # | Handling | Kilde | Effekt |
|---|---------|-------|--------|
| 1 | Flyt Session Log ud af CLAUDE.md | Alle | Reducerer CLAUDE.md med ~50 linjer |
| 2 | Fjern n8n + CHATLOG + credentials-referencer | Anthropic | Reducerer støj |
| 3 | Tilføj compaction-instruktion | Anthropic/Shrivu | Bevarer kritisk kontekst ved auto-compact |
| 4 | Lav bash wrapper til get_context.py | Shrivu | Simplificerer CLAUDE.md |
| 5 | Tilføj verifikations-standard | Anthropic | "Single highest-leverage thing" |

### Gør snart (medium effekt)

| # | Handling | Kilde |
|---|---------|-------|
| 6 | Opret 2-3 slash commands | Anthropic/rag-cli |
| 7 | Tilføj YAML frontmatter til skills | Anthropic |
| 8 | Embed /docs/ i Qdrant | rag-cli/Shrivu |
| 9 | Tilføj hybrid search til get_context.py | rag-cli |

### Kan vente (lavere prioritet)

| # | Handling | Kilde |
|---|---------|-------|
| 10 | Custom subagents (.claude/agents/) | Anthropic |
| 11 | Background indexing med watchdog | rag-cli |
| 12 | Status line i tmux | YK |
| 13 | Container isolation til eksperimenter | YK |

---

## UENIGHEDER MELLEM KILDER

| Emne | Anthropic | Shrivu | Vurdering |
|------|-----------|--------|-----------|
| `/compact` | Anbefaler det | Fraråder det | Brug `/clear` som default, `/compact` kun med instruktioner |
| Custom subagents | Anbefaler `.claude/agents/` | Fraråder det — brug Task tool | Vent med subagents, brug Task tool |
| Slash commands | Anbefaler `.claude/commands/` | "Signal broken tooling" hvis for mange | Lav 2-3 simple, ikke flere |
| Skills vs. agent_docs | Skills med frontmatter | Skills som formaliseret scripting | Begge tilgange virker, vores skills er fine |

---

## YDRASIL-SPECIFIKKE INDSIGTER

### Ting vi gør bedre end anbefalingerne

1. **Automatisk session logging** (tmux → Qdrant) — mere avanceret end "Document & Clear"
2. **Checkpoint hooks** (NOW.md) — automatiseret version af handoff-dokumenter
3. **CostGuardian pattern** — proaktiv omkostningsstyring, ikke nævnt i nogen kilde
4. **Huskeliste scanner** — regelbaseret monitoring uden AI-kald ($0)

### Ting vi gør dårligere

1. **CLAUDE.md er for lang** — Session Log, deprecated referencer, niche-indhold
2. **Ingen verifikation** — den vigtigste enkeltstående mangel
3. **Ingen git** — alle kilder antager git som fundament
4. **Ingen hybrid search** — ren semantisk søgning misser keyword-matches
5. **Ingen slash commands** — simpel forbedring vi ikke har udnyttet
6. **/docs/ ikke i Qdrant** — koster 57K tokens per søgning i stedet for ~500

---

## KILDER

- [Anthropic: Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Anthropic: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Shrivu Shankar: How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Shrivu Shankar: Building Multi-Agent Systems (Part 1-3)](https://blog.sshh.io/p/building-multi-agent-systems)
- [Shrivu Shankar: AI Can't Read Your Docs](https://blog.sshh.io/p/ai-cant-read-your-docs)
- [YK/CS Dojo: 32 Tips for Claude Code](https://www.youtube.com/watch?v=...)
- [rag-cli: RAG Pipeline for Claude Code](https://github.com/m-c-frank/rag-cli)
- [awesome-claude-code: 180+ Resources](https://github.com/...)
- [HumanLayer: Under 60 Lines Guide](https://humanlayer.dev/blog/...)
