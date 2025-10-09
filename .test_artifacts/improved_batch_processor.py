#!/usr/bin/env python3
"""
Improved Context-Aware Batch Processor for Documentation Cleanup.

Matches the detection patterns from detect_ai_patterns.py while preserving
technical accuracy through context-aware replacements.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
import json
from collections import defaultdict

# Context-aware replacement rules based on detect_ai_patterns.py
# Format: (pattern, replacement_function_or_string, flags, preserve_technical_context)

# Technical contexts to preserve (never replace)
TECHNICAL_CONTEXTS = [
    r'comprehensive\s+(test\s+)?coverage:\s+\d+',  # "comprehensive coverage: 95%"
    r'robust\s+control',  # Control theory term
    r'robust\s+stability',  # Control theory term
    r'robustness\s+margin',  # Control theory term
    r'advanced\s+MPC',  # Distinguishing from basic MPC
    r'enable\s+(flag|option|the|this|logging)',  # Technical enable usage
]


def is_technical_context(text: str, match_start: int, match_end: int) -> bool:
    """Check if match is in a technical context that should be preserved."""
    # Get surrounding context (100 chars before and after)
    context_start = max(0, match_start - 100)
    context_end = min(len(text), match_end + 100)
    context = text[context_start:context_end]

    for tech_pattern in TECHNICAL_CONTEXTS:
        if re.search(tech_pattern, context, re.IGNORECASE):
            return True
    return False


def smart_comprehensive_replace(match, full_text, match_start):
    """
    Smart replacement for 'comprehensive' - context-aware.

    Rules:
    - Keep if followed by metrics (e.g., "comprehensive coverage: 95%")
    - Keep if in formal academic context
    - Remove if used as filler adjective
    """
    matched_text = match.group(0)

    # Check context for metrics
    context_after = full_text[match_start:min(len(full_text), match_start + 100)]
    if re.search(r':\s*\d+', context_after):  # Followed by ": 95%" or similar
        return matched_text

    # Check for metric-backed usage
    if re.search(r'\d+%|\d+\.\d+', context_after[:50]):
        return matched_text

    # Otherwise, remove "comprehensive" adjective
    return ''


def create_replacement_rules():
    """Create comprehensive replacement rules matching detection patterns."""
    rules = []

    # ========== GREETING PATTERNS ==========
    greeting_patterns = [
        (r"\bLet's\s+", '', re.IGNORECASE),
        (r"\bLet\s+us\s+", '', re.IGNORECASE),
        (r"\bWe\s+will\s+", 'This document covers ', re.IGNORECASE),
        (r"\bWe'll\s+", '', re.IGNORECASE),
        (r"\bWelcome!\s*", '', 0),
        (r"\bYou'll\s+love\s+", '', re.IGNORECASE),
        (r"\bexciting\s+journey\b", 'process', re.IGNORECASE),
        (r"\bIn\s+this\s+section\s+we\s+will\s+", 'This section covers ', re.IGNORECASE),
        (r"\bNow\s+let's\s+", '', re.IGNORECASE),
        (r"\bYou\s+will\s+learn\s+", 'Learn ', re.IGNORECASE),
        (r"\bToday\s+we'll\s+", '', re.IGNORECASE),
    ]

    # ========== ENTHUSIASM PATTERNS ==========
    enthusiasm_patterns = [
        (r"\bpowerful\s+", '', re.IGNORECASE),
        (r"\bcomprehensive\s+", '', re.IGNORECASE),  # Simple remove unless technical
        (r"\bseamless\s+", '', re.IGNORECASE),
        (r"\bcutting-edge\s+", '', re.IGNORECASE),
        (r"\bstate-of-the-art\s+", '', re.IGNORECASE),
        (r"\bbest-in-class\s+", '', re.IGNORECASE),
        (r"\bindustry-leading\s+", '', re.IGNORECASE),
        (r"\brevolutionary\s+", 'novel ', re.IGNORECASE),
        (r"\badvanced\s+capabilities\b", 'specific capabilities', re.IGNORECASE),
        (r"\bsuperior\s+performance\b", 'improved performance', re.IGNORECASE),
        (r"\bamazing\s+", '', re.IGNORECASE),
        (r"\bincredible\s+", '', re.IGNORECASE),
        (r"\bexciting\s+", '', re.IGNORECASE),
        (r"\bexcellent\s+", '', re.IGNORECASE),
    ]

    # ========== HEDGE WORDS ==========
    hedge_patterns = [
        (r"\bleverage\s+the\s+", 'use the ', re.IGNORECASE),
        (r"\bleverage\s+", 'use ', re.IGNORECASE),
        (r"\butilize\s+the\s+", 'use the ', re.IGNORECASE),
        (r"\butilize\s+", 'use ', re.IGNORECASE),
        (r"\bdelve\s+into\s+", 'examine ', re.IGNORECASE),
        (r"\bfacilitate\s+", 'enable ', re.IGNORECASE),
        (r"\benable\s+", '', re.IGNORECASE),  # Will be checked for technical context
        (r"\bsolutions\s+", 'approaches ', re.IGNORECASE),
        (r"\bcapabilities\s+", 'features ', re.IGNORECASE),
        (r"\bemploy\s+", 'use ', re.IGNORECASE),
        (r"\bexploit\s+", 'use ', re.IGNORECASE),
    ]

    # ========== TRANSITIONS ==========
    transition_patterns = [
        (r"\bAs\s+we\s+can\s+see,?\s*", '', re.IGNORECASE),
        (r"\bIt'?s\s+worth\s+noting\s+that\s+", '', re.IGNORECASE),
        (r"\bIt\s+is\s+worth\s+noting\s+that\s+", '', re.IGNORECASE),
        (r"\bAdditionally,\s+it\s+should\s+be\s+mentioned\s+that\s+", 'Additionally, ', re.IGNORECASE),
        (r"\bFurthermore,\s+we\s+observe\s+that\s+", 'Furthermore, ', re.IGNORECASE),
        (r"\bInterestingly,\s+", '', re.IGNORECASE),
        (r"\bNotably,\s+", '', re.IGNORECASE),
        (r"\bImportantly,\s+", '', re.IGNORECASE),
    ]

    # ========== REPETITIVE PATTERNS ==========
    repetitive_patterns = [
        (r"\bIn\s+this\s+(section|chapter|guide)\s+", 'This \\1 covers ', re.IGNORECASE),
        (r"\bThis\s+(section|chapter|guide)\s+will\s+", 'This \\1 covers ', re.IGNORECASE),
        (r"\bLet's\s+(explore|examine|look\s+at)\s+", '', re.IGNORECASE),
        (r"\bWe\s+(will|can)\s+(see|observe|note)\s+", '', re.IGNORECASE),
    ]

    # Combine all patterns
    rules.extend(greeting_patterns)
    rules.extend(enthusiasm_patterns)
    rules.extend(hedge_patterns)
    rules.extend(transition_patterns)
    rules.extend(repetitive_patterns)

    # Cleanup patterns
    rules.append((r'\s{2,}', ' ', 0))  # Multiple spaces
    rules.append((r'\n{3,}', '\n\n', 0))  # Excessive newlines

    return rules


def clean_file(file_path: Path, dry_run: bool = False) -> Dict:
    """
    Clean a single file of AI-ish patterns.

    Args:
        file_path: Path to markdown file
        dry_run: If True, don't write changes

    Returns:
        Dictionary with cleaning statistics
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        total_replacements = 0
        replacements_by_pattern = defaultdict(int)

        rules = create_replacement_rules()

        for pattern, replacement, flags in rules:
            # Count matches before replacement
            matches = list(re.finditer(pattern, content, flags))

            # Filter out technical contexts
            valid_matches = []
            for match in matches:
                if not is_technical_context(content, match.start(), match.end()):
                    valid_matches.append(match)

            if valid_matches:
                # Apply replacement (from end to start to preserve positions)
                for match in reversed(valid_matches):
                    # Handle backreferences in replacement
                    if callable(replacement):
                        new_text = replacement(match, content, match.start())
                    elif '\\' in str(replacement):
                        new_text = match.expand(replacement)
                    else:
                        new_text = replacement

                    content = content[:match.start()] + new_text + content[match.end():]
                    total_replacements += 1
                    replacements_by_pattern[pattern[:40]] += 1

        # Write back if changed and not dry run
        if content != original_content and not dry_run:
            file_path.write_text(content, encoding='utf-8')
            status = 'cleaned'
        elif content != original_content:
            status = 'dry_run_changes_detected'
        else:
            status = 'no_changes'

        return {
            'file': str(file_path.relative_to(Path.cwd())),
            'status': status,
            'total_replacements': total_replacements,
            'replacements_by_pattern': dict(replacements_by_pattern),
            'size_before': len(original_content),
            'size_after': len(content),
            'size_reduction': len(original_content) - len(content)
        }

    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'error': str(e),
            'total_replacements': 0,
            'size_reduction': 0
        }


def batch_clean(file_paths: List[Path], dry_run: bool = False) -> List[Dict]:
    """
    Batch clean multiple files.

    Args:
        file_paths: List of file paths to clean
        dry_run: If True, don't write changes

    Returns:
        List of cleaning results
    """
    results = []
    for i, file_path in enumerate(file_paths, 1):
        if not file_path.exists():
            results.append({
                'file': str(file_path),
                'status': 'not_found',
                'total_replacements': 0,
                'size_reduction': 0
            })
            print(f"[{i}/{len(file_paths)}] SKIP: {file_path.name} (not found)")
            continue

        result = clean_file(file_path, dry_run=dry_run)
        results.append(result)

        status_icon = "[OK]" if result['status'] == 'cleaned' else "[  ]"
        print(f"[{i}/{len(file_paths)}] {status_icon} {file_path.name}: "
              f"{result['total_replacements']} replacements "
              f"({result['size_reduction']} chars removed)")

    return results


def print_summary(results: List[Dict]):
    """Print summary statistics."""
    total_files = len(results)
    cleaned_files = len([r for r in results if r['status'] == 'cleaned'])
    total_replacements = sum(r.get('total_replacements', 0) for r in results)
    total_size_reduction = sum(r.get('size_reduction', 0) for r in results)

    print("\n" + "="*80)
    print("CLEANING SUMMARY")
    print("="*80)
    print(f"Total files processed: {total_files}")
    print(f"Files cleaned: {cleaned_files}")
    print(f"Files unchanged: {total_files - cleaned_files}")
    print(f"Total replacements: {total_replacements}")
    print(f"Total size reduction: {total_size_reduction:,} characters")
    print("="*80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Improved batch processor for documentation cleanup"
    )
    parser.add_argument(
        "--files",
        type=str,
        nargs="+",
        help="List of files to clean"
    )
    parser.add_argument(
        "--file-list",
        type=Path,
        help="JSON file containing list of files to clean"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files"
    )

    args = parser.parse_args()

    # Get file list
    if args.file_list:
        file_list_data = json.loads(args.file_list.read_text(encoding='utf-8'))
        file_paths = [Path(f) for f in file_list_data]
    elif args.files:
        file_paths = [Path(f) for f in args.files]
    else:
        print("Error: Must provide either --files or --file-list")
        exit(1)

    print(f"Processing {len(file_paths)} files...")
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    print("="*80)

    results = batch_clean(file_paths, dry_run=args.dry_run)
    print_summary(results)

    # Save results
    output_path = Path(".artifacts/docs_audit/improved_batch_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nDetailed results saved to: {output_path}")
