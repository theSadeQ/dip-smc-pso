#!/usr/bin/env python
"""
Deduplicate BibTeX file by keeping only the first occurrence of each entry key.
"""
import sys
import re

def deduplicate_bibtex(input_file, output_file):
    """Read a .bib file, remove duplicates, write to output."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all bibtex entries with their keys
    # Pattern: @TYPE{KEY,
    entry_pattern = re.compile(r'@(\w+)\{([^,\s]+),', re.MULTILINE)

    seen_keys = set()
    entries = []
    current_entry = []
    in_entry = False
    brace_count = 0

    lines = content.split('\n')

    for line in lines:
        # Check if this line starts a new entry
        match = entry_pattern.match(line.strip())
        if match and not in_entry:
            entry_type, key = match.groups()

            if key not in seen_keys:
                seen_keys.add(key)
                in_entry = True
                current_entry = [line]
                brace_count = line.count('{') - line.count('}')
            # If key already seen, skip this entry
            continue

        if in_entry:
            current_entry.append(line)
            brace_count += line.count('{') - line.count('}')

            # Entry complete when braces balanced
            if brace_count == 0:
                entries.append('\n'.join(current_entry))
                current_entry = []
                in_entry = False
        elif not match and line.strip():
            # Non-entry lines (comments, preamble)
            entries.append(line)

    # Write deduplicated entries
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(entries))

    print(f"[OK] Deduplicated {input_file}")
    print(f"[OK] Found {len(seen_keys)} unique entries")
    print(f"[OK] Wrote to {output_file}")

    return len(seen_keys)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python deduplicate_bibtex.py input.bib output.bib")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    count = deduplicate_bibtex(input_file, output_file)
    print(f"\\n[INFO] Total unique citations: {count}")
