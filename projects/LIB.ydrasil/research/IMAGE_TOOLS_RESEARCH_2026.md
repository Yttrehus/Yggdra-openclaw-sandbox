# Research: Billedgenkendelse & Billedgenerering for Ydrasil

**Dato:** 2026-02-02

## Sammenfatning

Tre ting kan gøres med det samme (gratis), resten kræver lidt setup eller kan vente.

---

## 1. Daniel Miessler / Fabric

Der findes **intet værktøj kaldet "ART"** i Fabric. Det der findes er:

- **`create_art_prompt`** — genererer detaljerede tekst-prompts til brug med DALL-E, Midjourney osv. En prompt-pipeline, ikke direkte billedgenerering.
- **`create_conceptmap`** (tilføjet nov 2025) — genererer interaktive HTML concept maps med Vis.js. Det nærmeste Fabric har på visuel output.
- **`create_logo`** — lignende prompt-generering til logoer.

Kilder: [Fabric GitHub](https://github.com/danielmiessler/Fabric), [Built-in Patterns](https://deepwiki.com/danielmiessler/fabric/3.3-built-in-patterns-reference)

---

## 2. Image Generation APIs — Tre Tiers

### Tier 1: API-baseret (kan bruges med det samme)

| Model | Pris/billede | Styrke |
|-------|-------------|--------|
| GPT Image 1 Mini | $0.005-0.05 | Billigst, god til iteration |
| GPT Image 1.5 | $0.04-0.08 | Bedste tekst-rendering i billeder |
| Flux 2 Pro | ~$0.05 | Infographics, teknisk dokumentation |
| Ideogram 3.0 | ~$0.03 | Nær-perfekt typografi |

### Tier 2: Code-to-Diagram (gratis, lokalt)

| Værktøj | Installation | Styrke |
|----------|-------------|--------|
| **D2** | `curl -fsSL https://d2lang.com/install.sh \| sh` | Native Go binary, ingen browser, bedste arkitektur-diagrammer |
| **Mermaid CLI** | `npm i -g @mermaid-js/mermaid-cli` | Flest diagram-typer, GitHub-support, Claude genererer det nativt |
| PlantUML | Kræver Java | Mest kontrol, stejlest læringskurve |

### Tier 3: Self-hosted (IKKE realistisk nu)
Flux/Stable Diffusion kræver 16-24 GB GPU VRAM. Vores VPS har ingen GPU.

---

## 3. Billedgenkendelse

**Claude Vision er allerede tilgængeligt** via Claude Code — dette tool kan læse billeder direkte. Ingen ekstra setup.

Til simpel lokal OCR uden API: **ocrs** (Rust binary).

---

## 4. UI Mockup Generation

Bedste workflow for solo-udvikler:
1. Beskriv UI'et til Claude Code → få HTML+TailwindCSS genereret
2. Preview i browser → tag screenshot
3. Send screenshot til Claude Vision → få forbedringsforslag
4. Iterér → Claude Code retter koden

Supplerende: [v0.dev](https://v0.dev) (gratis tier, text-til-React), Claude Artifacts (interaktiv prototyping).

---

## 5. Handlingsplan

### KAN GØRES NU (gratis)
- Brug Claude Code til at generere **Mermaid-diagrammer** (skill trees, mind maps, arkitektur)
- Brug Claude Vision til screenshot-analyse (allerede tilgængelig)
- Installer **D2** på VPS'en for arkitektur-diagrammer

### BEHØVER LIDT SETUP (~$0.60/måned)
- Python wrapper til OpenAI Image API (GPT Image 1 Mini til diagrammer)
- Integrer med eksisterende slash commands

### VENT TIL SENERE
- Self-hosted billedgenerering (kræver GPU-server)
- Fabric `create_conceptmap` (kræver Fabric installation)
- Avanceret v0.dev pipeline

---

## Kilder

- [Fabric GitHub](https://github.com/danielmiessler/Fabric)
- [Top Image APIs 2026](https://www.pixazo.ai/blog/top-image-generation-apis)
- [D2 Docs](https://d2lang.com/)
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Claude Vision Docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- [ocrs](https://github.com/robertknight/ocrs)
- [v0.dev](https://v0.dev)
