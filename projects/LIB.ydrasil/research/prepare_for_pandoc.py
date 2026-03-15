#!/usr/bin/env python3
"""Prepare HOW_TO_BUILD_AGENTS.md for pandoc conversion.
Replaces Mermaid blocks with image references.
Removes the title/metadata (handled by template).
"""
import re
from pathlib import Path

md = Path("HOW_TO_BUILD_AGENTS.md").read_text()

# Remove title and metadata block (first few lines before Abstract)
md = re.sub(r'^# How to Build.*?\n---\n', '', md, count=1, flags=re.DOTALL)

# Remove Table of Contents section
md = re.sub(r'## Table of Contents\n\n.*?\n---\n', '', md, count=1, flags=re.DOTALL)

# Replace mermaid blocks with image references
counter = 0
def replace_mermaid(m):
    global counter
    counter += 1
    return f'![](figures/diagram_{counter}.png){{ width=85% }}'

md = re.sub(r'```mermaid\n.*?```', replace_mermaid, md, flags=re.DOTALL)

# Fix figure captions - pandoc needs them as part of the image syntax
# Pattern: ![](image){ width=85% }\n\n*Figure N. Caption text*
def merge_caption(m):
    img_path = m.group(1)
    width = m.group(2)
    caption = m.group(3).strip('* ').rstrip('.')
    # Strip "Figure N. " prefix since LaTeX adds "Figure N:" automatically
    caption = re.sub(r'^Figure \d+\.\s*', '', caption)
    return f'![{caption}]({img_path}){{ {width} }}'

md = re.sub(
    r'!\[\]\(([^)]+)\)\{\s*(width=[^}]+)\s*\}\n\n\*([^*]+)\*',
    merge_caption, md
)

# Remove the Abstract section header (handled in template)
md = re.sub(r'^## Abstract\n', '## Abstract\n', md)

# Replace em dashes in code blocks with -- (pdflatex-safe)
def fix_code_utf8(m):
    code = m.group(0)
    code = code.replace('—', '--')
    code = code.replace('"', '"').replace('"', '"')
    code = code.replace("'", "'").replace("'", "'")
    return code

md = re.sub(r'```\w*\n.*?```', fix_code_utf8, md, flags=re.DOTALL)

# Strip "N. " prefix from ## section headings (LaTeX will number them)
md = re.sub(r'^## \d+\.\s+', '## ', md, flags=re.MULTILINE)
# Strip "N.N " prefix from ### subsection headings
md = re.sub(r'^### \d+\.\d+\s+', '### ', md, flags=re.MULTILINE)

# Promote headings in single pass to avoid cascading
# Must avoid promoting # comments inside code blocks
in_code = False
lines = md.split('\n')
new_lines = []
for line in lines:
    if line.startswith('```'):
        in_code = not in_code
        new_lines.append(line)
        continue
    if not in_code:
        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if m:
            hashes = m.group(1)
            text = m.group(2)
            new_hashes = '#' * (len(hashes) - 1)
            new_lines.append(f'{new_hashes} {text}')
            continue
    new_lines.append(line)
md = '\n'.join(new_lines)

# Make Abstract unnumbered by adding {.unnumbered} attribute
md = md.replace('# Abstract', '# Abstract {.unnumbered}')
# Also make Glossary, References, Appendices unnumbered
md = md.replace('# Glossary', '# Glossary {.unnumbered}')
md = md.replace('# References', '# References {.unnumbered}')
md = md.replace('# Appendices', '# Appendices {.unnumbered}')

Path("HOW_TO_BUILD_AGENTS_pandoc.md").write_text(md)
print(f"Wrote HOW_TO_BUILD_AGENTS_pandoc.md ({len(md)} chars, {counter} diagrams replaced)")
