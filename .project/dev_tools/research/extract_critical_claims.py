#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/extract_critical_claims.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Extract CRITICAL claims from claims_inventory.json.

Creates research-ready input files for the research pipeline.
"""

import json
from pathlib import Path
from typing import List, Dict, Any


def extract_critical_claims(
    inventory_path: str = ".artifacts/claims_inventory.json",
    output_all: str = ".artifacts/critical_claims_all_11.json",
    output_remaining: str = ".artifacts/critical_claims_remaining_7.json",
) -> None:
    """
    Extract all 11 CRITICAL claims and create input files.

    Args:
        inventory_path: Path to claims_inventory.json
        output_all: Output file for all 11 CRITICAL claims
        output_remaining: Output file for 7 remaining (not in Batch 01)
    """
    # IDs already researched in Batch 01
    batch01_ids = {
        "FORMAL-THEOREM-016",
        "FORMAL-THEOREM-019",
        "FORMAL-THEOREM-020",
        "FORMAL-THEOREM-023",
    }

    # Load inventory
    with open(inventory_path, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    # Get CRITICAL claim IDs
    critical_ids = inventory['research_queue']['CRITICAL']
    print(f"Found {len(critical_ids)} CRITICAL claims: {critical_ids}")

    # Extract claim details
    all_critical_claims = []
    remaining_claims = []

    for claim in inventory['claims']:
        if claim['id'] in critical_ids:
            # Format for research pipeline
            formatted_claim = {
                "id": claim['id'],
                "type": claim.get('type', 'theorem'),
                "number": claim.get('number'),
                "statement": claim.get('statement', claim.get('claim_text', '')),
                "proof": claim.get('proof'),
                "file_path": claim.get('file_path', ''),
                "line_number": claim.get('line_number', 0),
                "has_citation": claim.get('has_citation', False),
                "confidence": claim.get('confidence', 0.9),
                "suggested_keywords": claim.get('suggested_keywords', []),
                "context": claim.get('context', ''),
                "category": claim.get('category', 'theoretical'),
                "priority": claim.get('priority', 'CRITICAL'),
            }

            all_critical_claims.append(formatted_claim)

            # Check if not in Batch 01
            if claim['id'] not in batch01_ids:
                remaining_claims.append(formatted_claim)

    # Sort by ID for consistency
    all_critical_claims.sort(key=lambda x: x['id'])
    remaining_claims.sort(key=lambda x: x['id'])

    # Create output structure (matching test_claims_batch01.json format)
    output_all_data = {
        "metadata": {
            "total_claims": len(all_critical_claims),
            "by_priority": {"CRITICAL": len(all_critical_claims)},
        },
        "research_queue": {
            "CRITICAL": [c['id'] for c in all_critical_claims],
            "HIGH": [],
            "MEDIUM": [],
        },
        "claims": all_critical_claims,
    }

    output_remaining_data = {
        "metadata": {
            "total_claims": len(remaining_claims),
            "by_priority": {"CRITICAL": len(remaining_claims)},
        },
        "research_queue": {
            "CRITICAL": [c['id'] for c in remaining_claims],
            "HIGH": [],
            "MEDIUM": [],
        },
        "claims": remaining_claims,
    }

    # Save outputs
    with open(output_all, 'w', encoding='utf-8') as f:
        json.dump(output_all_data, f, indent=2, ensure_ascii=False)

    with open(output_remaining, 'w', encoding='utf-8') as f:
        json.dump(output_remaining_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Created {output_all}")
    print(f"   Total CRITICAL claims: {len(all_critical_claims)}")

    print(f"\n✅ Created {output_remaining}")
    print(f"   Remaining claims (not in Batch 01): {len(remaining_claims)}")

    print(f"\n📊 Batch 01 (already researched): {len(batch01_ids)} claims")
    print(f"   IDs: {sorted(batch01_ids)}")

    print(f"\n📊 Remaining (to be researched): {len(remaining_claims)} claims")
    print(f"   IDs: {[c['id'] for c in remaining_claims]}")


if __name__ == "__main__":
    extract_critical_claims()
