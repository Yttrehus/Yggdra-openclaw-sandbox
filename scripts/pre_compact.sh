#!/bin/bash
# pre_compact.sh v1.1
# Formål: Sikre at vigtig state er skrevet til disk og valideret før context compaction.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- PRE-COMPACT HOOK v1.1 ---"
echo "Tid: $(date)"

# Påmindelse til agenten om at opdatere state-filer
echo "ADVARSEL: Context compaction forestående. Sørg for at CONTEXT.md og DAGBOG.md er opdaterede."

# 1. Kørsel af auto-chatlog (BMS.auto-chatlog)
if [ -f "$PROJECT_ROOT/BMS.auto-chatlog/chatlog-engine.js" ]; then
    echo "Opdaterer chatlog..."
    node "$PROJECT_ROOT/BMS.auto-chatlog/chatlog-engine.js"
    
    # 2. Automatisk Fact Extraction efter chatlog opdatering (Lag 2)
    if [ -f "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/subagent_orchestrator.py" ]; then
        echo "Ekstraherer fakta (v2.1 LLM-Enhanced)..."
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/subagent_orchestrator.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/cleaner.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/validator.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/merger.py"
        
        # 3. Memory Re-indexing (Vidar-logik / Kvalitets-gate)
        if [ -f "$PROJECT_ROOT/scripts/memory_reindexer.py" ]; then
            echo "Kvalitetssikring: Re-indekserer hukommelse..."
            python3 "$PROJECT_ROOT/scripts/memory_reindexer.py"
        fi
        
        # 4. Qdrant Ingestion (Memory Architecture)
        if [ -f "$PROJECT_ROOT/scripts/memory.py" ] && [ -n "$OPENAI_API_KEY" ]; then
            echo "Ingester Fact Sheets til Qdrant..."
            python3 "$PROJECT_ROOT/scripts/memory.py" ingest "$PROJECT_ROOT/SIP.agent-sandbox/memory_ingest"
        fi
    fi
fi

# 5. Kørsel af Maintenance Audit
if [ -f "$PROJECT_ROOT/scripts/maintenance_audit.py" ]; then
    echo "Kører Maintenance Audit..."
    python3 "$PROJECT_ROOT/scripts/maintenance_audit.py"
fi

echo "--- HOOK AFSLUTTET ---"
