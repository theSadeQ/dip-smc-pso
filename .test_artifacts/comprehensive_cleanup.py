"""
Comprehensive AI-ish pattern cleanup with aggressive pattern matching.
"""

import json
from pathlib import Path

# Load baseline scan
scan_file = Path('D:/Projects/main/.artifacts/docs_audit/baseline_scan_fixed_tool.json')
data = json.loads(scan_file.read_text())

def clean_line(line: str, pattern_type: str, pattern_text: str) -> str:
    """Apply context-aware cleanup based on pattern type and text."""
    import re

    if pattern_type == 'hedge_words':
        if pattern_text == 'capabilities':
            # "Add X capabilities" -> "Add X support"
            line = re.sub(r'(Add \w+(?: \w+)?) capabilities\b', r'\1 support', line)
            # "X capabilities" at end of sentence -> "X"
            line = re.sub(r'\bcapabilities\.\s*$', '.', line)
            # "with X and Y capabilities" -> "with X and Y"
            line = re.sub(r'(\w+) and (\w+) capabilities\b', r'\1 and \2', line)
            # "capabilities include" -> "features include"
            line = re.sub(r'\bcapabilities include\b', 'features include', line, flags=re.IGNORECASE)
            # "optimization capabilities" -> "optimization features"
            line = re.sub(r'\b(\w+) capabilities\b', r'\1 features', line)
            # "enhanced capabilities" -> "enhanced features"
            line = re.sub(r'\benhanced capabilities\b', 'enhanced features', line, flags=re.IGNORECASE)

        elif pattern_text in ['enable', 'enables']:
            # "enables advanced" -> "provides"
            line = re.sub(r'\benables advanced\b', 'provides', line, flags=re.IGNORECASE)
            # Keep "enables real-time", "enables logging", etc.

        elif pattern_text in ['facilitate', 'facilitates']:
            # "facilitates integration" -> "enables integration"
            line = re.sub(r'\bfacilitates integration\b', 'enables integration', line, flags=re.IGNORECASE)
            # "facilitates testing" -> "enables testing"
            line = re.sub(r'\bfacilitates testing\b', 'enables testing', line, flags=re.IGNORECASE)

        elif pattern_text == 'employ':
            # "employ advanced" -> "use"
            line = re.sub(r'\bemploy\w* advanced\b', 'use', line, flags=re.IGNORECASE)

    elif pattern_type == 'enthusiasm':
        if pattern_text in ['comprehensive', 'Comprehensive']:
            # Skip if metric-backed (e.g., "95%+ (Comprehensive)")
            if re.search(r'\d+%.*comprehensive', line, re.IGNORECASE):
                return line
            # "comprehensive framework/solution/testing" -> remove adjective
            line = re.sub(r'\bcomprehensive (framework|solution|testing|coverage|suite)\b', r'\1', line, flags=re.IGNORECASE)
            line = re.sub(r'\bA comprehensive\b', 'A', line, flags=re.IGNORECASE)
            line = re.sub(r'\bthe comprehensive\b', 'the', line, flags=re.IGNORECASE)
            # Standalone "Comprehensive" in headers -> remove
            line = re.sub(r'\(Comprehensive\)', '', line)

        elif pattern_text in ['powerful', 'Powerful']:
            # Keep if followed by "hardware" or in statistical context
            if 'hardware' in line.lower() or 'statistical' in line.lower():
                return line
            # "powerful controller/optimizer/framework" -> remove adjective
            line = re.sub(r'\bpowerful (controller|optimizer|framework|algorithm|tool|engine|system)\b', r'\1', line, flags=re.IGNORECASE)

    elif pattern_type == 'greeting':
        if pattern_text in ["Let's", "Let us"]:
            # "Let's explore..." -> "This section covers..."
            line = re.sub(r"Let'?s explore the", 'The', line, flags=re.IGNORECASE)
            line = re.sub(r"Let'?s explore", 'This section covers', line, flags=re.IGNORECASE)
            line = re.sub(r"Let us examine", 'This section examines', line, flags=re.IGNORECASE)

        elif pattern_text in ['We will', 'we will']:
            line = re.sub(r'\bWe will discuss\b', 'This guide covers', line, flags=re.IGNORECASE)
            line = re.sub(r'\bWe will explore\b', 'This guide covers', line, flags=re.IGNORECASE)

    elif pattern_type == 'repetitive':
        if 'In this section' in line:
            line = re.sub(r'^In this section we will\b', 'This section covers', line, flags=re.IGNORECASE)
            line = re.sub(r'^In this section\b', 'This section covers', line, flags=re.IGNORECASE)

    return line

# Process all files
print("=" * 90)
print("COMPREHENSIVE AI-ISH PATTERN CLEANUP")
print("=" * 90)

total_files = 0
total_patterns_cleaned = 0
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

    # Read file
    try:
        content = path.read_text(encoding='utf-8')
        lines = content.splitlines(keepends=True)
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
        continue

    # Track changes
    changes_made = 0
    changes_list = []

    # Process patterns
    for pattern_type, patterns in file_entry['patterns'].items():
        for pattern in patterns:
            line_num = pattern['line']
            pattern_text = pattern['text']

            if 1 <= line_num <= len(lines):
                original_line = lines[line_num - 1]
                cleaned_line = clean_line(original_line, pattern_type, pattern_text)

                if cleaned_line != original_line:
                    lines[line_num - 1] = cleaned_line
                    changes_made += 1
                    changes_list.append({
                        'line': line_num,
                        'pattern': pattern_text,
                        'type': pattern_type,
                        'before': original_line.strip()[:80],
                        'after': cleaned_line.strip()[:80]
                    })

    # Write back if changes
    if changes_made > 0:
        try:
            path.write_text(''.join(lines), encoding='utf-8')
            total_files += 1
            total_patterns_cleaned += changes_made
            file_changes[str(file_path)] = changes_list

            short_path = str(file_path).replace('D:/Projects/main/', '')
            print(f"[OK] {short_path}: {changes_made} patterns cleaned")
        except Exception as e:
            print(f"[ERROR] Could not write {file_path}: {e}")

print("=" * 90)
print("SUMMARY:")
print(f"Files processed: {total_files}")
print(f"Patterns cleaned: {total_patterns_cleaned}")
print("=" * 90)

# Save changes
changes_file = Path('D:/Projects/main/.artifacts/docs_audit/comprehensive_cleanup_changes.json')
changes_file.write_text(json.dumps(file_changes, indent=2))
print(f"\nDetailed changes saved to: {changes_file}")
