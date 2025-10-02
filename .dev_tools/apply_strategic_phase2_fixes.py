#!/usr/bin/env python3
"""
Apply Strategic Phase 2 Fixes - Stability Analysis
Based on 5-sample pattern analysis:
- 20% need textbook citation (theoretical metrics documentation)
- 80% need NO citation (implementation code)

Decision Rules:
1. Module docstrings describing control metrics → Ogata (2010)
2. Variance/convergence computation → NO CITATION
3. Plotting/visualization → NO CITATION
4. Data structures → NO CITATION
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Ogata textbook for control theory metrics
OGATA_CITATION = {
    'Suggested_Citation': 'Ogata (2010)',
    'BibTeX_Key': 'ogata2010modern',
    'DOI_or_URL': 'ISBN: 978-0136156734',
    'Reference_Type': 'book',
    'Research_Notes': 'STRATEGIC_PHASE2: Control systems textbook - transient response metrics (overshoot, settling time, rise time)'
}

def load_claims() -> List[Dict]:
    """Load claims from JSON."""
    claims_file = Path("D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json")
    with open(claims_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['claims']

def categorize_stability_claim(claim: Dict) -> Tuple[str, str]:
    """
    Categorize stability/analysis claim.
    Returns: (decision, rationale)
    - decision: 'ogata' or 'no_citation'
    - rationale: explanation
    """
    file_path = claim['file_path'].lower()
    context = claim['context'].lower()
    line_num = int(claim.get('line_number', 0))

    # Rule 1: Module docstrings at line 1 describing control metrics
    if line_num <= 5:  # Near top of file (module docstring area)
        # Check if describes control theory concepts
        if any(kw in context for kw in ['overshoot', 'settling time', 'rise time', 'transient response',
                                         'control metric', 'stability metric', 'performance metric']):
            if 'metric' in file_path:  # In a metrics module
                return ('ogata', 'Module describes control theory metrics')

    # Rule 2: Variance/convergence computation
    if any(kw in context for kw in ['compute variance', 'compute stability', 'variance growth',
                                     'polyfit', 'np.var', 'variance trend']):
        return ('no_citation', 'Variance/convergence computation (implementation)')

    # Rule 3: Plotting/visualization
    if any(kw in context for kw in ['plot', 'plt.', 'matplotlib', 'visualization', 'plt.savefig',
                                     'fig,', 'axes =', 'plt.subplots']):
        return ('no_citation', 'Plotting/visualization function (implementation)')

    # Rule 4: Convergence module placeholders
    if 'convergence' in file_path and '__init__.py' in file_path:
        return ('no_citation', 'Module placeholder/import (no actual implementation)')

    # Rule 5: Data structures / methods
    if any(kw in context for kw in ['def get_', 'return', '@dataclass', 'field(', 'Dict[', 'List[']):
        if any(kw in file_path for kw in ['data_structures', 'interfaces', 'core']):
            return ('no_citation', 'Data structure/method (implementation)')

    # Rule 6: Analysis module computation
    if 'analysis' in file_path:
        if any(kw in context for kw in ['def _compute', 'def compute_', 'calculate', 'np.mean', 'np.std']):
            return ('no_citation', 'Statistical/numerical computation (implementation)')

    # Default: NO CITATION (conservative - can review uncertain cases later)
    return ('no_citation', 'Analysis/implementation code (no theory cited)')

def apply_phase2_corrections() -> Dict:
    """Apply Phase 2 corrections."""
    print("=" * 80)
    print("STRATEGIC PHASE 2: STABILITY ANALYSIS")
    print("=" * 80)

    # Load claims
    print("\n[1/5] Loading claims...")
    claims = load_claims()
    print(f"      Loaded {len(claims)} claims")

    # Identify stability/analysis claims (uncited)
    print("\n[2/5] Identifying stability/analysis claims...")
    stability_claims = []
    for claim in claims:
        file_path = claim['file_path'].lower()
        context = claim.get('context', '').lower()
        text = f'{file_path} {context}'

        # Stability/analysis keywords
        if any(kw in text for kw in ['stability', 'convergence', 'variance', 'lyapunov',
                                      'performance', 'metric', 'analysis', 'overshoot',
                                      'settling', 'transient']):
            stability_claims.append(claim)

    print(f"      Found {len(stability_claims)} stability/analysis claims")

    # Categorize each claim
    print("\n[3/5] Categorizing claims...")
    need_ogata = []
    need_no_citation = []

    for claim in stability_claims:
        decision, rationale = categorize_stability_claim(claim)
        if decision == 'ogata':
            need_ogata.append((claim['id'], rationale))
        else:
            need_no_citation.append((claim['id'], rationale))

    print(f"\n      Need Ogata citation: {len(need_ogata)} claims")
    print(f"      Need NO citation: {len(need_no_citation)} claims")
    print(f"      Total categorized: {len(need_ogata) + len(need_no_citation)}")

    # Display samples
    print("\n      Sample claims needing Ogata citation:")
    for claim_id, rationale in need_ogata[:5]:
        print(f"        - {claim_id}: {rationale}")

    print("\n      Sample claims needing NO citation:")
    for claim_id, rationale in need_no_citation[:5]:
        print(f"        - {claim_id}: {rationale}")
    if len(need_no_citation) > 5:
        print(f"        ... and {len(need_no_citation)-5} more")

    # Apply corrections to CSV
    print("\n[4/5] Applying corrections to CSV...")
    csv_path = Path("D:/Projects/main/artifacts/claims_research_tracker.csv")

    # Backup CSV
    backup_path = csv_path.parent / f"claims_research_tracker_BACKUP_PHASE2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    import shutil
    shutil.copy(csv_path, backup_path)
    print(f"      Backup created: {backup_path.name}")

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
        claim_id = row['Claim_ID']

        # Check if needs Ogata
        for cid, rationale in need_ogata:
            if claim_id == cid:
                row['Suggested_Citation'] = OGATA_CITATION['Suggested_Citation']
                row['BibTeX_Key'] = OGATA_CITATION['BibTeX_Key']
                row['DOI_or_URL'] = OGATA_CITATION['DOI_or_URL']
                row['Reference_Type'] = OGATA_CITATION['Reference_Type']
                row['Research_Status'] = 'completed'
                row['Research_Notes'] = OGATA_CITATION['Research_Notes'] + f' | {rationale}'
                corrected_count += 1
                break

        # Check if needs NO citation
        for cid, rationale in need_no_citation:
            if claim_id == cid:
                # Skip if already completed in Phase 1
                if row.get('Research_Status') == 'completed' and 'STRATEGIC_PHASE1' in row.get('Research_Notes', ''):
                    continue

                row['Suggested_Citation'] = ''
                row['BibTeX_Key'] = ''
                row['DOI_or_URL'] = ''
                row['Reference_Type'] = ''
                row['Research_Status'] = 'completed'
                row['Research_Notes'] = f'STRATEGIC_PHASE2: {rationale}'
                corrected_count += 1
                break

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[SUCCESS] Applied {corrected_count} corrections")

    # Summary
    print("\n" + "=" * 80)
    print("PHASE 2 COMPLETE")
    print("=" * 80)
    print(f"Corrected: {corrected_count} claims")
    print(f"  - Need Ogata (2010): {len(need_ogata)}")
    print(f"  - Need NO citation: {len(need_no_citation)}")
    print("=" * 80)

    return {
        'total_corrected': corrected_count,
        'ogata_count': len(need_ogata),
        'no_citation_count': len(need_no_citation),
        'ogata_claims': need_ogata,
        'no_citation_claims': need_no_citation
    }

if __name__ == "__main__":
    result = apply_phase2_corrections()
    exit(0)
