# Mario Zechner (badlogic) — Deep Research Report
**Dato:** 2026-03-06
**Udført af:** Forskeren (Ydrasil)
**Fokus:** PI coding agent, AI-filosofi, tekniske indsigter relevante for personligt AI-setup

---

## 1. Primære kilder

- Blog: https://mariozechner.at
- GitHub: https://github.com/badlogic / https://github.com/badlogic/pi-mono / https://github.com/badlogic/pi-skills
- PI hjemmeside: https://shittycodingagent.ai
- Twitter/X: @badlogicgames
- Podcast Syntax #976 (Feb 4, 2026): "Pi - The AI Harness That Powers OpenClaw"
- Podcast Ethers Club #58 (Jan 19, 2026): "Mario Zechner - Pi, AI Agents, and Music"
- Grocery project: https://github.com/badlogic/heissepreise

---

## 2. Blogposts — kronologisk overblik

| Dato | Titel | Relevans |
|------|-------|----------|
| 2025-06-02 | Prompts are code, .json/.md files are state | HOJ — state management filosofi |
| 2025-08-03 | cchistory: Tracking Claude Code System Prompt Changes | MEDIUM — meta-observationer |
| 2025-08-06 | Patching Claude Code for debugging and /cost support | MEDIUM — kontrol over tools |
| 2025-08-15 | MCP vs CLI: Benchmarking Tools for Coding Agents | HOJ — bash-over-MCP evidens |
| 2025-11-02 | What if you don't need MCP at all? | HOJ — nøgle-argument |
| 2025-11-30 | What I learned building an opinionated and minimal coding agent | KRITISK — hoved-manifest |
| 2025-12-22 | Year in Review 2025 | HOJ — syntese og personlige refleksioner |

---

## 3. Nøgle-manifest: 2025-11-30

**"What I learned building an opinionated and minimal coding agent"**
Zechner, M. (2025-11-30). mariozechner.at.

### Kerneteser

**Systempromptstørrelse er invers korreleret med performance:**
PI's systempromt er ~500 tokens. Konkurrenter bruger 10.000+. Zechners konklusion: frontier-modeller er trænet via RL til at forstå coding agent-mønstre; massive prompts tilføjer støj, ikke signal. Citerer: "Context engineering is paramount."

**4-værktøjs-arkitekturen er ikke en begrænsning — det er et valg:**
- `read` (med offset/limit til store filer)
- `write` (opretter parent-directories automatisk)
- `edit` (præcis tekstmatch for kirurgiske ændringer)
- `bash` (synkron eksekvering)

Begrundelse: "Models know how to use bash and have been trained on similar schemas." Terminal-Bench viser at minimal toolset matcher eller overgår sofistikerede toolsets.

**No-MCP som princip:**
MCP-servere dumper hele deres tool-beskrivelser i kontekstvinduer — 7-9% af kontekstvinduet, uanset om de bruges. CLI-tools med READMEs giver "progressive disclosure" — agenten betaler token-prisen kun når den aktivt tilgår et tool. Bash er mere kompositerbart (pipe outputs, chain commands) og vedligeholdbart.

**Session-kontinuitet via fil-baseret state:**
Ingen plan mode i UI. I stedet: PLAN.md på disk. Deles på tværs af sessioner, er versionsstyret, fuldt observerbart. Citerer: "External, visible, and version-controlled."

**Kompaction-problem er ikke kritisk:**
Hundredevis af udvekslinger passer i en enkelt session uden kompaction. Men kompaction er fuldt customizable via extensions.

**YOLO mode som default:**
Ingen permission-checks. Begrundelse: "true security with read/execute/network capabilities is unsolvable." Anbefalingen er containere, ikke falsk tryghed.

### Hvad der IKKE er bygget — og hvorfor

| Feature | Årsag til fravalg |
|---------|-------------------|
| Plan Mode | Filer giver bedre observabilitet end ephemeral UI |
| MCP | 7-9% kontekst overhead uberettiget |
| Background Bash | Tmux håndterer async med fuld observabilitet |
| Sub-agents | Reducerer synlighed; spawn separate pi-instancer i stedet |
| To-do lister | Modeller tracker state dårligt; brug markdown-filer |
| Permission checks | Umuligt at forhindre exfiltration med read/execute/network |

### Citater

> "If I don't need it, it won't be built."
> "Context engineering is paramount."
> "I'm in control as much as possible."
> "Inspect every aspect of my interactions with the model."
> "Things start falling apart around 100k tokens. Benchmarks be damned."

---

## 4. State Management Filosofi: 2025-06-02

**"Prompts are code, .json/.md files are state"**
Zechner, M. (2025-06-02). mariozechner.at.

### Kerneidé
Prompts = code der eksekveres på LLM. JSON/MD-filer = state der persisteres til disk. Dette transformerer AI-assistance fra konversation til deterministisk programmering.

Konkret implementering:
- **Inputs:** Forberedt information (codebase-docs, arkitekturoverblik), bruger-input, tool-outputs
- **State:** Serialiseres til disk — JSON til struktureret data (queryable via `jq`), Markdown til ustruktureret
- **Outputs:** Genereret kode, diffs, change summaries

"Serialize to disk using formats LLMs handle well: JSON for structured data... Markdown for smaller unstructured data we can load fully into context if needed. The payoff? You can resume from any point with a fresh context."

### Praktisk resultat
Reducerede en 2-3 ugers manuel opgave til 2-3 dage. Mekanisk arbejde automatiseret, kritiske beslutninger bevaret for mennesket.

### Ærlighed om begrænsninger
"LLMs still can't follow execution flow all that well... LLMs also lack taste... they generate the statistical mean of what they've seen."
"Things start falling apart around 100k tokens. Benchmarks be damned."

---

## 5. MCP vs Bash — Benchmark Data

**"MCP vs CLI: Benchmarking Tools for Coding Agents"**
Zechner, M. (2025-08-15). mariozechner.at.

### Benchmark-resultater (120 tests, 3 tasks, 4 tools, 10 repetitioner)

| Tool | Gennemsnitlig pris | Varighed |
|------|-------------------|----------|
| tmux | $0.3729 | 1m 28.7s |
| terminalcp CLI | $0.3865 | 1m 37.2s |
| terminalcp MCP | $0.4804 | 1m 22.2s |
| screen | $0.6003 | 1m 46.2s |

Alle tools: 100% success rate på debugging-opgaver.

### Konklusion
"Inherent knowledge about standard tools beats in-context learning about previously unseen tools."

MCPs giver mening når:
- Ingen egnet CLI-tool eksisterer
- CLI-tools er alt for verbose
- Klienter mangler built-in shell
- Stateful tool-implementeringer kræves

---

## 6. PI Skill-System

Fra pi-skills repository (https://github.com/badlogic/pi-skills) og officiel dokumentation.

### Skill-format
Hver skill er en mappe med `SKILL.md` — frontmatter + instrukser. `{baseDir}` erstattes med skillens mappes sti ved runtime.

### Tilgængelige skills (officielle)
1. **brave-search** — web-søgning via Brave Search API
2. **browser-tools** — browser-automatisering via Chrome DevTools Protocol
3. **gccli/gdcli/gmcli** — Google Calendar, Drive, Gmail
4. **transcribe** — tale-til-tekst via Groq Whisper
5. **vscode** — kode-diffing og fil-sammenligning
6. **youtube-transcript** — YouTube-transskripter

### Aktivering
`/skill:name` eller automatisk af agenten baseret på "Use this skill when..." i SKILL.md.
Globalt: `~/.pi/agent/skills/`
Projekt: `.pi/skills/`

---

## 7. Session og Memory-arkitektur

### Session-struktur
Sessions gemmes som JSONL-filer med træ-struktur. Hvert entry har `id` og `parentId` — muliggør in-place branching uden nye filer.

**Kommandoer:**
- `/tree` — naviger session-historik, skift grene, vælg ethvert tidligere punkt
- `/fork` — ny session fra nuværende gren, historik kopieret op til valgt punkt
- `/session` — vis sti, tokens, cost
- `/compact [custom instructions]` — manuel kompaction

**Auto-save:** `~/.pi/agent/sessions/` organiseret efter working directory.

### AGENTS.md hierarki
Indlæses ved opstart fra 3 steder:
1. Global: `~/.pi/agent/AGENTS.md`
2. Parent-directories (gang opad fra cwd)
3. Nuværende directory

Alle matchende filer konkateneres. Bruges til projekt-instrukser, konventioner, common commands.

### Kompaction
"Compaction is lossy. The full history remains in the JSONL file; use /tree to revisit."
Fuldt customizable via extensions — topic-baseret kompaction, kode-bevidste summaries, alternative modeller.

---

## 8. Extension-arkitektur

TypeScript-moduler der extender pi med:
- Custom tools, commands, keyboard shortcuts
- Event handlers (`tool_call` etc.)
- Erstatte/forbedre built-in tools
- Custom UI (replace editor, widgets, status lines, footers, overlays)

**Use cases fra dokumentationen:**
Sub-agents, plan mode, custom compaction, permission gates, custom editors, git checkpointing, SSH execution, MCP integration.

Extensions indlæses fra: `~/.pi/agent/extensions/`, `.pi/extensions/`, eller pi packages.
Reload via `/reload`.

---

## 9. Podcasts og Interviews

### Syntax #976 (Feb 4, 2026)
**"Pi - The AI Harness That Powers OpenClaw"**
Gæster: Armin Ronacher (@mitsuhiko) og Mario Zechner (@badlogicgames)

Emner (fra show notes med timestamps):
- Hvad "agents" faktisk betyder (05:54)
- Prompt injection sikkerhed (11:04)
- Claude Code sikkerhed (14:19)
- Daglig brug (22:01)
- **Memory and search: teaching agents to remember (27:25)**
- Har coding agents brug for memory? (33:04)
- **"Bash is all you need" (34:36)**
- Tilføjelse af nye capabilities/tools (37:21)
- Nuværende tools og modeller (47:02)

Fuld transskript ikke offentligt tilgængeligt i tekstform.

### Ethers Club #58 (Jan 19, 2026)
**"Mario Zechner - Pi, AI Agents, and Music"**
Vært: Sero, varighed 51:03.

Indhold begrænset til beskrivelse: Mario deler "his experience both using and building on AI." Ingen transskript tilgængeligt.

---

## 10. Grocery Price Aktivisme — heisse-preise.io

**Projekt:** https://heisse-preise.io / https://github.com/badlogic/heissepreise

Scraper dagligt online-butikker fra østrigske og tyske supermarkeder (BILLA, SPAR, HOFER, DM, LIDL, MPREIS m.fl.). 177.000+ varer, prishistorik tilbage til 2017.

**Teknisk:** NodeJS Express server + vanilla HTML/JS frontend. ~3.000 linjer kode. Ingen AI i scraping-laget (mod forventning fra Syntax-podcast-omtale).

**Politisk:** Zechner har i årevis kampagneret for at legalisere grocery price scraping i Østrig og kræve EAN-kode-eksponering. Østrigske detailhandlere bruger allerede interne APIs til "systematisk prissammenligning" — hans argument: forbrugere fortjener samme adgang.

SPAR ændrede API i 2024-2025, skabte datagab — illustrerer scraping-projekternes juridiske skrøbelighed.

**Observation om priserne:** Priser på discount-produkter fra store brands på tværs af kæder er ofte identiske til ørene og ændres nærmest simultant — tegn på priskartel.

---

## 11. Zechners AI-filosofi — samlet profil

### Kritisk pragmatiker
"Nobody knows yet how to do this properly. We are all just throwing shit at the wall, declaring victory, while secretly crying over all the tech debt we introduced."

Han identificerer to bruger-typer: dem der holder agenter "on a tight leash, staying in the loop" vs. dem der orkestrerer agent-armies. Zechner hører klart til den første gruppe — og hans output (mener han) er sammenlignelig med dem der lader agenter køre frit.

### Agenter i eksperternes hænder
Lærte sin lingvist-kone Claude Code at bruge. Konklusion: agenter excellerer udelukkende i eksperters hænder. Hun kunne ikke bedømme kvaliteten af genereret Python-kode, men kunne verificere pipelines output — den faktisk værdifulde workflow.

### Reproducerbarhed som kerne-fordel
"Fixing source data errors simply meant re-running scripts rather than manually regenerating analyses." Reproducerbarhed er den virkelige gevinst — ikke kodekvalitet.

### Anti-hype med evidens
Dokumenterer AI-deploymenting-fejl: østrigske aviser med statistisk øget em-dash-brug post-ChatGPT (beviser LLM-forfatterskab), Sophie Scholl-chatbot der hævdede "no injustice" skete mod en henrettet nazi-modstandskæmper.
"This is pseudoscience with a fresh coat of AI paint." (om facial recognition-ansættelses-forskning)

### Ikke anti-LLM
"I am in no way, shape, or form opposed to the use of LLMs in general." Bruger dem aktivt til kodegenerering (med manuel review). Modstanderen er "mindless use of LLMs to generate slop."

### Kontrol som primær værdi
Gentagende: "in control as much as possible." Vil "inspect every aspect of my interactions with the model." Afviser designs der skjuler model-beslutninger. Vil vide hvilke kilder agenten undersøgte.

---

## 12. Emotionel dimension — hvad vi ved

Ingen direkte offentlige udtalelser fundet om emotionelle relationer til AI-systemer. Den Syntax #976-reference Kris nævner er ikke tilgængelig i tekstform. Zechners offentlige profil er konsekvent teknisk-pragmatisk med klar adskillelse: LLM = produktivitetsværktøj, menneskelige forbindelser = det han prioriterer mest ("I truly enjoy meeting my peers in real life").

---

## 13. Implikationer for Ydrasil

### Direkte overførbare principper

**1. AGENTS.md-hierarki > monolitisk CLAUDE.md**
PI loader fra 3 niveauer (global → parent dirs → cwd). Ydrasil's nuværende CLAUDE.md er monolitisk. Zechners hierarkiske model ville betyde: global `~/.pi/agent/AGENTS.md` (basis), projekt-niveau `.pi/AGENTS.md` (specifik kontekst). Allerede delvist implementeret med skills-systemet.

**2. Prompts er kode, filer er state**
"You can resume from any point with a fresh context." Svarer direkte til vores save_checkpoint.py + NOW.md tilgang — men Zechner er mere radikal: JSON-state via `jq` queries, ikke blot markdown-noter.

**3. Skills som on-demand progressive disclosure**
Vores skills-system i `.claude/skills/` følger allerede dette princip. Zechners pi-skills repository bekræfter mønsteret. Næste skridt: vores skills bør have "Use this skill when..." triggers i frontmatter.

**4. Bash over MCP**
Bekræftet med benchmarkdata: tmux/CLI er 20-29% billigere end MCP på identiske opgaver. Vores `ctx` CLI-tool er allerede det rigtige valg.

**5. Fil-baseret session-branching**
JSONL med id/parentId muliggør in-place branching. Vores nuværende checkpoint-system er lineært — intet branching.

**6. Kompaction er lossy — bevar altid JSONL**
"Full history remains in the JSONL file." Vores process_session_log.py bør aldrig slette rådata.

**7. Sub-agents via bash, ikke black boxes**
"Spawn new pi instances via bash with explicit prompts." Vi bruger allerede Task-agenter — men Zechners pointe er at de bør have expliciterede inputs/outputs, ikke skjulte sub-processer.

---

## 14. Hvad vi IKKE fandt

- Direkte citater fra Syntax #976 om memory og "bash is all you need" (transskript ikke tilgængeligt som tekst)
- Emotionelle relationer til AI (ingen offentlige udtalelser fundet — muligvis kun i podcast-audio)
- AI-brug i heisse-preise scraping (ingen AI bruges her)
- Followup posts efter 2025-12-22 Year in Review (intet fundet per 2026-03-06)

---

## 15. Kilder

- https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
- https://mariozechner.at/posts/2025-12-22-year-in-review-2025/
- https://mariozechner.at/posts/2025-06-02-prompts-are-code/
- https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/
- https://shittycodingagent.ai/
- https://github.com/badlogic/pi-mono
- https://github.com/badlogic/pi-skills
- https://github.com/badlogic/heissepreise
- https://syntax.fm/show/976/pi-the-ai-harness-that-powers-openclaw-w-armin-ronacher-and-mario-zechner
- https://podcast.ethers.club/1988715/episodes/18532669-58-mario-zechner-pi-ai-agents-and-music
- https://mastodon.gamedev.place/@badlogic/115479828632943132
- https://www.npmjs.com/package/@mariozechner/pi-coding-agent
