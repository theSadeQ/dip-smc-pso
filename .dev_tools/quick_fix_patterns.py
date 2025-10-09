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
    # CRITICAL files to process (11-30)
    critical_files = [
        "docs/factory/troubleshooting_guide.md",
        "docs/reports/pso_code_quality_beautification_assessment.md",
        "docs/PHASE_6_COMPLETION_REPORT.md",
        "docs/DOCUMENTATION_INVENTORY_SUMMARY.md",
        "docs/factory/pso_factory_api_reference.md",
        "docs/workflows/complete_integration_guide.md",
        "docs/benchmarks/phase_3_2_completion_report.md",
        "docs/reports/DOCUMENTATION_EXPERT_TECHNICAL_ASSESSMENT_REPORT.md",
        "docs/technical/factory_integration_fixes_issue6.md",
        "docs/GitHub_Issue_4_PSO_Integration_Resolution_Report.md",
        "docs/api/phase_4_3_completion_report.md",
        "docs/analysis/COMPLETE_CONTROLLER_COMPARISON_MATRIX.md",
        "docs/api/phase_4_1_completion_report.md",
        "docs/reports/GITHUB_ISSUE_6_FINAL_INTEGRATION_VALIDATION_REPORT.md",
        "docs/reports/PSO_OPTIMIZATION_TEST_VALIDATION_REPORT.md",
        "docs/guides/tutorials/tutorial-01-validation-report.md",
        "docs/fault_detection_system_documentation.md",
        "docs/reports/FACTORY_BEAUTIFICATION_OPTIMIZATION_REPORT.md",
        "docs/reports/GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md",
        "docs/reports/pso_code_quality_optimization_report.md",
    ]

    total_replacements = 0
    files_modified = 0

    for filepath_str in critical_files:
        filepath = Path(filepath_str)
        if not filepath.exists():
            print(f"[SKIP] {filepath_str}: File not found")
            continue

        count = fix_file(filepath)
        if count > 0:
            print(f"[OK] {filepath_str}: {count} replacements")
            files_modified += 1
            total_replacements += count
        else:
            print(f"[SKIP] {filepath_str}: No changes needed")

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Files modified: {files_modified}/{len(critical_files)}")
    print(f"  Total replacements: {total_replacements}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
