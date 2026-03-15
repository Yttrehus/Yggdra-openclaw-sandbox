# Anthropic & Claude — Samlet Overblik, februar 2026

## 1. Claude i Excel / Regneark

Claude er nu tilgaengelig direkte i Microsoft Excel som en add-in. Efter en tre-maaneders beta (kun Max og Enterprise) blev den **24. januar 2026 aabnet for Pro-abonnenter**.

Noeglefunktioner:
- Laeser komplekse multi-tab workbooks med celle-niveau citationer
- Debugger formler (#REF!, #VALUE!, cirkulaere referencer)
- Opretter pivottabeller og diagrammer
- Uploader filer og understotter .xlsx og .xlsm
- 6 nye finansielle skills: DCF-modeller, sammenlignelige selskaber, due diligence, earnings-analyser m.fl.
- Drives af Sonnet 4.5, med auto-komprimering af lange sessioner
- Overwrite-beskyttelse og et "Claude Log"-ark til sporbarhed

Kilder:
- [Anthropic: Claude for Excel](https://www.therundown.ai/p/claude-for-excel-opens-the-gates)
- [Claude Help Center: Excel](https://support.claude.com/en/articles/12650343-claude-in-excel)
- [TechRadar: Claude i Excel](https://www.techradar.com/pro/claude-is-coming-to-your-spreadsheets-but-is-it-enough-to-make-you-an-emperor-of-excel-and-what-will-microsoft-copilot-think)
- [Anthropic: Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services)

---

## 2. Modelopdateringer

### Claude Opus 4.5 (november 2025)
- Anthropics mest intelligente model. 50-75% faerre tool-calling- og build/lint-fejl.
- Eneste model med "effort"-parameter (lav/medium/hoej token-forbrug).
- Paa medium er den paa niveau med Sonnet 4.5 paa SWE-bench men bruger 76% faerre tokens.
- Pris: **$5 / $25 pr. million tokens** (input/output).

### Claude Sonnet 4.5 (januar 2026)
- "Verdens bedste coding-model" ifoelge Anthropic. Foerer OSWorld (61.4%).
- Kan koere autonomt i op til **30 timer** paa komplekse opgaver.
- 200k og 1M (beta) token kontekstvindue.
- Pris: **$3 / $15 pr. million tokens** (uaendret fra Sonnet 4).

### Claude Haiku 4.5
- Matcher Sonnet 4 paa coding, computer use og agent-opgaver.
- Pris: **$1 / $5 pr. million tokens**.

### Udgaaede modeller
- Opus 4 og 4.1 er fjernet fra baade Claude og Claude Code.

Kilder:
- [Anthropic: Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- [Anthropic: Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5)
- [The New Stack: Opus 4.5](https://thenewstack.io/anthropics-new-claude-opus-4-5-reclaims-the-coding-crown-from-gemini-3/)
- [Claude API Docs: Models](https://platform.claude.com/docs/en/about-claude/models/overview)

---

## 3. Claude Code (CLI-vaerktoej)

### Version 2.1.0 (8. januar 2026) — 1.096 commits
- **Shift+Enter** for linjeskift uden setup
- **Skills**: hot reload, forked context, custom agents, invoker med `/`
- **Hooks** direkte i agents og skills frontmatter
- **Wildcard tool permissions**: f.eks. `Bash(*-h*)`
- **`/teleport`**: flytte sessionen til claude.ai/code
- **Sprogkonfiguration**: svar paa brugerens sprog
- **LSP-vaerktoej**: go-to-definition, find references, hover docs
- **Checkpoints**: gem fremskridt, rul tilbage til tidligere tilstand
- **VS Code extension** (native)
- **Claude Code Analytics API**: organisations-niveau metrics
- Rettelse af en **kommando-injektionssaarbarhed** og en **hukommelseslaekage** i tree-sitter

Kilder:
- [GitHub: Claude Code Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [VentureBeat: Claude Code 2.1.0](https://venturebeat.com/orchestration/claude-code-2-1-0-arrives-with-smoother-workflows-and-smarter-agents)
- [Releasebot: Claude Code](https://releasebot.io/updates/anthropic/claude-code)

---

## 4. Anthropic Selskabsnyheder

### Finansiering
- **$10-15 mia. funding-runde** lukket til en **$350 mia. vaerdi** (ca. fordoblet paa 4 maaneder).
- Ledende investorer: **Coatue** og **GIC** (Singapores suveraene fond), hver $1,5 mia.
- **Sequoia Capital** ogsaa med stor investering.
- Microsoft og Nvidia annoncerede i november: MS op til $5 mia., Nvidia op til $10 mia.

### Oekonomi
- **~$10 mia. i omsaetning i 2025** (op fra ~$1 mia. i starten af 2025).
- Claude Code alene genererer **>$500 mio. run-rate revenue**.

### Infrastruktur
- **$50 mia.** planlagt til datacentre i Texas og New York (med FluidStack).
- Primaer bruger af Amazon-datacenter i Indiana (2,2 GW).

### IPO
- Har hyret Wilson Sonsini til at forberede boersnotering — forventet **2026-2027**.

### Partnerships
- **Allianz**: Claude Code til alle medarbejdere + custom AI-agenter.
- **US Department of Energy**: videnskabelig forskning.
- **Salesforce**: Agentforce 360-integration forventet midt-2026.
- Nyt kontor i **Bengaluru, Indien** (aabner 2026).

Kilder:
- [CNBC: Anthropic funding](https://www.cnbc.com/2026/01/27/anthropic-fundraising-microsoft-nvidia.html)
- [CNBC: Term sheet](https://www.cnbc.com/2026/01/07/anthropic-funding-term-sheet-valuation.html)
- [TechCrunch: Allianz](https://techcrunch.com/2026/01/09/anthropic-adds-allianz-to-growing-list-of-enterprise-wins/)
- [Bloomberg: Sequoia](https://www.bloomberg.com/news/articles/2026-01-18/sequoia-to-join-funding-round-for-ai-startup-anthropic-ft-says)

---

## 5. Nye API-funktioner

- **Code Execution Tool**: Claude koerer Python i sandbox. 50 gratis timer/dag, derefter $0,05/time.
- **MCP Connector**: forbind til enhver remote MCP-server uden klientkode.
- **Files API**: filer paa tvaers af sessioner.
- **Programmatic Tool Calling**: Claude skriver kode der kalder flere tools paa een gang.
- **Tool Search Tool**: adgang til tusindvis af tools uden at forbruge kontekstvindue.
- **Agent Skills (beta)**: praebyggede skills til PowerPoint, Excel, Word, PDF.
- **Structured Outputs**: JSON og strict tool use til Sonnet 4.5 og Opus 4.1+.
- **Prompt caching**: op til 1 times cache.
- **Platform-rebrand**: console.anthropic.com er nu **platform.claude.com**.

Kilder:
- [Anthropic: Agent Capabilities API](https://www.anthropic.com/news/agent-capabilities-api)
- [Anthropic: Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Releasebot: Anthropic](https://releasebot.io/updates/anthropic)

---

## 6. Computer Use & Cowork

### Claude Cowork (12. januar 2026)
- Claude Code-kapaciteter i en **visuel desktop-app** til ikke-udviklere.
- Koerer i en isoleret VM (Apple Virtualization Framework paa Mac).
- Giv Claude adgang til en mappe — den laeser, redigerer og opretter filer.
- Koerer med Opus 4.5 som standard.
- **Plugins**: Produktivitet, Enterprise-soegning, Salg, Finans.
- **Browser-integration** via Claude i Chrome.
- Tilgaengelig for **Pro-abonnenter ($20/md)** fra 16. januar.
- Bygget af teamet paa ca. **halvanden uge** — primaert med Claude Code selv.
- Windows-support og cross-device sync paa vej.

### Agent-kapaciteter generelt
- Sonnet 4.5: op til 30 timers autonom koersel.
- Sub-agents: "Manager Claude" kan spawne specialiserede mini-agenter.
- Langtidshukommelse paa tvaers af sessioner.

Kilder:
- [TechCrunch: Cowork](https://techcrunch.com/2026/01/12/anthropics-new-cowork-tool-offers-claude-code-without-the-code/)
- [Simon Willison: Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/)
- [VentureBeat: Cowork](https://venturebeat.com/technology/anthropic-launches-cowork-a-claude-desktop-agent-that-works-in-your-files-no)
- [Claude blog: Cowork](https://claude.com/blog/cowork-research-preview)

---

## 7. MCP (Model Context Protocol)

- MCP er nu **industristandard** — adopteret af OpenAI, Google DeepMind, Microsoft.
- **10.000+ offentlige MCP-servere**, 97 mio. maanedlige SDK-downloads.
- **Doneret til Linux Foundation** (december 2025) under "Agentic AI Foundation" — medstiftet af Anthropic, Block og OpenAI.
- **MCP Apps** (januar 2026): foerste officielle extension — tools kan returnere interaktive UI-komponenter (dashboards, formularer, visualiseringer) direkte i samtalen.
- Understottet i ChatGPT, Claude, Goose og VS Code.

Kilder:
- [Anthropic: MCP donation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [MCP Blog: MCP Apps](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
- [The New Stack: Why MCP Won](https://thenewstack.io/why-the-model-context-protocol-won/)
- [Pento: A Year of MCP](https://www.pento.ai/blog/a-year-of-mcp-2025-review)

---

## 8. Priser (opdateret)

| Model | Input | Output |
|-------|-------|--------|
| Haiku 4.5 | $1/M tokens | $5/M tokens |
| Sonnet 4.5 | $3/M tokens | $15/M tokens |
| Opus 4.5 | $5/M tokens | $25/M tokens |

Consumer-planer: Pro ($20/md), Max, Team, Enterprise. Cowork og Excel er nu tilgaengelige for Pro.

---

## 9. Konkurrencesituation

- **Anthropic**: Foerer prediction markets for bedste coding-model (41% konfidens vs. OpenAI 33%, Google 14%).
- **OpenAI**: Lancerede GPT-5.1 og derefter GPT-5.2 i december. Annoncerede **reklamer i ChatGPT**.
- **Google**: Gemini 3.0 med staerkeste kontekstvindue og multimodal forstaelse. Deep Think foerer Humanity's Last Exam (41%).
- Opus 4.5 topper SWE-bench Verified (80,9%), GPT-5.2 taet paa (80,0%).
- Alle tre traener paa Google TPU'er — Google profiterer uanset hvem der "vinder".
- 2026 handler mindre om benchmarks og mere om **distribution, monetisering og omkostningseffektivitet**.

Kilder:
- [Axios: AI Race](https://www.axios.com/2026/01/17/chatgpt-ads-claude-gemini-ai-race)
- [RD World: GPT-5.2 vs Gemini 3.0 vs Opus 4.5](https://www.rdworldonline.com/how-gpt-5-2-stacks-up-against-gemini-3-0-and-claude-opus-4-5/)
- [Livewire: Google vs Anthropic vs OpenAI](https://www.livewiremarkets.com/wires/2026-the-year-google-will-defeat-anthropic-and-openai)

---

## 10. Relevans for Ydrasil

1. **Claude Code 2.1** med skills, hot reload og LSP er direkte relevant for dagligt arbejde.
2. **MCP Apps** kan potentielt give interaktive UI-komponenter i Qdrant-integrationer.
3. **Opus 4.5 effort-parameter** kan spare tokens/penge paa rutine-opgaver.
4. **Claude i Excel** kan vaere nyttigt til rutedata-analyse og oekonomisk rapportering.
5. **Cowork** er interessant til fil-arbejde uden terminal.
