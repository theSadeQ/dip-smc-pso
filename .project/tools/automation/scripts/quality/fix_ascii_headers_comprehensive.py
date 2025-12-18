#======================================================================================\\\
#========================= fix_ascii_headers_comprehensive.py =========================\\\
#======================================================================================\\\

#!/usr/bin/env python3
"""Comprehensive ASCII header fixer for DIP SMC PSO project."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

def generate_ascii_header(file_path: str) -> List[str]:
    """Generate proper ASCII header for a file with exact 90-character width."""
    # Convert to forward slashes and normalize path
    normalized_path = file_path.replace('\\', '/').replace('DIP_SMC_PSO/', '')

    # Remove leading './' if present
    if normalized_path.startswith('./'):
        normalized_path = normalized_path[2:]

    # Calculate the exact padding needed for 90-character width
    total_width = 90
    header_content = f" {normalized_path} "

    # Calculate padding: total width - 4 (for #===\\\) - content length
    padding_needed = total_width - 4 - len(header_content)
    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding

    # Build the header lines with exact 90 characters
    top_line = '#' + '=' * 86 + '\\\\\\'
    middle_line = '#' + '=' * left_padding + header_content + '=' * right_padding + '\\\\\\'
    bottom_line = '#' + '=' * 86 + '\\\\\\'

    # Ensure exactly 90 characters
    top_line = top_line[:90]
    middle_line = middle_line[:90]
    bottom_line = bottom_line[:90]

    return [top_line, middle_line, bottom_line]

def fix_ascii_header(file_path: str) -> bool:
    """Fix ASCII header for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Generate correct header
        header_lines = generate_ascii_header(file_path)

        # Check if file already has some form of ASCII header
        has_existing_header = False
        start_index = 0

        if len(lines) >= 3:
            for i in range(min(5, len(lines))):  # Check first 5 lines
                if lines[i].strip().startswith('#=') and lines[i].strip().endswith('\\\\\\'):
                    has_existing_header = True
                    # Find the end of the existing header
                    for j in range(i, min(i+5, len(lines))):
                        if not (lines[j].strip().startswith('#=') and lines[j].strip().endswith('\\\\\\')):
                            start_index = j
                            break
                    else:
                        start_index = min(i+3, len(lines))
                    break

        # Build new content
        new_lines = []

        # Add correct header
        new_lines.extend([line + '\n' for line in header_lines])
        new_lines.append('\n')  # Empty line after header

        # Add remaining content (skip existing header if any)
        if has_existing_header:
            # Skip existing malformed header
            remaining_lines = lines[start_index:]
            # Skip any empty lines immediately after the old header
            while remaining_lines and remaining_lines[0].strip() == '':
                remaining_lines = remaining_lines[1:]
            new_lines.extend(remaining_lines)
        else:
            # No existing header, keep all content
            new_lines.extend(lines)

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def fix_all_headers() -> Dict[str, int]:
    """Fix ASCII headers for all Python files in the project."""
    stats = {
        "fixed": 0,
        "skipped": 0,
        "errors": 0
    }

    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                # Skip certain files that shouldn't have headers
                if file in ['__init__.py'] and os.path.getsize(file_path) < 50:
                    stats["skipped"] += 1
                    continue

                # Skip files in certain directories
                relative_path = os.path.relpath(file_path, '.')
                if any(skip_dir in relative_path for skip_dir in ['.git', '__pycache__', '.pytest_cache']):
                    stats["skipped"] += 1
                    continue

                print(f"Fixing header in: {relative_path}")
                if fix_ascii_header(file_path):
                    stats["fixed"] += 1
                else:
                    stats["errors"] += 1

    return stats

def verify_headers() -> Dict[str, List[str]]:
    """Verify that all headers are now correct."""
    results = {
        "correct": [],
        "still_incorrect": []
    }

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    if len(lines) >= 3:
                        first_line = lines[0].strip()
                        second_line = lines[1].strip()
                        third_line = lines[2].strip()

                        if (len(first_line) == 90 and first_line.startswith('#=') and first_line.endswith('\\\\\\') and
                            len(second_line) == 90 and second_line.startswith('#=') and second_line.endswith('\\\\\\') and
                            len(third_line) == 90 and third_line.startswith('#=') and third_line.endswith('\\\\\\')):
                            results["correct"].append(relative_path)
                        else:
                            results["still_incorrect"].append(relative_path)
                    else:
                        results["still_incorrect"].append(relative_path)

                except Exception as e:
                    results["still_incorrect"].append(relative_path)

    return results

if __name__ == "__main__":
    print("Starting comprehensive ASCII header fix...")
    print("=" * 60)

    # Fix all headers
    stats = fix_all_headers()

    print(f"\nProcessing complete:")
    print(f"  Files fixed: {stats['fixed']}")
    print(f"  Files skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")

    # Verify results
    print("\nVerifying headers...")
    verification = verify_headers()

    print(f"\nVerification results:")
    print(f"  Correct headers: {len(verification['correct'])}")
    print(f"  Still incorrect: {len(verification['still_incorrect'])}")

    if verification['still_incorrect']:
        print("\nFiles still needing attention:")
        for file_path in verification['still_incorrect'][:10]:
            print(f"  {file_path}")
        if len(verification['still_incorrect']) > 10:
            print(f"  ... and {len(verification['still_incorrect']) - 10} more")

    print(f"\nASCII header compliance: {len(verification['correct'])}/{len(verification['correct']) + len(verification['still_incorrect'])} files")