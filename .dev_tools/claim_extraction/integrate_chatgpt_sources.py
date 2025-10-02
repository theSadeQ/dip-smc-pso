"""
Integrate ChatGPT Citation Results into CSV Tracker

Parses chatgpt_sources.md files from research batch folders and updates
claims_research_tracker.csv with citation data.

Usage:
    python integrate_chatgpt_sources.py --batch "01_CRITICAL_sliding_mode_classical"
    python integrate_chatgpt_sources.py --batch "01_CRITICAL_sliding_mode_classical" --verify
"""

import re
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ChatGPTSourcesParser:
    """Parse chatgpt_sources.md files and extract citation data."""

    def __init__(self, sources_file: Path):
        self.sources_file = sources_file
        self.content = sources_file.read_text(encoding='utf-8')

    def parse_claims(self) -> List[Dict]:
        """Parse all claims from chatgpt_sources.md."""
        claims = []

        # Pattern to match claim blocks
        claim_pattern = r'CLAIM \d+ \(ID: ([\w-]+)\):\s*\n\s*\n' \
                       r'- Citation: ([^\n]+)\n' \
                       r'- BibTeX Key: ([^\n]+)\n' \
                       r'- DOI: ([^\n]+)\n' \
                       r'- Type: ([^\n]+)\n' \
                       r'- Note: ([^\n]+(?:\n(?!CLAIM)[^\n]+)*)'

        matches = re.finditer(claim_pattern, self.content, re.MULTILINE)

        for match in matches:
            claim_id, citation, bibtex_key, doi, ref_type, note = match.groups()

            # Clean up note (remove extra whitespace)
            note = ' '.join(note.split())

            claims.append({
                'claim_id': claim_id.strip(),
                'citation': citation.strip(),
                'bibtex_key': bibtex_key.strip(),
                'doi': doi.strip(),
                'type': ref_type.strip(),
                'note': note.strip()
            })

        return claims


class CSVIntegrator:
    """Integrate parsed citation data into claims_research_tracker.csv."""

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.rows = []
        self.headers = []
        self._load_csv()

    def _load_csv(self):
        """Load CSV file into memory."""
        with open(self.csv_path, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            self.rows = list(reader)

    def update_claims(self, claims_data: List[Dict]) -> Dict:
        """Update CSV with citation data."""
        stats = {
            'updated': 0,
            'not_found': [],
            'already_completed': []
        }

        for claim in claims_data:
            claim_id = claim['claim_id']

            # Find row in CSV
            row_idx = None
            for idx, row in enumerate(self.rows):
                if row['Claim_ID'] == claim_id:
                    row_idx = idx
                    break

            if row_idx is None:
                stats['not_found'].append(claim_id)
                continue

            row = self.rows[row_idx]

            # Check if already completed
            if row['Research_Status'] == 'completed':
                stats['already_completed'].append(claim_id)
                # Still update to ensure latest data
                pass

            # Update 6 tracking columns
            row['Research_Status'] = 'completed'
            row['Suggested_Citation'] = claim['citation']
            row['BibTeX_Key'] = claim['bibtex_key']

            # Handle DOI vs URL
            if claim['doi'] and claim['doi'].lower() not in ['n/a', 'na', '']:
                row['DOI_or_URL'] = claim['doi']
            else:
                # Try to extract URL from source documentation if DOI is N/A
                row['DOI_or_URL'] = claim['doi']  # Keep N/A for now

            row['Reference_Type'] = claim['type']
            row['Research_Notes'] = claim['note']

            stats['updated'] += 1

        return stats

    def save_csv(self):
        """Save updated CSV back to file."""
        with open(self.csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.rows)


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Integrate ChatGPT citation results into CSV tracker'
    )
    parser.add_argument(
        '--batch',
        required=True,
        help='Batch folder name (e.g., "01_CRITICAL_sliding_mode_classical")'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Run verification after integration'
    )

    args = parser.parse_args()

    # Paths
    base_path = Path(__file__).parent.parent.parent
    batch_folder = base_path / "artifacts" / "research_batches" / args.batch
    sources_file = batch_folder / "chatgpt_sources.md"
    csv_file = base_path / "artifacts" / "claims_research_tracker.csv"

    # Verify files exist
    if not sources_file.exists():
        print(f"[ERROR] chatgpt_sources.md not found in {batch_folder}")
        return 1

    if not csv_file.exists():
        print(f"[ERROR] claims_research_tracker.csv not found at {csv_file}")
        return 1

    print("="*80)
    print("CHATGPT SOURCES -> CSV INTEGRATION")
    print("="*80)
    print(f"\nBatch: {args.batch}")
    print(f"Sources file: {sources_file.name}")
    print(f"CSV file: {csv_file.name}")
    print()

    # Parse chatgpt_sources.md
    print("Parsing chatgpt_sources.md...")
    parser_obj = ChatGPTSourcesParser(sources_file)
    claims_data = parser_obj.parse_claims()

    if not claims_data:
        print("[ERROR] No claims found in chatgpt_sources.md")
        print("   Check file format matches expected structure")
        return 1

    print(f"  [OK] Found {len(claims_data)} claims\n")

    # Display parsed data
    for claim in claims_data:
        print(f"  - {claim['claim_id']}: {claim['citation']}")

    print()

    # Integrate into CSV
    print("Updating CSV...")
    integrator = CSVIntegrator(csv_file)
    stats = integrator.update_claims(claims_data)

    print(f"  [OK] Updated {stats['updated']} claims")

    if stats['not_found']:
        print(f"  [WARN] Not found in CSV: {', '.join(stats['not_found'])}")

    if stats['already_completed']:
        print(f"  [INFO] Already completed (re-updated): {', '.join(stats['already_completed'])}")

    # Save CSV
    integrator.save_csv()
    print(f"\n  [OK] CSV saved successfully")

    # Count unique citations
    unique_citations = set(c['citation'] for c in claims_data)
    print(f"\n  [OK] {len(unique_citations)} unique citations -> {len(claims_data)} claims")
    if len(unique_citations) < len(claims_data):
        efficiency = (1 - len(unique_citations)/len(claims_data)) * 100
        print(f"  [OK] Citation reuse: {efficiency:.0f}% efficiency gain!")

    print()
    print("="*80)
    print("=== INTEGRATION COMPLETE ===")
    print("="*80)

    # Verification
    if args.verify:
        print("\nRunning verification...")
        print("Command: python .dev_tools/claim_extraction/citation_tracker.py")
        print("(Run manually to see updated progress)")

    print(f"\nNext steps:")
    print(f"1. Run: python .dev_tools/claim_extraction/citation_tracker.py")
    print(f"2. Verify: Batch {args.batch} shows 100% completion")
    print(f"3. Check CSV manually to confirm data integrity")

    return 0


if __name__ == "__main__":
    exit(main())
