#!/bin/bash
# session_end.sh
# Formål: Logning af episoden ved sessionens afslutning.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
EPISODES_LOG="$PROJECT_ROOT/data/episodes.jsonl"

echo "--- SESSION END HOOK ---"
echo "Tid: $(date)"

# 1. Spørg agenten (via output) om at opsummere episoden
# Da hooks kører non-interaktivt, kan vi kun logge det vi har.

# 2. Log git status hvis der er ucommittede ændringer
if [[ $(git status --porcelain) ]]; then
  echo "ADVARSEL: Der er ucommittede ændringer i workspace!"
  git status --short
fi

# 3. Append en simpel event til episodes.jsonl
mkdir -p "$PROJECT_ROOT/data"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"timestamp\": \"$TIMESTAMP\", \"event\": \"session_end\", \"host\": \"$(hostname)\"}" >> "$EPISODES_LOG"

echo "Episode logget til $EPISODES_LOG"
echo "--- HOOK AFSLUTTET ---"
