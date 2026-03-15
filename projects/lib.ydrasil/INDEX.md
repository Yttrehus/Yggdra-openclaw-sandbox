# Ydrasil — Index

Alt data fra VPS-æraen (jan–feb 2026). Ikke bare en filliste — en guide til hvad der findes, hvad det handler om, og hvornår du griber til det.

---

## 1. Research (91 filer, [research/](research/))

Produceret jan–feb 2026 på VPS. Yttre + Claude byggede en 10-kapitel AI handbook, dyb agent-research, og systematisk videns-indsamling via Layer 1-5 metoden.

### Crown jewels

| Fil | Størrelse | Hvad | Hvornår du bruger den |
|-----|-----------|------|----------------------|
| [HOW_TO_BUILD_AGENTS.md](research/HOW_TO_BUILD_AGENTS.md) | 104K | Komplet practitioner's manual for AI agents — fra arkitektur til production | Når du bygger agent-systemer eller skills |
| [AI_MEMORY_SYSTEMS_SURVEY.md](research/AI_MEMORY_SYSTEMS_SURVEY.md) | 52K | Qdrant, ChromaDB, Pinecone, episodisk vs semantisk hukommelse | Hukommelsesarkitektur-beslutninger |
| [SOFTWARE_ENGINEERING_PRINCIPLES_SURVEY.md](research/SOFTWARE_ENGINEERING_PRINCIPLES_SURVEY.md) | 56K | Layer 1 bredde-research over SE principper | Fundamentale design-beslutninger |
| [YDRASIL_ATLAS.md](docs/YDRASIL_ATLAS.md) | 27K | Master reference for hele VPS-systemet — projekter, data, hooks, alt | Når du vil forstå VPS-æraen |

### AI Handbook (10 kapitler)

Hvert kapitel har en research-udgave + praksis-udgaver. CH5/6/8 har 3-4 varianter (theory, practice, production, antipatterns).

| Kapitel | Emne | Nøgleindsigt |
|---------|------|-------------|
| [CH1](research/CH1_RESEARCH_METHODOLOGY.md) | Research-metodik | "En anekdote er ikke evidens. Tre uafhængige kilder er." |
| [CH2](research/CH2_CONTEXT_WINDOW.md) | Context windows | GPT-4 bruger kun ~10% af 128K til reasoning. Resten er spildte tokens |
| [CH3](research/CH3_CLAUDE_CODE.md) | Claude Code | 20K high-signal context slår 1M stuffed window |
| [CH4](research/CH4_LLM_LANDSCAPE.md) | LLM-landskab | Industrien har ikke realiseret 10% af potentialet |
| [CH5](research/CH5_EMBEDDINGS_VECTOR_DBS.md) | Embeddings & RAG | 3 varianter: teori, RAG praksis, RAG produktion |
| [CH6](research/CH6_AGENTS_AUTOMATION.md) | Agents & automation | 3 varianter: teori (49K), praksis, produktion |
| [CH7](research/CH7_ADVANCED_PROMPTING.md) | Prompting | Teori + praksis + antipatterns |
| [CH8](research/CH8_AI_TOOLS_ECOSYSTEM.md) | Tools-økosystem | 2 teori-varianter + praksis |
| [CH9](research/CH9_SETUP_INFRASTRUCTURE.md) | Infrastruktur | Setup + produktion + antipatterns |
| [CH10](research/CH10_VISUALIZATION_UNDERSTANDING.md) | Visualisering | Kommunikation > dashboards |

### Agent-research

| Fil | Hvad |
|-----|------|
| [agents_context_engineering.md](research/agents_context_engineering.md) | Kontekst-styring i langkørende agents |
| [agents_framework_comparison.md](research/agents_framework_comparison.md) | LangChain vs LangGraph vs CrewAI vs Autogen |
| [agents_langgraph_deep_dive.md](research/agents_langgraph_deep_dive.md) | LangGraph-specifik deep dive |
| [agents_evaluation_observability.md](research/agents_evaluation_observability.md) | Hvordan evaluerer og overvåger du agents |
| [agent_implementation_notes.md](research/agent_implementation_notes.md) | Praktiske implementeringsnoter |
| [armin_ronacher_agent_philosophy_2026.md](research/armin_ronacher_agent_philosophy_2026.md) | Flask-skaberen om agent-filosofi |

### Hukommelse & vidensarkitektur

| Fil | Hvad |
|-----|------|
| [ai_memory_research.md](research/ai_memory_research.md) | State-of-the-art memory til LLM agents |
| [memory_bridge_research.md](research/memory_bridge_research.md) | Bridging mellem sessions |
| [memory_autonomy_research_2026-02-23.md](research/memory_autonomy_research_2026-02-23.md) | Autonom hukommelse |
| [human_memory_research.md](research/human_memory_research.md) | Kognitionsvidenskab → AI-design paralleller |
| [brainmap_research_report.md](research/brainmap_research_report.md) | Layer 3 deep research synthesis (v1 + v2) |
| [context_window_workarounds_2026.md](research/context_window_workarounds_2026.md) | Praktiske workarounds for context limits |

### Visualisering & vidensstyring

| Fil | Hvad |
|-----|------|
| [knowledge_visualization_survey.md](research/knowledge_visualization_survey.md) | Hvad findes i knowledge viz + mindmapping (pass 1 + 2) |
| [ch10_visualization_tools_research.md](research/ch10_visualization_tools_research.md) | Værktøjer til AI-system visualisering |
| [ch10_explainability_research.md](research/ch10_explainability_research.md) | AI explainability-spektrum |

### Nate Jones & Daniel Miessler

| Fil | Hvad |
|-----|------|
| [NATE_JONES_5_VIDEOER_2026-02.md](research/NATE_JONES_5_VIDEOER_2026-02.md) | 5 kernevideoer analyseret |
| [NATE_JONES_EXTRA_VIDEOER_2026-02.md](research/NATE_JONES_EXTRA_VIDEOER_2026-02.md) | Ekstra videoer |
| [nate_jones_memory_video.md](research/nate_jones_memory_video.md) | Specifik video om AI-hukommelse |
| [LOCAL_AI_HARDWARE_OPTIONS_2026.md](research/LOCAL_AI_HARDWARE_OPTIONS_2026.md) | Lokal AI hardware — skrevet til ikke-teknisk bruger |
| [LOCAL_AI_INFRASTRUCTURE_2026.md](research/LOCAL_AI_INFRASTRUCTURE_2026.md) | OpenClaw video-analyse |

### Systematisk research (Layer 1-2)

| Fil | Hvad |
|-----|------|
| [LAYER1_PASS2_WITH_ABSTRACTS.md](research/LAYER1_PASS2_WITH_ABSTRACTS.md) | Anden gennemgang med abstracts per kategori |
| [LAYER2_PASS1_SOURCES.md](research/LAYER2_PASS1_SOURCES.md) | Kilder identificeret |
| [LAYER2_PASS2_VERIFICATION.md](research/LAYER2_PASS2_VERIFICATION.md) | Kildeverifikation |

### Diverse research

| Fil | Hvad |
|-----|------|
| [CLAUDE_CODE_BEST_PRACTICES.md](research/CLAUDE_CODE_BEST_PRACTICES.md) | Samlet best practices fra Anthropic + community |
| [claude_code_ecosystem_2026.md](research/claude_code_ecosystem_2026.md) | 43K — komplet Claude Code økosystem-oversigt |
| [DATA_SCIENCE_ENGINEERING_SURVEY.md](research/DATA_SCIENCE_ENGINEERING_SURVEY.md) | Data science/engineering koncepter for personligt AI-system |
| [AI_WORKFLOW_RESEARCH_2026.md](research/AI_WORKFLOW_RESEARCH_2026.md) | AI workflow patterns |
| [AI_CLAUDE_ANTHROPIC_2026.md](research/AI_CLAUDE_ANTHROPIC_2026.md) | Claude i Excel, nyheder jan 2026 |
| [autonomous_ai_setup.md](research/autonomous_ai_setup.md) | Hvad andre gør — autonom AI setup |
| [PRE_DEEP_RESEARCH_REPORT.md](research/PRE_DEEP_RESEARCH_REPORT.md) | Claude Opus deep research rapport |
| [whisper_pricing_2026.md](research/whisper_pricing_2026.md) | STT-tjenester sammenlignet for 100-200 timer audio |
| [voice_app_project_state.md](research/voice_app_project_state.md) | Voice pipeline projekt-status |
| [mario_zechner_pi_research_2026-03-06.md](research/mario_zechner_pi_research_2026-03-06.md) | Pi-baseret research |
| [IMAGE_TOOLS_RESEARCH_2026.md](research/IMAGE_TOOLS_RESEARCH_2026.md) | Gratis billedværktøjer |
| [notion-best-practices.md](research/notion-best-practices.md) | Notion best practices |
| [research-methodology.md](research/research-methodology.md) | Meta: research-metodik |
| [RESEARCH_METHODOLOGY_META.md](research/RESEARCH_METHODOLOGY_META.md) | Meta-research fra 14+ kilder |
| [AUDIT_FRAMEWORK_RESEARCH.md](research/AUDIT_FRAMEWORK_RESEARCH.md) | Audit-framework evaluering |
| [academic_writing_standards.md](research/academic_writing_standards.md) | Reference for omskrivning af practitioner's manual |
| [MASTER_PLAN.md](research/MASTER_PLAN.md) | Oprindelig masterplan |
| [RESEARCH_INDEX.md](research/RESEARCH_INDEX.md) | Fuld kategoriseret oversigt over al research |

---

## 2. Docs (41 filer, [docs/](docs/))

Interne dokumenter produceret på VPS. Dagbog, profiler, audits, system-dokumentation.

### Kernedokumenter — start her

| Fil | Størrelse | Hvad | Hvornår |
|-----|-----------|------|---------|
| [YDRASIL_ATLAS.md](docs/YDRASIL_ATLAS.md) | 27K | Alt i Yggdra: projekter, data, hooks, principper | Forstå VPS-æraen |
| [DAGBOG.md](docs/DAGBOG.md) | 25K | Daglig arbejdsjournal — beslutninger, mønstre, tanker | Forstå hvorfor ting blev gjort |
| [KRIS_KOMPLET_AI_BIOGRAFI.md](docs/KRIS_KOMPLET_AI_BIOGRAFI.md) | 39K | Fra Gandalf til Ydrasil — fuld AI-rejse | Kontekst om hvem Yttre er |
| [TELOS.md](docs/TELOS.md) | 11K | Hvem du er, hvad du vil, hvorfor — PAI fundament | Identitet og retning |
| [GDRIVE_OVERBLIK.md](docs/GDRIVE_OVERBLIK.md) | 29K | Komplet scan af Google Drive (1518 filer) | Finde ting i GDrive |

### Audits (system-evalueringer)

| Fil | Dato | Type |
|-----|------|------|
| [AUDIT_2026-02-01.md](docs/AUDIT_2026-02-01.md) | 1. feb | Intern audit: filer, scripts, services, docs, hooks |
| [AUDIT_2026-02-03.md](docs/AUDIT_2026-02-03.md) | 3. feb | 7-dimensions framework + kritisk re-evaluering |
| [AUDIT_2026-02-10.md](docs/AUDIT_2026-02-10.md) | 10. feb | Red Team / Blue Team / Neutral — 8 dimensioner |
| [AUDIT_PLAN_2026-02-12.md](docs/AUDIT_PLAN_2026-02-12.md) | 12. feb | Audit-plan |
| [AUDIT_SESSION2_20260213.md](docs/AUDIT_SESSION2_20260213.md) | 13. feb | 12 min research-session |

### Profiler & identitet

| Fil | Hvad |
|-----|------|
| [KRIS_PROFILE.md](docs/KRIS_PROFILE.md) | Profil skrevet af Claude Opus |
| [KRIS_BRAIN_ANALYSE.md](docs/KRIS_BRAIN_ANALYSE.md) | Kognitiv analyse |
| [TELOS_BILAG.md](docs/TELOS_BILAG.md) | Rå udtalelser brugt til TELOS |
| [VOICE_DIARY_20260213_ANALYSE.md](docs/VOICE_DIARY_20260213_ANALYSE.md) | 45 min voice diary analyseret |

### Transport & system

| Fil | Hvad |
|-----|------|
| [TRANSPORTINTRA_PROFIL.md](docs/TRANSPORTINTRA_PROFIL.md) | TransportIntra v3.0 (endelig) |
| [TRANSPORTINTRA_REDESIGN.md](docs/TRANSPORTINTRA_REDESIGN.md) | Redesign-plan |
| [AI_ARKITEKTUR.md](docs/AI_ARKITEKTUR.md) | Agentic workflow-mål |
| [ARCHITECTURE_CONTINUOUS_MEMORY.md](docs/ARCHITECTURE_CONTINUOUS_MEMORY.md) | Continuous memory design |
| [PAI_BLUEPRINT.md](docs/PAI_BLUEPRINT.md) | Miessler PAI v2 tilpasset |
| [PLANTEGNING.md](docs/PLANTEGNING.md) | System-plantegning v0.1 |
| [PC_SETUP.md](docs/PC_SETUP.md) | Lenovo X1 Carbon hardware |

### API & tools

| Fil | Hvad |
|-----|------|
| [GOOGLE_CLOUD_API_KOMPENDIUM.md](docs/GOOGLE_CLOUD_API_KOMPENDIUM.md) | 28K — komplet Google Cloud API guide |
| [GOOGLE_TASKS_MANUAL.md](docs/GOOGLE_TASKS_MANUAL.md) | Google Tasks manual |
| [LLM_OVERSIGT.md](docs/LLM_OVERSIGT.md) | LLM priser, context, typer |
| [TOKEN_OPTIMIZATION.md](docs/TOKEN_OPTIMIZATION.md) | Token-optimering |

### Rapporter & analyse

| Fil | Hvad |
|-----|------|
| [NATE_JONES_ANALYSE.md](docs/NATE_JONES_ANALYSE.md) | 61K — dyb analyse af Nate Jones videoer |
| [RAPPORT_MED_ANALYSE_20260213.md](docs/RAPPORT_MED_ANALYSE_20260213.md) | 36K rapport med analyse |
| [SAMLET_RAPPORT_20260213.md](docs/SAMLET_RAPPORT_20260213.md) | 21K samlet rapport |
| [RESEARCH_WORKFLOWS.md](docs/RESEARCH_WORKFLOWS.md) | Multi-agent research patterns |
| [VOICE_ASSISTANT_RESEARCH.md](docs/VOICE_ASSISTANT_RESEARCH.md) | Wake word engines, on-device STT |

### Diverse

| Fil | Hvad |
|-----|------|
| [CHATLOG.md](docs/CHATLOG.md) | VPS chatlog (ældre format) |
| [SESSION_LOG.md](docs/SESSION_LOG.md) | Auto-genereret sessionslog |
| [HANDLINGSPLAN.md](docs/HANDLINGSPLAN.md) | Handlingsplan baseret på videoer |
| [IDEAS.md](docs/IDEAS.md) | Idé-parkering |
| [MANUAL.md](docs/MANUAL.md) | Yggdra manual (levende dokument) |

---

## 3. VPS Projekter (9 stk, `/root/Yggdra/projects/`)

Alle har CONTEXT.md. Tilgås via `ssh vps "cat /root/Yggdra/projects/<navn>/CONTEXT.md"`.

| Projekt | Status | Hvad | Nøgledetalje |
|---------|--------|------|-------------|
| **transport** | PRODUKTION | Webapp-klon af TransportIntra for rute 256 | Live app — ændringer er live. UI/UX partial, GPS/diesel todo |
| **assistent** | Partial | AI personlig assistent (mail, kalender, filer) | Hotmail autosort kører. Kalender, proaktivitet: todo |
| **automation** | Partial | Pipelines, triggers, cron jobs | Voice pipeline virker. Token-fri pipelines + hooks: todo |
| **arkitektur** | Under revision | System, filer, hukommelse, infrastruktur | Filstruktur + CLAUDE.md revideres. HOT/WARM/COLD hukommelse partial |
| **forskning** | Partial | Research-pipeline, Layer 1-5, bog-projekt | 60+ markdown-filer, Layer 1-2 done. ChatGPT 434MB export ubehandlet |
| **notion** | Ikke startet | Notion som visuelt lag oven på Yggdra | MCP-integration planlagt |
| **rejse** | Ikke startet | Planlægning og booking | Alt todo |
| **bogfoering** | Ikke startet | Økonomi, skat, fakturering | Alt todo |
| **research-architecture** | Ikke startet | Meta-forskning: metoder, frameworks, kvalitetskriterier | Scope defineret, intet implementeret |

---

## 4. Qdrant (7 collections, 84.210 vektorer)

**Adgang:** `ssh vps` (åbner tunnel) → `ctx "query" --limit 5` fra Git Bash.
**Embedding:** text-embedding-3-small (1536 dim, cosine). Alle collections bruger samme model.

| Collection | Points | Payload-keys | Hvad det indeholder | Eksempel-query |
|------------|--------|-------------|---------------------|---------------|
| **sessions** | 42.106 | summary, raw_preview, date, source_file | Tmux session-logs med AI-genererede summaries. Dækker alt VPS-arbejde | `ctx "voice pipeline setup"` |
| **routes** | 40.053 | (rutedata) | TransportIntra stops, adresser, GPS-koordinater, sortering | `ctx "rute 256" --limit 3` |
| **docs** | 1.169 | source, file, header, content, summary | Embeddings af docs/-filerne. Sandsynligt overlap med lokale kopier | `ctx "arkitektur hukommelse"` |
| **advisor_brain** | 453 | type, author, book, chapter, section, text | Nate Jones videoer + Daniel Miessler frameworks + bog-kapitler | `ctx "prompting best practices"` |
| **knowledge** | 246 | source, substack, title, url, date, text | Nate Jones Substack-artikler (chunked) | `ctx "AI career advice"` |
| **miessler_bible** | 102 | (Miessler PAI) | Daniel Miessler PAI v2 framework komplet | `ctx "personal AI architecture"` |
| **conversations** | 81 | role, content, date, source | Tidlige chatlogs (pre-Claude Code æra). Kræver `fastembed` | Historisk reference |

---

## 5. VPS Sessions (131 JSONL, [sessions/](sessions/))

Claude Code sessions fra VPS, 11. feb – ca. 2. mar 2026. Processeret til [vps-chatlog.md](vps-chatlog.md) (49K linjer).

| Stat | Værdi |
|------|-------|
| JSONL-filer | 131 |
| Parsed beskeder | 3.861 |
| Sektioner (90-min gap) | 77 |
| Subagent JSONL | 781 (ikke processeret) |

**vps-chatlog.md** er den læsbare udgave — søg der i stedet for at parse JSONL.

---

## 6. VPS Data (`/root/Yggdra/data/`)

Tilgås via `ssh vps "ls /root/Yggdra/data/<mappe>"`. Ikke downloadet lokalt (for stort/operationelt).

| Mappe/fil | Hvad |
|-----------|------|
| routes/ | Rute-CSV'er og JSON |
| api_logs/ | TransportIntra API logs |
| episodes.jsonl | Episodisk hukommelse (events over tid) |
| CREDENTIALS.md | API-nøgler (downloadet til lokal `data/`) |
| voice_memos/ | Rå voice memos |
| voice_pipeline_state.json | Pipeline-tilstand |
| gmail/ | Gmail-data |
| youtube/ | YouTube-data |
| nate_transcripts_*.txt | Nate Jones transskriptioner (30 videoer) |
| miessler_bible/ | Miessler-kildemateriale |
| mindmaps/ | Genererede mindmaps |
| clusters/ | Klynge-analyser |
| checkpoints/ | VPS session checkpoints |
| audits/ | Audit-resultater |
| atlas_pdf/ | PDF-versioner af atlas |
| raw/ | Rå importerede data |
| gdrive_import/ | Google Drive import (1.1 GB — ubehandlet) |
| substack/ | Substack-artikler |
| telos/ | TELOS-relateret data |
| intelligence/ | AI intelligence pipeline data |
| uploads/, exports/, inbox/ | Diverse I/O |

---

## 7. VPS Scripts (67 Python scripts, `/root/Yggdra/scripts/`)

Tilgås via `ssh vps "ls /root/Yggdra/scripts/"`. Embeddings, automation, operationelle scripts. Ikke downloadet — kører på VPS.

---

## Hurtigreference

| Jeg vil... | Gå til |
|------------|--------|
| Forstå VPS-systemet | [YDRASIL_ATLAS.md](docs/YDRASIL_ATLAS.md) |
| Bygge agents | [HOW_TO_BUILD_AGENTS.md](research/HOW_TO_BUILD_AGENTS.md) |
| Forstå hukommelsesarkitektur | [AI_MEMORY_SYSTEMS_SURVEY.md](research/AI_MEMORY_SYSTEMS_SURVEY.md) |
| Læse hvad der skete dag for dag | [DAGBOG.md](docs/DAGBOG.md) |
| Forstå hvem Yttre er (AI-kontekst) | [KRIS_KOMPLET_AI_BIOGRAFI.md](docs/KRIS_KOMPLET_AI_BIOGRAFI.md) |
| Søge i VPS-viden semantisk | `ctx "dit spørgsmål"` |
| Finde en specifik VPS-session | Søg i [vps-chatlog.md](vps-chatlog.md) |
| Se TransportIntra API | `ssh vps "cat /root/Yggdra/data/TRANSPORTINTRA_API_REFERENCE.md"` |
| Finde noget i Google Drive | [GDRIVE_OVERBLIK.md](docs/GDRIVE_OVERBLIK.md) |
| Forstå identitet og retning | [TELOS.md](docs/TELOS.md) |
