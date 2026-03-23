---
title: Source Registry — Alle Videns-kilder
date: 2026-03-22
category: Videns-vedligeholdelse
status: audit-passed
---

# Source Registry — Alle Videns-kilder (marts 2026)

## Metadata
- **Emne:** Register over videnskilder
- **Kontekst:** Yggdra Projektet
- **Standard:** APA 7th
- **Status:** Færdig-auditeret

## 1. Aktive Kilder (automatiserede)

Yggdra anvender en række automatiserede kilder til at indsamle information om AI-udviklingen (Anthropic, n.d.; OpenAI, n.d.).

| Kilde | Type | Frekvens | Kvalitet (1-5) | Pipeline |
|-------|------|----------|----------------|----------|
| Anthropic SDK releases | GitHub | Daglig | 5 | ai_intelligence.py |
| Claude Code releases | GitHub | Daglig | 5 | ai_intelligence.py |
| HN AI stories | Web API | Daglig | 4 | ai_intelligence.py |
| arXiv cs.AI + cs.CL | Atom API | Daglig | 3 | ai_intelligence.py |
| Nate B Jones | YouTube RSS | Daglig | 5 | youtube_monitor.py |

## 2. Manglende Kilder (anbefalet tilføjelse)

For at sikre en fuldstændig dækning af markedet bør følgende kilder integreres i pipelinen:
1. **Blog RSS:** Officielle blogs fra Anthropic, OpenAI og Google DeepMind (Google DeepMind, n.d.).
2. **Pricing Pages:** Overvågning af prisændringer hos de største providers.
3. **LMArena:** Dynamisk tracking af model-benchmarks (LMSYS, 2026).

## 3. Konklusion og Indsigt

Systemet har god dækning af tekniske releases (GitHub), men mangler struktureret input fra officielle forretningsmæssige udmeldinger (blogs) og prisændringer. Ved at lukke dette gap reduceres risikoen for at handle på forældet viden (Miessler, 2026).

## Referencer

Anthropic. (n.d.). *Anthropic research*. https://www.anthropic.com/research/rss
ArXiv. (n.d.). *ArXiv API documentation*. https://arxiv.org/help/api/index
Google DeepMind. (n.d.). *DeepMind blog*. https://deepmind.google/blog/rss.xml
Hacker News. (n.d.). *Hacker News API*. https://github.com/HackerNews/API
Hugging Face. (n.d.). *Hugging Face blog*. https://huggingface.co/blog/feed.xml
OpenAI. (n.d.). *OpenAI blog*. https://openai.com/blog/rss/
Qdrant. (n.d.). *Qdrant documentation*. https://qdrant.tech/documentation/
Reddit. (n.d.). *Reddit API documentation*. https://www.reddit.com/dev/api/
Willison, S. (n.d.). *Simon Willison's weblog*. https://simonwillison.net/atom/everything/
