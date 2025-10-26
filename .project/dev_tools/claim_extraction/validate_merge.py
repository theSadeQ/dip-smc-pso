"""Quick validation script for claims_inventory.json"""
import json
from pathlib import Path

# Load inventory
inv_path = Path(__file__).parent.parent.parent / "artifacts" / "claims_inventory.json"
with open(inv_path, 'r', encoding='utf-8') as f:
    inv = json.load(f)

# Get metadata
metadata = inv['metadata']
queue = inv['research_queue']
claims = inv['claims']

# Priority breakdown
critical_claims = [c for c in claims if c['priority'] == 'CRITICAL']
high_claims = [c for c in claims if c['priority'] == 'HIGH']
medium_claims = [c for c in claims if c['priority'] == 'MEDIUM']

print("="*80)
print("VALIDATION REPORT")
print("="*80)

# Validate totals
print(f"\nTotal claims: {len(claims)} (metadata says: {metadata['total_claims']})")
assert len(claims) == metadata['total_claims'], "Claim count mismatch!"

# Validate priority distribution
print(f"\nPriority distribution validation:")
print(f"  CRITICAL: {len(critical_claims)} (metadata: {metadata['by_priority']['CRITICAL']})")
print(f"  HIGH: {len(high_claims)} (metadata: {metadata['by_priority']['HIGH']})")
print(f"  MEDIUM: {len(medium_claims)} (metadata: {metadata['by_priority']['MEDIUM']})")

assert len(critical_claims) == metadata['by_priority']['CRITICAL']
assert len(high_claims) == metadata['by_priority']['HIGH']
assert len(medium_claims) == metadata['by_priority']['MEDIUM']

# Validate research queue
print(f"\nResearch queue validation:")
print(f"  CRITICAL queue: {len(queue['CRITICAL'])} IDs")
print(f"  HIGH queue: {len(queue['HIGH'])} IDs")
print(f"  MEDIUM queue: {len(queue['MEDIUM'])} IDs")

assert len(queue['CRITICAL']) == len(critical_claims)
assert len(queue['HIGH']) == len(high_claims)
assert len(queue['MEDIUM']) == len(medium_claims)

# Sample CRITICAL claims
print(f"\nSample CRITICAL claims (uncited theorems/lemmas):")
for i, claim in enumerate(critical_claims[:3], 1):
    print(f"\n  {i}. ID: {claim['id']}")
    print(f"     Type: {claim.get('type', 'N/A')}")
    print(f"     File: {claim['file_path']}")
    print(f"     Line: {claim['line_number']}")
    print(f"     Has citation: {claim.get('has_citation', False)}")
    if 'statement' in claim:
        print(f"     Statement (first 100 chars): {claim['statement'][:100]}...")

# Sample HIGH claims
print(f"\nSample HIGH claims (uncited implementations):")
for i, claim in enumerate(high_claims[:3], 1):
    print(f"\n  {i}. ID: {claim['id']}")
    print(f"     Scope: {claim.get('scope', 'N/A')}")
    print(f"     File: {claim['file_path']}")
    print(f"     Line: {claim['line_number']}")
    print(f"     Has citation: {claim.get('has_citation', False)}")
    if 'claim_text' in claim:
        print(f"     Claim (first 100 chars): {claim['claim_text'][:100]}...")

# Sample MEDIUM claims
print(f"\nSample MEDIUM claims (cited claims):")
for i, claim in enumerate(medium_claims[:2], 1):
    print(f"\n  {i}. ID: {claim['id']}")
    print(f"     Category: {claim.get('category', 'N/A')}")
    print(f"     File: {claim['file_path']}")
    print(f"     Has citation: {claim.get('has_citation', False)}")
    print(f"     Citation format: {claim.get('citation_format', 'N/A')}")

# Deduplication analysis
duplication_rate = metadata['sources']['duplicates_removed'] / (metadata['total_claims'] + metadata['sources']['duplicates_removed']) * 100
print(f"\n\nDeduplication analysis:")
print(f"  Before: {metadata['total_claims'] + metadata['sources']['duplicates_removed']} claims")
print(f"  After: {metadata['total_claims']} claims")
print(f"  Removed: {metadata['sources']['duplicates_removed']} duplicates ({duplication_rate:.1f}%)")

# Citation coverage
print(f"\nCitation coverage:")
print(f"  Cited: {metadata['citation_status']['cited']} claims")
print(f"  Uncited: {metadata['citation_status']['uncited']} claims")
print(f"  Coverage: {metadata['citation_status']['coverage']}")

print("\n" + "="*80)
print("All validations PASSED!")
print("="*80)
