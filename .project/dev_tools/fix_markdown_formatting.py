#!/usr/bin/env python3
"""
Fix Markdown formatting issues in plant/models_guide.md.
Ensures proper blank lines between block elements.
"""

import re
import sys
from pathlib import Path


def fix_markdown(content: str) -> str:
    """Fix Markdown formatting issues."""
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Add blank line before headings (except first line)
        if line.startswith('#') and i > 0 and fixed_lines and fixed_lines[-1].strip():
            if not fixed_lines[-1].startswith('#'):
                fixed_lines.append('')

        # Add blank line after closing $$ before text
        if line.strip() == '$$' and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.startswith('#') and not next_line.strip() == '---':
                fixed_lines.append(line)
                fixed_lines.append('')
                i += 1
                continue

        # Add blank line after closing ``` before text
        if line.strip() == '```' and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.startswith('#') and not next_line.strip() == '---':
                fixed_lines.append(line)
                fixed_lines.append('')
                i += 1
                continue

        # Split lines where heading appears after other content
        if ' ### ' in line or ' ## ' in line:
            parts = re.split(r'( ###? )', line)
            for j, part in enumerate(parts):
                if part.strip():
                    if j > 0 and (part.startswith(' ##') or part.startswith('##')):
                        fixed_lines.append('')
                    fixed_lines.append(part.strip())
            i += 1
            continue

        # Split lines where table starts after text
        if ' | ' in line and '|' in line:
            # Check if this is mid-line table start
            before_pipe = line[:line.index('|')].strip()
            if before_pipe and not before_pipe.endswith(':'):
                # Split: text before table, then table
                fixed_lines.append(before_pipe)
                fixed_lines.append('')
                fixed_lines.append(line[line.index('|'):])
                i += 1
                continue

        # Split lines where list starts after text
        if re.match(r'^.+:\s*\d+\.', line):
            # "Text: 1." pattern - split it
            match = re.match(r'^(.+?):\s*(\d+\..*)$', line)
            if match:
                fixed_lines.append(match.group(1) + ':')
                fixed_lines.append('')
                fixed_lines.append(match.group(2))
                i += 1
                continue

        # Add blank line before "Where:" after $$
        if line.strip().startswith('Where:') and fixed_lines and fixed_lines[-1].strip() == '$$':
            fixed_lines.append('')

        # Add blank line before lists after paragraphs
        if re.match(r'^\d+\. \*\*', line) and i > 0 and fixed_lines and fixed_lines[-1].strip():
            if not fixed_lines[-1].startswith((' ', '\t', '-', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                fixed_lines.append('')

        fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines)


def main():
    file_path = Path('docs/plant/models_guide.md')

    print(f"Reading {file_path}...")
    content = file_path.read_text(encoding='utf-8')

    print("Fixing Markdown formatting...")
    fixed_content = fix_markdown(content)

    print(f"Writing fixed content back to {file_path}...")
    file_path.write_text(fixed_content, encoding='utf-8')

    print("✓ Markdown formatting fixed!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
