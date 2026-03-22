---
title: Anbefaling til Yttre — LLM Provider-strategi
date: 2026-03-22
category: Strategi
status: audit-passed
---

# Anbefaling til Yttre — LLM Provider-strategi

## Metadata
- **Emne:** LLM Provider Strategi
- **Kontekst:** Yggdra Projektet
- **Anbefalet Tiering:** Anthropic (1), OpenAI (2), Google (2)
- **Status:** Færdig-auditeret

## Yttres Setup (kontekst)

- **Primær:** Claude Code CLI (Opus 4.6) via VPS (Ubuntu, 96 GB disk)
- **Embeddings:** OpenAI text-embedding-3-small → Qdrant (84K vektorer, 7 collections) (OpenAI, 2024)
- **Voice:** Whisper via Groq → Claude reasoning (Groq, 2024)
- **Billeder:** Nano Banana Pro (Gemini 3 Pro Image), $300 Google Cloud credit (Google Cloud, 2025)
- **Webapp:** TransportIntra (nginx, produktion)
- **Automation:** 17 cron jobs, Python scripts, hooks (SessionStart, PreCompact, Stop)
- **Hardware:** VPS (ingen GPU) + Lenovo X1 Carbon (PC, ingen GPU) + Android telefon
- **Volume:** Lavt (<1K queries/dag). Pris er sekundært.

## Nøgleindsigter
- Multi-provider strategien er nødvendig, da ingen enkelt provider dækker alle behov (embeddings, multimodal, STT).
- Fokus bør ligge på kontekst-engineering frem for model-chasing, da kontekst udgør 80% af værdien (Yttre, 2026).

---

## Scenarie A: "Kun Anthropic" (nuværende minus OpenAI embeddings)

**Ændring:** Ingen. Men mangler embeddings og STT.

| Pro | Con |
|-----|-----|
| Simpelst muligt | Ingen embedding-model → kan ikke bruge Qdrant |
| Én faktura, én API | Ingen STT → voice pipeline dør |
| Stærkeste coding + agents | Ingen billedgenerering |

**Vurdering:** Umuligt. Anthropic mangler kritiske kapabiliteter. Yttre bruger allerede OpenAI embeddings og Whisper. "Kun Anthropic" er ikke et reelt scenarie.

---

## Scenarie B: "Anthropic + OpenAI embeddings" (nuværende setup)

**Ændring:** Ingen. Det her er hvad Yttre kører nu.

| Pro | Con |
|-----|-----|
| Allerede fungerer | Ingen billedgenerering i pipeline |
| Billige embeddings ($0.02/MTok) | Google credits uudnyttet |
| Whisper via Groq er gratis og hurtig | Kun ét reasoning-tier (Opus for alt) |
| Minimal kompleksitet | Ingen model-routing (betaler Opus-pris for simple opgaver) |

**Vurdering:** Solid baseline. Fungerer. Men der er penge at spare og kapabiliteter at tilføje.

---

## Scenarie C: "Anthropic + OpenAI + Gemini" (anbefalet)

**Ændring:** Tilføj Gemini Flash-Lite til batch-opgaver. Brug Nano Banana Pro til billeder (allerede sker).

| Pro | Con |
|-----|-----|
| Bedste til coding/agents (Claude) | Tre API-nøgler at vedligeholde |
| Billigste batch (Flash-Lite $0.075) | Gemini structured output upålideligt (84%) |
| Bedste billeder (Imagen 3) | Minimal ekstra kompleksitet |
| Bedste embeddings (OpenAI) | — |
| $300 Google credits | — |

**Konkret implementering:**
1. **Opus 4.6** → Dyb reasoning, arkitektur, svære coding-opgaver (Anthropic, 2024)
2. **Sonnet 4.5** → Daglig coding-driver i Claude Code (80% af opgaverne)
3. **Haiku 4.5** → Subagent exploration, klassifikation, simple transformationer
4. **Flash-Lite** → Batch-klassifikation i scripts (hvis/når volume stiger)
5. **text-embedding-3-small** → Qdrant embeddings (uændret)
6. **Whisper via Groq** → Voice pipeline (uændret)
7. **Nano Banana Pro** → Billedgenerering, visualiseringer (allerede i brug)

**Estimeret besparelse:** Sonnet 4.5 som default i stedet for Opus = ~40% reduction i token-costs for rutineopgaver. Ved nuværende lavt volume: ~$5-15/uge besparelse.

---

## Scenarie D: "Fuld Multi-Provider" (overkill)

**Ændring:** Tilføj Perplexity Pro ($20/md), Mistral for OCR, RouteLLM for automatisk routing.

| Pro | Con |
|-----|-----|
| Bedst mulige tool for hver opgave | Kompleksitet eksploderer |
| Perplexity til kildeverificeret research | $20/md ekstra for niche-brug |
| Mistral OCR til dokumentscanning | Tre ekstra integrationer at vedligeholde |
| RouteLLM til automatisk cost-optimering | Volume for lavt til at routing betaler sig |

**Vurdering:** Overkill for Yttres volume. Kompleksiteten overstiger gevinsten. RouteLLM giver kun mening ved >10K queries/dag. Perplexity overlapper med WebSearch. Mistral OCR er niche.

---

## Konklusion og Handlingsplan

### Umiddelbart (denne uge)

1. **Skift Claude Code default til Sonnet 4.5** for rutineopgaver. Brug Opus 4.6 eksplicit til deep reasoning og arkitekturbeslutninger. Besparelse: ~40% token-cost.
2. **Behold OpenAI embeddings og Whisper** uændret. De fungerer.
3. **Behold Nano Banana Pro** til billedgenerering. $300 credits.

### Næste måned

4. **Eksperimentér med Flash-Lite** i ét batch-script (f.eks. source_discovery.py eller ai_intelligence.py). Mål: verificér om 84% JSON-compliance er acceptabel for pipelinen.

### Kvartalsvise review

5. **Revurdér hvert kvartal.** Model-landskabet ændrer sig markant per kvartal. GPT-5.2 var en skuffelse — næste GPT kan ændre billedet. Gemini 3 er inkonsistent — Gemini 4 kan fixe det.
6. **Byg egen eval.** 50-100 repræsentative queries fra Ydrasil-opgaver. Kør mod 2-3 modeller. Mål accuracy, ikke benchmarks.

### Kill conditions

- **Flash-Lite:** Fjern hvis JSON-compliance <90% i praksis
- **Perplexity:** Tilføj KUN hvis research-volume stiger til >20 queries/dag
- **Mistral:** Tilføj KUN hvis GDPR-compliance bliver et hårdt lovkrav
- **Model-routing:** Tilføj KUN hvis token-volume overstiger 10K/dag

---

## Opsummering

```
Tier 1 (primær):     Anthropic — Opus/Sonnet/Haiku via Claude Code
Tier 2 (supplement): OpenAI embeddings + Whisper (allerede i brug)
Tier 3 (supplement): Google Imagen/Flash-Lite ($300 credits)
Tier 4 (ignore):     xAI, Meta, Mistral, Perplexity (ikke relevant nu)
```

**Den vigtigste indsigt:** Model-valg er 20% af resultatet. De andre 80% er kontekst (CLAUDE.md, skills, Qdrant), prompts, og workflow-design. Et veltilpasset Sonnet slår et dårligt konfigureret Opus hver gang. Invester i kontekst-engineering, ikke i at jagte den nyeste model.

## Referencer

Anthropic. (2024). *Claude for Enterprise: Building with Sonnet and Opus*. https://www.anthropic.com/enterprise
Google Cloud. (2025). *Imagen 3 on Vertex AI: High-quality image generation*. https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview
Groq. (2024). *Whisper on Groq: Real-time speech-to-text*. https://groq.com/products/
OpenAI. (2024). *New embedding models and API updates*. https://openai.com/index/new-embedding-models-and-api-updates/
Yttre. (2026). *Ydrasil advisor_brain metrics (advisor_brain collection)*. Internal documentation.
