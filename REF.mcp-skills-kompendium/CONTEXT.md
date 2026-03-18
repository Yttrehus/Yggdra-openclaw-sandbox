# MCP/Skills Kompendium

## Metadata
- **Status:** v1 færdig. Kompendium + adversarial evaluering afsluttet.
- **Sidst opdateret:** 2026-03-14 (session 18)

## Hvad er det
Kurateret opslagsværk over MCP-servere og Claude Code skills. Kategoriseret, ranket, og vurderet — men designet som **reference**, ikke som indkøbsliste. Yttre beslutter selv hvad der installeres.

## Struktur

```
mcp-skills-kompendium/
├── CONTEXT.md              ← denne fil
├── kompendium-mcp.md       ← MCP-servere: top 25+, kategoriseret, ranket
├── kompendium-skills.md    ← Skills: top 20+, kategoriseret, ranket
├── needs-mapping.md        ← Yggdra-behov → løsnings-mapping
├── anbefaling.md           ← Claudes anbefaling (separat, kan ignoreres)
└── research/adversarial/   ← Steelman, red team, steelman RT, neutral evaluator
```

## Hvor er vi

### Færdigt
- MCP-landskab scannet (~25 servere vurderet)
- Skills-landskab scannet (community + officielle, overlap-analyse med 12 eksisterende)
- Yggdra-behov mappet (11 backlog-briefs → konkrete løsninger)
- Adversarial proces gennemført (6 agents, 4 runder: steelman → red team → steelman RT → neutral evaluator)
- Kompendier skrevet (kompendium-mcp.md, kompendium-skills.md)
- Anbefaling skrevet (anbefaling.md)

### Mangler
- [ ] Skills index i `.claude/skills/INDEX.md` ikke oprettet endnu
- [ ] Ingen af anbefalingerne er installeret endnu
- [ ] Rå agent-rapporter (mcp-landscape, skills-landscape, yggdra-needs) ikke gemt — kun destilleret i kompendierne

## Hvad vi lærte

### Om processen
- **Adversarial-metoden virkede.** 6 agents i 4 runder fangede reelle bias: toolbox mentality (flere tools ≠ bedre), kapacitets-blindhed (18 deliverables for solo-dev med fuldtidsjob), og princip-brud (bash-first vs. MCP-servere). Red team vandt — den neutrale evaluator reducerede fra 5 MCP + 9 skills → 1 MCP + 2 skills.
- **Kompendium ≠ handlingsplan.** Den første iteration blandede opslagsværk og anbefaling sammen. Yttre korrigerede: han vil have et neutralt katalog han selv kan vælge fra — ikke en indkøbsliste. Separation i to dokumenter (kompendium + anbefaling) løste det.
- **Rå research-data forsvinder.** Agent-rapporter lever kun i session-konteksten. Kompendierne destillerer det vigtigste, men detaljer (specifikke GitHub-repos, installationskommandoer, community-scores) kan gå tabt. Overvej at gemme rå output næste gang.

### Om MCP/skills-landskabet (marts 2026)
- **MCP-økosystemet er ungt.** Mange servere er alpha/beta. Breaking changes er normale. Vedligeholdelse er uforudsigelig.
- **Størstedelen af MCP-servere er redundante med Claude Code.** Filesystem, Git, Fetch — alle duplikerer built-in capabilities (Read/Write/Edit/Bash/WebFetch).
- **Skills er lavrisiko.** Markdown-filer der kan inspiceres og redigeres. Worst case: de gør ingenting. MCP-servere er runtime-processer med reelle fejl-modes.
- **Superpowers (obra) er den stærkeste single-kilde** for community skills. 14 battle-tested skills, konsistent kvalitet. Cherry-pick relevante, installér ikke hele pakken.
- **Qdrant MCP er det mest oplagte** men har et uløst tunneling-problem (VPS-hosted Qdrant, lokalt Claude Code). Bash-first alternativ (ctx-wrapper) virker allerede.

## Beslutninger
- Kompendiet er et **opslagsværk** — Yttre vælger selv hvad der installeres
- Adversarial-processen testede en handlingsplan, ikke kompendiet
- Skills (markdown) er lavrisiko. MCP (runtime) er højrisiko. Forskellige evalueringskriterier.
- Bash-first: hvis bash kan løse det, behøver det ikke en MCP
- Solnedgangsklausul på alt der installeres

## Forbedringer til v2

### Opdatering
- **Kvartalsvis review.** MCP-landskabet ændrer sig hurtigt. Sæt en reminder (Q2 2026) til at scanne awesome-mcp-servers og awesome-claude-skills for nye entries.
- **Tilføj "sidst verificeret" dato** til hver entry i kompendierne — så man kan se hvad der er friskt vs. potentielt forældet.

### Dybde
- **Installationsguides.** Kompendierne ranker, men forklarer ikke *hvordan*. En kort install-sektion per MCP/skill ville gøre opslagsværket mere actionable.
- **Hands-on test af top 5.** Research er desk-research. Faktisk installation + 30 min brug ville afsløre om ting virker out-of-the-box eller kræver debugging.

### Proces
- **Gem rå agent-output næste gang.** Enten til `research/` mappen eller som session-artifact. Destillerede kompendier mister detaljer.
- **Adversarial-processen som skill.** Gentag den for andre projekter. Format: context scout → parallel research → steelman → red team → steelman RT → neutral evaluator. Kan formaliseres som en `.claude/skills/adversarial-review/` skill.

### Manglende perspektiver
- **Token-budget analyse.** Hvor mange tokens koster hver MCP-server i tool-registrering? Aldrig kvantificeret.
- **Maintenance-cost estimat.** Hvor mange timer/måned koster det at holde X dependencies opdateret?
- **Rollback-plan.** Hvad gør du hvis en MCP korrumperer data eller en skill overskriver filer?

## Kilder
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — officielle MCP-servere
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — community-kurateret
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — skills-hovedliste
- [obra/superpowers](https://github.com/obra/superpowers) — battle-tested skills-pakke
- [anthropics/skills](https://github.com/anthropics/skills) — officielle Anthropic skills
- [trailofbits/skills](https://github.com/trailofbits/skills) — professionelle sikkerhedsskills
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — bredeste kurateret liste
