#==========================================================================================\\\
#================= .dev_tools/claim_extraction/formal_extractor.py =====================\\\
#==========================================================================================\\\

"""
Formal Mathematical Claim Extractor

Extracts formal mathematical claims (theorems, lemmas, propositions, corollaries) from
Markdown documentation files. Uses regex patterns to identify claim structures, detect
existing citations, extract proofs, and generate confidence scores for citation research.

Target: 40-50 formal claims across documentation corpus
Precision: >=90% on manual review
Performance: <2 seconds execution
"""

import re
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FormalClaim:
    """Formal mathematical claim requiring citation verification.

    Attributes:
        id: Unique identifier (e.g., "FORMAL-THEOREM-001")
        type: Claim type (theorem, lemma, proposition, corollary, definition, assumption)
        number: Optional theorem/lemma number
        statement: Full claim statement
        proof: Associated proof block if present
        file_path: Relative path from project root
        line_number: Line where claim starts
        has_citation: Whether claim already has {cite} syntax
        confidence: Confidence score [0.0, 1.0] based on structural clues
        suggested_keywords: Keywords for AI research assistance
        context: Surrounding context (5 lines before/after)
    """
    id: str
    type: str
    number: Optional[int]
    statement: str
    proof: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    confidence: float
    suggested_keywords: List[str]
    context: str = ""


class FormalClaimExtractor:
    """Extract formal mathematical claims from Markdown documentation."""

    # Regex patterns for formal claim structures
    FORMAL_CLAIM_PATTERN = re.compile(
        r'\*\*(?P<type>Theorem|Lemma|Proposition|Corollary|Definition|Assumption)\s*'
        r'(?P<number>\d+)?\s*(?:\((?P<name>[^)]+)\))?\*\*\s*:?\s*(?P<statement>.+?)(?=\n\n|\*\*Proof\*\*|$)',
        re.DOTALL | re.MULTILINE
    )

    # Pattern for proof blocks (ends with □ or ∎)
    PROOF_PATTERN = re.compile(
        r'\*\*Proof\*\*:?\s*(?P<proof>.+?)(?:□|∎|\n\n##|\n\n\*\*)',
        re.DOTALL | re.MULTILINE
    )

    # Pattern for existing citations {cite}`reference`
    CITATION_PATTERN = re.compile(r'\{cite\}`[^`]+`')

    # Exclusion patterns: Skip documentation examples and meta-documentation
    # These paths contain example theorems used for documentation, not actual research claims
    EXCLUDE_PATTERNS = [
        r'docs/tools/',           # Tool documentation with examples
        r'docs/plans/',           # Planning documents with placeholder examples
        r'docs/testing/',         # Test documentation
        r'.*_guide\.md$',         # User guides with examples
        r'.*_reference\.md$',     # Reference docs with pattern examples
        r'.*_template\.md$',      # Templates
    ]

    # Keywords indicating SMC/optimization domains
    DOMAIN_KEYWORDS = {
        'sliding': ['sliding mode', 'SMC', 'Utkin', 'reaching condition'],
        'stability': ['Lyapunov', 'stability', 'convergence', 'asymptotic'],
        'super_twisting': ['super-twisting', 'Levant', 'Moreno', 'higher-order'],
        'adaptive': ['adaptive', 'estimation', 'uncertainty'],
        'pso': ['PSO', 'particle swarm', 'Kennedy', 'Eberhart', 'swarm intelligence'],
        'control': ['robust', 'finite-time', 'chattering', 'boundary layer']
    }

    def __init__(self, root_dir: Path):
        """Initialize extractor with project root directory.

        Args:
            root_dir: Project root directory for relative path calculations
        """
        self.root_dir = Path(root_dir)
        self.claims: List[FormalClaim] = []
        self.claim_counter = 0

    def extract_from_file(self, file_path: Path) -> List[FormalClaim]:
        """Extract formal claims from a single Markdown file.

        Args:
            file_path: Path to Markdown file

        Returns:
            List of extracted formal claims
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return []

        file_claims = []
        relative_path = file_path.relative_to(self.root_dir).as_posix()

        # Find all formal claim matches
        for match in self.FORMAL_CLAIM_PATTERN.finditer(content):
            claim_type = match.group('type').lower()
            number_str = match.group('number')
            number = int(number_str) if number_str else None
            name = match.group('name')
            statement = match.group('statement').strip()

            # Get line number (1-indexed)
            line_number = content[:match.start()].count('\n') + 1

            # Extract context (5 lines before and after)
            context_start = max(0, line_number - 6)
            context_end = min(len(lines), line_number + 5)
            context = '\n'.join(lines[context_start:context_end])

            # Check for citation
            has_citation = bool(self.CITATION_PATTERN.search(statement))

            # Try to find associated proof
            proof = None
            proof_match = self.PROOF_PATTERN.search(content, match.end())
            if proof_match and (proof_match.start() - match.end()) < 200:
                proof = proof_match.group('proof').strip()

            # Calculate confidence score
            confidence = self._calculate_confidence(
                claim_type, statement, proof, has_citation, context
            )

            # Extract keywords for research
            keywords = self._extract_keywords(statement, context)

            # Generate unique ID
            self.claim_counter += 1
            claim_id = f"FORMAL-{claim_type.upper()}-{self.claim_counter:03d}"

            claim = FormalClaim(
                id=claim_id,
                type=claim_type,
                number=number,
                statement=statement,
                proof=proof,
                file_path=relative_path,
                line_number=line_number,
                has_citation=has_citation,
                confidence=confidence,
                suggested_keywords=keywords,
                context=context
            )

            file_claims.append(claim)

        logger.info(f"Extracted {len(file_claims)} formal claims from {relative_path}")
        return file_claims

    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded based on exclusion patterns.

        Args:
            file_path: Path to check against exclusion patterns

        Returns:
            True if file should be excluded, False otherwise
        """
        # Convert to forward slashes for consistent matching across platforms
        normalized_path = str(file_path).replace('\\', '/')

        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, normalized_path):
                return True
        return False

    def extract_from_directory(self, docs_dir: Path) -> List[FormalClaim]:
        """Recursively extract formal claims from all Markdown files in directory.

        Applies exclusion patterns to skip documentation examples and meta-documentation.

        Args:
            docs_dir: Documentation directory to scan

        Returns:
            List of all extracted formal claims
        """
        all_claims = []
        md_files = list(docs_dir.rglob("*.md"))

        # Filter out excluded files
        filtered_files = [f for f in md_files if not self._should_exclude_file(f)]
        excluded_count = len(md_files) - len(filtered_files)

        logger.info(f"Scanning {len(filtered_files)} Markdown files in {docs_dir} ({excluded_count} excluded)")

        for md_file in filtered_files:
            file_claims = self.extract_from_file(md_file)
            all_claims.extend(file_claims)

        self.claims = all_claims
        return all_claims

    def _calculate_confidence(
        self,
        claim_type: str,
        statement: str,
        proof: Optional[str],
        has_citation: bool,
        context: str
    ) -> float:
        """Calculate confidence score for claim requiring citation.

        Confidence scoring algorithm:
        - Base score: 0.6 for formal claim structure
        - +0.2 if theorem/lemma (higher priority than definitions)
        - +0.1 if proof exists (indicates rigorous claim)
        - -0.3 if already has citation (lower priority)
        - +0.1 if mentions author names or specific techniques

        Args:
            claim_type: Type of claim
            statement: Claim statement
            proof: Optional proof block
            has_citation: Whether citation exists
            context: Surrounding context

        Returns:
            Confidence score [0.0, 1.0]
        """
        score = 0.6  # Base score for formal structure

        # Higher priority for theorems/lemmas vs definitions
        if claim_type in ('theorem', 'lemma'):
            score += 0.2
        elif claim_type == 'proposition':
            score += 0.1

        # Proof existence indicates rigorous claim
        if proof:
            score += 0.1

        # Already cited claims have lower research priority
        if has_citation:
            score -= 0.3

        # Check for technical keywords suggesting need for citation
        technical_indicators = [
            'finite-time', 'Lyapunov', 'stability', 'convergence',
            'robust', 'super-twisting', 'chattering', 'reaching condition'
        ]
        combined_text = f"{statement} {context}".lower()
        if any(indicator.lower() in combined_text for indicator in technical_indicators):
            score += 0.1

        return max(0.0, min(1.0, score))  # Clamp to [0, 1]

    def _extract_keywords(self, statement: str, context: str) -> List[str]:
        """Extract suggested keywords for AI research.

        Args:
            statement: Claim statement
            context: Surrounding context

        Returns:
            List of suggested research keywords
        """
        keywords = []
        combined_text = f"{statement} {context}".lower()

        # Check each domain for keyword matches
        for domain, domain_keywords in self.DOMAIN_KEYWORDS.items():
            for keyword in domain_keywords:
                if keyword.lower() in combined_text:
                    keywords.append(keyword)

        # Deduplicate and return unique keywords
        return list(set(keywords))

    def generate_metadata(self) -> Dict[str, Any]:
        """Generate metadata summary of extraction results.

        Returns:
            Metadata dictionary with counts and statistics
        """
        cited_count = sum(1 for c in self.claims if c.has_citation)
        uncited_count = len(self.claims) - cited_count

        by_type = {}
        for claim in self.claims:
            by_type[claim.type] = by_type.get(claim.type, 0) + 1

        return {
            'total_claims': len(self.claims),
            'cited': cited_count,
            'uncited': uncited_count,
            'by_type': by_type,
            'avg_confidence': sum(c.confidence for c in self.claims) / len(self.claims) if self.claims else 0.0
        }

    def export_to_json(self, output_path: Path) -> None:
        """Export claims to JSON file with metadata.

        Args:
            output_path: Path for output JSON file
        """
        metadata = self.generate_metadata()

        output_data = {
            'metadata': metadata,
            'claims': [asdict(claim) for claim in self.claims]
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(self.claims)} claims to {output_path}")
        logger.info(f"Metadata: {metadata}")


def main():
    """Main execution: extract formal claims from docs/ directory."""
    import time
    start_time = time.time()

    # Paths relative to project root
    project_root = Path(__file__).resolve().parents[2]
    docs_dir = project_root / "docs"
    output_path = project_root / "artifacts" / "formal_claims.json"

    extractor = FormalClaimExtractor(project_root)
    claims = extractor.extract_from_directory(docs_dir)

    # Export results
    extractor.export_to_json(output_path)

    elapsed = time.time() - start_time
    logger.info(f"Extraction completed in {elapsed:.2f} seconds")

    # Performance validation
    if elapsed > 2.0:
        logger.warning(f"Performance target missed: {elapsed:.2f}s > 2.0s")
    else:
        logger.info(f"Performance target met: {elapsed:.2f}s < 2.0s")

    return claims


if __name__ == "__main__":
    main()
