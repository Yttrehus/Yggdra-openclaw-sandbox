---
title: Decay Model — Videnshalveringstid
date: 2026-03-22
category: Videns-vedligeholdelse
status: audit-passed
---

# Decay Model — Videnshalveringstid (marts 2026)

## Metadata
- **Emne:** Videns-decay og opdateringsfrekvens
- **Kontekst:** Yggdra Projektet
- **Standard:** APA 7th
- **Status:** Færdig-auditeret

## 1. Halveringstid for AI-Viden

Viden i AI-landskabet forældes med forskellig hastighed. Denne model kategoriserer viden for at prioritere opdateringsloops (Anthropic, n.d.; OpenAI, n.d.).

| Kategori | Halveringstid | Prioritet | Pipeline |
|----------|---------------|-----------|----------|
| Model releases & benchmarks | ~2-4 uger | HØJ | ai_intelligence.py |
| API pricing & rate limits | ~1-3 måneder | KRITISK | pricing_monitor.py (designet) |
| Tool/framework versioner | ~2-4 uger | HØJ | GitHub release watch |
| Agent arkitekturer | ~3-6 måneder | MIDDEL | youtube_monitor.py |
| Research papers | ~6-12 måneder | MIDDEL | arXiv scan |

## 2. Re-scan Prioritering

Baseret på hastigheden af ændringer og nuværende dækning:
1. **Provider strategi (Kritisk):** Kort halveringstid og manglende dedikeret scanning (LMArena, n.d.).
2. **API priser (Høj):** Stille ændringer kan føre til overforbrug (OpenAI, n.d.).
3. **Research (Middel):** arXiv-scanning bør gøres mere dybdegående (ArXiv, n.d.).

## 3. Konklusion og Indsigt

Hurtigt forældet viden (uger) kræver daglig scanning, mens viden med mellemlang halveringstid (måneder) bør trigge automatiske tidsbaserede re-scans. Statisk research uden decay-markering er en teknisk gæld, der skal adresseres via metadata (Miessler, 2026).

## Referencer

Anthropic. (n.d.). *Claude models documentation*. https://docs.anthropic.com/en/docs/about-claude/models
ArXiv. (n.d.). *Artificial intelligence (cs.AI) section*. https://arxiv.org/list/cs.AI/recent
Hacker News. (n.d.). *Algolia search for AI stories*. https://hn.algolia.com/
LMArena. (n.d.). *Chatbot arena leaderboard*. https://chat.lmsys.org/?leaderboard
OpenAI. (n.d.). *API pricing page*. https://openai.com/api/pricing/
Qdrant. (n.d.). *Release notes and updates*. https://github.com/qdrant/qdrant/releases
Reddit. (n.d.). *r/ClaudeAI community*. https://www.reddit.com/r/ClaudeAI/
Willison, S. (n.d.). *LLM and AI tooling log*. https://simonwillison.net/tags/llms/
