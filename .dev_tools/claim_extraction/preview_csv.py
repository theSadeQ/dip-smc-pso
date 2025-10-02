"""Preview CSV structure for user."""
import csv
from pathlib import Path

csv_path = Path(__file__).parent.parent.parent / "artifacts" / "claims_research_tracker.csv"

with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Show column headers
print("="*80)
print("CSV COLUMN HEADERS")
print("="*80)
headers = list(rows[0].keys())
for i, header in enumerate(headers, 1):
    marker = "<<< USER FILLS" if header in ['Research_Status', 'Suggested_Citation', 'BibTeX_Key', 'DOI_or_URL', 'Reference_Type', 'Research_Notes'] else ""
    print(f"{i:2d}. {header:30s} {marker}")

# Show sample CRITICAL claim
print("\n" + "="*80)
print("SAMPLE CRITICAL CLAIM (Uncited Theorem - Research First!)")
print("="*80)
critical = [r for r in rows if r['Priority'] == 'CRITICAL'][0]

key_fields = ['Priority', 'Claim_ID', 'Category', 'Type', 'Research_Description',
              'File_Path', 'Line_Number', 'Research_Status', 'Suggested_Citation',
              'BibTeX_Key', 'DOI_or_URL']

for field in key_fields:
    value = critical.get(field, 'N/A')
    if field in ['Research_Status', 'Suggested_Citation', 'BibTeX_Key', 'DOI_or_URL'] and not value:
        value = '<EMPTY - YOU FILL THIS>'
    print(f"{field:25s}: {value}")

# Show sample HIGH claim
print("\n" + "="*80)
print("SAMPLE HIGH CLAIM (Uncited Implementation)")
print("="*80)
high = [r for r in rows if r['Priority'] == 'HIGH'][0]

for field in key_fields:
    value = high.get(field, 'N/A')
    if field in ['Research_Status', 'Suggested_Citation', 'BibTeX_Key', 'DOI_or_URL'] and not value:
        value = '<EMPTY - YOU FILL THIS>'
    print(f"{field:25s}: {value}")

print("\n" + "="*80)
print(f"Total rows in CSV: {len(rows)}")
print("Open in Excel and filter by Priority to start researching!")
print("="*80)
