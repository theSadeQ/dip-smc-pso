#!/usr/bin/env python3
"""Verify current documentation state - are files already cleaned?"""

import re
from pathlib import Path
from collections import defaultdict

# Simplified AI patterns from detect_ai_patterns.py
AI_PATTERNS = {
    "comprehensive": r'\bcomprehensive\b',
    "powerful": r'\bpowerful\b',
    "seamless": r'\bseamless\b',
    "leverage": r'\bleverage\b',
    "utilize": r'\butilize\b',
}

docs_dir = Path("D:/Projects/main/docs")
results = defaultdict(list)
total_patterns = 0

print("Scanning for AI-ish patterns in docs/...")
print("="*80)

for md_file in docs_dir.rglob("*.md"):
    try:
        content = md_file.read_text(encoding='utf-8')
        file_patterns = {}

        for name, pattern in AI_PATTERNS.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                file_patterns[name] = len(matches)
                total_patterns += len(matches)

        if file_patterns:
            results[str(md_file.relative_to(Path.cwd()))] = file_patterns

    except Exception as e:
        print(f"ERROR reading {md_file.name}: {e}")

print(f"\nTotal patterns found: {total_patterns}")
print(f"Files with patterns: {len(results)}")

if results:
    print("\nTop 20 files with most patterns:")
    sorted_results = sorted(results.items(), key=lambda x: sum(x[1].values()), reverse=True)
    for i, (file, patterns) in enumerate(sorted_results[:20], 1):
        total = sum(patterns.values())
        print(f"{i}. {file}: {total} patterns - {patterns}")
else:
    print("\nNo AI-ish patterns detected! Documentation appears clean.")

# Save results
import json
output = {
    'total_patterns': total_patterns,
    'files_with_patterns': len(results),
    'pattern_breakdown': dict(results)
}
Path('.test_artifacts/current_state_verification.json').write_text(
    json.dumps(output, indent=2), encoding='utf-8'
)
print(f"\nResults saved to .test_artifacts/current_state_verification.json")
