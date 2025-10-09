"""
Batch cleanup of AI-ish patterns in documentation files.
Applies context-aware replacements based on REPLACEMENT_GUIDELINES.md
"""

import json
from pathlib import Path
import re

# Load the baseline scan
scan_file = Path('D:/Projects/main/.artifacts/docs_audit/baseline_scan_fixed_tool.json')
data = json.loads(scan_file.read_text())

# Replacement rules (context-aware)
def clean_capabilities(line: str) -> str:
    """Remove redundant 'capabilities' word."""
    # "Add X capabilities" -> "Add X support"
    line = re.sub(r'(Add \w+ (?:sensor|controller|optimizer)) capabilities', r'\1 support', line)
    line = re.sub(r'(Add analog|digital|IMU) capabilities', r'\1 support', line)

    # "with X and Y capabilities" -> "with X and Y"
    line = re.sub(r'(\w+) and (\w+) calculation capabilities', r'\1 and \2 calculation', line)
    line = re.sub(r'fusion and orientation calculation capabilities', r'fusion and orientation calculation', line)

    # "capabilities include" -> "features include"
    line = re.sub(r'\bcapabilities include\b', 'features include', line, flags=re.IGNORECASE)

    # "optimization capabilities" -> "optimization features"
    line = re.sub(r'\boptimization capabilities\b', 'optimization features', line, flags=re.IGNORECASE)

    return line

def clean_comprehensive(line: str) -> str:
    """Remove non-metric-backed 'comprehensive' usage."""
    # Keep metric-backed uses like "95%+ (Comprehensive)"
    if re.search(r'\d+%.*comprehensive', line, re.IGNORECASE):
        return line

    # Remove from "comprehensive framework/solution/testing"
    line = re.sub(r'\bcomprehensive (framework|solution|testing|coverage)\b', r'\1', line, flags=re.IGNORECASE)
    line = re.sub(r'\bA comprehensive\b', 'A', line, flags=re.IGNORECASE)
    line = re.sub(r'\bthe comprehensive\b', 'the', line, flags=re.IGNORECASE)

    return line

def clean_powerful(line: str) -> str:
    """Remove non-technical 'powerful' usage."""
    # Keep technical uses like "requires powerful hardware"
    if 'hardware' in line.lower() or 'statistical' in line.lower():
        return line

    line = re.sub(r'\bpowerful (controller|optimizer|framework|algorithm)\b', r'\1', line, flags=re.IGNORECASE)

    return line

def clean_enable_facilitate(line: str) -> str:
    """Refine enable/facilitate usage."""
    # "enables real-time" is OK, but "enables advanced" is not
    line = re.sub(r'\benables advanced\b', 'provides', line, flags=re.IGNORECASE)
    line = re.sub(r'\bfacilitates integration\b', 'enables integration', line, flags=re.IGNORECASE)
    line = re.sub(r'\bfacilitates testing\b', 'enables testing', line, flags=re.IGNORECASE)

    return line

def clean_greeting(line: str) -> str:
    """Remove greeting phrases."""
    # "Let's explore..." -> "This section covers..."
    line = re.sub(r"Let's explore the", 'The', line)
    line = re.sub(r"Let's explore", 'This section covers', line)
    line = re.sub(r"We will discuss", 'This guide covers', line)
    line = re.sub(r"Welcome!", '', line)

    return line

def clean_repetitive(line: str) -> str:
    """Remove repetitive structures."""
    line = re.sub(r'^In this section we will\b', 'This section covers', line, flags=re.IGNORECASE)
    line = re.sub(r'^In this section\b', 'This section covers', line, flags=re.IGNORECASE)

    return line

def clean_file(file_path: str, patterns: dict) -> tuple[int, list]:
    """Clean a single file based on detected patterns."""
    path = Path(file_path)
    if not path.exists():
        return 0, []

    content = path.read_text(encoding='utf-8')
    lines = content.splitlines(keepends=True)

    changes = []
    modifications = 0

    # Apply all cleaning functions
    for i, line in enumerate(lines, 1):
        original = line

        # Apply cleaners if patterns exist in this category
        if 'hedge_words' in patterns:
            line = clean_capabilities(line)
            line = clean_enable_facilitate(line)

        if 'enthusiasm' in patterns:
            line = clean_comprehensive(line)
            line = clean_powerful(line)

        if 'greeting' in patterns:
            line = clean_greeting(line)

        if 'repetitive' in patterns:
            line = clean_repetitive(line)

        if line != original:
            modifications += 1
            changes.append({
                'line': i,
                'before': original.strip(),
                'after': line.strip()
            })

        lines[i - 1] = line

    if modifications > 0:
        path.write_text(''.join(lines), encoding='utf-8')

    return modifications, changes

# Process all files except DOCUMENTATION_STYLE_GUIDE.md
print("=" * 90)
print("BATCH CLEANUP OF AI-ISH PATTERNS")
print("=" * 90)

total_files_processed = 0
total_patterns_removed = 0
all_changes = {}

for file_entry in data['files']:
    file_path = file_entry['file']

    # Skip DOCUMENTATION_STYLE_GUIDE.md (intentional examples)
    if 'DOCUMENTATION_STYLE_GUIDE.md' in file_path:
        continue

    if file_entry['total_issues'] == 0:
        continue

    patterns = file_entry['patterns']
    mods, changes = clean_file(file_path, patterns)

    if mods > 0:
        total_files_processed += 1
        total_patterns_removed += mods
        all_changes[file_path] = changes

        short_path = file_path.replace('D:/Projects/main/', '')
        print(f"[OK] {short_path}: {mods} patterns cleaned")

print("=" * 90)
print("SUMMARY:")
print(f"Files processed: {total_files_processed}")
print(f"Patterns removed: {total_patterns_removed}")
print("=" * 90)

# Save detailed changes
changes_file = Path('D:/Projects/main/.artifacts/docs_audit/batch_cleanup_changes.json')
changes_file.write_text(json.dumps(all_changes, indent=2))
print(f"\nDetailed changes saved to: {changes_file}")
