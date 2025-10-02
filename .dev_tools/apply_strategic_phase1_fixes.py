#!/usr/bin/env python3
"""
Apply Strategic Phase 1 Fixes - Quick Wins
Fixes 19 claims: threading (9), design patterns (8), serialization (2)

All are pure implementation → NO CITATION NEEDED
"""

import csv
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Phase 1 Categories and Patterns
THREADING_PATTERNS = ['threading', 'lock', 'mutex', 'deadlock', 'concurrent', 'thread-safe']
PATTERN_KEYWORDS = ['factory', 'singleton', 'observer', 'pattern', '__init__.py']
SERIALIZATION_KEYWORDS = ['to_dict', 'from_dict', 'serialize', 'deserialize', 'to_json', 'from_json']

def load_claims() -> List[Dict]:
    """Load claims from JSON."""
    claims_file = Path("D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json")
    with open(claims_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['claims']

def identify_phase1_claims(claims: List[Dict]) -> Dict[str, List[str]]:
    """Identify Phase 1 claims by category."""
    phase1 = {
        'threading': [],
        'patterns': [],
        'serialization': []
    }

    for claim in claims:
        file_path = claim['file_path'].lower()
        context = claim['context'].lower()
        text = f"{file_path} {context}"

        # Threading/concurrency
        if any(kw in text for kw in THREADING_PATTERNS):
            if 'algorithm' not in text:  # Avoid concurrent algorithms
                phase1['threading'].append(claim['id'])
                continue

        # Design patterns (focus on factory in controllers)
        if 'factory' in file_path and 'controllers' in file_path:
            phase1['patterns'].append(claim['id'])
            continue

        if any(kw in text for kw in PATTERN_KEYWORDS):
            if '__init__.py' in file_path:
                phase1['patterns'].append(claim['id'])
                continue

        # Serialization
        if any(kw in text for kw in SERIALIZATION_KEYWORDS):
            phase1['serialization'].append(claim['id'])

    return phase1

def apply_corrections(csv_path: Path, corrections: Dict[str, str]) -> bool:
    """Apply corrections to CSV."""
    # Read CSV
    rows = []
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Apply corrections
    corrected_count = 0
    for row in rows:
        if row['Claim_ID'] in corrections:
            category = corrections[row['Claim_ID']]
            row['Suggested_Citation'] = ''
            row['BibTeX_Key'] = ''
            row['DOI_or_URL'] = ''
            row['Reference_Type'] = ''
            row['Research_Status'] = 'completed'
            row['Research_Notes'] = f'STRATEGIC_PHASE1: Implementation pattern ({category}) - no citation needed'
            corrected_count += 1

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return corrected_count == len(corrections)

def main():
    print("=" * 80)
    print("STRATEGIC PHASE 1: QUICK WINS")
    print("=" * 80)

    # Load claims
    print("\n[1/4] Loading claims...")
    claims = load_claims()
    print(f"      Loaded {len(claims)} claims")

    # Identify Phase 1 claims
    print("\n[2/4] Identifying Phase 1 claims...")
    phase1 = identify_phase1_claims(claims)

    print(f"\n      Threading/Concurrency: {len(phase1['threading'])} claims")
    print(f"      Design Patterns: {len(phase1['patterns'])} claims")
    print(f"      Serialization: {len(phase1['serialization'])} claims")
    print(f"      TOTAL: {sum(len(v) for v in phase1.values())} claims")

    # Create corrections mapping
    corrections = {}
    for claim_id in phase1['threading']:
        corrections[claim_id] = 'threading'
    for claim_id in phase1['patterns']:
        corrections[claim_id] = 'design_pattern'
    for claim_id in phase1['serialization']:
        corrections[claim_id] = 'serialization'

    # Display claims to be corrected
    print("\n[3/4] Claims to be corrected:")
    for category, claim_ids in phase1.items():
        if claim_ids:
            print(f"\n      {category.upper()}:")
            for claim_id in claim_ids[:5]:
                print(f"        - {claim_id}")
            if len(claim_ids) > 5:
                print(f"        ... and {len(claim_ids)-5} more")

    # Apply corrections
    print("\n[4/4] Applying corrections to CSV...")
    csv_path = Path("D:/Projects/main/artifacts/claims_research_tracker.csv")

    # Backup CSV
    backup_path = csv_path.parent / f"claims_research_tracker_BACKUP_PHASE1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    import shutil
    shutil.copy(csv_path, backup_path)
    print(f"      Backup created: {backup_path.name}")

    success = apply_corrections(csv_path, corrections)

    if success:
        print(f"\n[SUCCESS] Applied {len(corrections)} corrections")
        print(f"          CSV updated: {csv_path}")
    else:
        print(f"\n[ERROR] Some corrections failed")
        return False

    # Summary
    print("\n" + "=" * 80)
    print("PHASE 1 COMPLETE")
    print("=" * 80)
    print(f"Corrected: {len(corrections)} claims")
    print(f"  - Threading/Concurrency: {len(phase1['threading'])}")
    print(f"  - Design Patterns: {len(phase1['patterns'])}")
    print(f"  - Serialization: {len(phase1['serialization'])}")
    print("\nAll marked: 'no citation needed'")
    print("=" * 80)

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
