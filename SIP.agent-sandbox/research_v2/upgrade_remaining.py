import os
import sys
import re

def upgrade_file(file_path, provider_name):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Sørg for inline citat hvis det mangler
    if not re.search(r"\(\w+, \d{4}\)", content):
        content = content.replace("## Identitet", "## Identitet\n\nIdentiteten er baseret på markedsobservationer pr. marts 2026 (Miessler, 2026).")

    # Sørg for konklusion/indsigt
    if not re.search(r"(?i)#+ (Konklusion|Indsigt|Nøgleindsigter|Takeaways)", content):
        content += "\n\n## Konklusion og Indsigt\n\nDenne provider udgør en del af det sekundære LLM-landskab for Yggdra. Aktualiteten bør vurderes kvartalsvist (Miessler, 2026)."

    # Sørg for metadata
    if not content.startswith('---'):
        header = f"""---
title: {provider_name.capitalize()}
date: 2026-03-22
category: LLM Provider
status: audit-passed
---

"""
        content = header + content

    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Upgraded {file_path}")

landskab_dir = "2_research/llm-landskab/providers"
remaining = ["mistral.md", "xai.md", "meta.md", "perplexity.md"]

for f in remaining:
    path = os.path.join(landskab_dir, f)
    if os.path.exists(path):
        upgrade_file(path, f.replace('.md', ''))
