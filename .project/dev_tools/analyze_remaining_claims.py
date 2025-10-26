#!/usr/bin/env python3
"""
Analyze remaining Batch 08 claims to determine next steps
"""
import json
import csv
from pathlib import Path
from collections import Counter

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

# Find remaining claims
remaining = []
for cid in batch08_ids:
    if cid in csv_rows and csv_rows[cid]['Research_Status'] != 'completed':
        remaining.append(csv_rows[cid])

print(f"REMAINING CLAIMS ANALYSIS")
print(f"=" * 80)
print(f"Total remaining: {len(remaining)}")
print()

# Analyze by status
statuses = Counter(r['Research_Status'] for r in remaining)
print(f"Status Breakdown:")
for status, count in statuses.most_common():
    print(f"  {status}: {count}")
print()

# Analyze by category
categories = Counter(r.get('Category', 'unknown') for r in remaining)
print(f"Category Breakdown:")
for cat, count in categories.most_common():
    print(f"  {cat}: {count}")
print()

# Sample claims
print(f"Sample Remaining Claims (first 20):")
print("-" * 80)
for i, r in enumerate(remaining[:20], 1):
    claim_text = r.get('Claim_Text', '')[:100]
    print(f"{i}. {r['Claim_ID']} [{r['Research_Status']}]")
    print(f"   {claim_text}...")
    if r.get('Research_Notes'):
        print(f"   Notes: {r['Research_Notes'][:80]}")
    print()

# Check if they have code context
with_code = sum(1 for r in remaining if r.get('Code_Context', '').strip())
print(f"Claims with code context: {with_code}/{len(remaining)}")
print()

# Check if they need citations (Category A or B)
needs_citation = [r for r in remaining if r.get('Category') in ['A', 'B']]
print(f"Claims needing citations (Category A/B): {len(needs_citation)}")

if needs_citation:
    print("\nSample claims needing citations:")
    for r in needs_citation[:10]:
        print(f"  {r['Claim_ID']}: {r.get('Claim_Text', '')[:80]}")
