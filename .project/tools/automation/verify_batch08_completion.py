#!/usr/bin/env python3
"""
Verify Batch 08 completion status
"""
import json
import csv
from pathlib import Path

# Load Batch 08 claim IDs
batch08_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json')
with open(batch08_path, 'r', encoding='utf-8') as f:
    batch08_data = json.load(f)
    batch08_ids = set(c['id'] for c in batch08_data['claims'])

# Load CSV
csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')
csv_rows = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_rows[row['Claim_ID']] = row

# Count completed
completed = sum(1 for cid in batch08_ids if cid in csv_rows and csv_rows[cid]['Research_Status'] == 'completed')

print(f"=" * 80)
print(f"BATCH 08 FINAL STATUS")
print(f"=" * 80)
print()
print(f"Total Batch 08 claims: {len(batch08_ids)}")
print(f"Completed: {completed}")
print(f"Remaining: {len(batch08_ids) - completed}")
print(f"Completion: {100*completed/len(batch08_ids):.1f}%")
print()

if completed == len(batch08_ids):
    print(f"[SUCCESS] 100% COMPLETION ACHIEVED!")
    print()
    print(f"All 314 Batch 08 claims have been cited and marked complete.")
else:
    print(f"[PENDING] {len(batch08_ids) - completed} claims still need citations")
    print()
    print(f"Remaining claim IDs:")
    remaining_ids = sorted([cid for cid in batch08_ids if cid not in csv_rows or csv_rows[cid]['Research_Status'] != 'completed'])
    for cid in remaining_ids[:20]:
        print(f"  - {cid}")
    if len(remaining_ids) > 20:
        print(f"  ... and {len(remaining_ids) - 20} more")

print()
print(f"=" * 80)
