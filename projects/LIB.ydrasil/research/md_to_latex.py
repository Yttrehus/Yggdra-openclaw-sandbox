#!/usr/bin/env python3
"""Convert HOW_TO_BUILD_AGENTS.md to LaTeX."""
import re
from pathlib import Path

md = Path("HOW_TO_BUILD_AGENTS.md").read_text()

# Track footnotes - extract them and convert to \footnote inline
footnotes = {}
for m in re.finditer(r'^\[\^(\d+)\]:\s*\*\*(.+?)\*\*\s+(.*?)$', md, re.MULTILINE):
    num, term, text = m.groups()
    # Clean up markdown formatting in footnote text
    clean = text.replace('*', '')
    footnotes[num] = f"\\textbf{{{term}}} {clean}"

# Remove footnote definitions from body
md = re.sub(r'^\[\^(\d+)\]:\s*\*\*.*$', '', md, flags=re.MULTILINE)

# --- Build LaTeX body ---
lines = md.split('\n')
output = []
in_code = False
code_lang = ''
in_table = False
table_lines = []
mermaid_counter = 0
in_mermaid = False
skip_mermaid = False

def escape_latex(s):
    """Escape LaTeX special chars, but preserve commands."""
    # Don't escape if it looks like it already has LaTeX commands
    s = s.replace('&', '\\&')
    s = s.replace('%', '\\%')
    s = s.replace('#', '\\#')
    s = s.replace('_', '\\_')
    s = s.replace('$', '\\$')
    # Fix over-escaping in URLs - we'll handle URLs separately
    return s

def process_inline(s):
    """Process inline markdown formatting."""
    # Bold+italic
    s = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', s)
    # Bold
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    # Italic
    s = re.sub(r'\*(.+?)\*', r'\\textit{\1}', s)
    # Inline code
    s = re.sub(r'`([^`]+)`', r'\\texttt{\1}', s)
    # Footnote references
    def fn_replace(m):
        num = m.group(1)
        if num in footnotes:
            return f'\\footnote{{{footnotes[num]}}}'
        return ''
    s = re.sub(r'\[\^(\d+)\]', fn_replace, s)
    # Links [text](url)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', s)
    # Em dash
    s = s.replace(' — ', ' --- ')
    s = s.replace('— ', '--- ')
    return s

def flush_table():
    global table_lines, in_table
    if not table_lines:
        return []

    result = []
    # Parse header
    headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    ncols = len(headers)
    col_spec = 'l' * ncols

    # For wider tables, use p columns
    if ncols >= 3:
        col_spec = 'p{0.35\\textwidth}p{0.25\\textwidth}p{0.35\\textwidth}'
    if ncols == 2:
        col_spec = 'p{0.5\\textwidth}p{0.45\\textwidth}'

    result.append('\\begin{table}[htbp]')
    result.append('\\centering')
    result.append('\\small')
    result.append(f'\\begin{{tabular}}{{{col_spec}}}')
    result.append('\\toprule')

    header_cells = ' & '.join(process_inline(h) for h in headers)
    result.append(f'{header_cells} \\\\')
    result.append('\\midrule')

    # Data rows (skip separator row)
    for row in table_lines[2:]:
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) == ncols:
            cell_text = ' & '.join(process_inline(c) for c in cells)
            result.append(f'{cell_text} \\\\')

    result.append('\\bottomrule')
    result.append('\\end{tabular}')
    result.append('\\end{table}')
    result.append('')

    table_lines = []
    in_table = False
    return result

i = 0
while i < len(lines):
    line = lines[i]

    # Mermaid blocks -> includegraphics
    if line.strip() == '```mermaid':
        mermaid_counter += 1
        in_mermaid = True
        i += 1
        continue

    if in_mermaid:
        if line.strip() == '```':
            in_mermaid = False
            output.append('')
            output.append('\\begin{figure}[htbp]')
            output.append('\\centering')
            output.append(f'\\includegraphics[width=0.85\\textwidth]{{figures/diagram_{mermaid_counter}.png}}')
            # Check next line for caption
            if i + 1 < len(lines) and lines[i + 1].startswith('*Figure'):
                caption = lines[i + 1].strip('* ')
                # Extract figure number and caption text
                cap_match = re.match(r'Figure (\d+)\.\s*(.*)', caption)
                if cap_match:
                    cap_text = process_inline(cap_match.group(2).rstrip('.'))
                    output.append(f'\\caption{{{cap_text}}}')
                    output.append(f'\\label{{fig:{cap_match.group(1)}}}')
                i += 1  # skip caption line
            output.append('\\end{figure}')
            output.append('')
        i += 1
        continue

    # Code blocks
    if line.strip().startswith('```') and not in_code:
        lang = line.strip()[3:].strip()
        in_code = True
        if lang == 'python':
            output.append('\\begin{lstlisting}[language=Python]')
        else:
            output.append('\\begin{lstlisting}')
        i += 1
        continue

    if line.strip() == '```' and in_code:
        in_code = False
        output.append('\\end{lstlisting}')
        output.append('')
        i += 1
        continue

    if in_code:
        output.append(line)
        i += 1
        continue

    # Tables
    if '|' in line and line.strip().startswith('|') and not in_code:
        if not in_table:
            in_table = True
            table_lines = []
        table_lines.append(line)
        i += 1
        continue
    elif in_table:
        output.extend(flush_table())

    # Skip horizontal rules
    if line.strip() == '---':
        i += 1
        continue

    # Skip empty caption lines (already handled above)
    if line.startswith('*Figure') and line.endswith('*'):
        i += 1
        continue

    # Headers
    if line.startswith('# ') and not line.startswith('## '):
        # Title - skip, handled in preamble
        i += 1
        continue

    if line.startswith('## '):
        title = line[3:].strip()
        # Remove anchor links
        title = re.sub(r'\[(.+?)\]\(#.+?\)', r'\1', title)
        title = process_inline(title)
        label = re.sub(r'[^a-z0-9]+', '-', title.lower().replace('\\textbf{', '').replace('}', ''))
        output.append(f'\\section{{{title}}}')
        output.append(f'\\label{{sec:{label}}}')
        output.append('')
        i += 1
        continue

    if line.startswith('### '):
        title = line[4:].strip()
        title = process_inline(title)
        output.append(f'\\subsection{{{title}}}')
        output.append('')
        i += 1
        continue

    if line.startswith('#### '):
        title = line[5:].strip()
        title = process_inline(title)
        output.append(f'\\subsubsection{{{title}}}')
        output.append('')
        i += 1
        continue

    # Block quotes
    if line.startswith('> '):
        quote_lines = []
        while i < len(lines) and (lines[i].startswith('> ') or lines[i].startswith('>')):
            quote_lines.append(lines[i].lstrip('> ').strip())
            i += 1
        quote_text = ' '.join(l for l in quote_lines if l)
        quote_text = process_inline(quote_text)
        output.append('\\begin{quote}')
        output.append(f'\\textit{{{quote_text}}}')
        output.append('\\end{quote}')
        output.append('')
        continue

    # Bullet lists
    if line.strip().startswith('- '):
        list_items = []
        while i < len(lines) and lines[i].strip().startswith('- '):
            item = lines[i].strip()[2:]
            item = process_inline(item)
            list_items.append(item)
            i += 1
        output.append('\\begin{itemize}')
        for item in list_items:
            output.append(f'  \\item {item}')
        output.append('\\end{itemize}')
        output.append('')
        continue

    # Numbered lists
    if re.match(r'^\d+\.\s', line.strip()):
        list_items = []
        while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
            item = re.sub(r'^\d+\.\s*', '', lines[i].strip())
            item = process_inline(item)
            list_items.append(item)
            i += 1
        output.append('\\begin{enumerate}')
        for item in list_items:
            output.append(f'  \\item {item}')
        output.append('\\end{enumerate}')
        output.append('')
        continue

    # Regular paragraphs
    if line.strip():
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') and not lines[i].startswith('```') and not lines[i].startswith('|') and not lines[i].startswith('> ') and not lines[i].strip().startswith('- ') and not re.match(r'^\d+\.\s', lines[i].strip()) and lines[i].strip() != '---':
            para_lines.append(lines[i])
            i += 1
        para = ' '.join(para_lines)
        para = process_inline(para)
        output.append(para)
        output.append('')
        continue

    # Empty lines
    output.append('')
    i += 1

# Flush any remaining table
if in_table:
    output.extend(flush_table())

body = '\n'.join(output)

# --- Build full document ---
preamble = r"""\documentclass[11pt, a4paper]{article}

% --- Typography ---
\usepackage[T1]{fontenc}
\usepackage{tgpagella}                    % Palatino clone — classic, readable
\usepackage[scaled=0.85]{beramono}        % Monospace for code
\usepackage{microtype}                     % Optimal word spacing for justified text

% --- Layout ---
\usepackage[
  top=1.25in,
  bottom=1.25in,
  left=1.25in,
  right=1.25in
]{geometry}
\usepackage{setspace}
\setstretch{1.4}                           % 1.4 line spacing — generous, readable

% --- Headers & Sections ---
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}

\definecolor{darkblue}{RGB}{0, 51, 102}
\definecolor{codebg}{RGB}{245, 245, 245}
\definecolor{codeframe}{RGB}{200, 200, 200}

\titleformat{\section}
  {\Large\bfseries\color{darkblue}}
  {\thesection.}{0.5em}{}
\titleformat{\subsection}
  {\large\bfseries\color{darkblue}}
  {\thesubsection}{0.5em}{}
\titleformat{\subsubsection}
  {\normalsize\bfseries}
  {\thesubsubsection}{0.5em}{}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textit{How to Build AI Agents}}
\fancyhead[R]{\small\textit{\nouppercase{\leftmark}}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% --- Code listings ---
\usepackage{listings}
\lstset{
  backgroundcolor=\color{codebg},
  frame=single,
  rulecolor=\color{codeframe},
  basicstyle=\ttfamily\small,
  keywordstyle=\color{darkblue}\bfseries,
  commentstyle=\color{gray}\itshape,
  stringstyle=\color{teal},
  breaklines=true,
  breakatwhitespace=true,
  tabsize=4,
  showstringspaces=false,
  aboveskip=1em,
  belowskip=1em,
  xleftmargin=1em,
  xrightmargin=1em,
  numbers=none,
}

% --- Tables ---
\usepackage{booktabs}
\usepackage{array}

% --- Graphics ---
\usepackage{graphicx}
\graphicspath{{./}}

% --- Links ---
\usepackage[
  colorlinks=true,
  linkcolor=darkblue,
  urlcolor=darkblue,
  citecolor=darkblue
]{hyperref}

% --- Misc ---
\usepackage{enumitem}
\setlist{nosep, leftmargin=1.5em}

% --- Title ---
\title{
  \vspace{-2em}
  {\huge\bfseries\color{darkblue} How to Build AI Agents}\\[0.5em]
  {\Large A Practitioner's Manual}\\[1em]
  {\normalsize Version 1.0 \quad|\quad March 2026}
}
\author{
  \textit{Produced by Yggdra Research System}\\[0.5em]
  \small Intended audience: Software engineers, technical leads, and\\
  \small technology decision-makers evaluating or building AI agent systems.
}
\date{}

\begin{document}

\maketitle
\thispagestyle{empty}

\vfill

\begin{abstract}
\noindent AI agents --- software systems where a large language model dynamically decides what actions to take rather than following a predetermined script --- have become one of the most discussed topics in software engineering. The promise is compelling: autonomous systems that can research, code, analyze, and coordinate complex tasks with minimal human oversight. The reality, as of early 2026, is more nuanced. Ninety-five percent of enterprise AI pilots fail to reach production. Multi-agent systems see 40\% pilot failure rates within six months. A single runaway agent generated a \$47,000 API bill over eleven days before anyone noticed.

This manual is a practitioner's guide to building AI agents that actually work. It synthesizes findings from over fifty research papers, fourteen original research reports, six production codebases, and three years of collective deployment experience. The document covers the full lifecycle: from deciding whether you need an agent at all, through architecture selection, context management, multi-agent coordination, evaluation, and production deployment.

The manual's central argument is that the scaffolding around the model --- the tools, the context management, the evaluation infrastructure, the safety controls --- provides roughly eighty percent of the value in any agent system. The model itself provides twenty percent.
\end{abstract}

\vfill
\newpage

\tableofcontents
\newpage

"""

postamble = r"""

\end{document}
"""

doc = preamble + body + postamble

# Post-processing fixes
# Fix escaped underscores in code listings
code_blocks = list(re.finditer(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', doc, re.DOTALL))
for block in reversed(code_blocks):
    fixed = block.group().replace('\\_', '_').replace('\\&', '&').replace('\\%', '%').replace('\\#', '#').replace('\\$', '$')
    doc = doc[:block.start()] + fixed + doc[block.end():]

# Fix URLs in \href - unescape underscores
def fix_href(m):
    url = m.group(1).replace('\\_', '_')
    text = m.group(2)
    return f'\\href{{{url}}}{{{text}}}'
doc = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', fix_href, doc)

# Fix texttt with escaped underscores
def fix_texttt(m):
    content = m.group(1).replace('\\_', '_')
    return f'\\texttt{{{content}}}'
doc = re.sub(r'\\texttt\{([^}]+)\}', fix_texttt, doc)

# Remove duplicate abstract (it's in preamble already)
# Find the "Abstract" section in body and remove it
doc = re.sub(r'\\section\{Abstract\}.*?(?=\\section)', '', doc, count=1, flags=re.DOTALL)

# Remove the metadata lines (Version, Date, Produced by, Intended audience)
doc = re.sub(r'\\textbf\{Version:\}.*?\n\n', '', doc)
doc = re.sub(r'\\textbf\{Date:\}.*?\n\n', '', doc)
doc = re.sub(r'\\textbf\{Produced by:\}.*?\n\n', '', doc)
doc = re.sub(r'\\textbf\{Intended audience:\}.*?\n\n', '', doc, flags=re.DOTALL)

# Fix Table of Contents as a section -> skip it (we use \tableofcontents)
doc = re.sub(r'\\section\{Table of Contents\}.*?(?=\\section)', '', doc, count=1, flags=re.DOTALL)

Path("HOW_TO_BUILD_AGENTS.tex").write_text(doc)
print(f"Wrote HOW_TO_BUILD_AGENTS.tex ({len(doc)} chars)")
