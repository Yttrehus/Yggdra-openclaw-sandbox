#!/bin/bash
# pre_compact.sh
# Formål: Sikre at vigtig state er skrevet til disk før context compaction.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- PRE-COMPACT HOOK ---"
echo "Tid: $(date)"

# Påmindelse til agenten om at opdatere state-filer
echo "ADVARSEL: Context compaction forestående."
echo "Sørg for at CONTEXT.md og DAGBOG.md er opdateret med dine seneste tanker."

# Kørsel af auto-chatlog (BMS.auto-chatlog)
if [ -f "$PROJECT_ROOT/BMS.auto-chatlog/chatlog-engine.js" ]; then
    echo "Opdaterer chatlog..."
    node "$PROJECT_ROOT/BMS.auto-chatlog/chatlog-engine.js"
    
    # Automatisk Fact Extraction efter chatlog opdatering (SIP sandbox)
    if [ -f "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/subagent_orchestrator.py" ]; then
        echo "Ekstraherer fakta (v2.1 LLM-Enhanced)..."
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/subagent_orchestrator.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/cleaner.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/validator.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/merger.py"
        python3 "$PROJECT_ROOT/SIP.agent-sandbox/fact_extraction_v2/notifier.py"
        
        # Automatisk ingestion af Fact Sheets til Qdrant (Memory Architecture)
        if [ -f "$PROJECT_ROOT/scripts/memory.py" ] && [ -n "$OPENAI_API_KEY" ]; then
            echo "Ingester Fact Sheets til Qdrant..."
            python3 "$PROJECT_ROOT/scripts/memory.py" ingest "$PROJECT_ROOT/SIP.agent-sandbox/memory_ingest"
        else
            echo "Spring over Qdrant ingestion (mangler scripts/memory.py eller OPENAI_API_KEY)"
        fi
    fi
fi

echo "--- HOOK AFSLUTTET ---"
