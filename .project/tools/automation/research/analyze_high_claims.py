#!/usr/bin/env python3
"""Analyze HIGH claims for batching strategy."""

import json
from collections import defaultdict
from pathlib import Path

inv_path = Path(".artifacts/claims_inventory.json")
with open(inv_path, 'r', encoding='utf-8') as f:
    inv = json.load(f)

high_claims = [c for c in inv['claims'] if c['priority'] == 'HIGH']

# Group by top-level src module
groups = defaultdict(list)
for claim in high_claims:
    path = claim.get('file_path', '')
    if not path:
        groups['unknown'].append(claim['id'])
        continue

    path = path.replace('\\', '/')
    parts = path.split('/')

    if len(parts) >= 2 and parts[0] == 'src':
        module = parts[1]
        groups[module].append(claim['id'])
    else:
        groups['other'].append(claim['id'])

print("HIGH Claims Distribution by Module:")
print("=" * 60)
for group, ids in sorted(groups.items(), key=lambda x: -len(x[1])):
    print(f"{group:20s}: {len(ids):4d} claims ({len(ids)/len(high_claims)*100:5.1f}%)")

print("=" * 60)
print(f"Total HIGH claims: {len(high_claims)}")
