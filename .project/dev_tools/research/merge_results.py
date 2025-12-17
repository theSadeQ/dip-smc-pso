#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/merge_results.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Merge V3 test results with new critical batch results.

Creates unified research_results.json with all 11 CRITICAL claims.
"""

import json
from pathlib import Path
from typing import List, Dict, Any


def load_v3_results(v3_backup_path: str = None) -> Dict[str, Any]:
    """Load V3 test results from backup/log. Defaults to centralized log directory."""
    if v3_backup_path is None:
        from src.utils.logging.paths import LOG_DIR
        v3_backup_path = str(LOG_DIR / "test_pipeline_batch01_v3.log")
    """
    Load V3 test results from backup/log.

    For now, reconstruct from the current research_results.json
    which should have been backed up or we can use session history.
    """
    # Check if there's a backup
    backup_file = Path("artifacts/research/research_results_v3_backup.json")

    if backup_file.exists():
        with open(backup_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # If no backup, we need to reconstruct from session history
    # For now, we'll note that V3 tested these 4 claims:
    v3_claim_ids = {
        "FORMAL-THEOREM-016",
        "FORMAL-THEOREM-019",
        "FORMAL-THEOREM-020",
        "FORMAL-THEOREM-023",
    }

    print(f"Note: V3 backup not found. V3 tested claims: {v3_claim_ids}")
    print("Current research_results.json will be treated as new batch only.")

    return None


def merge_research_results(
    new_results_path: str = "artifacts/research/research_results.json",
    v3_backup_path: str = "artifacts/research/research_results_v3_backup.json",
    output_path: str = "artifacts/research/critical_batch_complete.json",
) -> None:
    """
    Merge V3 and new research results.

    Args:
        new_results_path: Current research_results.json (7 new claims)
        v3_backup_path: V3 backup (4 claims)
        output_path: Merged output file
    """
    # Load new results (7 claims)
    with open(new_results_path, 'r', encoding='utf-8') as f:
        new_results = json.load(f)

    print(f"Loaded new results: {len(new_results['results'])} claims")

    # Try to load V3 backup
    v3_backup = Path(v3_backup_path)

    if v3_backup.exists():
        with open(v3_backup, 'r', encoding='utf-8') as f:
            v3_results = json.load(f)

        print(f"Loaded V3 backup: {len(v3_results['results'])} claims")

        # Merge results
        all_results = v3_results['results'] + new_results['results']

        # Create merged output
        merged = {
            "session_id": "critical_batch_complete",
            "progress": {
                "session_id": "critical_batch_complete",
                "started_at": v3_results['progress']['started_at'],
                "last_updated": new_results['progress']['last_updated'],
                "total_claims": len(all_results),
                "claims_processed": len(all_results),
                "claims_successful": len(all_results),
                "claims_failed": 0,
                "current_batch": "CRITICAL",
                "current_claim_id": None,
                "errors": [],
                "performance": {}
            },
            "results": all_results
        }

        print(f"\nMerged results: {len(all_results)} total claims")
        print(f"  V3 batch: {len(v3_results['results'])} claims")
        print(f"  New batch: {len(new_results['results'])} claims")

    else:
        print("\nWarning: V3 backup not found!")
        print("Creating complete results from available data...")
        print("Note: This assumes current research_results.json has all 7 new claims.")

        # Use new results as base
        merged = new_results
        merged['session_id'] = "critical_batch_partial_7claims"

        print(f"\nPartial results: {len(merged['results'])} claims (7 new)")
        print("V3 batch (4 claims) needs to be re-merged manually if backup exists.")

    # Save merged results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved merged results to: {output_path}")

    # Print claim IDs for verification
    print("\nMerged claim IDs:")
    for i, result in enumerate(merged['results'], 1):
        print(f"  {i}. {result['claim_id']}")


if __name__ == "__main__":
    merge_research_results()
