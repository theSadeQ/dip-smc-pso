"""
Final targeted cleanup for remaining AI-ish patterns.
Focuses on: excellent, enable (context), comprehensive, capabilities, welcome, Let's
"""

import json
from pathlib import Path
import re

# Load post-cleanup scan
scan_file = Path('D:/Projects/main/.artifacts/docs_audit/post_cleanup_full_scan.json')
data = json.loads(scan_file.read_text())

def clean_line_targeted(line: str, pattern_text: str, pattern_type: str) -> str:
    """Apply aggressive targeted cleanup."""

    pattern_lower = pattern_text.lower()

    if pattern_lower == 'excellent':
        # Remove "excellent" unless it's "excellent agreement" (technical)
        if 'excellent agreement' not in line.lower():
            line = re.sub(r'\bexcellent\s+', '', line, flags=re.IGNORECASE)
            line = re.sub(r'\bexcellent\b', 'good', line, flags=re.IGNORECASE)

    elif pattern_lower == 'enable':
        # Only keep if truly technical ("enable logging", "enable real-time")
        if not any(x in line.lower() for x in ['logging', 'real-time', 'debugging', 'monitoring', 'tracing']):
            line = re.sub(r'\benables\s+', 'provides ', line, flags=re.IGNORECASE)

    elif pattern_lower == 'comprehensive':
        # Remove unless metric-backed
        if not re.search(r'\d+%', line):
            line = re.sub(r'\bcomprehensive\s+', '', line, flags=re.IGNORECASE)
            line = re.sub(r'\bthe\s+comprehensive\b', 'the', line, flags=re.IGNORECASE)

    elif pattern_lower == 'capabilities':
        line = re.sub(r'\bcapabilities\b', 'features', line, flags=re.IGNORECASE)

    elif pattern_lower == 'welcome':
        # Remove "Welcome!" entirely
        line = re.sub(r'\bWelcome!\s*', '', line, flags=re.IGNORECASE)

    elif pattern_lower in ["let's", "let us"]:
        line = re.sub(r"Let'?s\s+explore", 'This section covers', line, flags=re.IGNORECASE)
        line = re.sub(r"Let\s+us\s+examine", 'This section examines', line, flags=re.IGNORECASE)

    elif pattern_lower == "we'll":
        line = re.sub(r"\bWe'?ll\s+", 'This guide will ', line, flags=re.IGNORECASE)

    elif pattern_lower == 'powerful':
        # Remove unless "hardware" context
        if 'hardware' not in line.lower():
            line = re.sub(r'\bpowerful\s+', '', line, flags=re.IGNORECASE)

    elif pattern_lower == 'seamless':
        line = re.sub(r'\bseamless\s+', '', line, flags=re.IGNORECASE)

    elif pattern_lower == 'cutting-edge':
        line = re.sub(r'\bcutting-edge\s+', '', line, flags=re.IGNORECASE)

    elif pattern_lower == 'superior performance':
        line = re.sub(r'\bsuperior performance\b', 'good performance', line, flags=re.IGNORECASE)

    elif pattern_lower == 'exploit':
        # Only remove in marketing context, keep in technical context
        if 'exploit' in line and 'vulnerability' not in line.lower():
            line = re.sub(r'\bexploit\s+', 'use ', line, flags=re.IGNORECASE)

    return line

print("=" * 90)
print("FINAL TARGETED CLEANUP")
print("=" * 90)

total_files = 0
total_cleaned = 0
file_changes = {}

for file_entry in data['files']:
    file_path = file_entry['file']

    # Skip DOCUMENTATION_STYLE_GUIDE.md
    if 'DOCUMENTATION_STYLE_GUIDE.md' in file_path:
        continue

    if file_entry['total_issues'] == 0:
        continue

    path = Path(file_path)
    if not path.exists():
        continue

    try:
        content = path.read_text(encoding='utf-8')
        lines = content.splitlines(keepends=True)
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        continue

    changes = 0
    change_list = []

    # Process all patterns
    for pattern_type, patterns in file_entry['patterns'].items():
        for pattern in patterns:
            line_num = pattern['line']
            pattern_text = pattern['text']

            if 1 <= line_num <= len(lines):
                original = lines[line_num - 1]
                cleaned = clean_line_targeted(original, pattern_text, pattern_type)

                if cleaned != original:
                    lines[line_num - 1] = cleaned
                    changes += 1
                    change_list.append({
                        'line': line_num,
                        'pattern': pattern_text,
                        'before': original.strip()[:80],
                        'after': cleaned.strip()[:80]
                    })

    if changes > 0:
        try:
            path.write_text(''.join(lines), encoding='utf-8')
            total_files += 1
            total_cleaned += changes
            file_changes[str(file_path)] = change_list

            short_path = str(file_path).replace('D:/Projects/main/', '')
            print(f"[OK] {short_path}: {changes} patterns")
        except Exception as e:
            print(f"[ERROR] Could not write {file_path}: {e}")

print("=" * 90)
print(f"Files processed: {total_files}")
print(f"Patterns cleaned: {total_cleaned}")
print("=" * 90)

# Save changes
changes_file = Path('D:/Projects/main/.artifacts/docs_audit/final_cleanup_changes.json')
changes_file.write_text(json.dumps(file_changes, indent=2))
print(f"\nChanges saved to: {changes_file}")
