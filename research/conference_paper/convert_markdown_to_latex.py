#!/usr/bin/env python3
"""
Markdown to LaTeX Conversion Script for LT-7 Research Paper
Automates conversion of remaining sections from LT7_RESEARCH_PAPER.md to LaTeX format
"""

import re
import sys
from pathlib import Path

# Section mapping: markdown section number -> LaTeX file
SECTION_MAP = {
    "2": "system_model.tex",
    "3": "controller_design.tex",
    "4": "stability_analysis.tex",
    "5": "pso_optimization.tex",
    "6": "experimental_setup.tex",
    "7": "performance_results.tex",
    "8": "robustness_analysis.tex",
    "9": "discussion.tex",
    "10": "conclusion.tex",
}

def convert_headers(text):
    """Convert markdown headers to LaTeX sections"""
    # ### -> \subsection{}
    text = re.sub(r'^### (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
    # #### -> \subsubsection{}
    text = re.sub(r'^#### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    return text

def convert_formatting(text):
    """Convert markdown formatting to LaTeX"""
    # **bold** -> \textbf{bold}
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\\textbf{\1}', text)
    # *italic* -> \textit{italic}
    text = re.sub(r'\*([^\*]+)\*', r'\\textit{\1}', text)
    # `code` -> \texttt{code}
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    return text

def convert_lists(text):
    """Convert markdown lists to LaTeX"""
    lines = text.split('\n')
    in_itemize = False
    in_enumerate = False
    result = []

    for line in lines:
        # Numbered list
        if re.match(r'^\d+\.\s+', line):
            if not in_enumerate:
                result.append('\\begin{enumerate}')
                in_enumerate = True
            item = re.sub(r'^\d+\.\s+', '', line)
            result.append(f'    \\item {item}')
        # Bullet list
        elif re.match(r'^[\-\*]\s+', line):
            if not in_itemize:
                result.append('\\begin{itemize}')
                in_itemize = True
            item = re.sub(r'^[\-\*]\s+', '', line)
            result.append(f'    \\item {item}')
        # End of list
        else:
            if in_enumerate:
                result.append('\\end{enumerate}')
                in_enumerate = False
            if in_itemize:
                result.append('\\end{itemize}')
                in_itemize = False
            result.append(line)

    # Close any open lists
    if in_enumerate:
        result.append('\\end{enumerate}')
    if in_itemize:
        result.append('\\end{itemize}')

    return '\n'.join(result)

def convert_citations(text):
    """Convert [1,2,3] to \cite{ref1,ref2,ref3}"""
    # Single citation: [1] -> \cite{ref1}
    text = re.sub(r'\[(\d+)\]', r'~\\cite{ref\1}', text)
    # Multiple citations: [1,2,3] -> \cite{ref1,ref2,ref3}
    def multi_cite(match):
        nums = match.group(1).split(',')
        refs = ','.join([f'ref{n.strip()}' for n in nums])
        return f'~\\cite{{{refs}}}'
    text = re.sub(r'\[(\d+(?:,\s*\d+)+)\]', multi_cite, text)
    return text

def convert_math(text):
    """Convert markdown math to LaTeX math"""
    # Inline math: $...$ stays as $...$
    # Block math: $$...$$ -> \[...\]
    text = re.sub(r'\$\$([^\$]+)\$\$', r'\\[\1\\]', text)
    return text

def convert_figures(text):
    """Convert figure references to LaTeX"""
    # **Figure 7.1:** -> \begin{figure}...\end{figure}
    def fig_ref(match):
        fig_num = match.group(1)
        caption = match.group(2)
        return f'''\\begin{{figure}}[t]
\\centering
\\includegraphics[width=\\columnwidth]{{figure_{fig_num}.pdf}}
\\caption{{{caption}}}
\\label{{fig:{fig_num}}}
\\end{{figure}}'''
    text = re.sub(r'\*\*Figure ([\d\.]+):\*\*\s*(.+)', fig_ref, text)
    return text

def convert_tables(text):
    """Convert markdown tables to LaTeX booktabs"""
    # TODO: Implement table conversion
    # Placeholder for now
    return text

def convert_section(markdown_text, section_num):
    """Convert a complete section from markdown to LaTeX"""
    # Apply all conversions
    latex = convert_headers(markdown_text)
    latex = convert_formatting(latex)
    latex = convert_lists(latex)
    latex = convert_citations(latex)
    latex = convert_math(latex)
    latex = convert_figures(latex)
    latex = convert_tables(latex)

    return latex

def main():
    """Main conversion function"""
    source_file = Path("../../analysis_reports/long_term/LT7_RESEARCH_PAPER.md")
    output_dir = Path(".")

    if not source_file.exists():
        print(f"[ERROR] Source file not found: {source_file}")
        return 1

    print(f"[INFO] Reading source file: {source_file}")
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract sections based on ## markers
    sections = re.split(r'^## (\d+)\.\s+', content, flags=re.MULTILINE)

    print(f"[INFO] Found {len(sections)//2} sections")

    # Process each section
    for i in range(1, len(sections), 2):
        section_num = sections[i]
        section_content = sections[i+1] if i+1 < len(sections) else ""

        if section_num in SECTION_MAP:
            output_file = output_dir / SECTION_MAP[section_num]
            print(f"[INFO] Converting Section {section_num} -> {output_file}")

            latex_content = convert_section(section_content, section_num)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"% Converted from LT7_RESEARCH_PAPER.md Section {section_num}\n")
                f.write(f"% Auto-generated by convert_markdown_to_latex.py\n\n")
                f.write(latex_content)

            print(f"[OK] Section {section_num} converted")

    print("[OK] Conversion complete")
    return 0

if __name__ == '__main__':
    sys.exit(main())
