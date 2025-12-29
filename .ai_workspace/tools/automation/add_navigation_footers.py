"""
Add standardized navigation footers to all category index.md files.

Adds bidirectional navigation from category indexes back to NAVIGATION.md.
Fixes UX gap where users get "trapped" in category indexes.

Usage:
    python .ai_workspace/dev_tools/add_navigation_footers.py --dry-run
    python .ai_workspace/dev_tools/add_navigation_footers.py --apply

Features:
- Automatically calculates relative paths based on file depth
- Detects existing footers to avoid duplication
- Handles both index.md and INDEX.md (case-insensitive)
- Dry-run mode shows preview before making changes
- Detailed reporting of modifications

Author: Claude Code
Date: November 2025
"""

import re
import argparse
from pathlib import Path
from typing import List, Tuple

# Configuration
DOCS_ROOT = Path("D:/Projects/main/docs")
FOOTER_SEPARATOR = "\n---\n\n"
NAVIGATION_KEYWORD = "Master Navigation Hub"

def find_all_index_files() -> List[Path]:
    """
    Find all index.md files in docs/ directory.

    Returns:
        List of Path objects for all index files (case-insensitive)
    """
    # Find both index.md and INDEX.md
    index_files = list(DOCS_ROOT.rglob("index.md"))
    index_files_upper = list(DOCS_ROOT.rglob("INDEX.md"))

    # Combine and remove duplicates
    all_files = list(set(index_files + index_files_upper))

    # Exclude NAVIGATION.md itself
    all_files = [f for f in all_files if f.name != "NAVIGATION.md"]

    return sorted(all_files)

def has_navigation_footer(content: str) -> bool:
    """
    Check if file already has navigation footer.

    Args:
        content: File content as string

    Returns:
        True if footer exists, False otherwise
    """
    return NAVIGATION_KEYWORD in content

def calculate_relative_path(file_path: Path, target_file: str) -> str:
    """
    Calculate relative path from index file to target file.

    Args:
        file_path: Path to the index file
        target_file: Target filename (e.g., "NAVIGATION.md" or "index.md")

    Returns:
        Relative path string (e.g., "../NAVIGATION.md", "../../index.md")
    """
    # Calculate depth: how many directories deep from docs/
    relative_to_docs = file_path.relative_to(DOCS_ROOT)
    depth = len(relative_to_docs.parts) - 1  # -1 for the file itself

    # Special case: root index.md (docs/index.md)
    if depth == 0:
        return target_file

    # Build relative path with correct number of ../
    return "../" * depth + target_file

def create_footer(file_path: Path) -> str:
    """
    Create standardized navigation footer with correct relative paths.

    Args:
        file_path: Path to the index file

    Returns:
        Footer string with proper relative paths
    """
    nav_path = calculate_relative_path(file_path, "NAVIGATION.md")
    index_path = calculate_relative_path(file_path, "index.md")

    footer = (
        f"{FOOTER_SEPARATOR}"
        f"**Navigation**: Return to [Master Navigation Hub]({nav_path}) | "
        f"Browse all [Documentation Categories]({index_path})\n"
    )

    return footer

def add_footer_to_file(file_path: Path, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Add navigation footer to index file if missing.

    Args:
        file_path: Path to the index file
        dry_run: If True, don't modify file (preview only)

    Returns:
        Tuple of (was_modified, status_message)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Error reading file: {e}"

    # Check if footer already exists
    if has_navigation_footer(content):
        return False, "Footer already exists"

    # Create footer with correct relative paths
    footer = create_footer(file_path)

    # Append footer to content
    new_content = content.rstrip() + footer

    # Write to file (unless dry-run)
    if not dry_run:
        try:
            file_path.write_text(new_content, encoding="utf-8")
            return True, "Footer added successfully"
        except Exception as e:
            return False, f"Error writing file: {e}"

    return True, "Would add footer (dry-run mode)"

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Add standardized navigation footers to all category index.md files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes without modifying files
  python add_navigation_footers.py --dry-run

  # Apply changes to all files
  python add_navigation_footers.py --apply

  # Default is dry-run mode
  python add_navigation_footers.py
        """
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview changes without modifying files (default if --apply not specified)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to files (required for actual modification)"
    )

    args = parser.parse_args()

    # Default to dry-run if --apply not specified
    dry_run = not args.apply

    # Print mode
    mode_str = "[DRY-RUN MODE]" if dry_run else "[APPLY MODE]"
    print(f"\n{mode_str} Starting navigation footer insertion...\n")

    # Find all index files
    index_files = find_all_index_files()
    print(f"[INFO] Found {len(index_files)} index files in docs/\n")

    # Process each file
    modified_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in index_files:
        # Calculate relative path for display
        rel_path = file_path.relative_to(DOCS_ROOT)

        # Add footer
        was_modified, status_msg = add_footer_to_file(file_path, dry_run=dry_run)

        # Update counters
        if "Error" in status_msg:
            error_count += 1
            prefix = "[ERROR]"
        elif was_modified:
            modified_count += 1
            prefix = "[DRY-RUN]" if dry_run else "[MODIFIED]"
        else:
            skipped_count += 1
            prefix = "[SKIPPED]"

        # Print status
        print(f"{prefix} {rel_path}: {status_msg}")

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files found: {len(index_files)}")
    print(f"Modified: {modified_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print("="*60 + "\n")

    if dry_run and modified_count > 0:
        print("[INFO] This was a dry-run. No files were modified.")
        print("[INFO] Run with --apply to make actual changes:\n")
        print("       python .ai_workspace/dev_tools/add_navigation_footers.py --apply\n")
    elif not dry_run and modified_count > 0:
        print(f"[SUCCESS] Successfully added footers to {modified_count} files!")
        print("[INFO] Next steps:")
        print("       1. Verify changes: git diff docs/")
        print("       2. Test Sphinx build: sphinx-build -M html docs docs/_build -W")
        print("       3. Commit changes: git add . && git commit\n")
    elif modified_count == 0:
        print("[INFO] All files already have navigation footers. No changes needed.\n")

    # Exit code
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    exit(main())
