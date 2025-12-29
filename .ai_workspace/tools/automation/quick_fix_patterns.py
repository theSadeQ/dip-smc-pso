#!/usr/bin/env python3
"""Quick batch replacement for AI-ish patterns in documentation."""

import re
from pathlib import Path
import sys

# Pattern replacements (context-aware)
REPLACEMENTS = [
    # Enthusiasm & Marketing
    (r'\bcomprehensive\s+(framework|system|suite|infrastructure)\b', r'\1'),
    (r'\bpowerful\s+(capabilities|features|tools|framework)\b', r'\1'),
    (r'\bseamless\s+(integration|workflow)\b', r'integration'),
    (r'\bcutting-edge\s+(algorithms|techniques)\b', r'algorithms (see references)'),
    (r'\bstate-of-the-art\s+(\w+)\b', r'\1 (see references)'),
    (r'\brobust\s+(implementation|system)\b', r'reliable \1'),

    # Hedge words
    (r'\bleverage\s+the\s+(\w+)\b', r'use the \1'),
    (r'\bleverages?\s+', r'uses '),
    (r'\butilize\s+', r'use '),
    (r'\bdelve\s+into\b', r'examine'),
    (r'\bfacilitate\s+', r'enable '),

    # Greeting language
    (r"Let's explore\s+", r'This section covers '),
    (r"Let's examine\s+", r'This section examines '),
    (r"Welcome!\s*", r''),
    (r"You'll love\s+", r''),

    # Repetitive structures
    (r'In this section we will\s+', r'This section covers '),
    (r'Now let\'s look at\s+', r'The following examines '),
    (r'As we can see,?\s*', r''),
    (r"It's worth noting that\s+", r''),
]

def fix_file(filepath: Path) -> int:
    """Apply pattern fixes to a single file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        replacements_made = 0

        for pattern, replacement in REPLACEMENTS:
            content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE | re.MULTILINE)
            replacements_made += count

        if content != original_content:
            filepath.write_text(content, encoding='utf-8')
            return replacements_made
        return 0
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return 0

def main():
    # Process ALL markdown files in docs/ recursively
    docs_dir = Path("docs/")
    if not docs_dir.exists():
        print(f"Error: {docs_dir} directory not found")
        sys.exit(1)

    # Find all markdown files
    all_md_files = sorted(docs_dir.rglob("*.md"))

    print(f"Found {len(all_md_files)} markdown files in docs/")
    print(f"{'='*60}\n")

    total_replacements = 0
    files_modified = 0

    for filepath in all_md_files:
        filepath_str = str(filepath)

        count = fix_file(filepath)
        if count > 0:
            print(f"[OK] {filepath_str}: {count} replacements")
            files_modified += 1
            total_replacements += count

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Files scanned: {len(all_md_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
