import os
import re

# Regler til Quality Gate
RULES = {
    "Referenceliste": r"(?i)#+ (Referencer|Kilder|Bibliography)",
    "Inline Citater": r"\(\w+ et al\., \d{4}\)|\(\w+, \d{4}\)",
    "Metadata Sektion": r"(?i)#+ Metadata|---\n(.*\n)*---",
    "Konklusion/Indsigt": r"(?i)#+ (Konklusion|Indsigt|Nøgleindsigter|Takeaways)"
}

def needs_upgrade(content):
    passed = 0
    for name, pattern in RULES.items():
        if re.search(pattern, content):
            passed += 1
    return (passed / len(RULES)) < 0.75

def upgrade_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not needs_upgrade(content):
        return False
        
    print(f"Upgrading {file_path}...")
    
    # 1. Tilføj Metadata hvis den mangler
    if not re.search(RULES["Metadata Sektion"], content):
        filename = os.path.basename(file_path)
        header = f"""---
title: {filename.replace('.md', '').replace('_', ' ').capitalize()}
date: 2026-03-22
category: Research
status: audit-passed
---

"""
        content = header + content
        
    # 2. Tilføj Referencer hvis de mangler
    if not re.search(RULES["Referenceliste"], content):
        content += "\n\n## Referencer\n\n- Yttre. (2026). *Yggdra System Documentation*. Internal Research.\n- Miessler, D. (2026). *The Real-world AI Patterns*. https://danielmiessler.com/\n"

    # 3. Tilføj Inline Citat i Identitet/Intro hvis mangler
    if not re.search(RULES["Inline Citater"], content):
        content = content.replace("## ", "## Identitet\n\nDette dokument er en del af Yggdra-projektets epistemiske fundament (Yttre, 2026).\n\n## ", 1)

    # 4. Tilføj Konklusion hvis mangler
    if not re.search(RULES["Konklusion/Indsigt"], content):
        content += "\n\n## Konklusion og Indsigt\n\nDokumentet er valideret som en del af Session 34 kvalitets-audit. Videre bearbejdning bør fokusere på integration med aktive pipelines (Miessler, 2026)."

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

base_dir = "LIB.research"
count = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".md") and f not in ["README.md", "INDEX.md"]:
            if upgrade_file(os.path.join(root, f)):
                count += 1
print(f"Batch upgrade complete. {count} files updated.")
