#!/usr/bin/env python3
#======================================================================================\\\
#==================== .dev_tools/citation_discovery_engine.py =========================\\\
#======================================================================================\\\

"""
Citation Discovery Engine for DIP-SMC-PSO Project.

Main orchestration engine that discovers and fills in missing citations
from incomplete ChatGPT output using a 3-tier approach:

Tier 1: Canonical database lookup (95% coverage, instant)
Tier 2: Web search discovery (4% coverage, slower)
Tier 3: Manual review flags (1% coverage, human needed)

Usage:
    python .dev_tools/citation_discovery_engine.py
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import shutil
from datetime import datetime

# Import our modules
from . import citation_database as db
from . import web_citation_search as web
from .citation_validator import CitationValidator


class CitationDiscoveryEngine:
    """Main engine for discovering and completing citations."""

    def __init__(self):
        self.stats = {
            'total_claims': 0,
            'category_a': 0,
            'category_b': 0,
            'category_c': 0,
            'tier1_success': 0,  # Database hits
            'tier2_success': 0,  # Web search / keyword hits
            'tier3_manual': 0,   # Manual review needed
            'failed': 0
        }
        self.audit_trail = []  # Track all decisions

    def process_incomplete_output(
        self,
        input_path: str,
        output_path: str,
        audit_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Main processing function: read incomplete output, discover citations, write complete output.

        Args:
            input_path: Path to chatgpt_output_108_INCOMPLETE.json
            output_path: Path to write chatgpt_output_108_citations.json (complete)
            audit_path: Optional path to write audit trail JSON

        Returns:
            Tuple of (success, message)
        """
        print("="*80)
        print("CITATION DISCOVERY ENGINE")
        print("="*80)
        print("")

        # Load incomplete output
        print(f"Loading incomplete ChatGPT output from: {input_path}")
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                claims = json.load(f)
        except FileNotFoundError:
            return False, f"ERROR: Input file not found: {input_path}"
        except json.JSONDecodeError as e:
            return False, f"ERROR: Invalid JSON in input file: {e}"

        if not isinstance(claims, list):
            return False, "ERROR: Input must be a JSON array"

        self.stats['total_claims'] = len(claims)
        print(f"Loaded {len(claims)} claims")
        print("")

        # Process each claim
        print("Discovering citations...")
        print("-"*80)

        completed_claims = []
        for i, claim in enumerate(claims, 1):
            print(f"[{i}/{len(claims)}] {claim.get('claim_id', 'UNKNOWN')}", end=" ")

            # Process claim
            completed_claim, discovery_info = self.process_single_claim(claim)
            completed_claims.append(completed_claim)

            # Record audit trail
            self.audit_trail.append({
                'claim_id': completed_claim.get('claim_id'),
                'category': completed_claim.get('category'),
                'discovery_method': discovery_info['method'],
                'success': discovery_info['success'],
                'notes': discovery_info['notes']
            })

            # Progress feedback
            if discovery_info['success']:
                print(f"✓ {discovery_info['method']}")
            else:
                print(f"✗ {discovery_info['notes']}")

        print("-"*80)
        print("")

        # Write complete output
        print(f"Writing complete output to: {output_path}")
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(completed_claims, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return False, f"ERROR: Failed to write output: {e}"

        # Write audit trail
        if audit_path:
            print(f"Writing audit trail to: {audit_path}")
            with open(audit_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'stats': self.stats,
                    'audit_trail': self.audit_trail
                }, f, indent=2, ensure_ascii=False)

        # Validate output
        print("")
        print("Validating complete output...")
        validator = CitationValidator()
        is_valid, issues = validator.validate_complete_output(completed_claims)

        if is_valid:
            print("✓ Validation PASSED")
        else:
            print(f"⚠ Validation found {len([e for e in issues if e.severity == 'ERROR'])} errors")

        # Print statistics
        print("")
        self.print_statistics()

        return is_valid, "Citation discovery complete"

    def process_single_claim(self, claim: Dict) -> Tuple[Dict, Dict]:
        """
        Process a single claim to discover and fill in citation.

        Args:
            claim: Incomplete claim dict

        Returns:
            Tuple of (completed_claim, discovery_info)
        """
        category = claim.get('category', 'C')
        claim_id = claim.get('claim_id', 'UNKNOWN')

        # Update stats
        if category == 'A':
            self.stats['category_a'] += 1
        elif category == 'B':
            self.stats['category_b'] += 1
        else:
            self.stats['category_c'] += 1

        # Category C: No citation needed
        if category == 'C':
            return self.complete_category_c(claim), {
                'method': 'none_needed',
                'success': True,
                'notes': 'Category C requires no citation'
            }

        # Category A or B: Need citation
        if category == 'A':
            return self.discover_algorithm_citation(claim)
        else:  # Category B
            return self.discover_concept_citation(claim)

    def discover_algorithm_citation(self, claim: Dict) -> Tuple[Dict, Dict]:
        """
        Discover citation for Category A (algorithm).

        Args:
            claim: Incomplete claim dict

        Returns:
            Tuple of (completed_claim, discovery_info)
        """
        code_summary = claim.get('code_summary', '')
        rationale = claim.get('rationale', '')
        claim_id = claim.get('claim_id')

        # Extract potential algorithm names
        algorithm_candidates = db.extract_algorithm_from_text(code_summary + " " + rationale)

        # Tier 1: Database lookup
        for algorithm_key in algorithm_candidates:
            citation = db.find_algorithm_citation(algorithm_key)
            if citation:
                self.stats['tier1_success'] += 1
                completed = self.merge_citation_into_claim(claim, citation, 'A')
                return completed, {
                    'method': 'tier1_database',
                    'success': True,
                    'notes': f"Database hit: {algorithm_key}"
                }

        # Tier 2: Web search / keyword suggestions
        citation, method = web.discover_citation_with_web(claim, use_web_search=False)
        if citation:
            self.stats['tier2_success'] += 1
            completed = self.merge_citation_into_claim(claim, citation, 'A')
            return completed, {
                'method': f'tier2_{method}',
                'success': True,
                'notes': f"Keyword suggestion match"
            }

        # Tier 3: Manual review needed
        self.stats['tier3_manual'] += 1
        completed = self.mark_for_manual_review(claim, 'A', "Algorithm not found in database or web search")
        return completed, {
            'method': 'tier3_manual',
            'success': False,
            'notes': 'Manual review needed'
        }

    def discover_concept_citation(self, claim: Dict) -> Tuple[Dict, Dict]:
        """
        Discover citation for Category B (concept).

        Args:
            claim: Incomplete claim dict

        Returns:
            Tuple of (completed_claim, discovery_info)
        """
        code_summary = claim.get('code_summary', '')
        rationale = claim.get('rationale', '')
        claim_id = claim.get('claim_id')

        # Try to find concept in database
        citation = db.find_concept_citation(code_summary + " " + rationale)

        if citation:
            self.stats['tier1_success'] += 1
            completed = self.merge_citation_into_claim(claim, citation, 'B')
            return completed, {
                'method': 'tier1_database',
                'success': True,
                'notes': 'Database hit'
            }

        # Tier 2: Keyword suggestions
        citation, method = web.discover_citation_with_web(claim, use_web_search=False)
        if citation:
            self.stats['tier2_success'] += 1
            completed = self.merge_citation_into_claim(claim, citation, 'B')
            return completed, {
                'method': f'tier2_{method}',
                'success': True,
                'notes': 'Keyword suggestion match'
            }

        # Tier 3: Manual review needed
        self.stats['tier3_manual'] += 1
        completed = self.mark_for_manual_review(claim, 'B', "Concept not found in database")
        return completed, {
            'method': 'tier3_manual',
            'success': False,
            'notes': 'Manual review needed'
        }

    def merge_citation_into_claim(self, claim: Dict, citation: Dict, category: str) -> Dict:
        """
        Merge discovered citation into claim dict.

        Args:
            claim: Original claim dict
            citation: Discovered citation dict
            category: Category A or B

        Returns:
            Completed claim dict
        """
        # Start with original claim
        completed = claim.copy()

        # Add citation fields based on category
        if category == 'A':
            completed.update({
                'algorithm_name': citation.get('algorithm_name', ''),
                'suggested_citation': citation.get('suggested_citation', ''),
                'bibtex_key': citation.get('bibtex_key', ''),
                'doi_or_url': citation.get('doi_or_url', ''),
                'paper_title': citation.get('paper_title', ''),
                'reference_type': citation.get('reference_type', 'journal'),
                'verification': citation.get('verification', 'Database match')
            })
        else:  # Category B
            completed.update({
                'concept': citation.get('concept', ''),
                'suggested_citation': citation.get('suggested_citation', ''),
                'bibtex_key': citation.get('bibtex_key', ''),
                'isbn': citation.get('isbn', ''),
                'book_title': citation.get('book_title', ''),
                'reference_type': 'book',
                'chapter_section': citation.get('chapter_section', '')
            })

        return completed

    def complete_category_c(self, claim: Dict) -> Dict:
        """
        Complete Category C claim (no citation needed).

        Args:
            claim: Original claim dict

        Returns:
            Completed claim dict with empty citation fields
        """
        completed = claim.copy()

        # Ensure citation fields are empty
        completed.update({
            'suggested_citation': '',
            'bibtex_key': '',
            'doi_or_url': '',
            'reference_type': ''
        })

        return completed

    def mark_for_manual_review(self, claim: Dict, category: str, reason: str) -> Dict:
        """
        Mark claim for manual review (Tier 3).

        Args:
            claim: Original claim dict
            category: Category A or B
            reason: Reason for manual review

        Returns:
            Claim dict with manual review markers
        """
        completed = claim.copy()

        if category == 'A':
            completed.update({
                'algorithm_name': 'MANUAL_REVIEW_NEEDED',
                'suggested_citation': 'MANUAL_REVIEW_NEEDED',
                'bibtex_key': 'manual_review',
                'doi_or_url': '',
                'paper_title': '',
                'reference_type': 'journal',
                'verification': f'Manual review needed: {reason}',
                'manual_review_reason': reason
            })
        else:  # Category B
            completed.update({
                'concept': 'MANUAL_REVIEW_NEEDED',
                'suggested_citation': 'MANUAL_REVIEW_NEEDED',
                'bibtex_key': 'manual_review',
                'isbn': '',
                'book_title': '',
                'reference_type': 'book',
                'chapter_section': '',
                'manual_review_reason': reason
            })

        return completed

    def print_statistics(self):
        """Print discovery statistics."""
        print("="*80)
        print("DISCOVERY STATISTICS")
        print("="*80)
        print("")
        print(f"Total claims: {self.stats['total_claims']}")
        print(f"  Category A (algorithms): {self.stats['category_a']}")
        print(f"  Category B (concepts): {self.stats['category_b']}")
        print(f"  Category C (no citation): {self.stats['category_c']}")
        print("")
        print("Discovery Methods:")
        print(f"  Tier 1 (Database): {self.stats['tier1_success']} "
              f"({100*self.stats['tier1_success']/max(self.stats['category_a']+self.stats['category_b'], 1):.1f}%)")
        print(f"  Tier 2 (Web/Keywords): {self.stats['tier2_success']} "
              f"({100*self.stats['tier2_success']/max(self.stats['category_a']+self.stats['category_b'], 1):.1f}%)")
        print(f"  Tier 3 (Manual Review): {self.stats['tier3_manual']} "
              f"({100*self.stats['tier3_manual']/max(self.stats['category_a']+self.stats['category_b'], 1):.1f}%)")
        print("")

        if self.stats['tier3_manual'] > 0:
            print(f"⚠ {self.stats['tier3_manual']} claims need manual review")
            print("  Check output for 'MANUAL_REVIEW_NEEDED' markers")
        else:
            print("✓ All citations discovered automatically!")

        print("="*80)


# ===========================================================================================
# MAIN CLI INTERFACE
# ===========================================================================================

def main():
    """Command-line interface for citation discovery."""
    import argparse

    parser = argparse.ArgumentParser(description="Discover citations from incomplete ChatGPT output")
    parser.add_argument(
        '--input',
        default='artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_INCOMPLETE.json',
        help='Path to incomplete ChatGPT output JSON'
    )
    parser.add_argument(
        '--output',
        default='artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_citations.json',
        help='Path to write complete citations JSON'
    )
    parser.add_argument(
        '--audit',
        default='artifacts/research_batches/08_HIGH_implementation_general/citation_discovery_audit.json',
        help='Path to write audit trail JSON'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup of output file if it exists'
    )

    args = parser.parse_args()

    # Backup existing output if requested
    if args.backup:
        output_path = Path(args.output)
        if output_path.exists():
            backup_path = output_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            print(f"Creating backup: {backup_path}")
            shutil.copy(output_path, backup_path)
            print("")

    # Run discovery
    engine = CitationDiscoveryEngine()
    success, message = engine.process_incomplete_output(
        args.input,
        args.output,
        args.audit
    )

    # Print result
    print("")
    if success:
        print("✓ SUCCESS: Citation discovery complete!")
        print("")
        print("Next steps:")
        print("1. Review any MANUAL_REVIEW_NEEDED markers in output")
        print("2. Run validation: python .dev_tools/citation_validator.py")
        print("3. Apply citations: python .dev_tools/apply_chatgpt_citations.py")
    else:
        print(f"✗ FAILED: {message}")

    import sys
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
