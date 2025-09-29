#======================================================================================\\\
#============================== analyze_ascii_headers.py ==============================\\\
#======================================================================================\\\

#!/usr/bin/env python3
"""Analyze ASCII header compliance across the codebase."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

def analyze_ascii_headers() -> Dict[str, List[str]]:
    """Analyze ASCII header compliance across Python files."""

    results = {
        "compliant": [],
        "missing_headers": [],
        "incorrect_format": [],
        "wrong_width": []
    }

    # Expected ASCII header pattern
    expected_pattern = re.compile(r'^#={85,95}\\{3}$')

    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    if len(lines) < 3:
                        results["missing_headers"].append(relative_path)
                        continue

                    # Check first three lines for ASCII header
                    first_line = lines[0].strip()
                    second_line = lines[1].strip() if len(lines) > 1 else ""
                    third_line = lines[2].strip() if len(lines) > 2 else ""

                    # Check if it has the expected ASCII header format
                    if (first_line.startswith('#=') and first_line.endswith('\\\\\\') and
                        second_line.startswith('#=') and second_line.endswith('\\\\\\') and
                        third_line.startswith('#=') and third_line.endswith('\\\\\\')):

                        # Check width compliance (should be 90 characters)
                        if len(first_line) == 90 and len(third_line) == 90:
                            results["compliant"].append(relative_path)
                        else:
                            results["wrong_width"].append(relative_path)
                    elif first_line.startswith('#='):
                        results["incorrect_format"].append(relative_path)
                    else:
                        results["missing_headers"].append(relative_path)

                except (UnicodeDecodeError, IOError) as e:
                    print(f"Error reading {relative_path}: {e}")
                    results["missing_headers"].append(relative_path)

    return results

def generate_ascii_header(file_path: str) -> List[str]:
    """Generate proper ASCII header for a file."""
    # Convert to forward slashes for consistency
    normalized_path = file_path.replace('\\', '/')

    # Remove leading './' if present
    if normalized_path.startswith('./'):
        normalized_path = normalized_path[2:]

    # Calculate padding for centering
    total_width = 90
    equals_per_side = (total_width - len(normalized_path) - 6) // 2  # 6 = '# ' + ' #'

    # Ensure we have at least some padding
    if equals_per_side < 5:
        equals_per_side = 5

    # Build the header lines
    top_line = '#' + '=' * (total_width - 4) + '\\\\\\'
    middle_line = '#' + '=' * equals_per_side + ' ' + normalized_path + ' ' + '=' * (total_width - len(normalized_path) - equals_per_side - 6) + '\\\\\\'
    bottom_line = '#' + '=' * (total_width - 4) + '\\\\\\'

    # Ensure exact 90-character width
    top_line = top_line[:90]
    middle_line = middle_line[:90]
    bottom_line = bottom_line[:90]

    return [top_line, middle_line, bottom_line]

if __name__ == "__main__":
    results = analyze_ascii_headers()

    print("ASCII Header Compliance Analysis")
    print("=" * 50)
    print(f"Compliant files: {len(results['compliant'])}")
    print(f"Missing headers: {len(results['missing_headers'])}")
    print(f"Incorrect format: {len(results['incorrect_format'])}")
    print(f"Wrong width: {len(results['wrong_width'])}")
    print()

    if results['missing_headers']:
        print("Files missing ASCII headers:")
        for file_path in sorted(results['missing_headers'])[:20]:  # Show first 20
            print(f"  {file_path}")
        if len(results['missing_headers']) > 20:
            print(f"  ... and {len(results['missing_headers']) - 20} more")
        print()

    if results['incorrect_format']:
        print("Files with incorrect format:")
        for file_path in sorted(results['incorrect_format'])[:10]:
            print(f"  {file_path}")
        print()

    if results['wrong_width']:
        print("Files with wrong width:")
        for file_path in sorted(results['wrong_width'])[:10]:
            print(f"  {file_path}")
        print()

    # Generate sample headers for missing files
    print("\nSample headers for missing files:")
    for file_path in sorted(results['missing_headers'])[:5]:
        print(f"\nFor {file_path}:")
        header_lines = generate_ascii_header(file_path)
        for line in header_lines:
            print(line)