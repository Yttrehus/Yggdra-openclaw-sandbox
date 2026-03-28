#!/bin/bash
# session_end.sh v1.1
# Formål: Logning af episoden og automatisk synkronisering.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
EPISODES_LOG="$PROJECT_ROOT/data/episodes.jsonl"

echo "--- SESSION END HOOK v1.1 ---"
echo "Tid: $(date)"

# 1. Hukommelses-vedligeholdelse (Lag 2/3)
if [ -f "$PROJECT_ROOT/scripts/memory_reindexer.py" ]; then
    echo "Kører Memory Re-indexer..."
    python3 "$PROJECT_ROOT/scripts/memory_reindexer.py"
fi

# 2. Ugentlig Rapport (Lag 5)
if [ -f "$PROJECT_ROOT/scripts/weekly_report.py" ]; then
    echo "Opdaterer ugerapport..."
    python3 "$PROJECT_ROOT/scripts/weekly_report.py"
fi

# 3. Log event
mkdir -p "$PROJECT_ROOT/data"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"timestamp\": \"$TIMESTAMP\", \"event\": \"session_end\", \"host\": \"$(hostname)\"}" >> "$EPISODES_LOG"

# 4. Trigger Notion Update (Lag 4)
if [ -f "$PROJECT_ROOT/scripts/notion_sync.py" ]; then
    echo "Synkroniserer til Notion..."
    python3 "$PROJECT_ROOT/scripts/notion_sync.py" --session-end
fi

# 5. Git Safety Check
if [[ $(git status --porcelain) ]]; then
  echo "ADVARSEL: Der er ucommittede ændringer i workspace!"
  git status --short
fi

echo "--- HOOK AFSLUTTET ---"
