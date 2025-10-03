#!/usr/bin/env python3
"""
Rename ChatGPT output files from " - Copy.md" to "_output.json"
"""
import os
from pathlib import Path

subgroups_dir = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/subgroups')

# Find all files with " - Copy" in name
copy_files = list(subgroups_dir.glob('*Copy*'))

print(f"RENAMING OUTPUT FILES")
print(f"=" * 80)
print(f"Found {len(copy_files)} files to rename")
print()

for old_file in copy_files:
    # Extract group key from filename
    # Example: "group_01_smc_adaptive_hybrid_prompt - Copy.md"
    # Target:  "group_01_smc_adaptive_hybrid_output.json"

    old_name = old_file.name

    # Remove " - Copy.md" and replace with "_output.json"
    new_name = old_name.replace('_prompt - Copy.md', '_output.json')

    new_file = old_file.parent / new_name

    # Rename
    old_file.rename(new_file)

    print(f"[OK] Renamed:")
    print(f"     From: {old_name}")
    print(f"     To:   {new_name}")
    print()

print(f"All files renamed successfully!")
