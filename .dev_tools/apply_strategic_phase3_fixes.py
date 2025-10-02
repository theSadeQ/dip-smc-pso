#!/usr/bin/env python3
"""
Apply Strategic Phase 3 Fixes - Optimization Algorithms

Citations:
- Differential Evolution (6 claims) → Storn & Price (1997)
- Genetic Algorithm (8 claims) → Goldberg (1989)
- BFGS (4 claims) → Nocedal & Wright (2006)
- Nelder-Mead (5 claims) → Nelder & Mead (1965)
- Infrastructure (15 claims) → NO CITATION
"""

import csv
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Algorithm citations
CITATIONS = {
    'differential_evolution': {
        'Suggested_Citation': 'Storn & Price (1997)',
        'BibTeX_Key': 'storn1997differential',
        'DOI_or_URL': '10.1023/A:1008202821328',
        'Reference_Type': 'journal',
        'Research_Notes': 'STRATEGIC_PHASE3: Differential Evolution - seminal paper on DE algorithm'
    },
    'genetic_algorithm': {
        'Suggested_Citation': 'Goldberg (1989)',
        'BibTeX_Key': 'goldberg1989genetic',
        'DOI_or_URL': 'ISBN: 978-0201157673',
        'Reference_Type': 'book',
        'Research_Notes': 'STRATEGIC_PHASE3: Genetic Algorithms - foundational textbook'
    },
    'bfgs': {
        'Suggested_Citation': 'Nocedal & Wright (2006)',
        'BibTeX_Key': 'nocedal2006numerical',
        'DOI_or_URL': 'ISBN: 978-0387303031',
        'Reference_Type': 'book',
        'Research_Notes': 'STRATEGIC_PHASE3: Quasi-Newton methods (BFGS) - standard numerical optimization reference'
    },
    'nelder_mead': {
        'Suggested_Citation': 'Nelder & Mead (1965)',
        'BibTeX_Key': 'nelder1965simplex',
        'DOI_or_URL': '10.1093/comjnl/7.4.308',
        'Reference_Type': 'journal',
        'Research_Notes': 'STRATEGIC_PHASE3: Nelder-Mead simplex method - original algorithm paper'
    }
}

# Claim categorization based on analysis
CLAIM_CATEGORIES = {
    # Differential Evolution
    'CODE-IMPL-278': 'differential_evolution',
    'CODE-IMPL-279': 'differential_evolution',
    'CODE-IMPL-280': 'differential_evolution',
    'CODE-IMPL-281': 'differential_evolution',
    'CODE-IMPL-282': 'differential_evolution',
    'CODE-IMPL-283': 'differential_evolution',

    # Genetic Algorithm
    'CODE-IMPL-285': 'genetic_algorithm',
    'CODE-IMPL-286': 'genetic_algorithm',
    'CODE-IMPL-288': 'genetic_algorithm',
    'CODE-IMPL-289': 'genetic_algorithm',
    'CODE-IMPL-290': 'genetic_algorithm',
    'CODE-IMPL-291': 'genetic_algorithm',
    'CODE-IMPL-292': 'genetic_algorithm',
    'CODE-IMPL-293': 'genetic_algorithm',

    # BFGS
    'CODE-IMPL-296': 'bfgs',
    'CODE-IMPL-297': 'bfgs',
    'CODE-IMPL-298': 'bfgs',
    'CODE-IMPL-299': 'bfgs',

    # Nelder-Mead
    'CODE-IMPL-300': 'nelder_mead',
    'CODE-IMPL-301': 'nelder_mead',
    'CODE-IMPL-302': 'nelder_mead',
    'CODE-IMPL-303': 'nelder_mead',
    'CODE-IMPL-304': 'nelder_mead',

    # NO CITATION (infrastructure)
    'CODE-IMPL-271': 'no_citation',  # Base class
    'CODE-IMPL-272': 'no_citation',  # Base infrastructure
    'CODE-IMPL-273': 'no_citation',  # Base infrastructure
    'CODE-IMPL-274': 'no_citation',  # Base infrastructure
    'CODE-IMPL-275': 'no_citation',  # Base infrastructure
    'CODE-IMPL-277': 'no_citation',  # Module import
    'CODE-IMPL-294': 'no_citation',  # Module import
    'CODE-IMPL-295': 'no_citation',  # Module import
    'CODE-IMPL-308': 'no_citation',  # PSO memory management
    'CODE-IMPL-312': 'no_citation',  # PSO context manager
    'CODE-IMPL-360': 'no_citation',  # PSO bounds optimizer
    'CODE-IMPL-361': 'no_citation',  # PSO bounds optimizer
    'CODE-IMPL-363': 'no_citation',  # PSO bounds optimizer
    'CODE-IMPL-366': 'no_citation',  # PSO bounds validator
    'CODE-IMPL-367': 'no_citation',  # PSO bounds validator
}

def apply_phase3_corrections() -> Dict:
    """Apply Phase 3 corrections."""
    print("=" * 80)
    print("STRATEGIC PHASE 3: OPTIMIZATION ALGORITHMS")
    print("=" * 80)

    # Count by category
    category_counts = {}
    for claim_id, category in CLAIM_CATEGORIES.items():
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\n[1/3] Claims by category:")
    for category, count in sorted(category_counts.items()):
        print(f"      {category}: {count}")
    print(f"      TOTAL: {len(CLAIM_CATEGORIES)}")

    # Apply corrections to CSV
    print("\n[2/3] Applying corrections to CSV...")
    csv_path = Path("D:/Projects/main/artifacts/claims_research_tracker.csv")

    # Backup CSV
    backup_path = csv_path.parent / f"claims_research_tracker_BACKUP_PHASE3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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

        if claim_id in CLAIM_CATEGORIES:
            category = CLAIM_CATEGORIES[claim_id]

            if category == 'no_citation':
                # Mark as no citation needed
                row['Suggested_Citation'] = ''
                row['BibTeX_Key'] = ''
                row['DOI_or_URL'] = ''
                row['Reference_Type'] = ''
                row['Research_Status'] = 'completed'
                row['Research_Notes'] = 'STRATEGIC_PHASE3: Infrastructure/base class - no citation needed'
            else:
                # Apply algorithm citation
                citation = CITATIONS[category]
                row['Suggested_Citation'] = citation['Suggested_Citation']
                row['BibTeX_Key'] = citation['BibTeX_Key']
                row['DOI_or_URL'] = citation['DOI_or_URL']
                row['Reference_Type'] = citation['Reference_Type']
                row['Research_Status'] = 'completed'
                row['Research_Notes'] = citation['Research_Notes']

            corrected_count += 1

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[SUCCESS] Applied {corrected_count} corrections")

    # Summary
    print("\n" + "=" * 80)
    print("PHASE 3 COMPLETE")
    print("=" * 80)
    print(f"Total corrected: {corrected_count} claims")
    print(f"\nCitations applied:")
    print(f"  - Differential Evolution (Storn & Price 1997): {category_counts.get('differential_evolution', 0)}")
    print(f"  - Genetic Algorithm (Goldberg 1989): {category_counts.get('genetic_algorithm', 0)}")
    print(f"  - BFGS (Nocedal & Wright 2006): {category_counts.get('bfgs', 0)}")
    print(f"  - Nelder-Mead (Nelder & Mead 1965): {category_counts.get('nelder_mead', 0)}")
    print(f"  - No citation needed: {category_counts.get('no_citation', 0)}")
    print("=" * 80)

    return category_counts

if __name__ == "__main__":
    result = apply_phase3_corrections()
    exit(0)
