# Armin Ronacher — Agent-filosofi og praktisk setup
**Forskeren, 2026-03-06**
Kilder: lucumr.pocoo.org, GitHub (mitsuhiko/badlogic), Syntax podcast ep. 976, The Pragmatic Engineer podcast

---

## Hvem er Armin Ronacher

- Skaber af Flask, Jinja2, Click, Werkzeug — Pythons infra-lag
- Medgrundlægger og CTO af Sentry (forlod 2025)
- Grundlagde Earendil (2026) — nyt startup, AI-fokus
- GitHub: mitsuhiko | Blog: lucumr.pocoo.org | Bluesky: mitsuhiko.at
- Resident i Wien, Østrig

---

## 1. PI — Det minimale agent-fundament (jan. 31, 2026)

**Post:** https://lucumr.pocoo.org/2026/1/31/pi/

Pi er skrevet af Mario Zechner (badlogic). Ronacher bruger det som sit primære coding agent-interface.

### Arkitektur

Kernen er bevidst minimal: **4 tools — Read, Write, Edit, Bash.** Intet mere i grundkernen.

Sessioner er træstrukturer, ikke lineære samtaler. Man kan forgrene en session ("branch into fresh review context"), løse et delproblem, og bringe resultatet tilbage til main-sessionen. Dette er Pi's svar på context-management.

Custom messages i sessionsfilerne gemmer state for extensions — ikke alt sendes til LLM'en. Dette er den centrale memory-mekanisme: state er filer på disk, ikke model-hukommelse.

### Selvmodifikation — kerneprincipper

"If you want the agent to do something it doesn't do yet, you don't go and download an extension. You ask the agent to extend itself."

Hot-reloading: agenten skriver kode, reloader, tester — i loop — indtil extensionen virker.

Ronacher's egne extensions:
- `/answer` — ekstraherer og reformatterer agent-spørgsmål
- `/todos` — markdown-baseret task-liste (stateful)
- `/review` — forgrener session til code review
- `/control` — multi-agent kommunikation uden kompleks orkestrering
- `/files` — viser ændrede/refererede filer på tværs af sessioner

### MCP-fravalg (bevidst)

"This is not a lazy omission. This is from the philosophy of how Pi works."

Pi har ingen MCP-support. Filosofien: i stedet for at downloade et MCP-plugin beder du agenten skrive et CLI-script. Det er billigere, mere forudsigeligt og agenten forstår det bedre.

### Provider-agnostisk design

Pi's SDK "doesn't lean in too much into any model-provider-specific feature set that cannot be transferred to another." Sessions kan flyttes mellem providers. Ronacher startede MiniJinja-Go-port med Claude Opus 4.5, skiftede til GPT-5.2 Codex til test-fixing.

---

## 2. MOM — Master Of Mischief (Slack-bot)

**GitHub:** https://github.com/badlogic/pi-mono/tree/main/packages/mom

MOM er bygget af Mario Zechner oven på Pi. Ronacher nævner den som eksempel på hvad Pi-SDK'en muliggør. MOM er Ronacher-miljøets version af "personlig assistent som Slack-bot."

### Arkitektur

Pr. Slack-kanal:
- `log.jsonl` — komplet beskedhistorik (ground truth)
- `context.jsonl` — hvad LLM'en faktisk ser (synkroniseres fra log)
- `MEMORY.md` — kanalspecifik kontekst der bevares på tværs af sessioner

Execution: Docker container (isoleret) eller direkte på host. Mounter kun en `/data`-mappe.

Workflow når du nævner MOM i Slack:
1. Nye beskeder synkroniseres fra `log.jsonl` til `context.jsonl`
2. MEMORY.md-filer loades
3. MOM svarer med tilgængelige tools
4. Tool-output til thread (holder kanalen ren), svar til kanal

### Selvforvaltende

MOM installerer sine egne dependencies (kører `apk add git` hvis den mangler det), skriver egne CLI-wrappers til API'er, og opretter skills-filer (SKILL.md) som den bruger fremover. Den konfigurerer sine egne credentials.

### Analog til vores setup

MOM er PI's svar på det Kris kalder "Ydrasil" — en agent med persistent memory, Telegram-integration, og selvudvidende skills-system. Vores MEMORY.md-system er identisk med MOM's MEMORY.md pr. kanal. Vores Ydrasil-arkitektur er parallelt til MOM.

---

## 3. MCP-kritik og sikkerhed

**Post:** https://lucumr.pocoo.org/2025/11/21/agents-are-hard/
**Talk:** "Ubertool MCPs" (Claude Code Anonymous London, aug. 2025)

### Hans MCP-position

"I barely use MCP because Claude Code is very capable of just running regular tools."

Han bruger kun Playwright MCP. Alt andet løser han med scripts/Makefile-kommandoer og beder agenten bruge dem.

Kritik: MCP-servere er "overengineered" og "include large toolsets that consume lots of context." De er ekstra fejlkilder.

Alternativet: Skriv et shell-script. Agenten kan køre det via Bash. Ingen ekstra lag, ingen ekstra state.

### Sikkerhed og prompt injection

Ronacher er ikke den der har skrevet mest om dette direkte, men hans arkitekturvalg reflekterer sikkerhedsfilosofien:

- Minimal tool-surface reducerer angrebsflade
- CLI-scripts frem for MCP reducerer protokolkompleksitet
- Docker-isolering for agenter med ekstern adgang (MOM)
- Agenter bør ikke have adgang til både private data OG ekstern kommunikation OG mulighed for at eksekvere uden review

"Lethal trifecta" (Simon Willison, som Ronacher er enig i): private data + untrusted content + external communication = prompt injection risiko.

---

## 4. Agent-design filosofi

**Post:** https://lucumr.pocoo.org/2025/11/21/agents-are-hard/

### SDK-valg

Brug IKKE Vercel AI SDK eller andre abstraktionslag til agents. Gå direkte mod OpenAI/Anthropic SDK. Årsag: "the differences between models are significant enough that you will need to build your own agent abstraction."

Vercel AI SDK ødelægger message history ved brug af Anthropic's web search tool. Det er uacceptabelt.

### Caching

Foretrækker Anthropic's **manuelle cache-points** frem for automatisk caching. Placering: efter system prompt + ved session-start. Dynamisk information injiceres EFTER cache-points for at bevare cache-effektivitet.

Fordele ved manuel caching:
- Forudsigelig pris
- Mulighed for at splitte samtalen i to retninger simultaneously
- Mulighed for context-editing

### Model-præferencer (til agent-loops)

- **Haiku + Sonnet**: bedste tool-callers til loops — slår GPT-familien
- **Gemini 2.5**: bedst til dokumentopsummering og PDF/billede-udtræk (undgår Sonnet's safety-filters)
- GPT-modeller: ikke stærke i tool-calling loops

### Fejl-isolation

To kritiske mønstre:
1. Sub-agent execution — kør iterative tasks i separat agent, rapportér kun summary
2. Context editing — fjern uproduktive fejl-detaljer fra kontekst, men bevar hvad der *ikke* virker

### Reinforcement

Agenten har brug for feedback-loops — ikke bare "her er opgaven, kør." Værktøjer der ekkoer state tilbage (todo-lister der bekræfter hvad der er gjort) øger pålidelighed markant.

### Evals

"The hardest problem." Traditionelle eksterne eval-systemer virker ikke til agents. Man skal instrumentere de faktiske test-runs. Ingen god løsning endnu.

---

## 5. "Agent Psychosis" (jan. 18, 2026)

**Post:** https://lucumr.pocoo.org/2026/1/18/agent-psychosis/

Ronacher er ikke anti-AI. Men han identificerer et mønster i builder-community: ukritisk accept af AI-output, "forcing the AI down a path without any real critical thinking."

Kerneproblem: "It takes you a minute of prompting...but actually honestly reviewing a pull request takes many times longer." = Review er bottlenecks, ikke generation.

Token-forbrug: ustrukturerede agent-loops er massivt spildsomme vs. velforberedte sessioner. Nuværende priser er muligvis subsidiererede.

Hans position: "AI agents are amazing...They are also massive slop machines if you turn off your brain."

---

## 6. "The Final Bottleneck" (feb. 13, 2026)

**Post:** https://lucumr.pocoo.org/2026/2/13/the-final-bottleneck/

Historisk: "Writing code was slower than reviewing code." Nu er det omvendt.

Ny bottleneck: human review + accountability. Maskiner kan ikke holdes ansvarlige. Så længe software skal have en ansvarlig person bag sig, er review og godkendelse irreduktibel.

Starbucks-analogien: 2500+ PRs i limbo i OpenClaw. Engineers mister overblik over egne codebases. PRs bliver forældede inden merge.

Hans konklusion: VI ved ikke endnu hvordan society vil håndtere dette. Det kræver nye accountability-mekanismer vi ikke har designet.

---

## 7. Hukommelsessystemer — hans syn

Fra Pi-arkitekturen og MOM:

**"Agent memory isn't model learning. It's state ownership + rehydration."**

Konkret: memory er plain Markdown på disk. Filer er ground truth. Modellen "husker" kun hvad der skrives til disk og loades i kontekst.

OpenClaw's tilgang (som Pi inspirerer):
- Temporal decay: nyere info scorer højere (stale memories shouldn't dominate)
- MMR re-ranking: undgå at returnere 5 næsten-duplikater
- Sessioner som træer: forgren, løs, bring tilbage

Hans fravalg af automatisk memory (Mem0, LightRAG osv.):
Ikke eksplicit nævnt af Ronacher, men Pi's arkitektur siger det implicit: simple fil-baserede systemer frem for komplekse vector-memory-abstraktioner.

---

## 8. Anthropic vs. OpenAI — model lock-in

Ronacher er bevidst provider-agnostisk i Pi's design. Sessions bærer ikke provider-specifik state.

Præferencer (funktionelt):
- Anthropic/Claude: bedst til tool-calling loops, caching-API er overlegen
- GPT: god til mobile (ChatGPT voice mode), Codex til test-fixing
- Gemini: dokumenter, PDF, billeder

Kritik af Vercel AI SDK: abstraherer for meget, ødelægger provider-specifikke features. Gå direkte til SDK.

Konklusion: Ronacher vælger model ud fra opgave, ikke loyalitet. Bygger abstraktioner der tillader skift.

---

## 9. MiniJinja → Go port (jan. 14, 2026)

**Post:** https://lucumr.pocoo.org/2026/1/14/minijinja-go-port/

Praktisk demonstration af Pi's kapabiliteter:
- 10 timers session (3 timers supervision + 7 timer uovervåget natten)
- ~45 minutters aktiv human-tid
- $60 i API-tokens, 2.2M tokens totalt
- Claude Opus 4.5 til start, GPT-5.2 Codex til long-tail test-fixing
- Al prompting via voice gennem Pi

Tilgangen: test-driven porting. Agenten genbrugte eksisterende Rust-snapshot-tests som validation. Agenten afveg fra literal port til "behavioral port" (tree-walking interpreter, Go's reflection) — Ronacher tillod det fordi adfærden matchede.

---

## 10. Talks og podcasts

| Format | Titel | Dato |
|--------|-------|------|
| Podcast | Syntax ep. 976: "Pi — The AI Harness That Powers OpenClaw" | 2026 |
| Podcast | The Pragmatic Engineer: "Python, Go, Rust, TypeScript and AI" | okt. 2025 |
| Talk | "Ubertool MCPs" — Claude Code Anonymous London | aug. 2025 |
| Talk | "Agentic Coding: The Future of Software Development with Agents" | jun. 2025 |
| Talk | "How to vibe code to a billion dollars" — Tech Soirée Vienna | aug. 2025 |
| Talk | "The Machine and Me" — CASE Conference Berlin | jan. 2026 |
| Talk | "Do Dumb Things" — PyCon Austria | apr. 2025 |

Syntax ep. 976 er den mest relevante — gennemgang af Pi's arkitektur, Bash-is-all-you-need, risici ved agents.

---

## 11. Relevans for Ydrasil-setup

### Direkte overførbare principper

1. **4-tool kerne**: Vi har Bash, Read, Write, Edit i Claude Code. Det er nok. Tilføj scripts frem for MCP.
2. **MEMORY.md pr. agent**: MOM's MEMORY.md-pr-kanal er præcis hvad vi har bygget. Vi er på rette spor.
3. **Sessioner som træer**: Pi's branching svarer til vores worktree-setup for Byggeren.
4. **Selvudvidende skills**: Agents der skriver egne CLI-tools frem for at downloade plugins — vores `.claude/skills/` mappe er analog.
5. **Filer som ground truth**: State gemmes i filer (MEMORY.md, episodes.jsonl), ikke i model-hukommelse.
6. **Sub-agent isolation**: Fejl i sub-agents påvirker ikke main context. Vi gør dette allerede.
7. **Temporal decay**: Nyere viden bør vægtes højere i Qdrant-søgning.

### Hvad vi mangler

- **Session-træer/branching**: Pi kan forgrene og merge. Vi kan ikke det endnu.
- **Hot-reload af skills**: Pi kan skrive en extension og teste den live. Vi har ikke dette.
- **Voice-til-agent**: Ronacher prompter udelukkende via voice til Pi. Vi har voice-pipeline men bruger den ikke til agent-prompting.

### Fravalg bekræftet

Ronacher's fravalg af MCP (undtagen Playwright) + fravalg af Mem0/LightRAG-lignende systemer bekræfter vores linje: simple fil-baserede løsninger frem for komplekse abstraktioner.

---

## Nøglecitater

"If you want the agent to do something it doesn't do yet, you don't go and download an extension. You ask the agent to extend itself."

"Software that is malleable like clay."

"Machines cannot be accountable. Humans remain responsible for shipped code."

"AI agents are amazing...They are also massive slop machines if you turn off your brain."

"Agent memory isn't model learning. It's state ownership + rehydration."

"The differences between models are significant enough that you will need to build your own agent abstraction."

---

## Primære kilder

- https://lucumr.pocoo.org/2026/1/31/pi/
- https://lucumr.pocoo.org/2025/11/21/agents-are-hard/
- https://lucumr.pocoo.org/2026/1/18/agent-psychosis/
- https://lucumr.pocoo.org/2026/2/13/the-final-bottleneck/
- https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/
- https://lucumr.pocoo.org/2026/3/5/theseus/
- https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/
- https://lucumr.pocoo.org/2025/6/4/changes/
- https://lucumr.pocoo.org/2025/1/30/how-i-ai/
- https://lucumr.pocoo.org/2026/1/14/minijinja-go-port/
- https://github.com/badlogic/pi-mono/tree/main/packages/mom
- https://www.listennotes.com/podcasts/syntax-tasty-web/976-pi-the-ai-harness-that-hi4-HCR0QnK/
