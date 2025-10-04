#!/usr/bin/env python3
#==========================================================================================\\\
#=================================== docs/validate_week2.py =============================\\\
#==========================================================================================\\\
"""
Week 2 Documentation Validation Script

Comprehensive validation of Week 2 Controllers & Mathematical Foundations documentation.
Validates file existence, line counts, code quality, and content structure.
"""

from pathlib import Path
import re
from typing import Dict, List, Tuple

# Expected files and minimum line counts (relative to docs/ directory)
EXPECTED_FILES = {
    "mathematical_foundations/smc_complete_theory.md": 800,
    "mathematical_foundations/controller_comparison_theory.md": 500,
    "controllers/classical_smc_technical_guide.md": 800,
    "controllers/adaptive_smc_technical_guide.md": 700,
    "controllers/sta_smc_technical_guide.md": 750,
    "controllers/factory_system_guide.md": 600,
    "controllers/control_primitives_reference.md": 400,
}

# Index files
INDEX_FILES = [
    "mathematical_foundations/index.md",
    "controllers/index.md"
]


def validate_file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return Path(filepath).exists()


def count_lines(filepath: str) -> int:
    """Count lines in file."""
    try:
        return len(Path(filepath).read_text(encoding='utf-8').splitlines())
    except Exception:
        return 0


def check_code_blocks(filepath: str) -> Tuple[int, int, List[Tuple[int, str]]]:
    """Count and validate Python code blocks."""
    content = Path(filepath).read_text(encoding='utf-8')
    code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)

    valid = 0
    invalid = []
    for i, code in enumerate(code_blocks, 1):
        try:
            compile(code, f"<{filepath}:block{i}>", "exec")
            valid += 1
        except SyntaxError as e:
            invalid.append((i, str(e)))

    return len(code_blocks), valid, invalid


def validate_cross_refs(filepath: str) -> Tuple[int, int]:
    """Check for cross-references."""
    content = Path(filepath).read_text(encoding='utf-8')
    doc_refs = re.findall(r'\{doc\}`([^`]+)`', content)
    ref_refs = re.findall(r'\{ref\}`([^`]+)`', content)
    return len(doc_refs), len(ref_refs)


def check_math_notation(filepath: str) -> int:
    """Count math blocks."""
    content = Path(filepath).read_text(encoding='utf-8')
    math_blocks = re.findall(r'```{math}', content)
    inline_math = re.findall(r'\$[^$]+\$', content)
    return len(math_blocks) + len(inline_math)


def validate_headers(filepath: str) -> bool:
    """Check for proper header structure."""
    content = Path(filepath).read_text(encoding='utf-8')
    # Check for at least one top-level header
    headers = re.findall(r'^# .+', content, re.MULTILINE)
    return len(headers) > 0


def main():
    print("=" * 70)
    print("WEEK 2 DOCUMENTATION VALIDATION REPORT")
    print("=" * 70)

    total_lines = 0
    all_valid = True
    total_code_blocks = 0
    total_valid_code = 0

    # Validate main content files
    for filepath, min_lines in EXPECTED_FILES.items():
        print(f"\n[FILE] {Path(filepath).name}")

        # Check existence
        if not validate_file_exists(filepath):
            print(f"  [FAIL] File does not exist!")
            all_valid = False
            continue
        else:
            print(f"  [PASS] File exists")

        # Check line count
        lines = count_lines(filepath)
        total_lines += lines
        if lines >= min_lines:
            print(f"  [PASS] Line count: {lines} (target: {min_lines}+)")
        else:
            print(f"  [WARN] Line count: {lines} (target: {min_lines}+)")
            all_valid = False

        # Check headers
        if validate_headers(filepath):
            print(f"  [PASS] Has proper header structure")
        else:
            print(f"  [WARN] Missing header structure")

        # Check code blocks
        if "technical_guide" in filepath or "primitives" in filepath or "factory" in filepath:
            total_blocks, valid_blocks, invalid = check_code_blocks(filepath)
            total_code_blocks += total_blocks
            total_valid_code += valid_blocks

            if total_blocks > 0:
                success_rate = (valid_blocks / total_blocks) * 100
                print(f"  [CODE] {total_blocks} blocks, {valid_blocks} valid ({success_rate:.1f}%)")

                if invalid and len(invalid) <= 3:  # Show up to 3 errors
                    for block_num, error in invalid[:3]:
                        # Encode error safely for Windows console
                        safe_error = error[:50].encode('ascii', errors='replace').decode('ascii')
                        print(f"    [WARN] Block {block_num}: {safe_error}...")

        # Check math notation
        if "theory" in filepath or "mathematical" in Path(filepath).parent.name:
            math_count = check_math_notation(filepath)
            if math_count > 0:
                print(f"  [MATH] {math_count} math notation instances")
            else:
                print(f"  [WARN] No math notation found (expected in theory docs)")

        # Check cross-references
        doc_refs, ref_refs = validate_cross_refs(filepath)
        if doc_refs > 0 or ref_refs > 0:
            print(f"  [REFS] {doc_refs} doc refs, {ref_refs} label refs")

    # Validate index files
    print("\n" + "=" * 70)
    print("INDEX FILES VALIDATION")
    print("=" * 70)

    for index_file in INDEX_FILES:
        print(f"\n[INDEX] {Path(index_file).name}")
        if validate_file_exists(index_file):
            print(f"  [PASS] Index file exists")
            lines = count_lines(index_file)
            print(f"  [INFO] Lines: {lines}")
        else:
            print(f"  [FAIL] Index file missing!")
            all_valid = False

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal Content Lines: {total_lines}")
    print(f"Target: 4,550+ lines")

    if total_lines >= 4550:
        print(f"[PASS] STATUS: DELIVERED - {total_lines} lines")
    else:
        print(f"[WARN] STATUS: BELOW TARGET - {total_lines} lines (target: 4,550+)")

    if total_code_blocks > 0:
        code_success_rate = (total_valid_code / total_code_blocks) * 100
        print(f"\nCode Quality: {total_valid_code}/{total_code_blocks} blocks valid ({code_success_rate:.1f}%)")
        if code_success_rate >= 90:
            print(f"[PASS] Code quality: EXCELLENT")
        elif code_success_rate >= 75:
            print(f"[INFO] Code quality: ACCEPTABLE (some snippets incomplete)")
        else:
            print(f"[FAIL] Code quality: NEEDS IMPROVEMENT")

    print("\n" + "=" * 70)

    if all_valid and total_lines >= 4550:
        print("[PASS] ALL VALIDATION CHECKS PASSED!")
        return 0
    else:
        print("[WARN] SOME VALIDATION CHECKS FAILED - REVIEW ABOVE")
        return 1


if __name__ == "__main__":
    exit(main())
