#!/usr/bin/env python3
"""
Comprehensive Markdown heading formatter for Sphinx documentation.

Fixes two main patterns that cause Sphinx sidebar rendering issues:
1. Multiple headings on same line: # Title ## Subtitle
2. Heading followed by body text: ## Heading Body text continues...

Usage:
    python fix_all_markdown_headings.py file1.md file2.md ...
    python fix_all_markdown_headings.py @filelist.txt
"""

import re
import sys
from pathlib import Path
from typing import List


def fix_heading_line(line: str) -> List[str]:
    """
    Fix heading line with multiple aggressive patterns.

    Returns list of lines (may split into multiple lines).
    Applies patterns in priority order, recursing on splits.

    Args:
        line: Input line to process

    Returns:
        List of lines (original if no issues, split if issues found)
    """
    # Only process lines starting with heading markers
    if not line.strip().startswith('#'):
        return [line]

    # Pattern 1: Multiple headings on same line (HIGHEST PRIORITY)
    # Match: # Title ## Subtitle  or  ## Title ### Something
    # Split before the second heading marker
    match = re.match(r'^(\s*#{1,6}\s+[^#\n]+?)\s+(#{2,6}\s+)', line)
    if match:
        before = match.group(1).rstrip()
        after = line[len(match.group(1)):].lstrip()
        # Recurse on 'after' to handle remaining issues
        after_fixed = fix_heading_line(after)
        return [before + '\n', '\n'] + after_fixed

    # Pattern 2: Code block after heading
    # Match: ## Title ```bash  or  ## Title ```python
    match = re.match(r'^(#{1,6}\s+[^\n]+?)\s+(```[\w]*)', line)
    if match:
        heading = match.group(1).rstrip()
        rest = line[len(heading):].lstrip()
        return [heading + '\n', '\n', rest]

    # Pattern 3: Punctuation Detection (IMPROVED)
    # Match: ## What is X? This framework...  or  # Title! Welcome...
    # Split at capital letter if punctuation exists anywhere in heading
    # Also catches: "# Getting Started Welcome..." (! at end of line)
    if any(punct in line for punct in ['. ', '! ', '? ']):
        # Find capital letter after reasonable heading length
        match = re.match(r'^(#{1,6}\s+[^#]{8,90}?)\s+([A-Z][a-z]{2,}.{12,})', line)
        if match:
            heading_part = match.group(1).rstrip()
            body_part = match.group(2)
            # Verify heading ends sensibly (not mid-word)
            if heading_part[-1] in ' !?.,:;-' or heading_part[-1].isupper():
                return [heading_part + '\n', '\n', body_part]

    # Pattern 4: Colon Patterns (BIDIRECTIONAL)
    # Pattern 4A: Capital word BEFORE colon (e.g., "JSON Run validator:")
    match = re.match(r'^(#{1,6}\s+.{8,60}?)\s+([A-Z][a-z]{2,}[^:]{5,40}?:)', line)
    if match:
        heading = match.group(1).rstrip()
        rest = line[len(heading):].lstrip()
        # Ensure we're not splitting valid title formatting
        if len(rest) > 15 and not rest.startswith('**'):
            return [heading + '\n', '\n', rest]

    # Pattern 4B: Capital word AFTER colon (e.g., "Title: This is body")
    match = re.match(r'^(#{1,6}\s+.+?:)\s+([A-Z][a-z]{2,}.{10,})', line)
    if match:
        heading = match.group(1).rstrip()
        rest = line[len(heading):].lstrip()
        return [heading + '\n', '\n', rest]

    # Pattern 5: Sentence Starter Detection (MAXIMUM AGGRESSIVENESS)
    # Look for sentence starter words after first 5-80 chars of heading
    sentence_starters = [
        'Welcome', 'The', 'This', 'These', 'That', 'Those',
        'Run', 'Start', 'Follow', 'Execute', 'Install', 'Open',
        'A', 'An', 'In', 'On', 'At', 'To', 'For', 'With', 'By',
        'Provides', 'Includes', 'Contains', 'Implements',
        'Supports', 'Requires', 'Ensures', 'Allows', 'Enables',
        'It', 'You', 'We', 'They', 'See', 'When', 'How',
        'What', 'Why', 'Where', 'Which', 'Who', 'Adjust', 'Click'
    ]

    # Build regex to match any sentence starter after heading
    starter_pattern = '|'.join(re.escape(word) for word in sentence_starters)
    # Reduced minimums: 5-80 char heading, 12+ chars after starter
    match = re.match(fr'^(#{1,6}\s+[^#]{{5,80}}?)\s+({starter_pattern})\b\s*(.{{12,}})', line)
    if match:
        heading = match.group(1).rstrip()
        rest = line[len(heading):].lstrip()
        # Extra validation: ensure heading doesn't end mid-word
        if len(heading.strip()) >= 10:  # Avoid splitting very short headings
            return [heading + '\n', '\n', rest]

    # Pattern 6: List marker
    # Match: ## Key Features - **Item 1**
    match = re.match(r'^(#{1,6}\s+[^\n]+?)\s+([-*]\s+\*\*)', line)
    if match:
        heading = match.group(1).rstrip()
        rest = line[len(heading):].lstrip()
        return [heading + '\n', '\n', rest]

    # Pattern 7: Excessive Length + Sentence Starter (NEW - Conservative Safety Net)
    # If line > 150 chars AND contains sentence starter, likely has body text
    if len(line) > 150:
        # Reuse sentence starters from Pattern 5
        sentence_starters = [
            'Welcome', 'The', 'This', 'These', 'That', 'Those',
            'Run', 'Start', 'Follow', 'Execute', 'Install',
            'A', 'An', 'In', 'On', 'At', 'To', 'For', 'With', 'By',
            'Provides', 'Includes', 'Contains', 'Implements',
            'Supports', 'Requires', 'Ensures', 'Allows', 'Enables'
        ]
        starter_pattern = '|'.join(re.escape(word) for word in sentence_starters)
        # Only split if we find a sentence starter in the long line
        match = re.match(fr'^(#{1,6}\s+.{{15,100}}?)\s+({starter_pattern})\b(.{{20,}})', line)
        if match:
            heading = match.group(1).rstrip()
            rest = line[len(heading):].lstrip()
            return [heading + '\n', '\n', rest]

    # No issues found, return line as-is
    return [line]


def process_file(filepath: Path) -> bool:
    """
    Process a single markdown file, fixing heading issues.

    Returns True if file was modified, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Process each line
        new_lines = []
        modified = False

        for line in lines:
            fixed = fix_heading_line(line)
            if len(fixed) > 1 or (len(fixed) == 1 and fixed[0] != line):
                modified = True
            new_lines.extend(fixed)

        # Write back if modified
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Fixed: {filepath}")
            return True

        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_all_markdown_headings.py file1.md file2.md ...")
        print("       python fix_all_markdown_headings.py @filelist.txt")
        sys.exit(1)

    files_to_process = []

    # Handle @filelist.txt syntax
    for arg in sys.argv[1:]:
        if arg.startswith('@'):
            # Read file list from file
            listfile = Path(arg[1:])
            if not listfile.exists():
                print(f"File list not found: {listfile}", file=sys.stderr)
                sys.exit(1)

            with open(listfile, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        files_to_process.append(Path(line))
        else:
            files_to_process.append(Path(arg))

    # Process all files
    total = len(files_to_process)
    modified = 0

    for filepath in files_to_process:
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            continue

        if process_file(filepath):
            modified += 1

    print(f"\nProcessed {total} files, modified {modified}")


if __name__ == '__main__':
    main()
