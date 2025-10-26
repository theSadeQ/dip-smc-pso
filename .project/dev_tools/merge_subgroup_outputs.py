#!/usr/bin/env python3
"""
Merge all 10 subgroup outputs into single chatgpt_output_91_citations.json
"""
import json
from pathlib import Path

# Load all subgroup outputs
subgroups_dir = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/subgroups')
output_files = sorted(subgroups_dir.glob('group_*_output.json'))

if not output_files:
    print("ERROR: No output files found!")
    print(f"Expected files in: {subgroups_dir}")
    print()
    print("Please process all 10 subgroups with ChatGPT first:")
    print("  - Save each ChatGPT response as: subgroups/group_XX_*_output.json")
    exit(1)

print(f"MERGING SUBGROUP OUTPUTS")
print(f"=" * 80)
print()

all_claims = []
total_by_category = {'A': 0, 'B': 0, 'C': 0}

for i, output_file in enumerate(output_files, 1):
    print(f"[{i:2d}/10] Loading: {output_file.name}")

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            subgroup_claims = json.load(f)

        if not isinstance(subgroup_claims, list):
            print(f"  ERROR: Expected JSON array, got {type(subgroup_claims)}")
            continue

        # Count categories
        for claim in subgroup_claims:
            cat = claim.get('category', 'unknown')
            if cat in total_by_category:
                total_by_category[cat] += 1

        all_claims.extend(subgroup_claims)
        print(f"  Loaded {len(subgroup_claims)} claims")

    except Exception as e:
        print(f"  ERROR: {e}")

print()
print(f"=" * 80)
print(f"MERGE SUMMARY")
print(f"=" * 80)
print(f"Total claims merged: {len(all_claims)}")
print(f"  Category A (papers): {total_by_category['A']}")
print(f"  Category B (textbooks): {total_by_category['B']}")
print(f"  Category C (no citation): {total_by_category['C']}")
print()

if len(all_claims) != 91:
    print(f"WARNING: Expected 91 claims, got {len(all_claims)}")
    print()

# Save merged output
output_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_91_citations.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_claims, f, indent=2)

print(f"Saved merged output: {output_path}")
print()
print(f"Next step:")
print(f"  python .dev_tools/apply_chatgpt_citations.py")
