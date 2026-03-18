# Layer 1 Pass 1: Knowledge Visualization & Digital Mind Mapping Survey

**Date:** 2026-02-17
**Purpose:** Broad survey of what exists in practical knowledge visualization and digital mind mapping
**Scope:** Tools, methods, libraries, and research relevant to building a personal "brainmap"

---

## 1. Digital Mind Mapping Tools

Traditional mind mapping software for creating hierarchical, radial idea structures.

| Tool | What It Is | Key Differentiator | Brainmap Relevance |
|------|-----------|-------------------|-------------------|
| **MindMeister** | Web-based collaborative mind mapper with real-time editing. Easiest starting point, generous free tier. | Real-time collaboration, clean UI | Low — too simple/hierarchical for a personal AI brainmap |
| **XMind** | Desktop-focused mind mapper producing polished, presentation-ready maps. | Visual polish, export quality | Low — static output, no programmatic access |
| **Miro** | Collaborative whiteboard platform with mind mapping as one of many capabilities. | Team workshops, infinite canvas | Medium — infinite canvas concept is relevant |
| **Mapify** | AI-powered tool that converts PDFs, videos, documents into mind maps automatically. | Content-to-map conversion (PDF, YouTube, etc.) | High — auto-structuring content is directly relevant |
| **GitMind** | Free AI mind mapper that can summarize articles, generate maps from topics, extract YouTube transcripts. | Free + AI generation | Medium — good feature set but closed platform |
| **EdrawMind** | AI-powered outliner that transforms scattered thoughts into organized knowledge systems. | AI outlines + summaries | Medium — organization concept is relevant |

**Key insight:** The market is shifting hard toward AI-assisted generation (content in, map out). The global mind-mapping software market is projected to reach USD 6.3B by 2032. But most tools remain hierarchical (tree-shaped) rather than graph-shaped.

**Sources:** [Storyflow Best Mind Mapping 2025](https://storyflow.so/blog/best-mind-mapping-tools-2025), [Digital Project Manager AI Mind Mapping 2026](https://thedigitalprojectmanager.com/tools/best-ai-mind-mapping-tools/), [Mapify](https://mapify.so/), [XMind vs Miro](https://xmind.app/xmind-vs-miro/)

---

## 2. Knowledge Graphs

Structured representations where entities (nodes) connect through typed relationships (edges), enabling semantic queries and reasoning.

| Tool/Concept | What It Is | Brainmap Relevance |
|-------------|-----------|-------------------|
| **Neo4j** | Leading graph database. Index-free adjacency for fast traversal. Supports RDF/SPARQL. v5.21 is current production standard. | High — production-grade graph storage for personal knowledge |
| **GraphRAG** | Architecture pattern using knowledge graphs as retrieval/reasoning layer for LLMs. FalkorDB achieved 90% hallucination reduction vs traditional RAG. | Very High — directly relevant to AI-powered personal brainmap |
| **LightRAG** | Lightweight alternative to GraphRAG. Comparable accuracy with 10x token reduction through dual-level retrieval. Released Oct 2024. | High — practical for personal scale |
| **Graphiti (Zep)** | Open-source framework for building real-time knowledge graphs for AI agents. | High — designed exactly for AI agent memory |
| **PersonaAgent** | Research system integrating persona prompts + knowledge graph + GraphRAG for personalized AI. | Very High — academic validation of the personal brainmap concept |
| **Semantic Web / JSON-LD / RDF** | Standards for machine-readable metadata. Enables interoperability between knowledge systems. | Medium — useful for data portability, overkill for personal use |

**Key insight:** GraphRAG is the hottest intersection — combining knowledge graphs with LLM retrieval. Neo4j released LLM Knowledge Graph Builder in 2025 for auto-constructing graphs from text. The personal AI assistant use case is being actively researched (PersonalAI, PersonaAgent papers on arXiv).

**Sources:** [Neo4j Knowledge Graph](https://neo4j.com/use-cases/knowledge-graph/), [Personal Knowledge Graphs: Notes to Insights](https://dasroot.net/posts/2025/12/personal-knowledge-graphs-notes-insights/), [AI-Enhanced Personal Knowledge Graphs](https://aicompetence.org/ai-enhanced-personal-knowledge-graphs/), [Graphiti on GitHub](https://github.com/getzep/graphiti), [PersonaAgent arXiv](https://arxiv.org/html/2511.17467)

---

## 3. Zettelkasten Method (Niklas Luhmann)

A note-taking methodology based on atomic, interconnected notes rather than hierarchical filing.

| Aspect | Details |
|--------|---------|
| **Origin** | Niklas Luhmann, German sociologist. 90,000+ index cards. Produced 70 books and 400+ articles. |
| **Core principle** | Each note is atomic (one idea), uniquely addressed, and linked to other notes. The network grows organically through connections, not categories. |
| **Digital tools** | Obsidian, Roam Research, Logseq all implement Zettelkasten principles digitally. |
| **Relation to mind mapping** | Mind maps are top-down (central idea radiates outward). Zettelkasten is bottom-up (notes accumulate and connections emerge). They're complementary, not competing. |
| **Key researcher** | Sonke Ahrens — "How to Take Smart Notes" (2017), the modern Zettelkasten bible. |

**Key insight:** Zettelkasten's bottom-up emergence is more aligned with how a personal brainmap should work than top-down mind mapping. The method proves that small atomic units + rich linking = powerful knowledge system. This is the intellectual foundation for graph-based PKM tools.

**Sources:** [Zettelkasten.de Introduction](https://zettelkasten.de/introduction/), [Sloww Zettelkasten 101](https://www.sloww.co/zettelkasten/), [Luhmann's Original Method](https://www.ernestchiang.com/en/posts/2025/niklas-luhmann-original-zettelkasten-method/)

---

## 4. Personal Knowledge Management (PKM) Systems

Frameworks and tools for capturing, organizing, and retrieving personal knowledge.

| System/Framework | What It Is | Brainmap Relevance |
|-----------------|-----------|-------------------|
| **Building a Second Brain (Tiago Forte)** | Methodology using PARA (Projects, Areas, Resources, Archives) to organize digital knowledge. Book published 2022. | Medium — good organizational framework but hierarchical, not graph-based |
| **PARA Method** | Four containers: Projects (active), Areas (ongoing), Resources (reference), Archives (done). | Medium — useful classification layer on top of a graph |
| **CODE Method** | Capture, Organize, Distill, Express — Forte's workflow for processing information. | Medium — workflow pattern applicable to any system |
| **Notion** | All-in-one workspace with databases, pages, templates. Document-based, hierarchical. | Low — powerful but not graph-native |
| **Kosmik** | Visual PKM combining spatial canvas with document management. Privacy-focused. | High — spatial + documents is the right direction |

**Key insight:** PKM is evolving from "Building a Second Brain" (hierarchical, folder-based) toward "Personal AI Companion" (graph-based, AI-augmented). A 2025 ACM paper explicitly traces this evolution: PKM -> Second Brain -> Personal AI Companion. Privacy-first, local-first is a growing movement.

**Sources:** [Building a Second Brain](https://www.buildingasecondbrain.com/), [Forte Labs 4 Levels of PKM](https://fortelabs.com/blog/the-4-levels-of-personal-knowledge-management/), [ACM: From PKM to Personal AI Companion](https://dl.acm.org/doi/10.1145/3688828.3699647), [Kosmik Best PKM Apps](https://www.kosmik.app/blog/best-pkm-apps)

---

## 5. Graph-Based Note-Taking

Tools that treat notes as nodes in a graph with bidirectional links, enabling non-linear knowledge exploration.

| Tool | What It Is | Key Feature | Brainmap Relevance |
|------|-----------|-------------|-------------------|
| **Obsidian** | Local-first markdown editor with graph view. Plugin ecosystem of 1500+. | Best graph visualization of any note tool. Local files = full data ownership. | High — proven graph-based PKM, but visualization is read-only |
| **Roam Research** | Pioneered bidirectional linking and block-level references. Daily notes workflow. | Block-level transclusion, everything is a graph node | Medium — innovative concepts but closed platform, $15/mo |
| **Logseq** | Open-source outliner with graph view. Block-based like Roam but free. | Open source, daily journal workflow, block-level linking | High — open source + graph + local-first |
| **Heptabase** | Visual-first PKM with spatial whiteboards. Cards on a canvas with connections. | Spatial canvas — arrange ideas like sticky notes on a wall | Very High — closest existing tool to a "brainmap" concept |
| **Scrintal** | Visual board-based notes with bidirectional links. Designed for researchers/writers. | Visual boards + deep linking, recently redesigned UI | High — visual thinking + knowledge management |
| **InfraNodus** | Text network analysis tool that visualizes PKM knowledge graphs from Obsidian/Roam/Logseq. | Finds gaps and clusters in existing knowledge graphs | High — analytical layer on top of existing notes |

**Key insight:** Heptabase and Scrintal represent the frontier — spatial canvas + graph connections + writing tools. Obsidian has the largest ecosystem but its graph view is more decorative than functional. The real innovation is happening in visual-spatial tools.

**Sources:** [Obsidian vs Logseq 2025](https://www.glukhov.org/post/2025/11/obsidian-vs-logseq-comparison/), [InfraNodus PKM Visualization](https://infranodus.com/use-case/visualize-knowledge-graphs-pkm), [Heptabase Alternatives](https://toolfinder.co/alternatives/heptabase), [Scrintal vs Heptabase](https://scrintal.com/comparisons/heptabase-alternative), [Visual Modelling with Heptabase & Scrintal](https://medium.com/pkm-in-the-wild/visual-modelling-with-heptabase-scrintal-4c0cadf83377)

---

## 6. Interactive Web-Based Visualization Libraries

JavaScript libraries for building custom graph/network visualizations in the browser.

| Library | What It Is | Performance | Brainmap Relevance |
|---------|-----------|-------------|-------------------|
| **D3.js** | The foundational data visualization library. SVG-based. Maximum customization, steep learning curve. | Good up to ~10K elements (SVG limit) | High — ultimate flexibility but requires significant dev effort |
| **Cytoscape.js** | Graph theory library from University of Toronto. Built-in graph algorithms (shortest path, clustering, etc.). | Good up to ~10K elements | Very High — graph algorithms + visualization in one package |
| **Sigma.js** | WebGL-powered graph renderer designed for large networks. | Handles 100K edges easily. Struggles at 50K+ with force layout. | High — best performance for large graphs in browser |
| **vis.js** | Easy-to-use network visualization. Rich docs. | Moderate (canvas-based) | Low — mostly deprecated, avoid for new projects |
| **React Flow** | React library for node-based UIs, workflow builders, visual editors. | Good for interactive editors | Very High — perfect for building an editable brainmap UI |
| **Rete.js** | Framework for visual programming interfaces. Supports React, Vue, Angular, Svelte. | Good for editor UIs | High — node-based editor paradigm fits brainmap editing |
| **Three.js / WebGL** | 3D rendering in browser. Used for 3D graph visualization. | Excellent for large datasets | Medium — 3D adds complexity without clear knowledge benefit |

**Key insight:** For a personal brainmap, the sweet spot is: **Cytoscape.js** for graph logic/algorithms + **React Flow** for the interactive editor UI. Sigma.js if you need to scale to very large graphs. D3.js is overkill for this use case (too low-level). vis.js is deprecated.

**Sources:** [Top 10 JS Libraries for Knowledge Graph Visualization](https://www.getfocal.co/post/top-10-javascript-libraries-for-knowledge-graph-visualization), [Cytoscape.js](https://js.cytoscape.org/), [Sigma.js](https://www.sigmajs.org/), [React Flow](https://reactflow.dev), [Rete.js](https://retejs.org/), [Best Methods for Large Network Graphs](https://weber-stephen.medium.com/the-best-libraries-and-methods-to-render-large-network-graphs-on-the-web-d122ece2f4dc)

---

## 7. AI-Assisted Mind Mapping (State of the Art 2025-2026)

Current capabilities of AI in automated knowledge structuring and visualization.

| Capability | Current State | Tool Examples |
|-----------|--------------|---------------|
| **Content-to-map** | Mature. PDFs, videos, articles auto-converted to maps. | Mapify, GitMind, MindMap AI |
| **AI structure suggestion** | Emerging. AI proposes branch organization and connections. | EdrawMind, Creately VIZ, Ayoa |
| **Knowledge graph from text** | Production-ready. LLMs extract entities and relationships from unstructured text. | Neo4j LLM KG Builder, Graphiti |
| **Graph-based RAG** | Active research. Knowledge graphs as retrieval layer for LLMs. | GraphRAG (Microsoft), LightRAG, FalkorDB |
| **Personalized AI memory** | Early research. Knowledge graphs storing user interaction history for personalized responses. | PersonaAgent, PersonalAI (arXiv) |
| **Auto-linking concepts** | Emerging. AI identifies connections between existing notes. | Mem.ai, Reflect |

**Key insight:** The pieces exist but nobody has assembled them into a coherent personal brainmap system. Content-to-graph extraction works. Graph-based RAG works. Personalized AI memory is being researched. The opportunity is integration — building the connective tissue between these capabilities.

**Sources:** [Neo4j LLM KG Builder 2025](https://neo4j.com/blog/developer/llm-knowledge-graph-builder-release/), [GraphRAG for Personalized Assistants](https://medium.com/@ema.ilic9/graphrag-for-personalized-assistants-fcd677253a9f), [Affordable AI Assistants with KG of Thoughts](https://graphrag.com/appendices/research/2504.02670/)

---

## 8. Multi-Dimensional Knowledge Representation

Going beyond 2D graphs to represent knowledge in richer dimensional spaces.

| Approach | What It Is | Brainmap Relevance |
|----------|-----------|-------------------|
| **Embedding spaces** | Representing concepts as vectors in high-dimensional space (e.g., OpenAI embeddings in 1536 dimensions). Similar concepts cluster together. | Very High — already using this with Qdrant. Foundation for semantic search. |
| **Spatial computing / AR/VR** | Visualizing data in 3D/immersive environments. Apple Vision Pro, Meta Quest driving interest. | Low for now — Kris uses phone, not headset |
| **Multidimensional scaling (MDS)** | Reducing high-dimensional data to 2D/3D for visualization while preserving distances. t-SNE, UMAP are popular methods. | High — can visualize embedding clusters as a 2D map |
| **Hyperbolic geometry** | Representing hierarchical data in hyperbolic space (more room for branching than Euclidean). Used by Poincare embeddings. | Medium — elegant for hierarchies but adds complexity |
| **Semantic zoom** | Different detail levels at different zoom levels (city -> neighborhood -> building analogy). | Very High — essential for navigating large knowledge spaces |

**Key insight:** The most practical approach is: store knowledge as embeddings (already done with Qdrant), project to 2D using UMAP/t-SNE for visualization, and implement semantic zoom for navigation. No need for VR/AR. The phone screen is the constraint.

**Sources:** [Spatial Computing for Data Visualization](https://www.csm.tech/americas/insights/blogdetails/spatial-computing-for-data-visualization-turning-complex-data-into-immersive-insights), [Multidimensional Data in Spatial Interface](https://medium.com/@HolographicInterfaces/multidimdata-857a7563001a), [ACM Survey on Multidimensional Scaling](https://dl.acm.org/doi/10.1145/3178155)

---

## 9. Spaced Repetition + Mind Maps

Combining visual knowledge organization with optimized retention algorithms.

| Tool/Concept | What It Is | Brainmap Relevance |
|-------------|-----------|-------------------|
| **Traverse** | The only tool that integrates mind mapping + flashcards + spaced repetition in one system. Imports Anki decks. | High — proves the concept works. Mind map for understanding, spaced repetition for retention. |
| **Anki** | Open-source flashcard app using spaced repetition algorithm (SM-2 variant). 10M+ users. | Medium — retention engine, but no graph/visual component |
| **WisdomTree** | TheBrain plugin that adds spaced repetition to mind map nodes. | Medium — niche but validates the intersection |
| **RemNote** | Note-taking + flashcard tool with automatic card generation from notes. | Medium — closest to automated spaced repetition from knowledge |

**Key insight:** Traverse is the proof of concept: mind map first (build understanding), then create flashcards from map nodes (build retention). For a brainmap, the principle is: visualization aids comprehension, spaced repetition aids retention. Both are needed. The practical integration is: flag important nodes for review, schedule them using SM-2 or FSRS algorithm.

**Sources:** [Traverse](https://traverse.link/), [Traverse at Ness Labs](https://nesslabs.com/traverse-featured-tool), [WisdomTree on TheBrain Forums](https://forums.thebrain.com/post/wisdomtree-spaced-repetition-in-a-mindmap-11818585), [Anki Algorithm Explained](https://www.growexx.com/blog/anki-algorithm-explained-how-spaced-repetition-works/)

---

## 10. Visual Programming / Node-Based Editors (Inspiration)

Software paradigms where logic is built by connecting visual nodes, relevant as UI inspiration for brainmap editing.

| Tool | What It Is | Brainmap Relevance |
|------|-----------|-------------------|
| **React Flow (xyflow)** | React/Svelte library for building node-based UIs. Used in workflow builders, no-code tools. Highly customizable nodes, edges, and interactions. | Very High — ideal foundation for an interactive brainmap editor |
| **Rete.js** | TypeScript framework for visual programming. Supports dataflow and control flow processing on graphs. Multi-framework (React, Vue, Angular, Svelte). | High — more opinionated than React Flow, includes graph execution |
| **Node-RED** | IBM's flow-based programming tool for IoT/automation. Proves nodes+wires UI works for non-programmers. | Medium — UI paradigm inspiration, not directly usable |
| **Unreal Blueprints** | Visual scripting in Unreal Engine. Demonstrates that complex logic can be expressed as connected nodes. | Low — game engine specific, but proves the paradigm scales |
| **ComfyUI** | Node-based UI for Stable Diffusion workflows. Massively popular in AI art community. | Medium — proves node UIs work for AI pipelines on consumer hardware |
| **n8n** | Workflow automation with visual node editor. Already running on Kris' server. | Medium — familiar paradigm, could inspire brainmap interactions |

**Key insight:** React Flow is the clear winner for building a custom brainmap UI. It is the most popular, best maintained, and most flexible. The node-based editor paradigm (from visual programming) maps perfectly to knowledge graph editing: nodes = concepts, edges = relationships, and the spatial layout is user-controlled.

**Sources:** [React Flow](https://reactflow.dev), [xyflow](https://xyflow.com), [Rete.js](https://retejs.org/), [Awesome Node-Based UIs (GitHub)](https://github.com/xyflow/awesome-node-based-uis), [12 React Libraries for Visual Builders](https://medium.com/@somendradev23/12-react-libraries-for-visual-builders-flows-charts-interactive-ui-that-feel-like-magic-53373af910e5)

---

## Synthesis: What This Means for a Personal Brainmap

### The Gap in the Market
Nobody has built a system that combines:
1. **Personal knowledge graph** (your notes, conversations, decisions)
2. **AI-powered auto-structuring** (LLM extracts entities/relationships from conversations)
3. **Visual spatial interface** (interactive graph you can explore and edit)
4. **Semantic search** (find by meaning, not keywords)
5. **Spaced repetition** (surface important knowledge before you forget)
6. **Mobile-first** (works on a phone)

### Closest Existing Solutions
- **Heptabase** — spatial canvas + notes, but no AI integration or graph-based RAG
- **Obsidian + plugins** — graph view + local-first, but graph is decorative, not functional
- **Neo4j + GraphRAG** — powerful graph + AI, but no visual interface for personal use
- **Traverse** — mind map + spaced repetition, but no AI or knowledge graph

### Recommended Technology Stack (if building custom)
| Layer | Technology | Why |
|-------|-----------|-----|
| **Storage** | Qdrant (already running) + lightweight graph structure (JSON or Neo4j) | Embeddings for semantic search, graph for relationships |
| **Visualization** | React Flow or Cytoscape.js | Interactive, customizable, well-maintained |
| **AI extraction** | LLM (already available) for entity/relationship extraction from conversations | Auto-populate the graph from daily interactions |
| **Retention** | FSRS algorithm (modern spaced repetition, used in Anki v3) | Surface important nodes at optimal intervals |
| **Interface** | Mobile-responsive web app (already have webapp infrastructure) | Works on Kris' phone |
| **Dimensionality reduction** | UMAP for projecting embeddings to 2D | Visualize semantic clusters |

### Key Principles from Research
1. **Bottom-up > Top-down** (Zettelkasten): Let structure emerge from connections, don't impose categories
2. **Spatial > Hierarchical** (Heptabase/Scrintal): Position and proximity carry meaning
3. **Graph > Tree** (Knowledge graphs): Real knowledge has many-to-many relationships
4. **AI extraction > Manual entry** (GraphRAG): The system should build itself from conversations
5. **Semantic zoom** (Multi-dimensional): Different detail levels for different scales
6. **Retain what matters** (Spaced repetition): Not all nodes are equal, surface the important ones
