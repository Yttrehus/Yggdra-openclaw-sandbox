# Terminal-automatisering

**Dato:** 2026-03-13
**Status:** Backlog
**Oprindelse:** M6 fra PLAN v2/v3

## Opsummering
- VS Code åbner med de terminaler du bruger dagligt — automatisk
- Konfigureres via `.vscode/tasks.json` med `runOn: folderOpen`
- Eliminerer manuelt terminal-setup ved workspace-åbning

## Steps (fra original M6)
1. Definér terminaler per workspace (bash i rod, SSH til VPS, osv.)
2. `tasks.json` med `runOn: folderOpen`
3. Test og tilpas
