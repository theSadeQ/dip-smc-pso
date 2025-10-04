#!/usr/bin/env python3
#==========================================================================================\\\
#=================================== docs/validate_week34.py ============================\\\
#==========================================================================================\\\
"""
Week 3 & 4 Documentation Validation Script

Comprehensive validation of:
- Week 3: Plant Models & Optimization/Simulation Infrastructure
- Week 4: Advanced Controllers (Hybrid SMC, MPC, Swing-Up)

Validates file existence, line counts, code quality, and content structure.
"""

from pathlib import Path
import re
from typing import Dict, List, Tuple

# Week 3: Plant Models & Optimization/Simulation
WEEK3_FILES = {
    "plant/models_guide.md": 900,
    "plant/index.md": 100,
    "optimization_simulation/guide.md": 1200,
    "optimization_simulation/index.md": 100,
}

# Week 4: Advanced Controllers
WEEK4_FILES = {
    "controllers/hybrid_smc_technical_guide.md": 800,
    "controllers/mpc_technical_guide.md": 900,
    "controllers/swing_up_smc_technical_guide.md": 700,
}

# Updated index files
INDEX_FILES = [
    "controllers/index.md",
    "plant/index.md",
    "optimization_simulation/index.md",
]

# Combined target
TOTAL_TARGET_LINES = 4700


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
    """Count math blocks and inline math."""
    content = Path(filepath).read_text(encoding='utf-8')
    math_blocks = re.findall(r'```{math}', content)
    inline_math = re.findall(r'\$[^$]+\$', content)
    display_math = re.findall(r'\$\$[^$]+\$\$', content)
    return len(math_blocks) + len(inline_math) + len(display_math)


def validate_headers(filepath: str) -> bool:
    """Check for proper header structure."""
    content = Path(filepath).read_text(encoding='utf-8')
    # Check for at least one top-level header
    headers = re.findall(r'^# .+', content, re.MULTILINE)
    return len(headers) > 0


def check_ascii_banner(filepath: str) -> bool:
    """Check for ASCII banner header."""
    content = Path(filepath).read_text(encoding='utf-8')
    # Check for pattern: #==...===\\\
    banner_pattern = r'^#{2,}=+\\{3,}$'
    banners = re.findall(banner_pattern, content, re.MULTILINE)
    return len(banners) >= 2  # Expect top and bottom banner


def validate_file_group(files: Dict[str, int], group_name: str) -> Tuple[int, int, int, int]:
    """Validate a group of files and return stats."""
    print(f"\n{'=' * 70}")
    print(f"{group_name}")
    print(f"{'=' * 70}")

    total_lines = 0
    total_code_blocks = 0
    total_valid_code = 0
    all_valid = True

    for filepath, min_lines in files.items():
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
            percentage = (lines / min_lines) * 100
            print(f"  [PASS] Line count: {lines} (target: {min_lines}+, {percentage:.0f}%)")
        else:
            print(f"  [WARN] Line count: {lines} (target: {min_lines}+)")
            all_valid = False

        # Check headers
        if validate_headers(filepath):
            print(f"  [PASS] Has proper header structure")
        else:
            print(f"  [WARN] Missing header structure")

        # Check ASCII banner for technical guides
        if "technical_guide" in filepath or "models_guide" in filepath:
            if check_ascii_banner(filepath):
                print(f"  [PASS] ASCII banner header present")
            else:
                print(f"  [INFO] No ASCII banner (may be optional for this file)")

        # Check code blocks
        if any(keyword in filepath for keyword in ["guide", "technical", "models"]):
            total_blocks, valid_blocks, invalid = check_code_blocks(filepath)
            total_code_blocks += total_blocks
            total_valid_code += valid_blocks

            if total_blocks > 0:
                success_rate = (valid_blocks / total_blocks) * 100
                print(f"  [CODE] {total_blocks} blocks, {valid_blocks} valid ({success_rate:.1f}%)")

                if invalid and len(invalid) <= 3:  # Show up to 3 errors
                    for block_num, error in invalid[:3]:
                        safe_error = error[:50].encode('ascii', errors='replace').decode('ascii')
                        print(f"    [WARN] Block {block_num}: {safe_error}...")

        # Check math notation
        if any(keyword in filepath for keyword in ["models", "optimization", "technical", "theory"]):
            math_count = check_math_notation(filepath)
            if math_count > 0:
                print(f"  [MATH] {math_count} math notation instances")
            elif "optimization" in filepath or "models" in filepath:
                print(f"  [WARN] No math notation found (expected in technical docs)")

        # Check cross-references
        doc_refs, ref_refs = validate_cross_refs(filepath)
        if doc_refs > 0 or ref_refs > 0:
            print(f"  [REFS] {doc_refs} doc refs, {ref_refs} label refs")

    return total_lines, total_code_blocks, total_valid_code, 1 if all_valid else 0


def main():
    print("=" * 70)
    print("WEEK 3 & 4 DOCUMENTATION VALIDATION REPORT")
    print("=" * 70)
    print(f"\nValidation Date: {Path(__file__).stat().st_mtime}")
    print(f"Target: {TOTAL_TARGET_LINES}+ total lines")

    # Validate Week 3
    week3_lines, week3_code, week3_valid, week3_pass = validate_file_group(
        WEEK3_FILES, "WEEK 3: PLANT MODELS & OPTIMIZATION/SIMULATION"
    )

    # Validate Week 4
    week4_lines, week4_code, week4_valid, week4_pass = validate_file_group(
        WEEK4_FILES, "WEEK 4: ADVANCED CONTROLLERS"
    )

    # Validate index files
    print("\n" + "=" * 70)
    print("INDEX FILES VALIDATION")
    print("=" * 70)

    index_valid = True
    for index_file in INDEX_FILES:
        print(f"\n[INDEX] {Path(index_file).name}")
        if validate_file_exists(index_file):
            print(f"  [PASS] Index file exists")
            lines = count_lines(index_file)
            print(f"  [INFO] Lines: {lines}")

            # Check for Week 4 markers in controllers/index.md
            if index_file == "controllers/index.md":
                content = Path(index_file).read_text(encoding='utf-8')
                if "Week 4" in content:
                    print(f"  [PASS] Contains Week 4 roadmap markers")
                else:
                    print(f"  [WARN] Missing Week 4 roadmap markers")
                    index_valid = False
        else:
            print(f"  [FAIL] Index file missing!")
            index_valid = False

    # Summary
    total_lines = week3_lines + week4_lines
    total_code_blocks = week3_code + week4_code
    total_valid_code = week3_valid + week4_valid

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\nWeek 3 Lines: {week3_lines}")
    print(f"Week 4 Lines: {week4_lines}")
    print(f"Total Content Lines: {total_lines}")
    print(f"Target: {TOTAL_TARGET_LINES}+ lines")

    if total_lines >= TOTAL_TARGET_LINES:
        percentage = (total_lines / TOTAL_TARGET_LINES) * 100
        print(f"[PASS] STATUS: DELIVERED - {total_lines} lines ({percentage:.0f}% of target)")
    else:
        print(f"[WARN] STATUS: BELOW TARGET - {total_lines} lines (target: {TOTAL_TARGET_LINES}+)")

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

    all_passed = (
        total_lines >= TOTAL_TARGET_LINES and
        week3_pass and week4_pass and index_valid and
        (code_success_rate >= 90 if total_code_blocks > 0 else True)
    )

    if all_passed:
        print("[PASS] ALL VALIDATION CHECKS PASSED!")
        print("\n✅ Week 3 & 4 Documentation: PRODUCTION READY")
        return 0
    else:
        print("[WARN] SOME VALIDATION CHECKS FAILED - REVIEW ABOVE")
        print("\n⚠️ Week 3 & 4 Documentation: REVIEW REQUIRED")
        return 1


if __name__ == "__main__":
    exit(main())
