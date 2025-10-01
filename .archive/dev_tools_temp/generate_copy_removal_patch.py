#!/usr/bin/env python3
"""
Generate unified diff patch to remove unnecessary .copy() calls.
Only includes high-confidence (>=0.8) unnecessary copies.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import difflib

ROOT = Path(__file__).parent.parent

def generate_patch_for_file(file_path: Path, removals: List[Dict[str, Any]]) -> str:
    """Generate unified diff for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()

        modified_lines = original_lines.copy()

        # Sort removals by line number (descending) to avoid offset issues
        removals_sorted = sorted(removals, key=lambda x: x['line'], reverse=True)

        for removal in removals_sorted:
            line_num = removal['line'] - 1  # Convert to 0-indexed
            if line_num < len(modified_lines):
                original_line = modified_lines[line_num]
                # Remove .copy()
                modified_line = original_line.replace('.copy()', '')
                modified_lines[line_num] = modified_line

        # Generate unified diff
        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"a/{str(file_path.relative_to(ROOT)).replace(chr(92), '/')}",
            tofile=f"b/{str(file_path.relative_to(ROOT)).replace(chr(92), '/')}",
            lineterm='\n'
        )

        return ''.join(diff)

    except Exception as e:
        return f"# Error generating patch for {file_path}: {e}\n"

def main():
    """Generate bulk patch file."""
    # Load inventory
    with open(ROOT / 'copy_pattern_inventory.json', 'r') as f:
        data = json.load(f)

    # Filter high-confidence unnecessary copies
    unnecessary_copies = [
        item for item in data['by_category']['UNNECESSARY']
        if item['confidence'] >= 0.8
    ]

    print(f"Generating patch for {len(unnecessary_copies)} high-confidence unnecessary copies...")

    # Group by file
    files_to_patch = {}
    for item in unnecessary_copies:
        file_path = item['file'].replace('\\', '/')
        if file_path not in files_to_patch:
            files_to_patch[file_path] = []
        files_to_patch[file_path].append(item)

    # Generate patches
    all_patches = []
    for file_path_str, removals in sorted(files_to_patch.items()):
        file_path = ROOT / file_path_str
        patch = generate_patch_for_file(file_path, removals)
        if patch:
            all_patches.append(patch)

    # Write patch file
    patch_file = ROOT / 'remove_unnecessary_copies_bulk.patch'
    with open(patch_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_patches))

    print(f"\nPatch file generated: {patch_file}")
    print(f"Files affected: {len(files_to_patch)}")
    print(f"\nTo apply patch:")
    print(f"  git apply {patch_file.name}")
    print(f"\nTo review changes:")
    print(f"  git apply --stat {patch_file.name}")

if __name__ == "__main__":
    main()
