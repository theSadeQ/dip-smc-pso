"""
Generate research-friendly CSV from claims inventory for manual citation research.

Output: artifacts/claims_research_tracker.csv
Optimized for Excel with research tracking columns.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any


def truncate_text(text: str, max_length: int = 150) -> str:
    """Truncate text for CSV readability."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def prepare_research_rows(claims: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Convert claims to CSV-friendly research rows."""
    rows = []

    for claim in claims:
        # Get claim text (formal uses 'statement', code uses 'claim_text')
        claim_text = claim.get('statement') or claim.get('claim_text', 'N/A')

        # Extract algorithm/source info if available
        algorithm_name = claim.get('algorithm_name', 'N/A')
        source_attribution = claim.get('source_attribution', 'N/A')

        # Build description for research
        if algorithm_name != 'N/A' and source_attribution != 'N/A':
            research_description = f"{algorithm_name} (attributed to: {source_attribution})"
        elif algorithm_name != 'N/A':
            research_description = algorithm_name
        else:
            research_description = truncate_text(claim_text, 150)

        row = {
            # Sorting/Filtering columns
            'Priority': claim.get('priority', 'UNKNOWN'),
            'Category': claim.get('category', 'N/A'),
            'Type': claim.get('type', 'N/A'),
            'Has_Citation': 'YES' if claim.get('has_citation', False) else 'NO',

            # Identification
            'Claim_ID': claim.get('id', 'N/A'),

            # Content
            'Research_Description': research_description,
            'Full_Claim_Text': truncate_text(claim_text, 300),

            # Location
            'File_Path': claim.get('file_path', 'N/A'),
            'Line_Number': str(claim.get('line_number', 'N/A')),

            # Existing citation info (if any)
            'Existing_Citation_Format': claim.get('citation_format', 'N/A'),

            # Metadata
            'Scope': claim.get('scope', 'N/A'),
            'Confidence': f"{claim.get('confidence', 0.0):.2f}",

            # === RESEARCH TRACKING COLUMNS (empty for user to fill) ===
            'Research_Status': '',  # empty/in_progress/completed
            'Suggested_Citation': '',  # Author (Year) format
            'BibTeX_Key': '',  # e.g., levant2003higher
            'DOI_or_URL': '',  # Digital Object Identifier or URL
            'Reference_Type': '',  # journal/conference/book/arxiv/website
            'Research_Notes': ''  # Any additional notes
        }

        rows.append(row)

    return rows


def main():
    """Generate research CSV from claims inventory."""

    # Load claims inventory
    project_root = Path(__file__).parent.parent.parent
    inventory_path = project_root / "artifacts" / "claims_inventory.json"

    with open(inventory_path, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    claims = inventory['claims']

    # Sort by priority: CRITICAL first, then HIGH, then MEDIUM
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
    sorted_claims = sorted(
        claims,
        key=lambda c: priority_order.get(c.get('priority', 'UNKNOWN'), 99)
    )

    # Prepare CSV rows
    research_rows = prepare_research_rows(sorted_claims)

    # Define CSV columns (order matters for Excel readability)
    fieldnames = [
        # Priority/Filter columns (leftmost for easy sorting)
        'Priority',
        'Research_Status',  # User fills this
        'Category',
        'Type',
        'Has_Citation',

        # Identification
        'Claim_ID',

        # Research content
        'Research_Description',
        'Full_Claim_Text',

        # Research tracking (user fills these)
        'Suggested_Citation',
        'BibTeX_Key',
        'DOI_or_URL',
        'Reference_Type',
        'Research_Notes',

        # Location (for reference)
        'File_Path',
        'Line_Number',
        'Scope',

        # Metadata
        'Existing_Citation_Format',
        'Confidence'
    ]

    # Write CSV
    output_path = project_root / "artifacts" / "claims_research_tracker.csv"

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:  # UTF-8 BOM for Excel
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(research_rows)

    # Print summary
    print("="*80)
    print("RESEARCH CSV GENERATED")
    print("="*80)
    print(f"\nOutput: {output_path}")
    print(f"Total claims: {len(research_rows)}")

    # Priority breakdown
    from collections import Counter
    priority_counts = Counter(row['Priority'] for row in research_rows)
    print(f"\nPriority breakdown:")
    print(f"  CRITICAL: {priority_counts.get('CRITICAL', 0)} claims (research first)")
    print(f"  HIGH: {priority_counts.get('HIGH', 0)} claims (research second)")
    print(f"  MEDIUM: {priority_counts.get('MEDIUM', 0)} claims (validate existing)")

    print(f"\nResearch workflow:")
    print(f"  1. Open CSV in Excel/Google Sheets")
    print(f"  2. Filter by Priority = CRITICAL")
    print(f"  3. For each claim:")
    print(f"     - Research citation (Google Scholar, arXiv, etc.)")
    print(f"     - Fill in: Suggested_Citation, BibTeX_Key, DOI_or_URL")
    print(f"     - Update Research_Status: 'in_progress' -> 'completed'")
    print(f"  4. Repeat for HIGH priority claims")
    print(f"  5. Validate MEDIUM priority (existing citations)")

    print(f"\nResearch tracking columns (empty for you to fill):")
    print(f"  - Research_Status: empty/in_progress/completed")
    print(f"  - Suggested_Citation: Author (Year) format")
    print(f"  - BibTeX_Key: e.g., levant2003higher")
    print(f"  - DOI_or_URL: Digital Object Identifier or URL")
    print(f"  - Reference_Type: journal/conference/book/arxiv/website")
    print(f"  - Research_Notes: Any additional notes")

    print("\n" + "="*80)
    print("CSV ready for research! Open in Excel and start with CRITICAL claims.")
    print("="*80)


if __name__ == "__main__":
    main()
