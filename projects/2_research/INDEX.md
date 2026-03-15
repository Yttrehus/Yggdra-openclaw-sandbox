# Research Architecture — INDEX

Samlet oversigt over /root/Yggdra/research/ (81 .md filer, ~28.000 linjer).
Formål: Hurtigt finde den rigtige fil uden at scanne mappen.

## Crown Jewels

| Fil | Linjer | Hvad | Key Insight |
|-----|--------|------|-------------|
| HOW_TO_BUILD_AGENTS.md | 1075 | Samlet bog-manuskript | Scaffolding leverer ~80% af værdien — modellen kun 20%. 95% af enterprise AI-pilots fejler fordi de ignorerer dette |
| LAYER1_PASS2_WITH_ABSTRACTS.md | 828 | AI Memory Systems survey | Qdrant er det rationelle valg for self-hosted solo-projekter under 100M vektorer |
| LAYER2_PASS1_SOURCES.md | 787 | Bred kildekortlægning | Troværdige kilder = uafhængige communities (r/LocalLLaMA, ANN-Benchmarks), ikke vendor-docs |
| PRE_DEEP_RESEARCH_REPORT.md | 752 | Snapshot før bog-start | Layer 1-2 besvarer "hvad findes" — Layer 3 (deep research) mangler for handlingsanvisende konklusioner |
| memory_bridge_research.md | 674 | Menneske↔AI hukommelse | Capture, storage og retrieval er tre separate designudfordringer — ikke ét samlet problem |
| agents_langgraph_deep_dive.md | 666 | LangGraph deep dive | LangGraph 1.0 erstatter flade ReAct-loops med eksplicit state-maskinekontrol over grene og cykler |
| RESEARCH_INDEX.md | ~200 | Legacy katalog | Erstattet af denne fil |

## Kategorier

### 1. Bog-kapitler (34 filer, ~14.000 linjer)

Hele manuskriptet til "How to Build AI Agents". Kapitel 1-10 + danske versioner (KAP1-2) + research-noter per kapitel.

| Kapitel | Hovedfil | Key Insight |
|---------|----------|-------------|
| CH1 Research Methodology | CH1_RESEARCH_METHODOLOGY.md | Seriøs research kræver ≥3 uafhængige primærkilder — de fleste stopper ved ét søgeresultat |
| CH2 Context Window | CH2_CONTEXT_WINDOW.md | Brug max 40% af annonceret window — kvalitetsklip er pludseligt, ikke gradvist |
| CH3 Claude Code | CH3_CLAUDE_CODE.md | 20K tokens høj-signal kontekst slår 1M tokens fyld. Kontekst > kapabilitet |
| CH4 LLM Landscape | CH4_LLM_LANDSCAPE.md | Anthropic+Google dominerer 2026 Elo. ChatGPT faldet fra 86,7% til 64,5% markedsandel |
| CH5 RAG & Embeddings | CH5_EMBEDDINGS_VECTOR_DBS.md | text-embedding-3-small er standard; voyage-3.5-lite er dark horse (bedre MTEB, 4× kontekst) |
| CH6 Agents & Automation | CH6_AGENTS_AUTOMATION.md | 8 cron-jobs med 0 fejl slår enhver LLM-agent til deterministiske opgaver |
| CH7 Prompting | CH7_ADVANCED_PROMPTING.md | "Context engineering" > "prompt engineering" — prompten er ~5% af kontekstvinduet |
| CH8 Tools Ecosystem | CH8_AI_TOOLS_ECOSYSTEM.md | 3-4 tools dækker 90% af behov — differentiator er workflow-integration, ikke modelintelligens |
| CH9 Setup & Infrastructure | CH9_SETUP_INFRASTRUCTURE.md | Over-investering i infra, under-investering i produktion. Bedste infra = den du glemmer |
| CH10 Visualization | CH10_VISUALIZATION_UNDERSTANDING.md | IBM Watson ($62M, 80% failure) var kommunikationsproblem — "understands" importerede forkerte forventninger |
| Danske versioner | KAP1+KAP2 | Danske oversættelser af CH1-2 |
| Samlet manuskript | HOW_TO_BUILD_AGENTS.md | Se Crown Jewels |

**Kronologi:** Bog-projektet startede feb 2026. CH1-CH10 skrevet i rækkefølge. Research-noter (ch7_, ch9_, ch10_) er baggrundsmateriale der informerede kapitlerne.

### 2. Memory & Autonomi Research (8 filer, ~4.000 linjer)

Kernen af Ydrasils hukommelsesarkitektur. Spænder fra akademisk AI-memory til praktisk session-resume.

| Fil | Linjer | Fokus | Key Insight |
|-----|--------|-------|-------------|
| ai_memory_research.md | 619 | AI Long-Term Memory | De fleste systemer implementerer kun én dimension — misser cross-session persistens |
| human_memory_research.md | 609 | Menneskehukommelse & AI | Glemsel er en feature — retrieval-baseret arkitektur slår total persistens |
| memory_bridge_research.md | 674 | Menneske↔AI bro | Capture, storage, retrieval = tre separate udfordringer |
| AI_MEMORY_SYSTEMS_SURVEY.md | 540 | AI Memory survey | Qdrant rationelt for self-hosted <100M vektorer |
| memory_autonomy_research_2026-02-23.md | ~400 | Mem0/LightRAG/OpenClaw | Mem0 bedste match til stack; OpenClaw-principper bedste arkitektoniske blueprint (tool fravalgt, principper adopteret) |
| context_window_workarounds_2026.md | ~380 | Context workarounds | "Lost in the middle" + cost-scaling → disk-offload + hierarkisk summarization |

**Vigtig beslutning (23/2-2026):** Mem0, LightRAG og GraphRAG fravalgt pga. svagt evidensgrundlag. OpenClaw-principper (heartbeat, hybrid search, temporal decay) adopteret i stedet.

### 3. Agent Research (6 filer, ~3.500 linjer)

Frameworks, evaluering, og implementation patterns for AI-agenter.

| Fil | Linjer | Fokus | Key Insight |
|-----|--------|-------|-------------|
| agents_langgraph_deep_dive.md | 666 | LangGraph arkitektur | State-maskinekontrol over grene og cykler — LangChains nye standard |
| agents_evaluation_observability.md | 639 | Agent eval | METR: devs troede de var 20-30% hurtigere med AI — var 19% *langsommere*. Self-report er ubrugelig |
| agents_framework_comparison.md | 546 | Framework sammenligning | CrewAI: dual-model (Crews+Flows) — mental model er organisatorisk, ikke programmessig |
| agents_context_engineering.md | 493 | Context Engineering | 100:1 input/output-ratio i produktion. Filsystemet som ekstern hukommelse er mest undervurderet |
| agent_implementation_notes.md | ~200 | Implementation noter | 80% tid på tool-definitions, 20% på agent-logik. Fejl-wrapping i tools er kritisk |

### 4. Surveys & Kildekortlægning (7 filer, ~4.500 linjer)

Brede undersøgelser der kortlægger felter systematisk.

| Fil | Linjer | Felt | Key Insight |
|-----|--------|------|-------------|
| LAYER1_PASS2_WITH_ABSTRACTS.md | 828 | AI Memory survey | Se Crown Jewels |
| LAYER2_PASS1_SOURCES.md | 787 | Kilder kortlægning | Se Crown Jewels |
| LAYER2_PASS2_VERIFICATION.md | 600 | Kildeverificering | Tier 1 = uafhængige communities, ikke autoritative vendors |
| brainmap_research_report.md | ~330 | Mind mapping | Brainmap ≠ mindmap: graf (krydsende associationer) > træ (hierarki) |
| brainmap_research_report_v2.md | ~350 | Brainmap v2 | GRINDE-frameworket (Justin Sung) = mest transferable system til personlig vidensstrukturering |
| knowledge_visualization_survey.md | ~320 | Knowledge Viz | Markedet skifter mod AI auto-generering, men forbliver hierarkisk — modsat hvad kognitionsvidenskab anbefaler |
| knowledge_visualization_survey_pass2.md | ~300 | Knowledge Viz pass 2 | Argument mapping (Toulmin) = manglende lag: gemmer *hvad* man ved, men ikke *hvorfor* |

### 5. Tools & Økosystem (7 filer, ~2.500 linjer)

Konkrete værktøjer evalueret i kontekst af Ydrasil.

| Fil | Linjer | Værktøj | Key Insight |
|-----|--------|---------|-------------|
| claude_code_ecosystem_2026.md | 740 | Claude Code økosystem | 25+ repos, 1.500+ skills kortlagt — identificerer gaps i Yggdra vs best practice |
| CLAUDE_CODE_BEST_PRACTICES.md | ~280 | Claude Code best practices | CLAUDE.md under 60 linjer er idealet — context window er den vigtigste ressource |
| AI_CLAUDE_ANTHROPIC_2026.md | ~240 | Anthropic & Claude | Opus 4.5 er 50-75% bedre til tool-calling ved samme pris |
| IMAGE_TOOLS_RESEARCH_2026.md | ~200 | Billedgenerering | Tre tiers: GPT Image 1 Mini, Midjourney, Stable Diffusion — billig iteration uden specialsetup |
| notion-best-practices.md | ~180 | Notion | Power-feature = Relations (vidensgraf). AI kun meningsfyldt på Business ($20/md) |
| whisper_pricing_2026.md | ~100 | Speech-to-Text | Groq Whisper 8-9× billigere end OpenAI ($4 vs $36/100h). Klar anbefaling |
| ai_tools_uge10_2026.md | ~150 | AI tools uge 10 | Context Mode MCP: 98% komprimering, 30min→3h sessioner, men virker ikke på MCP-responses |

### 6. Person-research (5 filer, ~1.200 linjer)

Dybe dyk i specifikke eksperters tankegang og metoder.

| Fil | Linjer | Person | Key Insight |
|-----|--------|--------|-------------|
| NATE_JONES_5_VIDEOER_2026-02.md | ~270 | Nate B. Jones | "Attention drowning" — signal drukner i støj. Separate collections er svaret |
| NATE_JONES_EXTRA_VIDEOER_2026-02.md | ~250 | Nate B. Jones | Timidity > fejl som risiko: byg mange ting hurtigt, acceptér fejl som læring |
| nate_jones_memory_video.md | ~200 | Nate Jones | Ingen generel algoritme for relevans — byg din egen hukommelsesarkitektur |
| armin_ronacher_agent_philosophy_2026.md | ~220 | Armin Ronacher | 4 tools (Read/Write/Edit/Bash) + state som filer > model-hukommelse |
| mario_zechner_pi_research_2026-03-06.md | ~230 | Mario Zechner | Bash-over-MCP er mere robust. Evidensbaseret minimalisme |

### 7. Metodologi (6 filer, ~1.800 linjer)

Hvordan man researcher, skriver, og auditerer.

| Fil | Linjer | Fokus | Key Insight |
|-----|--------|-------|-------------|
| academic_writing_standards.md | 680 | Akademisk skrivestil | APA 7th edition: forfatter-dato, hængende indrykning, DOI som https://doi.org/... |
| AI_WORKFLOW_RESEARCH_2026.md | 565 | Personal Knowledge Mgmt | Fabric (200+ patterns, CLI-first) = state-of-the-art; Miesslers PAI er næste lag |
| RESEARCH_METHODOLOGY_META.md | ~370 | Meta-research | Amatør vs professionel = struktur, ikke intelligens. Definér spørgsmål FØR data |
| AUDIT_FRAMEWORK_RESEARCH.md | ~200 | Audit-praksis | Mangler 3 dimensioner: sikkerhed, operational resilience, monitoring |
| research-methodology.md | ~150 | Methodology (kort) | Scoping Review (Arksey & O'Malley) = bedste default for solo-forskere |

### 8. Infrastruktur (3 filer, ~1.100 linjer)

Hardware, lokal AI, autonomi-opsætning.

| Fil | Linjer | Fokus | Key Insight |
|-----|--------|-------|-------------|
| LOCAL_AI_HARDWARE_OPTIONS_2026.md | 503 | Lokal AI hardware | Mac Mini M4 Pro 64GB (~21.300 DKK) eller brugt PC+RTX 3090 (~9.000 DKK) |
| autonomous_ai_setup.md | 450 | OpenClaw og autonomi | Memory tiers (hot/warm/cold) + hooks til episodisk log = scaffolding > model |
| LOCAL_AI_INFRASTRUCTURE_2026.md | ~290 | Lokal AI-infra | Scaffolding > Model: kontekststyring har større indflydelse end grundmodel |

### 9. Projekt-state (3 filer, ~1.000 linjer)

Snapshots af projektstatus på bestemte tidspunkter.

| Fil | Linjer | Snapshot | Key Insight |
|-----|--------|---------|-------------|
| PRE_DEEP_RESEARCH_REPORT.md | 752 | State før bog-start | Layer 1-2 afsluttet → 3 kernespørgsmål som fundament for Layer 3 |
| MASTER_PLAN.md | ~180 | Research Master Plan | Alle 10 kapitler skrevet. Advisor brain embeddet: 321 Nate Jones + 3.082 Miessler chunks |
| voice_app_project_state.md | ~100 | Voice App state | Hybrid D: voice→VPS(Groq)→Claude+Qdrant→ElevenLabs→headset. 10-15h daglig brug |

### 10. LaTeX/Build (15 filer)

Kompileringsartefakter for bog og rapporter. Ikke research-indhold.
Filer: .aux, .log, .out, .toc, .tex, .pdf + md_to_latex.py, prepare_for_pandoc.py, template.latex

## Hurtigreference

| Jeg vil... | Gå til... |
|------------|-----------|
| Forstå bogens struktur | HOW_TO_BUILD_AGENTS.md |
| Finde et specifikt kapitel | CH{1-10}_*.md |
| Researche AI memory | ai_memory_research.md → memory_bridge_research.md |
| Evaluere agent-frameworks | agents_framework_comparison.md → agents_langgraph_deep_dive.md |
| Finde kilder og eksperter | LAYER2_PASS1_SOURCES.md |
| Verificere en kilde | LAYER2_PASS2_VERIFICATION.md |
| Lære research-metodik | RESEARCH_METHODOLOGY_META.md |
| Se hvad der blev besluttet om memory | memory_autonomy_research_2026-02-23.md |
| Evaluere lokal AI hardware | LOCAL_AI_HARDWARE_OPTIONS_2026.md |
| Se Claude Code patterns | claude_code_ecosystem_2026.md |
| Forstå en persons tankegang | armin_ronacher_*, mario_zechner_*, NATE_JONES_* |
