---
title: Voice Experience — Cadence and Persona Protocol
date: 2026-03-24
category: AI Frontier
status: draft
---

# Voice Experience — Cadence and Persona Protocol

## 1. Vision
For at opnå et "personligt kognitivt exoskeleton" skal stemme-interaktionen føles naturlig, hurtig og ikke-korporativ. Inspirationen hentes fra systemer som Grok (real-time respons) og kognitiv psykologi (menneskelig samtale-kadence).

## 2. Kadence-principper (The 300ms Rule)
Målet er at minimere den oplevede ventetid (latency).

- **Korte sætninger:** Assistenten skal bryde komplekse svar op i mindre bidder. Dette tillader TTS-motoren (ElevenLabs) at starte afspilning hurtigere.
- **Thinking out loud:** Ved længere ræsonnementer kan assistenten starte med en acknowledge ("Lad mig tjekke det...") mens den dybe tænkning kører i baggrunden.
- **Adaptiv hastighed:** Kadencen skal matche brugerens tilstand. Hurtige korte kommandoer kræver hurtige korte svar. Strategiske diskussioner tillader en mere reflekterende hastighed.

## 3. Persona & Sprog (The "Route 256" Style)
Da ejeren ofte interagerer med systemet under kørsel, skal sproget være:
- **Præcist:** Ingen overflødig høflighed ("Jeg vil med glæde hjælpe dig med...").
- **Jordnært:** En blanding af professionel kompetence og praktisk forståelse.
- **Kontekstbevidst:** Systemet skal vide, hvornår det er upassende at give lange tekniske forklaringer (f.eks. under kørsel).

## 4. Multimodalt Flow
- **Voice-to-Visual:** Evnen til at bede om en visualisering ("Tegn lige det her projekt-hierarki") mens man taler, med øjeblikkelig feedback i mobil-interfacet (Notion).

## 5. Tekniske Mål
| Metric | Mål | Status |
|--------|-----|--------|
| TTFT (Time to First Token) | < 500ms | Afventer Groq |
| TTS Start Latency | < 1.2s | Afventer ElevenLabs |
| Word Error Rate (STT) | < 5% | Whisper via Groq |

---

## Referencer
- Anthropic. (2024). *Claude's conversational style guide*. https://docs.anthropic.com/
- ElevenLabs. (2025). *Latency optimization for real-time applications*. https://elevenlabs.io/docs/
- Miessler, D. (2026). *The human-like assistant persona*. https://danielmiessler.com/
