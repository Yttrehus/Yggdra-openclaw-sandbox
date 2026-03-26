#!/bin/bash
# pull_upstream.sh
# Formål: Genopret videns-kontinuitet ved at hente de seneste data fra ejerens VPS.

echo "--- PULL UPSTREAM DATA ---"
echo "Tid: $(date)"

# Opdatering af git (hvis ejeren har pushet)
git fetch upstream
git merge upstream/main

# Her kan vi senere tilføje rsync kommandoer hvis git ikke er nok
# f.eks. rsync -avz user@vps:/path/to/data/intelligence/ data/intelligence/

echo "--- PULL AFSLUTTET ---"
