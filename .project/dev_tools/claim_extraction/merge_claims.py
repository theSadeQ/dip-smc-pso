#==========================================================================================\\\
#====================== .dev_tools/claim_extraction/merge_claims.py ====================\\\
#==========================================================================================\\\

"""
Claims Database Merger - Phase 1 Tool 3

Merges formal and code claim databases with priority assignment and deduplication.

Priority Levels:
- CRITICAL: Uncited formal theorems/lemmas/propositions (scientific risk)
- HIGH: Uncited implementation claims (reproducibility risk)
- MEDIUM: Already cited claims

Deduplication: Jaccard similarity with threshold > 0.8

Output: artifacts/claims_inventory.json with research queue
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict


@dataclass
class MergeMetadata:
    """Metadata for merged claims database."""
    total_claims: int
    sources: Dict[str, int]
    by_priority: Dict[str, int]
    citation_status: Dict[str, Any]
    duplicates_removed: int


class ClaimsMerger:
    """Merges formal and code claims with priority assignment and deduplication."""

    def __init__(
        self,
        formal_claims_path: Path,
        code_claims_path: Path,
        output_path: Path,
        similarity_threshold: float = 0.8
    ):
        """Initialize merger with input/output paths.

        Args:
            formal_claims_path: Path to formal_claims.json
            code_claims_path: Path to code_claims.json
            output_path: Path for unified claims_inventory.json
            similarity_threshold: Jaccard similarity threshold for deduplication
        """
        self.formal_claims_path = formal_claims_path
        self.code_claims_path = code_claims_path
        self.output_path = output_path
        self.similarity_threshold = similarity_threshold

    def load_claims(self) -> Tuple[List[Dict], List[Dict]]:
        """Load formal and code claims from JSON files.

        Returns:
            Tuple of (formal_claims, code_claims)
        """
        with open(self.formal_claims_path, 'r', encoding='utf-8') as f:
            formal_data = json.load(f)

        with open(self.code_claims_path, 'r', encoding='utf-8') as f:
            code_data = json.load(f)

        # Add category field for priority assignment
        formal_claims = formal_data['claims']
        for claim in formal_claims:
            claim['category'] = 'theoretical'

        code_claims = code_data['claims']
        for claim in code_claims:
            claim['category'] = 'implementation'

        return formal_claims, code_claims

    def assign_priority(self, claim: Dict) -> str:
        """Assign priority based on category, type, and citation status.

        Priority Logic:
        - CRITICAL: Uncited formal theorems/lemmas/propositions (scientific risk)
        - HIGH: Uncited implementation claims (reproducibility risk)
        - MEDIUM: Already cited OR informal claims

        Args:
            claim: Claim dictionary

        Returns:
            Priority level: 'CRITICAL', 'HIGH', or 'MEDIUM'
        """
        # CRITICAL: Uncited formal theorems/lemmas/propositions
        if (claim.get('category') == 'theoretical' and
            claim.get('type') in ['theorem', 'lemma', 'proposition'] and
            not claim.get('has_citation', False)):
            return 'CRITICAL'

        # HIGH: Uncited implementation claims
        if (claim.get('category') == 'implementation' and
            not claim.get('has_citation', False)):
            return 'HIGH'

        # MEDIUM: Everything else (cited claims, informal claims)
        return 'MEDIUM'

    def generate_signature(self, claim: Dict) -> str:
        """Generate text signature for similarity comparison.

        Extracts key technical terms from claim text/statement.

        Args:
            claim: Claim dictionary

        Returns:
            Sorted pipe-separated signature of key terms
        """
        # Get text from claim (formal uses 'statement', code uses 'claim_text')
        text = claim.get('statement') or claim.get('claim_text', '')

        # Extract words longer than 3 characters (filter noise)
        words = re.findall(r'\b\w{4,}\b', text.lower())

        # Take first 10 unique words, sorted for consistency
        terms = sorted(set(words[:10]))

        return '|'.join(terms)

    def calculate_jaccard_similarity(self, sig1: str, sig2: str) -> float:
        """Calculate Jaccard similarity between two signatures.

        Jaccard similarity = |A ∩ B| / |A ∪ B|

        Args:
            sig1: First signature
            sig2: Second signature

        Returns:
            Similarity score [0, 1]
        """
        set1 = set(sig1.split('|'))
        set2 = set(sig2.split('|'))

        intersection = set1 & set2
        union = set1 | set2

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def deduplicate_claims(self, claims: List[Dict]) -> List[Dict]:
        """Remove near-duplicate claims using Jaccard similarity.

        Strategy:
        1. Generate signature for each claim
        2. Compare pairwise with existing claims
        3. Merge if similarity > threshold
        4. Keep higher-confidence version

        Args:
            claims: List of all claims

        Returns:
            Deduplicated claims list
        """
        deduplicated = []
        duplicates_count = 0

        for claim in claims:
            signature = self.generate_signature(claim)

            # Check against existing deduplicated claims
            is_duplicate = False
            for i, existing in enumerate(deduplicated):
                existing_sig = self.generate_signature(existing)
                similarity = self.calculate_jaccard_similarity(signature, existing_sig)

                if similarity > self.similarity_threshold:
                    is_duplicate = True
                    duplicates_count += 1

                    # Keep higher-confidence version
                    if claim['confidence'] > existing['confidence']:
                        deduplicated[i] = claim

                    break

            if not is_duplicate:
                deduplicated.append(claim)

        print(f"Deduplication: {duplicates_count} duplicates removed")
        print(f"  Before: {len(claims)} claims")
        print(f"  After: {len(deduplicated)} claims")

        return deduplicated

    def merge_and_process(self) -> Dict[str, Any]:
        """Main merge workflow.

        Returns:
            Unified claims inventory with metadata and research queue
        """
        print("Loading claims...")
        formal_claims, code_claims = self.load_claims()

        print(f"Loaded {len(formal_claims)} formal claims")
        print(f"Loaded {len(code_claims)} code claims")
        print(f"Total before deduplication: {len(formal_claims) + len(code_claims)}")

        # Merge all claims
        all_claims = formal_claims + code_claims

        # Deduplicate
        print("\nDeduplicating claims...")
        deduplicated_claims = self.deduplicate_claims(all_claims)

        # Assign priorities
        print("\nAssigning priorities...")
        for claim in deduplicated_claims:
            claim['priority'] = self.assign_priority(claim)

        # Calculate metadata
        priority_counts = Counter(c['priority'] for c in deduplicated_claims)
        cited_count = sum(1 for c in deduplicated_claims if c.get('has_citation', False))
        uncited_count = len(deduplicated_claims) - cited_count

        metadata = MergeMetadata(
            total_claims=len(deduplicated_claims),
            sources={
                "formal_extractor": len(formal_claims),
                "code_extractor": len(code_claims),
                "duplicates_removed": len(all_claims) - len(deduplicated_claims)
            },
            by_priority={
                "CRITICAL": priority_counts.get('CRITICAL', 0),
                "HIGH": priority_counts.get('HIGH', 0),
                "MEDIUM": priority_counts.get('MEDIUM', 0)
            },
            citation_status={
                "cited": cited_count,
                "uncited": uncited_count,
                "coverage": f"{100 * cited_count / len(deduplicated_claims):.1f}%"
            },
            duplicates_removed=len(all_claims) - len(deduplicated_claims)
        )

        # Create research queue (claim IDs organized by priority)
        research_queue = {
            "CRITICAL": [c['id'] for c in deduplicated_claims if c['priority'] == 'CRITICAL'],
            "HIGH": [c['id'] for c in deduplicated_claims if c['priority'] == 'HIGH'],
            "MEDIUM": [c['id'] for c in deduplicated_claims if c['priority'] == 'MEDIUM']
        }

        # Build unified inventory
        inventory = {
            "metadata": asdict(metadata),
            "research_queue": research_queue,
            "claims": deduplicated_claims
        }

        return inventory

    def save_inventory(self, inventory: Dict[str, Any]) -> None:
        """Save unified claims inventory to JSON.

        Args:
            inventory: Unified claims inventory
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)

        print(f"\nSaved unified claims inventory to: {self.output_path}")

    def print_summary(self, inventory: Dict[str, Any]) -> None:
        """Print summary statistics.

        Args:
            inventory: Unified claims inventory
        """
        metadata = inventory['metadata']

        print("\n" + "="*80)
        print("CLAIMS INVENTORY SUMMARY")
        print("="*80)

        print(f"\nTotal Claims: {metadata['total_claims']}")
        print(f"   Sources:")
        print(f"     - Formal Extractor: {metadata['sources']['formal_extractor']}")
        print(f"     - Code Extractor: {metadata['sources']['code_extractor']}")
        print(f"     - Duplicates Removed: {metadata['sources']['duplicates_removed']}")

        print(f"\nPriority Distribution:")
        print(f"     - CRITICAL: {metadata['by_priority']['CRITICAL']} claims (uncited theorems/lemmas)")
        print(f"     - HIGH: {metadata['by_priority']['HIGH']} claims (uncited implementations)")
        print(f"     - MEDIUM: {metadata['by_priority']['MEDIUM']} claims (cited claims)")

        print(f"\nCitation Coverage:")
        print(f"     - Cited: {metadata['citation_status']['cited']}")
        print(f"     - Uncited: {metadata['citation_status']['uncited']}")
        print(f"     - Coverage: {metadata['citation_status']['coverage']}")

        print(f"\nResearch Queue:")
        queue = inventory['research_queue']
        print(f"     - CRITICAL: {len(queue['CRITICAL'])} claims -> Research first")
        print(f"     - HIGH: {len(queue['HIGH'])} claims -> Research second")
        print(f"     - MEDIUM: {len(queue['MEDIUM'])} claims -> Research last")

        print("\n" + "="*80)


def main():
    """Main execution."""
    # Paths
    project_root = Path(__file__).parent.parent.parent
    formal_claims = project_root / "artifacts" / "formal_claims.json"
    code_claims = project_root / "artifacts" / "code_claims.json"
    output = project_root / "artifacts" / "claims_inventory.json"

    # Create merger
    merger = ClaimsMerger(
        formal_claims_path=formal_claims,
        code_claims_path=code_claims,
        output_path=output,
        similarity_threshold=0.8
    )

    # Execute merge workflow
    inventory = merger.merge_and_process()

    # Save and print summary
    merger.save_inventory(inventory)
    merger.print_summary(inventory)


if __name__ == "__main__":
    main()
