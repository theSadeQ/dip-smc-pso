#!/usr/bin/env python3
"""Merge remaining small modules into batch 8."""

import json
from pathlib import Path
from collections import defaultdict

# Load claims inventory
with open('.artifacts/claims_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

# Filter for remaining modules
remaining_modules = ['integration', 'config', 'core', 'fault_detection']
remaining_claims = []

for claim in inventory['claims']:
    if claim.get('priority') != 'HIGH':
        continue

    file_path = claim.get('file_path', '').replace('\\', '/')
    parts = file_path.split('/')

    if len(parts) >= 2 and parts[0] == 'src':
        module = parts[1]
        if module in remaining_modules:
            remaining_claims.append(claim)

print(f"Found {len(remaining_claims)} claims in remaining modules")

# Load existing batch 8 (benchmarks)
with open('.artifacts/batch_08_other_high.json', 'r', encoding='utf-8') as f:
    batch8 = json.load(f)

# Add remaining claims
batch8['claims'].extend(remaining_claims)
batch8['metadata']['total_claims'] = len(batch8['claims'])

# Update research queue
for claim in remaining_claims:
    priority = claim.get('priority', 'UNKNOWN')
    if priority not in batch8['research_queue']:
        batch8['research_queue'][priority] = []
    batch8['research_queue'][priority].append(claim['id'])

# Update metadata by_priority
by_priority = defaultdict(int)
for claim in batch8['claims']:
    priority = claim.get('priority', 'UNKNOWN')
    by_priority[priority] += 1
batch8['metadata']['by_priority'] = dict(by_priority)

# Save updated batch 8
with open('.artifacts/batch_08_other_high.json', 'w', encoding='utf-8') as f:
    json.dump(batch8, f, indent=2, ensure_ascii=False)

print(f"Updated batch 8: {len(batch8['claims'])} total claims")
print(f"Modules: benchmarks, integration, config, core, fault_detection")
