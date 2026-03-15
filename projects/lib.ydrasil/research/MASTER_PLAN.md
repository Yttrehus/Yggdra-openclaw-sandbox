# Research Master Plan

**Created:** 2026-02-09
**Purpose:** Build a complete AI Practitioner's Bible — Claude's third brain + Kris' handbook

---

## STATUS NOW

### What We HAVE Done
- [x] Nate Jones book: 453 YouTube transcripts → THE_BUILDERS_EDGE.md (41K words)
- [x] Daniel Miessler book: 3,082 sources → BECOME_YOURSELF.md (49K words)
- [x] Advisor Brain: Both books embedded in Qdrant (321 chunks)
- [x] Advisor identity in CLAUDE.md (always loaded)
- [x] Layer 1 research surveys (surface-level): memory systems, software engineering, data science
- [x] Layer 2 partial: sources + verification
- [x] Existing docs: PAI Blueprint, Telos, AI Architecture, LLM Overview
- [x] All 10 chapters written (English) ✅
- [x] Polish phase: Ch 1-2 rewritten Danish → English ✅
- [x] Polish phase: Ch 3 major revision (665 → ~287 lines, cut reference tables, added decision frameworks) ✅
- [x] Polish phase: Ch 4 trimmed (432 → ~277 lines, consolidated models, halved scaling section) ✅
- [x] Polish phase: "Our Setup" consistency verified across all chapters ✅
- [x] Polish phase: Decision trees verified in all chapters (Ch 1-10) ✅

### Handbook Chapters (AI Practitioner's Bible)

| # | Chapter | File | Lines | Status |
|---|---------|------|-------|--------|
| 1 | Research Methodology | `CH1_RESEARCH_METHODOLOGY.md` | ~224 | ✅ Polished (English) |
| 2 | Context Window | `CH2_CONTEXT_WINDOW.md` | ~211 | ✅ Polished (English) |
| 3 | Know Yourself (Claude Code) | `CH3_CLAUDE_CODE.md` | ~287 | ✅ Polished (major revision) |
| 4 | The LLM Landscape | `CH4_LLM_LANDSCAPE.md` | ~277 | ✅ Polished (trimmed) |
| 5 | RAG & Embeddings in Practice | `CH5_RAG_PRACTICE.md` | ~340 | ✅ Done |
| 6 | AI Agents & Automation | `CH6_AGENTS_PRACTICE.md` | ~340 | ✅ Done |
| 7 | Prompt Engineering | `CH7_PROMPTING_PRACTICE.md` | ~270 | ✅ Done |
| 8 | AI Tools & Ecosystem | `CH8_TOOLS_PRACTICE.md` | ~320 | ✅ Done |
| 9 | Setup & Infrastructure | `CH9_SETUP_INFRASTRUCTURE.md` | ~370 | ✅ Done |
| 10 | Visualization & Understanding | `CH10_VISUALIZATION_UNDERSTANDING.md` | ~295 | ✅ Done |

**Total estimated length:** ~2,934 lines (~50,000 words)

### Supporting Tasks
- [x] Embed completed chapters in Qdrant ✅ (132 chunks in advisor_brain)
- [x] Embed the finished handbook in advisor_brain ✅ (453 total: 146 Nate + 175 Miessler + 132 Bible)
- [x] Embed existing /research/ files ✅ (442 chunks from 26 files in docs collection)
- [x] Layer 2-5 research progression ✅ (superseded by book chapters — Ch 1-10 covers all topics deeper than Layer 1 surveys)

---

## BOOK IDENTITY

This book is Claude's **third brain** — alongside the Nate Jones book (judgment/strategy) and the Miessler book (purpose/meaning). It provides **self-awareness and capability knowledge**.

- **Primary function:** Operational knowledge base Claude uses when planning, researching, and building
- **Secondary function:** Readable guide for Kris to understand how Claude works and AI in general
- **Language:** English (all chapters)
- **Visual version:** Comes after content is complete (Napkin AI, diagrams, etc.)

---

## RESEARCH METHOD

Each chapter built with Ch 1 methodology:
1. Define precise questions
2. 3 parallel research agents (different angles)
3. Synthesize findings (neutral + strengths + weaknesses)
4. Verify key claims against primary sources
5. Distill to actionable chapter

---

**Last updated:** 2026-02-09
