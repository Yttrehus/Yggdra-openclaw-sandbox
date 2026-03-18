# Webscraping/Firecrawl Audit

**Dato:** 2026-03-10
**Klar til:** Backlog (mangler: måling af faktisk forbrug, Jina Reader test)

## Opsummering
- Audit af nuværende Firecrawl-setup: bruges dagligt til research, kører som Claude Code skill
- Konklusion: behold Firecrawl, men prioritér gratis WebFetch/WebSearch først
- Potentiel besparelse: gratis tier (500 sider/mnd) kan være nok

## Origin Story
Opstod fra idé-parkering: "Professionel webscraping-setup (Firecrawl allerede installeret — optimér til research og link-analyse)." Firecrawl var installeret men det var uklart om det blev brugt optimalt eller om der var bedre alternativer for en solo-udvikler.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-04-firecrawl-audit.md (187 linjer, dato 2026-03-10). Indeholder: capabilities-matrix, prissammenligning (Firecrawl vs Jina vs Tavily vs Perplexity vs built-in tools), 5 konkrete anbefalinger, action plan.

**Fra PLAN.md idé-parkering:**
> Professionel webscraping-setup (Firecrawl allerede installeret — optimér til research og link-analyse)

## Cowork Output (2026-03-10)

### Nuværende setup
Firecrawl skill installeret, API-nøgle konfigureret, .firecrawl/ gitignored. Daglig brug til research og dokumentationslæsning. Kun /scrape endpoint bruges reelt.

### Konklusion
**Behold Firecrawl, men prioritér gratis alternativer først.** Claude Code's built-in WebFetch + WebSearch dækker ~90% af research workflows gratis. Firecrawl Hobby ($16/mnd) er ikke dyrt men muligvis unødvendigt.

### Capabilities-vurdering
- /scrape: relevant (kerne-feature)
- /crawl, /extract, /map, /agent: ikke relevant for solo-udvikler research
- /search: muligvis, men WebSearch dækker det meste

### Prissammenligning (1.000 sider/mnd)
- Claude WebFetch: $0 (built-in)
- Jina Reader: ~$0,20 (pay-as-you-go)
- Firecrawl Hobby: $16
- Firecrawl gratis tier: 500 sider/mnd (ingen kreditkort)

### Alternativer
- **Jina Reader API:** Billigere, Apache 2.0 licens, dækker 70% af use cases
- **Tavily/Perplexity:** Søg-først workflow, ikke relevant for dokumentationslæsning

### Anbefalinger (prioriteret)
1. **Høj:** Brug WebFetch/WebSearch først, Firecrawl som fallback (5 min setup)
2. **Høj:** Mål faktisk forbrug — gratis tier (500 sider) kan være nok (2 min)
3. **Lav:** Overvej Jina Reader som secondary API (10 min)
4. **Lav:** Verificér at /extract endpoint ikke er aktiveret (separat billing $89+)

### Action items
- [ ] Mål faktisk Firecrawl-forbrug (credits/mnd)
- [ ] Vurder om gratis tier dækker behovet
- [ ] Etablér WebFetch/WebSearch som primær workflow
