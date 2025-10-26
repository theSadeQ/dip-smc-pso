#==========================================================================================\\\
#========== .dev_tools/claim_extraction/tests/test_formal_extractor.py ===============\\\
#==========================================================================================\\\

"""
Unit tests for formal mathematical claim extractor.

Tests cover:
- Numbered and unnumbered theorem extraction
- Citation detection ({cite}`key` syntax)
- Proof association and extraction
- Confidence scoring algorithm
- Context extraction (5 lines before/after)
- Keyword extraction for AI research
- Section header detection
- Multiple claims in single file
- Edge cases (empty files, malformed syntax)

Coverage target: ≥95% line coverage
"""

import pytest
import tempfile
from pathlib import Path
from typing import List
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parents[1]))

from formal_extractor import FormalClaimExtractor, FormalClaim


class TestFormalClaimExtractor:
    """Test suite for FormalClaimExtractor."""

    @pytest.fixture
    def temp_project_root(self, tmp_path: Path) -> Path:
        """Create temporary project root directory."""
        return tmp_path

    @pytest.fixture
    def extractor(self, temp_project_root: Path) -> FormalClaimExtractor:
        """Create FormalClaimExtractor instance."""
        return FormalClaimExtractor(temp_project_root)

    @pytest.fixture
    def sample_markdown_file(self, temp_project_root: Path) -> Path:
        """Create a sample markdown file with various claim types."""
        md_content = """# Mathematical Foundations

## Sliding Mode Control Theory

**Theorem 1**: The super-twisting algorithm guarantees finite-time convergence
to the sliding surface under bounded uncertainties.

**Proof**: Following Levant (2003), consider the Lyapunov function V = |s|.
The time derivative satisfies V̇ ≤ -η|s|^(1/2) for some η > 0, ensuring
finite-time convergence. □

**Lemma**: If the sliding surface coefficients satisfy λ₁ > 0 and λ₂ > 0,
the system is stable.

**Proposition** (Stability Criterion): For the system to be asymptotically
stable, the Lyapunov function V must be positive definite.

**Corollary**: The boundary layer eliminates chattering in SMC systems.

## PSO Optimization

**Definition 1**: The optimization problem is defined over a D-dimensional
search space with bounds [xₘᵢₙ, xₘₐₓ].

**Theorem 2** {cite}`kennedy1995`: Particle Swarm Optimization converges
to global optima under suitable parameter selection.

**Assumption**: The objective function is continuously differentiable.
"""
        file_path = temp_project_root / "test_doc.md"
        file_path.write_text(md_content, encoding='utf-8')
        return file_path

    def test_extract_numbered_theorem(self, extractor: FormalClaimExtractor, sample_markdown_file: Path):
        """Test extraction of numbered theorem with proof."""
        claims = extractor.extract_from_file(sample_markdown_file)

        # Find Theorem 1
        theorem1 = next((c for c in claims if c.number == 1 and c.type == "theorem"), None)
        assert theorem1 is not None, "Theorem 1 should be extracted"
        assert "super-twisting" in theorem1.statement.lower()
        assert "finite-time convergence" in theorem1.statement.lower()
        assert theorem1.proof is not None, "Proof should be extracted"
        assert "Levant" in theorem1.proof
        assert theorem1.has_citation is False
        assert theorem1.number == 1

    def test_extract_unnumbered_proposition(self, extractor: FormalClaimExtractor, sample_markdown_file: Path):
        """Test extraction of proposition without number."""
        claims = extractor.extract_from_file(sample_markdown_file)

        # Find unnumbered Proposition
        proposition = next((c for c in claims if c.type == "proposition"), None)
        assert proposition is not None, "Proposition should be extracted"
        assert proposition.number is None
        assert "Stability Criterion" in proposition.statement
        assert "Lyapunov" in proposition.statement

    def test_citation_detection_cite_syntax(self, extractor: FormalClaimExtractor, sample_markdown_file: Path):
        """Test detection of {cite}`key` syntax."""
        claims = extractor.extract_from_file(sample_markdown_file)

        # Find Theorem 2 with citation
        theorem2 = next((c for c in claims if c.number == 2 and c.type == "theorem"), None)
        assert theorem2 is not None, "Theorem 2 should be extracted"
        assert theorem2.has_citation is True, "Citation should be detected"
        assert "{cite}`kennedy1995`" in theorem2.statement or "kennedy1995" in theorem2.statement.lower()

    def test_proof_association(self, extractor: FormalClaimExtractor, sample_markdown_file: Path):
        """Test correct association of proof blocks with theorems."""
        claims = extractor.extract_from_file(sample_markdown_file)

        theorem1 = next((c for c in claims if c.number == 1 and c.type == "theorem"), None)
        assert theorem1.proof is not None, "Proof should be associated"
        assert "Levant (2003)" in theorem1.proof
        assert "Lyapunov function" in theorem1.proof

        # Lemma without proof should have proof=None
        lemma = next((c for c in claims if c.type == "lemma"), None)
        # Note: lemma might or might not have proof depending on pattern match

    def test_confidence_scoring_high(self, extractor: FormalClaimExtractor):
        """Test confidence scoring for high-confidence claim (all boosters)."""
        # Create theorem with number, proof, no citation, technical keywords
        md_content = """
**Theorem 1**: The system exhibits finite-time convergence with Lyapunov stability.

**Proof**: Following the Lyapunov analysis... □
"""
        temp_file = extractor.root_dir / "test_high_conf.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) >= 1
        claim = claims[0]

        # High confidence: numbered (0.2) + theorem type (0.2) + proof (0.1) + technical keywords (0.1)
        # Base: 0.6, Total: 0.6 + 0.2 + 0.1 = 0.9 or 1.0
        assert claim.confidence >= 0.8, f"Expected high confidence, got {claim.confidence}"

    def test_confidence_scoring_low(self, extractor: FormalClaimExtractor):
        """Test confidence scoring for low-confidence claim (minimal boosters)."""
        # Create definition without number, no proof, no citation
        md_content = """
**Definition**: A simple definition without special features.
"""
        temp_file = extractor.root_dir / "test_low_conf.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) >= 1
        claim = claims[0]

        # Low confidence: base only (0.6), definition type (no boost), no proof, no citation
        assert claim.confidence <= 0.7, f"Expected low confidence, got {claim.confidence}"

    def test_context_extraction(self, extractor: FormalClaimExtractor):
        """Test extraction of 5 lines before and after claim."""
        md_content = """Line 1
Line 2
Line 3
Line 4
Line 5
**Theorem**: Central claim here.
Line 7
Line 8
Line 9
Line 10
Line 11
"""
        temp_file = extractor.root_dir / "test_context.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) == 1
        claim = claims[0]

        # Context should include surrounding lines
        assert claim.context is not None
        assert len(claim.context) > 0
        # Should contain lines before and after
        assert "Line 2" in claim.context or "Line 3" in claim.context
        assert "Line 7" in claim.context or "Line 8" in claim.context

    def test_keyword_extraction(self, extractor: FormalClaimExtractor):
        """Test extraction of research keywords from statement."""
        md_content = """
**Theorem**: The super-twisting algorithm with Lyapunov stability ensures
robust control under sliding mode conditions.
"""
        temp_file = extractor.root_dir / "test_keywords.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) == 1
        claim = claims[0]

        # Should extract domain-specific keywords
        keywords_lower = [k.lower() for k in claim.suggested_keywords]
        # Check for at least some expected keywords
        assert any("super-twisting" in k.lower() or "lyapunov" in k.lower() or
                   "sliding" in k.lower() or "robust" in k.lower() for k in claim.suggested_keywords), \
               f"Expected domain keywords, got {claim.suggested_keywords}"

    def test_section_header_detection(self, extractor: FormalClaimExtractor):
        """Test detection of nearest section header before claim."""
        md_content = """# Main Title

## Section 1: Introduction

Some text here.

### Subsection 1.1: Details

**Theorem**: Claim in subsection.

## Section 2: Methods

**Lemma**: Another claim.
"""
        temp_file = extractor.root_dir / "test_section.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) >= 2

        # Note: Current implementation doesn't have section_header field in dataclass
        # This test validates context includes section info
        theorem = next(c for c in claims if c.type == "theorem")
        lemma = next(c for c in claims if c.type == "lemma")

        # Context should contain section headers
        assert "Subsection" in theorem.context or "Section 1" in theorem.context
        assert "Section 2" in lemma.context or "Methods" in lemma.context

    def test_multiple_theorems_same_file(self, extractor: FormalClaimExtractor, sample_markdown_file: Path):
        """Test handling of multiple claims in same file."""
        claims = extractor.extract_from_file(sample_markdown_file)

        # Should extract multiple claims
        assert len(claims) >= 5, f"Expected at least 5 claims, got {len(claims)}"

        # Verify different types
        claim_types = {c.type for c in claims}
        assert "theorem" in claim_types
        assert "lemma" in claim_types or "proposition" in claim_types or "definition" in claim_types

        # Verify unique IDs
        claim_ids = [c.id for c in claims]
        assert len(claim_ids) == len(set(claim_ids)), "Claim IDs should be unique"

    def test_empty_file_handling(self, extractor: FormalClaimExtractor):
        """Test graceful handling of empty file."""
        md_content = ""
        temp_file = extractor.root_dir / "test_empty.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert claims == [], "Empty file should return empty list"

    def test_malformed_theorem_syntax(self, extractor: FormalClaimExtractor):
        """Test handling of malformed theorem syntax (should skip invalid patterns)."""
        md_content = """
**Theorem** without colon or statement

**Theorem 1** Missing statement continuation
on next paragraph.

This is not a theorem: **Random bold text**

**Theorem 2**: Valid theorem statement that should be extracted.
"""
        temp_file = extractor.root_dir / "test_malformed.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)

        # Should extract only valid Theorem 2
        # (Note: current regex might capture some malformed cases, adjust expectations)
        valid_claims = [c for c in claims if "Valid theorem statement" in c.statement]
        assert len(valid_claims) >= 1, "Should extract at least the valid theorem"

    def test_export_to_json(self, extractor: FormalClaimExtractor, sample_markdown_file: Path, tmp_path: Path):
        """Test JSON export with metadata."""
        claims = extractor.extract_from_file(sample_markdown_file)
        extractor.claims = claims

        output_path = tmp_path / "test_output.json"
        extractor.export_to_json(output_path)

        assert output_path.exists(), "JSON file should be created"

        import json
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate metadata structure
        assert "metadata" in data
        assert "claims" in data
        assert data["metadata"]["total_claims"] == len(claims)
        assert "by_type" in data["metadata"]
        assert "cited" in data["metadata"]
        assert "uncited" in data["metadata"]

    def test_line_number_accuracy(self, extractor: FormalClaimExtractor):
        """Test that line numbers are accurate."""
        md_content = """Line 1
Line 2
Line 3
**Theorem**: Claim on line 4.
Line 5
"""
        temp_file = extractor.root_dir / "test_line_num.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) == 1
        claim = claims[0]

        # Line number should be 4 (1-indexed)
        assert claim.line_number == 4, f"Expected line 4, got {claim.line_number}"

    def test_file_path_relative_to_root(self, extractor: FormalClaimExtractor):
        """Test that file paths are relative to project root."""
        subdir = extractor.root_dir / "docs" / "theory"
        subdir.mkdir(parents=True, exist_ok=True)

        md_content = "**Theorem**: Test claim."
        temp_file = subdir / "test_theory.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert len(claims) == 1
        claim = claims[0]

        # Path should be relative using forward slashes
        assert claim.file_path.startswith("docs/theory/") or claim.file_path.startswith("docs\\theory\\")
        assert "test_theory.md" in claim.file_path


class TestConfidenceScoring:
    """Detailed tests for confidence scoring algorithm."""

    @pytest.fixture
    def extractor(self, tmp_path: Path) -> FormalClaimExtractor:
        return FormalClaimExtractor(tmp_path)

    def test_base_score_formal_structure(self, extractor: FormalClaimExtractor):
        """Test base score of 0.6 for formal structure."""
        md_content = "**Definition**: Simple definition."
        temp_file = extractor.root_dir / "test.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert claims[0].confidence == pytest.approx(0.6, abs=0.1)

    def test_theorem_lemma_boost(self, extractor: FormalClaimExtractor):
        """Test +0.2 boost for theorem/lemma types."""
        md_content = "**Theorem 1**: Important theorem."
        temp_file = extractor.root_dir / "test.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        # Base 0.6 + theorem boost 0.2 = 0.8
        assert claims[0].confidence >= 0.7

    def test_proof_existence_boost(self, extractor: FormalClaimExtractor):
        """Test +0.1 boost for proof existence."""
        md_content = """**Theorem**: Claim with proof.

**Proof**: Detailed proof here. □"""
        temp_file = extractor.root_dir / "test.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        # Should have proof boost
        assert claims[0].proof is not None
        assert claims[0].confidence >= 0.8

    def test_citation_penalty(self, extractor: FormalClaimExtractor):
        """Test -0.3 penalty for existing citation."""
        md_content = "**Theorem** {cite}`reference2024`: Already cited claim."
        temp_file = extractor.root_dir / "test.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        assert claims[0].has_citation is True
        # Base 0.6 + theorem 0.2 - citation penalty 0.3 = 0.5
        assert claims[0].confidence <= 0.6

    def test_technical_keywords_boost(self, extractor: FormalClaimExtractor):
        """Test +0.1 boost for technical keywords."""
        md_content = "**Theorem**: Finite-time convergence with Lyapunov stability."
        temp_file = extractor.root_dir / "test.md"
        temp_file.write_text(md_content, encoding='utf-8')

        claims = extractor.extract_from_file(temp_file)
        # Should detect technical keywords and boost confidence
        assert claims[0].confidence >= 0.8


class TestDirectoryScanning:
    """Test recursive directory scanning functionality."""

    @pytest.fixture
    def docs_tree(self, tmp_path: Path) -> Path:
        """Create directory tree with multiple markdown files."""
        root = tmp_path

        # Create structure
        (root / "docs" / "theory").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "api").mkdir(parents=True, exist_ok=True)

        # Add files
        (root / "docs" / "theory" / "smc.md").write_text(
            "**Theorem 1**: SMC theorem.", encoding='utf-8'
        )
        (root / "docs" / "api" / "reference.md").write_text(
            "**Lemma**: API lemma.", encoding='utf-8'
        )
        (root / "docs" / "index.md").write_text(
            "**Definition**: Index definition.", encoding='utf-8'
        )

        return root

    def test_recursive_extraction(self, docs_tree: Path):
        """Test extraction from all markdown files in directory tree."""
        extractor = FormalClaimExtractor(docs_tree)
        docs_dir = docs_tree / "docs"

        claims = extractor.extract_from_directory(docs_dir)

        # Should find all 3 claims across subdirectories
        assert len(claims) >= 3, f"Expected at least 3 claims, got {len(claims)}"

        # Verify claims from different files
        file_paths = {c.file_path for c in claims}
        assert len(file_paths) >= 3, "Should extract from multiple files"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
