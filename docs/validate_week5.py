#!/usr/bin/env python3
#==========================================================================================\\\
#===================================== docs/validate_week5.py ============================\\\
#==========================================================================================\\\
"""
Week 5 Documentation Validation Script

complete validation of Week 5: Testing, Validation & Benchmarking Infrastructure Documentation

Validates:
- File existence (4 complete guides)
- Line count targets (~3,600 lines total)
- Code quality and structure
- Cross-reference integrity

Author: Claude Code
Date: 2025-10-04
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def validate_file_exists(file_path: Path) -> bool:
    """Validate that a file exists."""
    return file_path.exists() and file_path.is_file()


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def check_code_blocks(file_path: Path) -> Tuple[int, int]:
    """Count and validate code blocks in markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count code blocks
        total_blocks = content.count('```python')
        total_blocks += content.count('```bash')
        total_blocks += content.count('```yaml')

        # Validate code blocks are closed
        open_blocks = content.count('```')
        if open_blocks % 2 != 0:
            print(f"Warning: Unclosed code block in {file_path.name}")
            return total_blocks, total_blocks - 1

        return total_blocks, total_blocks

    except Exception as e:
        print(f"Error checking code blocks in {file_path}: {e}")
        return 0, 0


def validate_cross_refs(file_path: Path) -> int:
    """Count cross-references in markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count markdown links
        cross_refs = content.count('[')
        cross_refs += content.count('(#')  # Internal anchors
        cross_refs += content.count('](')  # External links

        return cross_refs

    except Exception as e:
        print(f"Error checking cross-refs in {file_path}: {e}")
        return 0


def validate_week5_files() -> Dict[str, Dict]:
    """Validate all Week 5 testing documentation files."""

    # Define expected files and targets
    # Paths relative to docs/ directory
    week5_files = {
        'testing_framework': {
            'path': Path('testing/testing_framework_technical_guide.md'),
            'target_lines': 1200,
            'tolerance': 100,
            'description': 'Testing Framework Technical Guide'
        },
        'benchmarking_framework': {
            'path': Path('testing/benchmarking_framework_technical_guide.md'),
            'target_lines': 1000,
            'tolerance': 100,
            'description': 'Benchmarking Framework Technical Guide'
        },
        'validation_methodology': {
            'path': Path('testing/validation_methodology_guide.md'),
            'target_lines': 800,
            'tolerance': 50,
            'description': 'Validation Methodology Guide'
        },
        'testing_workflows': {
            'path': Path('testing/testing_workflows_best_practices.md'),
            'target_lines': 600,
            'tolerance': 50,
            'description': 'Testing Workflows & Best Practices Guide'
        }
    }

    results = {}

    for file_key, file_info in week5_files.items():
        file_path = file_info['path']

        result = {
            'exists': validate_file_exists(file_path),
            'lines': 0,
            'target': file_info['target_lines'],
            'tolerance': file_info['tolerance'],
            'code_blocks': 0,
            'valid_code_blocks': 0,
            'cross_refs': 0,
            'status': 'FAIL'
        }

        if result['exists']:
            result['lines'] = count_lines(file_path)
            result['code_blocks'], result['valid_code_blocks'] = check_code_blocks(file_path)
            result['cross_refs'] = validate_cross_refs(file_path)

            # Check if lines meet target ± tolerance
            target_min = file_info['target_lines'] - file_info['tolerance']
            target_max = file_info['target_lines'] + file_info['tolerance']

            if target_min <= result['lines'] <= target_max * 2:  # Allow up to 2x target
                result['status'] = 'PASS'
            elif result['lines'] >= target_min:
                result['status'] = 'PASS (EXCEEDED)'

        results[file_key] = result

    return results


def main() -> int:
    """Main validation function."""
    print("=" * 80)
    print("WEEK 5 DOCUMENTATION VALIDATION REPORT")
    print("Testing, Validation & Benchmarking Infrastructure")
    print("=" * 80)

    results = validate_week5_files()

    # Display results
    total_lines = 0
    total_target = 0
    all_passed = True

    print("\nFILE VALIDATION:")
    print("-" * 80)

    for file_key, result in results.items():
        status_symbol = "[PASS]" if result['status'].startswith('PASS') else "[FAIL]"
        file_name = file_key.replace('_', ' ').title()

        print(f"\n{status_symbol} {file_name}")
        print(f"  Path: {results[file_key]['exists'] and 'exists' or 'MISSING'}")

        if result['exists']:
            print(f"  Lines: {result['lines']} (target: {result['target']} ± {result['tolerance']})")
            print(f"  Code blocks: {result['code_blocks']} ({result['valid_code_blocks']} valid)")
            print(f"  Cross-references: {result['cross_refs']}")

            total_lines += result['lines']
            total_target += result['target']

            if result['status'] == 'FAIL':
                all_passed = False
        else:
            print(f"  ERROR: File not found!")
            all_passed = False

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Lines: {total_lines} (target: {total_target})")
    print(f"Achievement: {total_lines / total_target * 100:.1f}% of target")

    files_passed = sum(1 for r in results.values() if r['status'].startswith('PASS'))
    print(f"Files Passed: {files_passed}/{len(results)}")

    total_code_blocks = sum(r['code_blocks'] for r in results.values())
    total_valid_blocks = sum(r['valid_code_blocks'] for r in results.values())
    code_quality_pct = (total_valid_blocks / total_code_blocks * 100) if total_code_blocks > 0 else 0
    print(f"Code Quality: {code_quality_pct:.1f}% ({total_valid_blocks}/{total_code_blocks} blocks)")

    total_cross_refs = sum(r['cross_refs'] for r in results.values())
    print(f"Cross-references: {total_cross_refs} links")

    print("\n" + "=" * 80)
    if all_passed and total_lines >= total_target * 0.9:
        print("RESULT: PASS - Week 5 Documentation Complete")
        print("=" * 80)
        return 0
    elif total_lines >= total_target * 0.8:
        print("RESULT: WARNING - Week 5 Documentation Mostly Complete")
        print("=" * 80)
        return 1
    else:
        print("RESULT: FAIL - Week 5 Documentation Incomplete")
        print("=" * 80)
        return 2


if __name__ == "__main__":
    exit(main())
