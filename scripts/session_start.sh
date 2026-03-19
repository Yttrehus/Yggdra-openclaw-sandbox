#!/bin/bash
# session_start.sh
# Formål: Injektion af aktuel kontekst ved sessionsstart.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- SESSION START HOOK ---"
echo "Dato: $(date)"

# 1. Vis aktuel status fra CONTEXT.md
if [ -f "$PROJECT_ROOT/CONTEXT.md" ]; then
    echo ""
    echo "--- AKTUELE STATUS (fra CONTEXT.md) ---"
    head -n 20 "$PROJECT_ROOT/CONTEXT.md"
    echo "..."
fi

# 2. Tjek for nylige DAGBOG entries
if [ -f "$PROJECT_ROOT/DAGBOG.md" ]; then
    echo ""
    echo "--- SENESTE DAGBOGS-NOTER ---"
    tail -n 20 "$PROJECT_ROOT/DAGBOG.md"
fi

# 3. Tjek for aktive projekter i TRIAGE.md
if [ -f "$PROJECT_ROOT/0_backlog/TRIAGE.md" ]; then
    echo ""
    echo "--- TRIAGE OVERBLIK ---"
    grep -A 10 "## Klar" "$PROJECT_ROOT/0_backlog/TRIAGE.md"
fi

echo ""
echo "--- HOOK AFSLUTTET ---"
