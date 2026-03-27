#!/bin/bash
# pull_upstream.sh v1.2
# Formål: Genopret videns-kontinuitet, håndtér strukturel merge og verificér data.

echo "--- PULL UPSTREAM DATA & STRUCTURAL MERGE ---"
echo "Tid: $(date)"

# 1. Git Fetch
echo "[1/4] Henter data fra upstream..."
git fetch upstream

# 2. Håndtér Merge (Forsøg merge, hvis konflikter, kør translator)
echo "[2/4] Forsøger merge..."
if git merge upstream/main --no-edit; then
    echo "  [OK] Merge lykkedes uden konflikter."
else
    echo "  [WARN] Merge-konflikter detekteret. Kører Merge Translator..."
    git merge --abort
    python3 scripts/merge_translator.py
    # Forsøg merge igen efter translator har flyttet ting (hvis nødvendigt)
    git merge upstream/main --no-edit || echo "  [ERROR] Manuel konfliktløsning stadig påkrævet i CONTEXT.md/PROGRESS.md"
fi

# 3. Pre-flight Check (Data Integritet)
echo "[3/4] Verificerer data-integritet..."
MISSING_FILES=0
for i in {0..2}; do
    D=$(date -d "$i days ago" +%Y-%m-%d)
    if [ ! -f "data/intelligence/daily_$D.md" ]; then
        echo "  [WARN] daily_$D.md mangler stadig."
        ((MISSING_FILES++))
    else
        echo "  [OK] daily_$D.md fundet."
    fi
done

# 4. Kørsel af Audit
echo "[4/4] Opdaterer system-audit..."
python3 scripts/maintenance_audit.py

if [ $MISSING_FILES -eq 0 ]; then
    echo "--- PULL SUCCESS: Videns-kontinuitet genoprettet ---"
else
    echo "--- PULL PARTIAL: Systemet kræver stadig opmærksomhed på VPS-siden ---"
fi
