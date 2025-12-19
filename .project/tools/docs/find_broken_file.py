#!/usr/bin/env python
"""Find which markdown file causes Sphinx parsing error."""

import sys
from pathlib import Path
from docutils.core import publish_doctree
from myst_parser.parsers.docutils_ import Parser

def test_file(filepath):
    """Test if a markdown file can be parsed without errors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to parse with MyST
        parser = Parser()
        publish_doctree(
            source=content,
            source_path=str(filepath),
            parser=parser,
            settings_overrides={'report_level': 5}  # Suppress warnings
        )
        return None  # Success
    except AssertionError as e:
        if "isinstance(node.parent, nodes.document)" in str(e):
            return "TRANSITION_ERROR"
        return f"ASSERTION: {e}"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"

def main():
    docs_dir = Path('.')
    md_files = list(docs_dir.rglob('*.md'))

    # Exclude _build and _static
    md_files = [f for f in md_files if '_build' not in str(f) and '_static' not in str(f)]

    print(f"Testing {len(md_files)} markdown files...")

    problematic = []
    transition_errors = []

    for md_file in sorted(md_files):
        error = test_file(md_file)
        if error:
            problematic.append((md_file, error))
            if error == "TRANSITION_ERROR":
                transition_errors.append(md_file)
                print(f"[TRANSITION ERROR] {md_file}")
            else:
                print(f"[WARN] {md_file}: {error[:80]}")

    print(f"\nSummary: {len(transition_errors)} files with transition errors")
    for f in transition_errors:
        print(f"  - {f}")

    if not problematic:
        print("[OK] All files parsed successfully!")

    return 0 if not problematic else 1

if __name__ == '__main__':
    sys.exit(main())
