#!/usr/bin/env python3
"""
Check all subgroup output files for format issues
"""
import json
from pathlib import Path

subgroups_dir = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/subgroups')
output_files = sorted(subgroups_dir.glob('group_*_output.json'))

print(f"CHECKING SUBGROUP OUTPUT FORMATS")
print(f"=" * 80)
print()

for i, output_file in enumerate(output_files, 1):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"[{i:2d}] {output_file.name}: ERROR - Not a list!")
            continue

        first_claim = data[0] if data else {}
        claim_id = first_claim.get('claim_id', 'MISSING')

        # Check if properly formatted
        has_required = all(field in first_claim for field in ['claim_id', 'category', 'confidence', 'rationale', 'code_summary'])

        status = "[OK]" if has_required else "[BAD]"

        print(f"{status} [{i:2d}] {output_file.name}")
        print(f"         Claims: {len(data)}")
        print(f"         First claim_id: {claim_id}")
        print(f"         Fields: {list(first_claim.keys())[:8]}")

        if not has_required:
            print(f"         MISSING: {[f for f in ['claim_id', 'category', 'confidence', 'rationale', 'code_summary'] if f not in first_claim]}")

        print()

    except Exception as e:
        print(f"[ERROR] [{i:2d}] {output_file.name}: {e}")
        print()
