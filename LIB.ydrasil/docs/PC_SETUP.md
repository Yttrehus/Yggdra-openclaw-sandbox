# PC Setup Guide — Lokal Claude Code med øjne ind i VPS'en

**Dato:** 2026-03-03
**Hardware:** Lenovo X1 Carbon Gen 13
**Mål:** Claude Code lokalt, med SSH + Qdrant-adgang til VPS

---

## Fase 1: Fundament (første 2 timer)

### 1.1 Windows + WSL2

1. Åbn Microsoft Store → installer **Windows Terminal**
2. Åbn PowerShell som administrator:
   ```powershell
   wsl --install -d Ubuntu-24.04
   ```
3. Genstart PC'en når bedt om det
4. Åbn Ubuntu-24.04 fra Start-menuen → opret brugernavn `kris` + password
5. **VIGTIGT:** Alt kode lever under `/home/kris/` — ALDRIG under `/mnt/c/`

**Verificér:**
```bash
wsl --version     # Skal vise WSL 2
lsb_release -a    # Skal vise Ubuntu 24.04
```

### 1.2 Grundlæggende tools

```bash
sudo apt update && sudo apt install -y git curl build-essential python3 python3-venv python3-pip jq
```

### 1.3 Node.js 22 (via nvm)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 22
node --version    # Skal vise v22.x
```

### 1.4 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version  # Skal vise version
claude            # Login med Claude Code Max konto
```

### 1.5 SSH til VPS

```bash
# Generér nøgle
ssh-keygen -t ed25519 -C "kris-x1carbon" -f ~/.ssh/id_ed25519

# Kopiér public key til VPS (kræver VPS-password én gang)
ssh-copy-id root@72.62.61.51

# Test
ssh root@72.62.61.51 "hostname && date"
```

Tilføj i `~/.ssh/config`:
```bash
cat >> ~/.ssh/config << 'EOF'
Host vps
    HostName 72.62.61.51
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF
chmod 600 ~/.ssh/config
```

**Verificér:**
```bash
ssh vps "echo ok"    # Skal printe: ok
```

### 1.6 Qdrant-tunnel

```bash
# Start tunnel (baggrund)
ssh -L 6333:localhost:6333 vps -N &

# Test
curl -s http://localhost:6333/collections | jq '.result.collections | length'
# Skal vise: 7
```

Tilføj alias i `~/.bashrc`:
```bash
cat >> ~/.bashrc << 'EOF'

# Ydrasil aliases
alias qdrant-tunnel='ssh -L 6333:localhost:6333 vps -N &'
alias vps-status='ssh vps "docker ps --format \"table {{.Names}}\t{{.Status}}\" && echo --- && curl -s localhost:6333/collections | python3 -c \"import sys,json; [print(c[\\\"name\\\"]) for c in json.load(sys.stdin)[\\\"result\\\"][\\\"collections\\\"]]\""'
EOF
source ~/.bashrc
```

### 1.7 Clone Ydrasil

```bash
git clone https://github.com/Yttrehus/Ydrasil.git ~/Ydrasil
cd ~/Ydrasil
```

### 1.8 Python venv + dependencies

```bash
cd ~/Ydrasil
python3 -m venv scripts/venv
source scripts/venv/bin/activate
pip install qdrant-client openai fastembed sentence-transformers
```

### 1.9 Credentials

```bash
# Kopiér credentials fra VPS (ALDRIG i git!)
scp vps:/root/Ydrasil/data/CREDENTIALS.md ~/Ydrasil/data/CREDENTIALS.md

# Sæt env vars (tilføj i ~/.bashrc)
cat >> ~/.bashrc << 'EOF'

# API keys (læses fra CREDENTIALS.md af scripts)
export OPENAI_API_KEY="$(grep -oP '(?<=`)[^`]+' ~/Ydrasil/data/CREDENTIALS.md | head -1)"
EOF
source ~/.bashrc
```

---

## Fase 1 Verificering (alle 5 skal bestå)

```bash
# 1. Claude Code
claude --version

# 2. SSH
ssh vps "echo ok"

# 3. Qdrant (start tunnel først: qdrant-tunnel)
curl -s localhost:6333/collections | jq '.result.collections | length'
# Forventet: 7

# 4. ctx-kommandoen
cd ~/Ydrasil && source scripts/venv/bin/activate
python3 scripts/get_context.py "rute 256" --limit 1
# Forventet: rutedata

# 5. Claude Code med kontekst
cd ~/Ydrasil && claude
# Spørg: "hvad ved du om TI-appen?"
# Forventet: meningsfuldt svar fra Qdrant
```

**Hvis én fejler → fix den før du går videre.**

---

## Fase 2: Claude Code ser VPS'en (dag 1)

### 2.1 MCP Qdrant-server

```bash
# Installer MCP Qdrant server
pip install mcp-server-qdrant

# .mcp.json er allerede i git clone — men brug den lokale version:
cp ~/Ydrasil/.mcp.json.local ~/Ydrasil/.mcp.json
# Redigér .mcp.json og indsæt din OPENAI_API_KEY
```

### 2.2 "Kig dig selv igennem"-session

Start Claude Code i ~/Ydrasil og kør:
```bash
python3 scripts/vps_audit.py
```

Dette genererer et overblik over alt på VPS'en — filer, Qdrant collections, disk, services.
Gennemgå sammen med Claude: hvad bevares, hvad er rod, hvad kan slettes?

---

## Fase 3: Projekter (dag 2+)

### Mappestruktur
```
~/Ydrasil/               # Klonet fra VPS — hukommelse, scripts, data
~/projects/
  ti-app/                # Eget repo, egen CLAUDE.md
  revisor/               # Eget repo
  rejseagent/            # Eget repo
```

### Nyt projekt

```bash
# Brug skabelonen
cp -r ~/Ydrasil/templates/project-template ~/projects/MIT-PROJEKT
cd ~/projects/MIT-PROJEKT
git init
# Redigér CLAUDE.md — beskriv projektet
claude
```

---

## Retningslinjer

1. **Ét projekt ad gangen.** Start TI-app. 1 uge minimum.
2. **VPS'en kører videre.** PC = vindue ind, ikke erstatning.
3. **Qdrant = hukommelsen.** Ikke filer, ikke Notion.
4. **Nye projekter arver skabelon, ikke kode.**
5. **Evaluer efter 1 uge.** Produktiv inden 30 sek?
