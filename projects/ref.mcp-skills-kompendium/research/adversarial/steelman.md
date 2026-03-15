# Steelman — Forsvar af MCP/Skills-anbefalingen

## MCP-servere

### 1. Qdrant MCP — STÆRKESTE anbefaling
7 collections, ~84.000 vektorer. SSH-tunnel er workaround, ikke løsning. Hukommelsesarkitektur siger "vector DB er næste step." Qdrant MCP er det konkrete næste skridt.

### 2. Playwright MCP — produktionsrelevant
TransportIntra er live, ingen testframework, ingen CI/CD. Browser-automation = realistisk vej til QA for solo-developer.

### 3. Google Calendar MCP — operationel nødvendighed
To jobs med uforenelige skemaer. Briefen nævner eksplicit Google Calendar som uafklaret behov.

### 4. Context7 — eliminerer hallucinering
Selvlært udvikler = højere risiko for hallucineret API-syntaks. Sikkerhedsventil. Nul overhead hvis ubrugt.

### 5. Google Sheets MCP — bogføring er reelt behov
Rejseselskab kræver overblik. MCP eksisterer, gør jobbet, kræver ingen vedligeholdelse vs. custom integration.

## Skills

### writing-plans + executing-plans
Formaliserer PDCA-mønstret for Claude Code. Forstærkelse, ikke erstatning.

### requesting-code-review
Solo-developer uden peer review. Lavest-hængende frugt.

### dispatching-parallel-agents
Strukturerer ad hoc subagent-brug (allerede brugt i chatlog-engine, adversarial process).

### brainstorming
Konstruktiv modvægt til the-fool. Generativ vs. destruktiv tænkning.

### using-git-worktrees
11 backlog-briefs + parallelle sessions. Isoleret branch-arbejde.

### Trail of Bits audit
Produktion + root SSH + credentials.py = baseline due diligence.

### research-digest (custom)
160+ filer, ~30% duplikater. Ingen community-skill kender filstrukturen.

### session-state (custom)
PC har INGEN auto-save hooks (VPS har). Lukker det hul.

## Drop-liste forsvar
Filesystem, Git: redundante med Claude Code built-ins.
Postgres: uverificeret antagelse.
Fetch: redundant med Firecrawl + Playwright.
Time: bash.
Memory: Qdrant er overlegen med eksisterende data.
LangChain: maximal lock-in.

## Stærkeste version
- Qdrant + session-state = feedback loop (checkpoints til Qdrant)
- Playwright + Trail of Bits = security-aware QA pipeline
- Solnedgangsklausul per installation (Yttres egen metodik)
