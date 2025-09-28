#=======================================================================================\\\
#================================= fix_ascii_headers.py =================================\\\
#=======================================================================================\\\

#!/usr/bin/env python3
"""
ASCII Header Standardization Script for DIP SMC PSO Project

This script ensures all Python files have properly formatted 90-character ASCII headers
following the specification: exactly 90 characters wide with centered file paths.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def create_ascii_header(file_path: str, base_path: str = "") -> List[str]:
    """Create properly formatted 90-character ASCII header.

    Args:
        file_path: Absolute or relative path to the file
        base_path: Base path to remove from file_path for header display

    Returns:
        List of three header lines
    """
    # Convert to Path object for consistent handling
    path_obj = Path(file_path)

    # Get relative path from base_path if provided
    if base_path:
        try:
            rel_path = path_obj.relative_to(Path(base_path))
        except ValueError:
            rel_path = path_obj
    else:
        rel_path = path_obj

    # Use forward slashes consistently
    display_path = str(rel_path).replace('\\', '/')

    # Total width is 90 characters, ending with \\\
    total_width = 90
    end_marker = "\\\\\\"
    available_width = total_width - len(end_marker)

    # Create the centered path line
    if len(display_path) > available_width - 4:  # Leave space for padding
        # Truncate if too long
        display_path = "..." + display_path[-(available_width - 7):]

    padding_total = available_width - len(display_path)
    padding_left = padding_total // 2
    padding_right = padding_total - padding_left

    header_lines = [
        "#" + "=" * (available_width) + end_marker,
        "#" + "=" * padding_left + " " + display_path + " " + "=" * (padding_right - 1) + end_marker,
        "#" + "=" * (available_width) + end_marker
    ]

    return header_lines


def fix_ascii_header(file_path: str, base_path: str = "") -> bool:
    """Fix ASCII header in a Python file.

    Args:
        file_path: Path to the Python file
        base_path: Base path for relative path calculation

    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            return False

        # Check if file already has ASCII header
        has_header = (len(lines) >= 3 and
                     lines[0].startswith('#=') and
                     lines[2].startswith('#='))

        # Create new header
        new_header = create_ascii_header(file_path, base_path)
        new_header_lines = [line + '\n' for line in new_header]

        if has_header:
            # Replace existing header
            content_start = 3
            # Skip empty line after header if present
            if len(lines) > 3 and lines[3].strip() == '':
                content_start = 3
            else:
                new_header_lines.append('\n')  # Add empty line after header
                content_start = 3

            new_lines = new_header_lines + lines[content_start:]
        else:
            # Add header at the beginning
            new_header_lines.append('\n')  # Add empty line after header
            new_lines = new_header_lines + lines

        # Write back only if changed
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to fix ASCII headers across the project."""
    project_root = Path(__file__).parent

    # Process src/ directory
    src_path = project_root / "src"
    if src_path.exists():
        print("Fixing ASCII headers in src/ directory...")
        for py_file in src_path.rglob("*.py"):
            if py_file.name != "__init__.py" or py_file.stat().st_size > 10:  # Skip empty __init__.py
                fix_ascii_header(str(py_file), str(project_root))
                print(f"  Fixed: {py_file.relative_to(project_root)}")

    # Process tests/ directory
    tests_path = project_root / "tests"
    if tests_path.exists():
        print("\nFixing ASCII headers in tests/ directory...")
        for py_file in tests_path.rglob("*.py"):
            if py_file.name != "__init__.py" or py_file.stat().st_size > 10:  # Skip empty __init__.py
                fix_ascii_header(str(py_file), str(project_root))
                print(f"  Fixed: {py_file.relative_to(project_root)}")

    # Process root-level Python files
    print("\nFixing ASCII headers in root-level Python files...")
    for py_file in project_root.glob("*.py"):
        if py_file.name != "__init__.py":
            fix_ascii_header(str(py_file), str(project_root))
            print(f"  Fixed: {py_file.name}")

    print("\nASCII header standardization complete!")


if __name__ == "__main__":
    main()