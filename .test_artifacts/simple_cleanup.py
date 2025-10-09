#!/usr/bin/env python3
"""Simple direct cleanup for remaining 45 AI-ish patterns."""

import re
from pathlib import Path
import json

# Simple direct replacements (no complex logic needed for 45 patterns)
REPLACEMENTS = [
    # Remove standalone marketing buzzwords
    (r'\bcomprehensive\s+', '', re.IGNORECASE),
    (r'\bpowerful\s+', '', re.IGNORECASE),
    (r'\bseamless\s+', '', re.IGNORECASE),
    (r'\bleverage\s+', 'use ', re.IGNORECASE),
    (r'\butilize\s+', 'use ', re.IGNORECASE),

    # Clean up spacing
    (r'\s{2,}', ' ', 0),
]

# Load file list
files_to_clean = json.load(open('.test_artifacts/final_cleanup_files.json'))

results = []
total_before = 0
total_after = 0

for file_path in files_to_clean:
    p = Path(file_path)
    if not p.exists():
        print(f"SKIP: {p.name} (not found)")
        continue

    content = p.read_text(encoding='utf-8')
    original = content
    replacements_made = 0

    # Apply replacements
    for pattern, replacement, flags in REPLACEMENTS:
        before_len = len(content)
        content = re.sub(pattern, replacement, content, flags=flags)
        after_len = len(content)
        if after_len != before_len:
            replacements_made += 1

    # Write back if changed
    if content != original:
        p.write_text(content, encoding='utf-8')
        print(f"[OK] {p.name}: Modified ({len(original)} -> {len(content)} chars)")
        total_before += len(original)
        total_after += len(content)
    else:
        print(f"[  ] {p.name}: No changes")

    results.append({
        'file': file_path,
        'size_before': len(original),
        'size_after': len(content),
        'modified': content != original
    })

print("\n" + "="*80)
print("CLEANUP SUMMARY")
print("="*80)
print(f"Files processed: {len(results)}")
print(f"Files modified: {sum(1 for r in results if r['modified'])}")
print(f"Total size reduction: {total_before - total_after:,} characters")
print("="*80)

# Save results
Path('.test_artifacts/simple_cleanup_results.json').write_text(
    json.dumps(results, indent=2), encoding='utf-8'
)
