#!/usr/bin/env python3
"""
Analyze quality of remaining claims to determine processing strategy
"""
import json
import csv
from pathlib import Path
from collections import Counter

# Load Batch 08 claims
batch08_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json')
with open(batch08_path, 'r', encoding='utf-8') as f:
    batch08 = json.load(f)['claims']

# Load CSV
csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')
csv_rows = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_rows[row['Claim_ID']] = row

# Find remaining claims
batch08_ids = set(c['id'] for c in batch08)
remaining = [c for c in batch08 if c['id'] in csv_rows and csv_rows[c['id']]['Research_Status'] != 'completed']

print(f"REMAINING CLAIMS QUALITY ANALYSIS")
print(f"=" * 80)
print(f"Total remaining: {len(remaining)}\n")

# Analyze description patterns
description_patterns = Counter()
for c in remaining:
    desc = c.get('description', '')
    if '(attributed to: None)' in desc:
        description_patterns['attributed to: None'] += 1
    elif not desc or desc.strip() == '':
        description_patterns['empty'] += 1
    elif len(desc.split()) < 3:
        description_patterns['very short (< 3 words)'] += 1
    else:
        description_patterns['normal description'] += 1

print("Description Quality:")
for pattern, count in description_patterns.most_common():
    print(f"  {pattern}: {count} ({100*count/len(remaining):.1f}%)")
print()

# Sample claims by pattern
print("Sample descriptions (first 30):")
print("-" * 80)
for i, c in enumerate(remaining[:30], 1):
    desc = c.get('description', '').encode('ascii', 'replace').decode('ascii')
    file_path = c.get('file_path', '').encode('ascii', 'replace').decode('ascii')
    context = c.get('context', '').encode('ascii', 'replace').decode('ascii')[:80]
    print(f"{i}. {c['id']}: \"{desc}\"")
    print(f"   File: {file_path}")
    print(f"   Context: {context}...")
    print()

# Analyze file paths to find patterns
file_dirs = Counter()
for c in remaining:
    file_path = c.get('file_path', '')
    if file_path:
        # Extract top-level directory
        parts = file_path.replace('\\', '/').split('/')
        if len(parts) >= 2:
            file_dirs[f"{parts[0]}/{parts[1]}"] += 1

print("\nFile Distribution (top directories):")
for dir_path, count in file_dirs.most_common(10):
    print(f"  {dir_path}: {count}")
print()

# Check context quality
with_context = sum(1 for c in remaining if c.get('context', '').strip())
print(f"Claims with context: {with_context}/{len(remaining)} ({100*with_context/len(remaining):.1f}%)")

# Save remaining IDs for processing
remaining_ids = [c['id'] for c in remaining]
output_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/remaining_91_claims.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(remaining_ids),
        'claim_ids': remaining_ids,
        'full_claims': remaining
    }, f, indent=2)

print(f"\nSaved remaining claims to: {output_path}")
