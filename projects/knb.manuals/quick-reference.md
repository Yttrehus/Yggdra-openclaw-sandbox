# Quick Reference — Windows 11 Developer

## Windows 11 Shortcuts

| Genvej | Handling |
|--------|----------|
| `Win + Num` | Snap window to screen position (1-9) |
| `Win + Z` | Open Snap Layouts (choose layout) |
| `Win + D` | Toggle show desktop |
| `Win + E` | Open File Explorer |
| `Win + V` | Open Clipboard History |
| `Win + Shift + S` | Screenshot (Snip & Sketch) |
| `Win + X` | Quick Access menu (terminal, settings, disk mgmt) |
| `Win + I` | Settings |
| `Win + Ctrl + D` | New virtual desktop |
| `Win + Ctrl + Right/Left` | Switch virtual desktop |
| `Win + Tab` | Task View (all desktops + windows) |
| `Alt + Tab` | Switch app (current desktop) |
| `Alt + Shift + Right/Left` | Shift window between monitors |

---

## VS Code — Top 20 Shortcuts

| Genvej | Handling |
|--------|----------|
| `Ctrl + P` | Quick Open (search files by name) |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + K Ctrl + O` | Open Folder |
| `Ctrl + B` | Toggle Sidebar |
| `Ctrl + J` | Toggle Terminal |
| `Ctrl + Shift + \`` | New Terminal |
| `Ctrl + F` | Find in file |
| `Ctrl + H` | Find & Replace |
| `Ctrl + Shift + F` | Find across files |
| `Ctrl + G` | Go to Line |
| `Ctrl + Shift + O` | Go to Symbol in file |
| `Ctrl + T` | Go to Symbol (all files) |
| `Ctrl + /` | Toggle Line Comment |
| `Shift + Alt + A` | Toggle Block Comment |
| `Ctrl + Shift + K` | Delete Line |
| `Alt + Up/Down` | Move Line Up/Down |
| `Shift + Alt + Up/Down` | Duplicate Line Up/Down |
| `Ctrl + Shift + Enter` | Insert Line Above |
| `Ctrl + Enter` | Insert Line Below |
| `Ctrl + L` | Select entire line (repeat for multiple) |
| `Ctrl + D` | Select next occurrence (multi-edit) |
| `Ctrl + K Ctrl + X` | Trim trailing whitespace |

---

## Editing & Selection

| Genvej | Handling |
|--------|----------|
| `Home` | Go to line start |
| `End` | Go to line end |
| `Ctrl + Home` | Go to file start |
| `Ctrl + End` | Go to file end |
| `Shift + End` | Select to line end |
| `Shift + Home` | Select to line start |
| `Shift + Ctrl + Right` | Select word right |
| `Shift + Ctrl + Left` | Select word left |
| `Shift + Page Down` | Select page down |
| `Shift + Page Up` | Select page up |

---

## VS Code — Terminal & Debug

| Genvej | Handling |
|--------|----------|
| `Ctrl + `` | Toggle integrated terminal |
| `Ctrl + Shift + \`` | New terminal |
| `Ctrl + Shift + C` | Open terminal at current folder |
| `F5` | Start Debug |
| `F9` | Toggle Breakpoint |
| `F10` | Step Over |
| `F11` | Step Into |
| `Shift + F11` | Step Out |
| `Ctrl + Shift + D` | Debug View |

---

## PowerToys Shortcuts

| Genvej | Handling |
|--------|----------|
| `Win + Shift + A` | PowerToys Run (app launcher + calculator) |
| `Ctrl + Shift + C` | Color Picker |
| `Win + Shift + T` | Always On Top (toggle current window) |
| `Win + Shift + P` | Paste as plain text |
| `Win + Shift + V` | Paste as markdown |

**FancyZones:** Ctrl + click drag to position in layout, Win + drag to snap, Win + P to cycle layouts.

---

## Touchpad Gestures (ThinkPad X1 Carbon)

| Gesture | Handling |
|---------|----------|
| **3-finger tap** | Middle-click (paste in terminal) |
| **3-finger drag** | Drag & drop (without holding button) |
| **4-finger tap** | Action Center |
| **4-finger drag up** | Task View / Virtual desktops |
| **4-finger drag down** | Show desktop |
| **4-finger swipe left** | Previous app |
| **4-finger swipe right** | Next app |
| **2-finger pinch** | Zoom in/out |
| **2-finger scroll** | Scroll up/down |

---

## Git Bash / Terminal Commands

| Kommando | Hvad det gør |
|----------|------------|
| `cd ~` | Go to home (C:\Users\Krist) |
| `cd /c/Users/Krist/dev/projects/Yggdra` | Yggdra project root |
| `code .` | Open current folder in VS Code |
| `ls -la` | List with hidden files |
| `ls -lhS` | List sorted by size |
| `tree -L 2` | Tree view (2 levels) |
| `cat filename` | Print file content |
| `wc -l filename` | Line count |
| `pwd` | Print working directory |
| `mkdir -p a/b/c` | Create nested dirs |
| `rm -rf folder/` | Force delete (careful!) |
| `mv old new` | Rename/move |
| `cp -r src dst` | Copy recursively |
| `chmod +x script.sh` | Make executable |
| `git status` | Current branch & changes |
| `git log --oneline -n 10` | Last 10 commits |
| `git diff` | Unstaged changes |
| `git diff --staged` | Staged changes |
| `git add .` | Stage all |
| `git commit -m "msg"` | Commit |
| `git push origin main` | Push to main |
| `git pull origin main` | Pull from main |
| `git checkout -b feature` | New branch |
| `git switch main` | Switch branch |
| `git merge feature` | Merge branch |

---

## Windows Terminal / Profile Switching

| Kommando / Genvej | Hvad det gør |
|------------------|------------|
| `ctrl + shift + 1` | PowerShell |
| `ctrl + shift + 2` | Command Prompt |
| `ctrl + shift + 3` | Git Bash |
| `ctrl + shift + 4` | WSL (Ubuntu) |
| `ctrl + shift + t` | New tab (current profile) |
| `ctrl + shift + w` | Close tab |
| `ctrl + tab` | Next tab |
| `ctrl + shift + tab` | Previous tab |
| `alt + shift + d` | Split pane (duplicate) |
| `alt + shift + -` | Split pane (horizontal) |
| `alt + shift + +` | Split pane (vertical) |

---

## SSH / VPS (72.62.61.51)

| Kommando | Hvad det gør |
|----------|------------|
| `ssh root@72.62.61.51` | Connect to VPS |
| `ssh root@72.62.61.51 "command"` | Run command on VPS |
| `ssh root@72.62.61.51 "cat /path/file"` | Read file on VPS |
| `ssh -L 6333:localhost:6333 root@72.62.61.51` | Tunnel Qdrant (6333) |
| `scp -r local/ root@72.62.61.51:/root/path/` | Upload folder to VPS |
| `scp root@72.62.61.51:/root/file ~/` | Download file from VPS |

---

## Aliases (Add to ~/.bashrc or ~/.zshrc)

```bash
# Navigation
alias yttre="cd /c/Users/Krist"
alias yggdra="cd /c/Users/Krist/dev/projects/Yggdra"
alias dev="cd /c/Users/Krist/dev"

# Git shortcuts
alias ga="git add ."
alias gc="git commit -m"
alias gp="git push origin main"
alias gl="git log --oneline -n 10"
alias gs="git status"
alias gd="git diff"

# Quick access
alias vsc="code ."
alias ll="ls -lah"
alias x="exit"
```

---

## Quick Win10/11 Tips

| Tip | Hvordan |
|-----|--------|
| Disable notification sounds | Settings → System → Sound → Volume mixer → (App) → Volume 0 |
| Always show file extensions | File Explorer → View → Options → uncheck "Hide extensions" |
| Enable Dark Mode in VS Code | Preferences → Color Theme → Dark Modern (or Dracula) |
| Increase terminal font size | `Ctrl + Shift + P` → "Preferences: Open User Settings" → search "font size" |
| Pin folder to Quick Access | File Explorer → right-click folder → Pin to Quick Access |
| Use Segment Anything in PowerToys | Enable PowerToys utility on Image Editor |
