#!/usr/bin/env python3
"""
Add Batch 09 claims to claims_research_tracker.csv with corrected citations
"""
import json
import csv
from pathlib import Path
from datetime import datetime

# Paths
batch09_claims_path = Path('D:/Projects/main/artifacts/research_batches/09_HIGH_fault_detection/claims.json')
batch09_corrected_path = Path('D:/Projects/main/artifacts/research_batches/09_HIGH_fault_detection/batch_09_corrected_citations.json')
csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')
backup_path = Path(f'D:/Projects/main/artifacts/claims_research_tracker_BACKUP_ADD_BATCH09_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

# Load Batch 09 original claims
with open(batch09_claims_path, 'r', encoding='utf-8') as f:
    batch09_data = json.load(f)
    original_claims = {c['id']: c for c in batch09_data['claims']}

# Load corrected categorization
with open(batch09_corrected_path, 'r', encoding='utf-8') as f:
    corrected_claims = json.load(f)

# Load existing CSV
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

# Create new rows for Batch 09 claims
added_count = 0
category_counts = {'A': 0, 'B': 0, 'C': 0}

for corrected in corrected_claims:
    claim_id = corrected['claim_id']
    original = original_claims.get(claim_id, {})

    # Create new CSV row
    new_row = {
        'Priority': 'HIGH',
        'Research_Status': 'completed',
        'Category': 'implementation',
        'Type': 'implementation',
        'Has_Citation': 'YES' if corrected.get('needs_citation') else 'NO',
        'Claim_ID': claim_id,
        'Research_Description': original.get('description', ''),
        'Full_Claim_Text': original.get('context', corrected['code_summary']),
        'Suggested_Citation': '',
        'BibTeX_Key': '',
        'DOI_or_URL': '',
        'Reference_Type': '',
        'Research_Notes': '',
        'File_Path': original.get('file_path', ''),
        'Line_Number': original.get('line_number', ''),
        'Scope': '',
        'Existing_Citation_Format': '',
        'Confidence': '0.65'
    }

    # Apply citations if needed
    if corrected.get('needs_citation'):
        new_row['Suggested_Citation'] = corrected['suggested_citation']
        new_row['BibTeX_Key'] = corrected['bibtex_key']
        new_row['DOI_or_URL'] = corrected['doi_or_url']
        new_row['Reference_Type'] = corrected['reference_type']

        if corrected['category'] == 'A':
            new_row['Research_Notes'] = f"BATCH09: Category A - {corrected['algorithm_name']}"
        elif corrected['category'] == 'B':
            new_row['Research_Notes'] = f"BATCH09: Category B - {corrected['concept']}"
    else:
        new_row['Research_Notes'] = f"BATCH09: Category C - {corrected['implementation_type']} - no citation needed"

    csv_rows.append(new_row)
    added_count += 1
    category_counts[corrected['category']] += 1

# Save updated CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"\n{'='*80}")
print(f"BATCH 09 CLAIMS ADDED TO CSV")
print(f"{'='*80}")
print(f"\nTotal claims added: {added_count}/27")
print(f"\nCategory Breakdown:")
print(f"  Category A (algorithms): {category_counts['A']} (CODE-IMPL-509 - Goldberg 1991)")
print(f"  Category B (concepts): {category_counts['B']} (CODE-IMPL-024 - Montes de Oca et al. 2012)")
print(f"  Category C (implementation): {category_counts['C']} claims")
print(f"\n[OK] Updated: {csv_path}")
print(f"[OK] Backup: {backup_path}")
print(f"\n{'='*80}")
