# MCP-servere — Kompendium

Kurateret oversigt over MCP-servere relevante for solo-udviklere med Claude Code. Kategoriseret efter funktion, ranket efter community-adoption og modenhed.

**Konvention:** Relevans-score (1-5) er for Yggdra specifikt. Community-score er generel popularitet/modenhed.

---

## Allerede installeret

| Navn | Hvad den gør | Kilde |
|------|-------------|-------|
| **Figma** | Design-til-kode, screenshots, metadata | Officiel (Figma) |
| **Notion** | Database/dokument-adgang, søgning, sider | Officiel (Notion) |
| **Gmail** | Læse/søge mails, oprette udkast | Officiel (Google) |
| **Excalidraw** | Diagrammer, whiteboard | Community |
| **Firecrawl** (skill) | Web scraping, research, link discovery | Firecrawl |

---

## Kategori: Data & Databaser

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Qdrant** | Semantisk vektor-søgning. Query collections, upsert, filtrér. | Officiel (Qdrant) | 5 | Let (pip) | [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) |
| **SQLite** | SQL queries mod lokale .db filer. Skema-inspektion. | Officiel (Anthropic) | 3 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Postgres** | SQL queries mod PostgreSQL. Skema, tabeller, joins. | Officiel (Anthropic) | 2* | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Supabase** | Postgres + auth + storage via Supabase API | Officiel (Supabase) | 2 | Let | [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) |
| **Turso** | Edge SQLite (libSQL). Distribueret. | Community | 1 | Medium | [turso-extended/mcp-server](https://github.com/turso-extended/mcp-server) |

*Postgres: kun relevant hvis du kører Postgres. Yggdra bruger Qdrant + JSON + SQLite.

---

## Kategori: Browser & Web

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Playwright** | Browser-automation via accessibility tree. Klik, udfyld, navigér, screenshot. Håndterer JS-renderet indhold. | Officiel (Microsoft) | 5 | Let (npx) | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| **Puppeteer** | Browser-automation via screenshots. Ældre tilgang end Playwright. | Officiel (Anthropic) | 2 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Brave Search** | Web-søgning med lokal-søgning, billeder, nyheder. Gratis API tier. | Officiel (Brave) | 3 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Fetch** | Hent web-indhold som markdown. Simpel. | Officiel (Anthropic) | 1 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Perplexity** | AI-drevet web-research med citations. Dybere end WebSearch. | Officiel (Perplexity) | 3 | Let (API key) | [perplexityai/modelcontextprotocol](https://github.com/perplexityai/modelcontextprotocol) |

---

## Kategori: Google Suite

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Google Calendar** | Læs/opret events, søg, koordinér kalendere. | Community | 4 | Medium (OAuth) | [nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp) |
| **Google Sheets** | Læs/skriv regneark, formler, sheets. | Community | 3 | Medium (OAuth) | Flere implementationer |
| **Google Drive** | Søg/læs filer i Drive, Docs, Sheets. | Community | 2 | Medium (OAuth) | [piotr-agier/google-drive-mcp](https://github.com/piotr-agier/google-drive-mcp) |
| **Google Maps** | Geocoding, directions, places. | Officiel (Anthropic) | 2 | Let (API key) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |

---

## Kategori: Udviklerværktøjer

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Context7** | Henter up-to-date library/framework docs direkte i kontekst. Eliminerer hallucination af API-syntaks. | Community (Upstash) | 4 | Let (npx, gratis) | [upstash/context7](https://github.com/upstash/context7) |
| **Sentry** | Hent fejl-kontekst, stack traces, issue details fra Sentry. | Officiel (Sentry) | 3* | Let | [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) |
| **Docker** | Container management, logs, exec. Kan forbinde til remote daemon. | Community | 3 | Medium | [ckreiling/mcp-server-docker](https://github.com/ckreiling/mcp-server-docker) |
| **GitHub** | Issues, PRs, repo-søgning, kodeanalyse. | Officiel (Anthropic) | 2** | Let (token) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Linear** | Issue tracking, project management. | Community | 1 | Let (API key) | Flere implementationer |

*Sentry: kun relevant hvis du bruger Sentry. **GitHub: `gh` CLI via Bash dækker det meste.

---

## Kategori: Automation & Workflow

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **n8n** | Workflow automation. Triggers, actions, 400+ integrationer. | Community | 2 | Svær (kræver n8n) | [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) |
| **Zapier** | Workflow automation via Zapier platform. | Community | 1 | Medium (konto) | Flere implementationer |
| **Todoist** | Task management via naturligt sprog. | Community | 2* | Let (API key) | [greirson/mcp-todoist](https://github.com/greirson/mcp-todoist) |

*Todoist: kun relevant hvis du bruger Todoist.

---

## Kategori: AI & Tænkning

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Sequential Thinking** | Struktureret problemløsning i eksplicitte steps. Branching, revision. | Officiel (Anthropic) | 2 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| **Memory (Knowledge Graph)** | Persistent hukommelse som lokal JSON knowledge graph. | Officiel (Anthropic) | 2 | Let (npx) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |

---

## Kategori: Finans & Business

| Navn | Hvad den gør | Community | Relevans | Installation | Kilde |
|------|-------------|-----------|----------|-------------|-------|
| **Stripe** | Kunder, betalinger, abonnementer, fakturaer. | Officiel (Stripe) | 2* | Medium | [stripe/agent-toolkit](https://github.com/stripe/agent-toolkit) |
| **QuickBooks** | Bogføring, fakturaer, rapporter. | Community | 1 | Svær | Diverse |

*Stripe: kun relevant hvis rejseselskabet bruger Stripe.

---

## Redundante med Claude Code (installér IKKE medmindre specifikt behov)

| Navn | Hvad den gør | Hvorfor redundant |
|------|-------------|-------------------|
| **Filesystem** | Fil-operationer | Claude Code har Read/Write/Edit/Glob/Grep built-in |
| **Git** | Git-operationer | Claude Code kører `git` via Bash |
| **Fetch** | Hent web-indhold | Claude Code har WebFetch built-in |
| **Time** | Timezone-konvertering | `date` i bash / Python one-liner |
| **Slack** | Chat-integration | Solo-developer, ingen Slack |
| **AWS/Azure** | Cloud services | Ikke i stacken |
| **CI/CD** | GitHub Actions etc. | Ingen CI/CD pipeline eksisterer |

---

## Noter
- **Installation:** "Let" = npx/pip, ingen auth. "Medium" = kræver API key eller OAuth. "Svær" = kræver server/infrastruktur.
- **Opdatering:** MCP-økosystemet ændrer sig hurtigt. Genbesøg dette dokument kvartalsvis.
- **Bash-first:** Hvis det kan løses med `ssh VPS "command"` eller et Python-script, behøver det ikke en MCP.
