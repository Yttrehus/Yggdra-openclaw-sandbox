# Red Team — Angreb på MCP/Skills-anbefalingen

## 1. Svagheder i hver anbefaling

### Qdrant MCP — ALVORLIG SVAGHED
MCP kræver stadig netværksadgang til VPS port 6333. Tre scenarier, alle dårlige:
- Åben port 6333: Qdrant har ingen auth by default. Enhver med IP'en kan læse/skrive.
- MCP starter tunnel: Nu er MCP-serveren en SSH-manager forklædt som database-klient.
- MCP på VPS, Claude Code lokalt: Remote MCP kræver SSE-transport (eksperimentel) eller lokal proxy.

Det nuværende system (SSH-alias, ctx-wrapper) er simplere end alle tre scenarier.

### Playwright MCP — SVAG BEGRUNDELSE
TransportIntra QA er nævnt som use case, men hvor tit testes der realistisk? Tungt dependency (~200MB+ Chromium-binaries) for sporadisk brug.

### Google Calendar MCP — OVERVURDERET
Rejseselskabet har sæsonvariation, ikke daglige konflikter. Calendar-integration i en coding-session er kontekst-switch, ikke workflow-forbedring.

### Context7 — POTENTIEL FÆLDE
Yttre bruger Python + bash + vanilla JS. Simpel stack. Hvornår halluciner Claude om `subprocess.run()`? Context7 løser et problem for framework-tunge stacks.

### Google Sheets MCP — FORKERT TIMING
At tilføje Sheets MCP før bogførings-projektet er designet er at starte med værktøjet i stedet for problemet.

### writing-plans + executing-plans — REDUNDANS
PDCA + CONTEXT.md + solnedgangsklausul + "spørg før du bygger" er allerede et planlægningssystem. To parallelle systemer.

### TDD — UREALISTISK
Størstedelen af kodebasen er bash-scripts og procedurel automation. RED-GREEN-REFACTOR misfit.

### brainstorming — OVERFLØDIGT
Tilføjer en skill for at balancere en anden skill. Overhead, ikke value.

### git-worktrees — PREMATUR
Ét repo, én person, lineært arbejde. Mental overhead > gevinst.

### research-digest — SYMPTOM, IKKE ÅRSAG
Deduplikering løser ikke strukturproblemet. Kør oprydning manuelt én gang.

### session-state — OVERLAP
CONTEXT.md har allerede "Åbne tråde"-sektion. Hvad tilføjer denne skill?

## 2. Bias i analysen
- **Toolbox mentality:** Flere tools ≠ bedre workflow. Aldrig spurgt: "Hvad hvis nul installeres?"
- **Selection bias:** MCP valgt fordi de "passer", ikke fordi de er efterspurgt.
- **Survivorship bias:** Community-skills er uvetted GitHub-repos.
- **Bekvemmeligheds-bias:** Drop-listen aldrig testet (f.eks. Sequential Thinking).

## 3. Prioriterings-angreb
18 deliverables for én solo-developer. Realistisk completion rate ~30%. Korrekt: context-engineering hooks → ÉN MCP → ÉN skill → evaluér.

## 4. Mangler
- Ingen vedligeholdelsesplan
- Ingen test-kriterier (solnedgangsklausuler!)
- Ingen token-budget-analyse
- Ingen rollback-plan
- VPS-sikkerhed ikke adresseret

## 5. Princip-alignment
- "Bash-first" modsiger 5 MCP-servere (Node.js/Python sidecar-processer)
- "Ingen overkill" modsiger 18 deliverables
- "Minimal lock-in" modsiger MCP (Claude/Anthropic-specifikt)

## 6. Samlet dom
Tre ting overlever: context-engineering hooks, code-review skill, Qdrant MCP (KUN hvis tunneling er løst).
