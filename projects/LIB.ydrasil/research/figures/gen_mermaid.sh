#!/bin/bash
# Generate all black/white Mermaid diagrams
cd /root/Yggdra/research/figures

# Mermaid config for black/white theme
cat > mermaid-bw.json << 'CONF'
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#ffffff",
    "primaryTextColor": "#000000",
    "primaryBorderColor": "#333333",
    "lineColor": "#333333",
    "secondaryColor": "#f5f5f5",
    "tertiaryColor": "#eeeeee",
    "fontSize": "14px"
  }
}
CONF

render() {
    local name="$1"
    echo "Rendering $name..."
    mmdc -i "${name}.mmd" -o "${name}.png" -t neutral -b white \
         -w 2400 -s 3 -p puppeteer-config.json -c mermaid-bw.json 2>&1 | grep -v "^$"
}

# L0: Manual process
cat > level_0.mmd << 'EOF'
graph LR
    A["You"] --> B["Do the task\nyourself"]
    B --> C["Done"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
EOF

# L1: Cron + Scripts
cat > level_1.mmd << 'EOF'
graph LR
    A["⏰ Timer\n(cron)"] --> B["Python\nScript"]
    B --> C["Fetch\nData"]
    C --> D["Transform"]
    D --> E["Write\nOutput"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
EOF

# L2: Webhooks
cat > level_2.mmd << 'EOF'
graph LR
    A["External\nEvent"] -->|webhook| B["Handler\nScript"]
    B --> C["Process"]
    C --> D["Respond /\nStore"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
EOF

# L3: Workflow Engine
cat > level_3.mmd << 'EOF'
graph LR
    A["Trigger"] --> B["API A"]
    B --> C["Transform"]
    C --> D{"Condition"}
    D -->|Yes| E["API B"]
    D -->|No| F["API C"]
    E --> G["Notify"]
    F --> G
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
    style G stroke:#333,fill:#fff
EOF

# L4: LLM-in-the-Loop
cat > level_4.mmd << 'EOF'
graph LR
    A["Input"] --> B["Parse &\nValidate"]
    B --> C["LLM:\nClassify"]
    C -->|Category A| D["Handler A"]
    C -->|Category B| E["Handler B"]
    D --> F["Output"]
    E --> F
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,stroke-width:2px,fill:#f5f5f5
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
EOF

# L5: Autonomous Agent
cat > level_5.mmd << 'EOF'
graph LR
    A["Goal"] --> B["LLM:\nThink"]
    B --> C{"Done?"}
    C -->|No| D["Act:\nCall Tool"]
    D --> E["Observe\nResult"]
    E --> B
    C -->|Yes| F["Return\nAnswer"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,stroke-width:2px,fill:#f5f5f5
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
EOF

# ReAct loop (replaces diagram_4)
cat > react_loop.mmd << 'EOF'
graph LR
    A["Receive\nTask"] --> B["THINK\nReason about\nwhat to do"]
    B --> C{"Done?"}
    C -->|Yes| D["Return\nFinal Answer"]
    C -->|No| E["ACT\nCall a tool"]
    E --> F["OBSERVE\nRead result"]
    F --> B
    style A stroke:#333,fill:#fff
    style B stroke:#333,stroke-width:2px,fill:#f5f5f5
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
EOF

# Plan-and-Execute (replaces diagram_5)
cat > plan_execute.mmd << 'EOF'
graph TD
    A["Receive Task"] --> B["PLAN\nDecompose into\nnumbered steps"]
    B --> C["Show plan\nto human"]
    C -->|Approved| D["Execute Step 1"]
    C -->|Rejected| B
    D --> E{"More steps?"}
    E -->|Yes| F["Execute Next Step"]
    F --> G{"Need to\nre-plan?"}
    G -->|Yes| B
    G -->|No| E
    E -->|No| H["Return Result"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,stroke-width:2px,fill:#f5f5f5
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
    style G stroke:#333,fill:#fff
    style H stroke:#333,fill:#fff
EOF

# Six composable patterns (replaces diagram_3)
cat > six_patterns.mmd << 'EOF'
graph TD
    A["1. Augmented LLM\nModel + retrieval + tools"] --> B["2. Prompt Chaining\nSequential LLM calls\nwith validation gates"]
    B --> C["3. Routing\nLLM classifies input,\ndispatches to handlers"]
    C --> D["4. Parallelization\nFan-out to multiple LLMs,\nfan-in results"]
    D --> E["5. Orchestrator-Workers\nCentral LLM delegates\nto specialized workers"]
    E --> F["6. Evaluator-Optimizer\nGenerate, evaluate,\nimprove iteratively"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
EOF

# Hybrid pattern (replaces diagram_6)
cat > hybrid_pattern.mmd << 'EOF'
graph LR
    A["Input"] --> B["Parse &\nValidate"]
    B --> C["Query\nDatabase"]
    C --> D{"LLM\nDecision"}
    D -->|Cat. A| E["Handler A"]
    D -->|Cat. B| F["Handler B"]
    D -->|Uncertain| G["Human\nReview"]
    E --> H["Output"]
    F --> H
    G --> H
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,stroke-width:2px,fill:#f5f5f5
    style E stroke:#333,fill:#fff
    style F stroke:#333,fill:#fff
    style G stroke:#333,stroke-width:2px,fill:#f5f5f5
    style H stroke:#333,fill:#fff
EOF

# Context engineering stack (replaces diagram_7)
cat > context_stack.mmd << 'EOF'
graph BT
    L1["Layer 1: FOUNDATION\nFew general tools · Short descriptions · Cache-friendly prompts"] --> L2
    L2["Layer 2: OFFLOAD\nFile system as external memory · STATE.md, PLAN.md"] --> L3
    L3["Layer 3: REDUCTION\nSliding window compaction · Tool output compression"] --> L4
    L4["Layer 4: ISOLATION\nSub-agents with fresh context · Bring back summaries"] --> L5
    L5["Layer 5: PROGRESSIVE DISCLOSURE\nLoad skills/tools on demand · Tool masking"]
    style L1 stroke:#333,fill:#fff
    style L2 stroke:#333,fill:#fff
    style L3 stroke:#333,fill:#fff
    style L4 stroke:#333,fill:#fff
    style L5 stroke:#333,fill:#fff
EOF

# Multi-agent communication (replaces diagram_8)
cat > multi_agent_comm.mmd << 'EOF'
graph TD
    subgraph "Hierarchical"
        S1["Supervisor"] --> W1["Worker A"]
        S1 --> W2["Worker B"]
    end
    subgraph "Peer-to-Peer"
        P1["Agent A"] <--> P2["Agent B"]
        P2 <--> P3["Agent C"]
    end
    subgraph "Shared State"
        SS["State Object"]
        A1["Agent A"] --> SS
        A2["Agent B"] --> SS
    end
    subgraph "Sequential"
        H1["Agent A"] --> H2["Agent B"] --> H3["Agent C"]
    end
EOF

# Framework decision tree (replaces diagram_9)
cat > framework_decision.mmd << 'EOF'
graph TD
    A{"Need HITL\napproval gates?"}
    A -->|Yes| LG["LangGraph"]
    A -->|No| B{"Single agent\nsufficient?"}
    B -->|Yes| RAW["Raw API +\ntool calling"]
    B -->|No| C{"Codebase\ntask?"}
    C -->|Yes| CLAUDE["Claude Agent SDK"]
    C -->|No| D{"Open-source\nmodels?"}
    D -->|Yes| SMOL["smolagents"]
    D -->|No| E{"Microsoft?"}
    E -->|Yes| AG["AutoGen"]
    E -->|No| LG2["LangGraph\n(default)"]
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style LG stroke:#333,fill:#f5f5f5
    style RAW stroke:#333,fill:#f5f5f5
    style CLAUDE stroke:#333,fill:#f5f5f5
    style SMOL stroke:#333,fill:#f5f5f5
    style AG stroke:#333,fill:#f5f5f5
    style LG2 stroke:#333,fill:#f5f5f5
EOF

# Minimal agent - PI's 4 tools
cat > minimal_agent.mmd << 'EOF'
graph TD
    A["Agent Core\n(LLM + System Prompt\n~500 tokens)"] --> R["Read\nRead files"]
    A --> W["Write\nCreate files"]
    A --> E["Edit\nModify files"]
    A --> B["Bash\nRun commands"]
    B -.->|"curl, git, python,\nsql, grep..."| T["Everything else\nvia shell"]
    style A stroke:#333,stroke-width:2px,fill:#f5f5f5
    style R stroke:#333,fill:#fff
    style W stroke:#333,fill:#fff
    style E stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style T stroke:#333,stroke-dasharray: 5 5,fill:#fff
EOF

# Eval lifecycle flywheel
cat > eval_lifecycle.mmd << 'EOF'
graph LR
    A["Offline Eval\n(CI pipeline)"] -->|deploy| B["Production"]
    B --> C["Online Eval\n(live scoring)"]
    C -->|anomaly| D["Ad-hoc\nInvestigation"]
    D -->|new test case| A
    style A stroke:#333,fill:#fff
    style B stroke:#333,fill:#fff
    style C stroke:#333,fill:#fff
    style D stroke:#333,fill:#fff
EOF

# Run/Trace/Thread hierarchy
cat > eval_hierarchy.mmd << 'EOF'
graph TD
    T["Thread\n(multi-turn session)"]
    T --> TR1["Trace 1\n(task execution)"]
    T --> TR2["Trace 2\n(task execution)"]
    TR1 --> R1["Run 1\n(LLM call)"]
    TR1 --> R2["Run 2\n(LLM call)"]
    TR1 --> R3["Run 3\n(LLM call)"]
    TR2 --> R4["Run 4"]
    TR2 --> R5["Run 5"]
    style T stroke:#333,stroke-width:2px,fill:#f5f5f5
    style TR1 stroke:#333,fill:#fff
    style TR2 stroke:#333,fill:#fff
    style R1 stroke:#333,fill:#fff
    style R2 stroke:#333,fill:#fff
    style R3 stroke:#333,fill:#fff
    style R4 stroke:#333,fill:#fff
    style R5 stroke:#333,fill:#fff
EOF

# $47K incident: without vs with controls
cat > safety_comparison.mmd << 'EOF'
graph LR
    subgraph "Without Controls"
        A1["Agent A"] -->|loop| A2["Agent B"]
        A2 -->|loop| A1
        A1 -.->|"11 days\n$47,000"| X["💸"]
    end
    subgraph "With Controls"
        B1["Agent"] --> B2{"Step > 10?"}
        B2 -->|No| B3["Continue"]
        B2 -->|Yes| B4["STOP\n+ Summary"]
    end
EOF

# Render all
for f in level_*.mmd react_loop.mmd plan_execute.mmd six_patterns.mmd \
         hybrid_pattern.mmd context_stack.mmd multi_agent_comm.mmd \
         framework_decision.mmd minimal_agent.mmd eval_lifecycle.mmd \
         eval_hierarchy.mmd safety_comparison.mmd; do
    render "${f%.mmd}"
done

echo "All done."
ls -lh *.png | grep -v diagram_ | grep -v chart_
