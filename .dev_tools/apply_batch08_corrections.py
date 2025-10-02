#!/usr/bin/env python3
"""
Apply verified citation corrections to Batch 08 claims in CSV tracker.

This script applies the 15 severe/critical citation corrections identified
by automated verification (verify_batch08_citations.py).
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def apply_corrections(csv_path: Path, output_path: Path = None) -> None:
    """Apply verified citation corrections to CSV."""

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = csv_path.parent / f"claims_research_tracker_CORRECTED_{timestamp}.csv"

    print(f"Loading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)

    # Critical fixes (remove citations - implementation patterns)
    critical_fixes = {
        'CODE-IMPL-086': {
            'Suggested_Citation': '',
            'BibTeX_Key': '',
            'DOI_or_URL': '',
            'Research_Notes': 'Implementation pattern (factory) - no citation needed',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-109': {
            'Suggested_Citation': '',
            'BibTeX_Key': '',
            'DOI_or_URL': '',
            'Research_Notes': 'Implementation pattern (threading) - no citation needed',
            'Research_Status': 'completed'
        },
    }

    # Severe fixes (replace with correct citations)
    severe_fixes = {
        # Cross-validation group (3 claims)
        'CODE-IMPL-063': {
            'Suggested_Citation': 'Stone (1978)',
            'BibTeX_Key': 'stone1978cross',
            'DOI_or_URL': '10.1080/02331887808801414',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Shapiro & Wilk (normality) → Stone (cross-validation)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-064': {
            'Suggested_Citation': 'Stone (1978)',
            'BibTeX_Key': 'stone1978cross',
            'DOI_or_URL': '10.1080/02331887808801414',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Shapiro & Wilk (normality) → Stone (cross-validation)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-066': {
            'Suggested_Citation': 'Stone (1978)',
            'BibTeX_Key': 'stone1978cross',
            'DOI_or_URL': '10.1080/02331887808801414',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Shapiro & Wilk (normality) → Stone (cross-validation)',
            'Research_Status': 'completed'
        },

        # Outlier detection (1 claim)
        'CODE-IMPL-029': {
            'Suggested_Citation': 'Barnett & Lewis (1994)',
            'BibTeX_Key': 'barnett1994outliers',
            'DOI_or_URL': '10.1002/bimj.4710370219',
            'Reference_Type': 'book',
            'Research_Notes': 'CORRECTED: Was Efron (bootstrap) → Barnett (outlier detection)',
            'Research_Status': 'completed'
        },

        # Super-twisting group (5 claims)
        'CODE-IMPL-168': {
            'Suggested_Citation': 'Levant (2003)',
            'BibTeX_Key': 'levant2003higher',
            'DOI_or_URL': '10.1080/0020717031000099029',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Goldberg (genetic) → Levant (super-twisting)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-169': {
            'Suggested_Citation': 'Levant (2003)',
            'BibTeX_Key': 'levant2003higher',
            'DOI_or_URL': '10.1080/0020717031000099029',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Goldberg (genetic) → Levant (super-twisting)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-173': {
            'Suggested_Citation': 'Levant (2003)',
            'BibTeX_Key': 'levant2003higher',
            'DOI_or_URL': '10.1080/0020717031000099029',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Goldberg (genetic) → Levant (super-twisting)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-174': {
            'Suggested_Citation': 'Levant (2003)',
            'BibTeX_Key': 'levant2003higher',
            'DOI_or_URL': '10.1080/0020717031000099029',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Goldberg (genetic) → Levant (super-twisting)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-175': {
            'Suggested_Citation': 'Levant (2003)',
            'BibTeX_Key': 'levant2003higher',
            'DOI_or_URL': '10.1080/0020717031000099029',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Goldberg (genetic) → Levant (super-twisting)',
            'Research_Status': 'completed'
        },

        # SMC sliding surfaces (4 claims)
        'CODE-IMPL-186': {
            'Suggested_Citation': 'Utkin (1977)',
            'BibTeX_Key': 'utkin1977variable',
            'DOI_or_URL': '10.1109/TAC.1977.1101446',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Camacho (MPC) → Utkin (SMC)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-189': {
            'Suggested_Citation': 'Utkin (1977)',
            'BibTeX_Key': 'utkin1977variable',
            'DOI_or_URL': '10.1109/TAC.1977.1101446',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Camacho (MPC) → Utkin (SMC)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-190': {
            'Suggested_Citation': 'Utkin (1977)',
            'BibTeX_Key': 'utkin1977variable',
            'DOI_or_URL': '10.1109/TAC.1977.1101446',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Camacho (MPC) → Utkin (SMC)',
            'Research_Status': 'completed'
        },
        'CODE-IMPL-191': {
            'Suggested_Citation': 'Utkin (1977)',
            'BibTeX_Key': 'utkin1977variable',
            'DOI_or_URL': '10.1109/TAC.1977.1101446',
            'Reference_Type': 'journal',
            'Research_Notes': 'CORRECTED: Was Camacho (MPC) → Utkin (SMC)',
            'Research_Status': 'completed'
        },
    }

    # Combine all fixes
    all_fixes = {**critical_fixes, **severe_fixes}

    # Apply fixes
    corrections_applied = 0
    corrections_failed = 0

    for claim_id, updates in all_fixes.items():
        mask = df['Claim_ID'] == claim_id

        if mask.sum() == 0:
            print(f"WARNING: Claim {claim_id} not found in CSV")
            corrections_failed += 1
            continue

        if mask.sum() > 1:
            print(f"WARNING: Multiple rows for {claim_id} - updating all")

        for col, value in updates.items():
            if col in df.columns:
                df.loc[mask, col] = value
            else:
                print(f"WARNING: Column '{col}' not found in CSV")

        corrections_applied += 1

    # Save
    print(f"\nSaving corrected CSV to {output_path}...")
    df.to_csv(output_path, index=False)

    print(f"\n{'='*70}")
    print("CORRECTION SUMMARY")
    print(f"{'='*70}")
    print(f"Total corrections attempted: {len(all_fixes)}")
    print(f"Successfully applied: {corrections_applied}")
    print(f"Failed: {corrections_failed}")
    print(f"\nCorrected CSV saved to:")
    print(f"  {output_path}")
    print(f"\nOriginal CSV preserved at:")
    print(f"  {csv_path}")
    print(f"{'='*70}")


def main():
    # Find CSV file
    csv_path = Path("D:/Projects/main/artifacts/claims_research_tracker.csv")

    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        print("Please provide correct path to claims_research_tracker.csv")
        return

    apply_corrections(csv_path)


if __name__ == "__main__":
    main()
