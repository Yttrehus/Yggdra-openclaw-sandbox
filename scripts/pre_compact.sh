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

# Evt. kørsel af auto-chatlog hvis den findes
if [ -f "$PROJECT_ROOT/projects/auto-chatlog/chatlog-engine.js" ]; then
    echo "Opdaterer chatlog..."
    node "$PROJECT_ROOT/projects/auto-chatlog/chatlog-engine.js"
    
    # Automatisk Fact Extraction efter chatlog opdatering
    if [ -f "$PROJECT_ROOT/projects/sip/fact_extraction_v2/fact_extraction_poc.py" ]; then
        echo "Ekstraherer fakta..."
        python3 "$PROJECT_ROOT/projects/sip/fact_extraction_v2/fact_extraction_poc.py"
        python3 "$PROJECT_ROOT/projects/sip/fact_extraction_v2/cleaner.py"
        python3 "$PROJECT_ROOT/projects/sip/fact_extraction_v2/validator.py"
        python3 "$PROJECT_ROOT/projects/sip/fact_extraction_v2/merger.py"
        python3 "$PROJECT_ROOT/projects/sip/fact_extraction_v2/notifier.py"
    fi
fi

echo "--- HOOK AFSLUTTET ---"
