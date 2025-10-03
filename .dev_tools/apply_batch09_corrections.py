#!/usr/bin/env python3
"""
Apply Batch 09 corrected citations to claims_research_tracker.csv
"""
import json
import csv
from pathlib import Path
from datetime import datetime

# Paths
batch09_json_path = Path('D:/Projects/main/artifacts/research_batches/09_HIGH_fault_detection/batch_09_corrected_citations.json')
csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')
backup_path = Path(f'D:/Projects/main/artifacts/claims_research_tracker_BACKUP_BATCH09_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

# Load corrected JSON
with open(batch09_json_path, 'r', encoding='utf-8') as f:
    corrected_claims = json.load(f)

# Create claim lookup
claim_lookup = {claim['claim_id']: claim for claim in corrected_claims}

# Load CSV
csv_rows = []
with open(csv_path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        csv_rows.append(row)

# Create backup
with open(backup_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"[OK] Created backup: {backup_path}")

# Apply corrections
updated_count = 0
citation_applied = 0

for row in csv_rows:
    claim_id = row['Claim_ID']

    if claim_id in claim_lookup:
        corrected = claim_lookup[claim_id]

        # Update research status
        row['Research_Status'] = 'completed'

        if corrected.get('needs_citation'):
            # Apply citation
            if corrected['category'] == 'A':
                row['Suggested_Citation'] = corrected['suggested_citation']
                row['BibTeX_Key'] = corrected['bibtex_key']
                row['DOI_or_URL'] = corrected['doi_or_url']
                row['Research_Notes'] = f"BATCH09_CORRECTED: Category A - {corrected['algorithm_name']}"
                citation_applied += 1
            elif corrected['category'] == 'B':
                row['Suggested_Citation'] = corrected['suggested_citation']
                row['BibTeX_Key'] = corrected['bibtex_key']
                row['DOI_or_URL'] = corrected['doi_or_url']
                row['Research_Notes'] = f"BATCH09_CORRECTED: Category B - {corrected['concept']}"
                citation_applied += 1
        else:
            # Category C - clear citations
            row['Suggested_Citation'] = ''
            row['BibTeX_Key'] = ''
            row['DOI_or_URL'] = ''
            row['Research_Notes'] = f"BATCH09_CORRECTED: Category C - {corrected['implementation_type']} - no citation needed"

        updated_count += 1

# Save updated CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"\n{'='*80}")
print(f"BATCH 09 CORRECTIONS APPLIED")
print(f"{'='*80}")
print(f"\nTotal claims updated: {updated_count}/27")
print(f"Citations applied: {citation_applied}")
print(f"Category C (no citation): {updated_count - citation_applied}")
print(f"\nBreakdown:")
print(f"  Category A (algorithms): 1 (CODE-IMPL-509 - Goldberg 1991)")
print(f"  Category B (concepts): 1 (CODE-IMPL-024 - Montes de Oca et al. 2012)")
print(f"  Category C (implementation): 25 claims")
print(f"\n[OK] Updated: {csv_path}")
print(f"[OK] Backup: {backup_path}")
print(f"\n{'='*80}")
