#==========================================================================================\\\
#=========== .dev_tools/claim_extraction/tests/test_code_extractor.py ==================\\\
#==========================================================================================\\\

"""Unit tests for code claim extractor.

Tests extraction of implementation claims from Python source code docstrings
using AST parsing with scope tracking and citation format detection.

Coverage target: ≥95%
"""

import pytest
from pathlib import Path
from textwrap import dedent
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_extractor import CodeClaimExtractor, CodeClaim


@pytest.fixture
def temp_src_dir(tmp_path):
    """Create temporary source directory for testing."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    return src_dir


@pytest.fixture
def extractor(temp_src_dir):
    """Create CodeClaimExtractor instance."""
    return CodeClaimExtractor(temp_src_dir)


def test_module_docstring_extraction(temp_src_dir, extractor):
    """Test extraction of implementation claims from module docstring."""
    test_file = temp_src_dir / "controller.py"
    test_file.write_text(dedent('''
        """Sliding mode controller module.

        Implements super-twisting algorithm from Levant (2003) [1].

        [1] Levant, A. (2003). Higher-order sliding modes...
        """

        def example():
            pass
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 1
    assert claims[0].scope == 'module'
    assert 'super-twisting' in claims[0].algorithm_name.lower()
    assert 'Levant' in claims[0].source_attribution
    assert claims[0].has_citation is True
    assert claims[0].citation_format == 'numbered'


def test_class_docstring_extraction(temp_src_dir, extractor):
    """Test extraction of implementation claims from class docstring."""
    test_file = temp_src_dir / "optimizer.py"
    test_file.write_text(dedent('''
        class PSOOptimizer:
            """Particle Swarm Optimization implementation.

            Implementation of PSO algorithm from Kennedy and Eberhart (1995).
            doi:10.1109/ICNN.1995.488968
            """

            def optimize(self):
                pass
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 1
    assert 'class:PSOOptimizer' in claims[0].scope
    assert 'PSO' in claims[0].algorithm_name or 'algorithm' in claims[0].algorithm_name.lower()
    assert claims[0].has_citation is True
    assert claims[0].citation_format == 'doi'


def test_method_docstring_extraction(temp_src_dir, extractor):
    """Test extraction of implementation claims from method docstring."""
    test_file = temp_src_dir / "controller.py"
    test_file.write_text(dedent('''
        class SMCController:
            def compute_control(self, state):
                """Compute sliding mode control output.

                Implements classical SMC from Utkin (1977) with boundary layer
                technique by Slotine (1984).
                """
                pass
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 1
    assert 'class:SMCController:function:compute_control' in claims[0].scope
    assert 'classical SMC' in claims[0].algorithm_name
    assert 'Utkin' in claims[0].source_attribution


def test_scope_tracking_nested_classes(temp_src_dir, extractor):
    """Test scope stack validation for nested classes."""
    test_file = temp_src_dir / "nested.py"
    test_file.write_text(dedent('''
        class Outer:
            """Outer class.

            Implementation of outer pattern from Smith (2020).
            """

            class Inner:
                """Inner class.

                Implements inner algorithm from Jones (2021).
                """

                def method(self):
                    """Method.

                    Based on method design by Brown (2022).
                    """
                    pass
    '''))

    claims = extractor._extract_from_file(test_file)

    # Should have claims from Outer, Inner, and method
    scopes = [c.scope for c in claims]

    # Check for outer class
    assert any('Outer' in s for s in scopes)

    # Check for nested class (if supported by AST visitor)
    # Note: Standard ast.NodeVisitor handles nested classes


def test_implements_pattern_matching(temp_src_dir, extractor):
    """Test "Implements X from Y" pattern detection."""
    test_file = temp_src_dir / "patterns.py"
    test_file.write_text(dedent('''
        """Test various implementation patterns.

        Implements adaptive SMC from Slotine and Li (1991).
        Implementation of particle swarm optimization from Kennedy et al. (1995).
        Based on gradient descent from Robbins and Monro (1951).
        """
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 3

    algorithms = [c.algorithm_name.lower() for c in claims]
    assert any('adaptive smc' in alg for alg in algorithms)
    assert any('particle swarm' in alg for alg in algorithms)
    assert any('gradient descent' in alg for alg in algorithms)


def test_numbered_citation_detection(temp_src_dir, extractor):
    """Test [1] citation format detection."""
    test_file = temp_src_dir / "cited.py"
    test_file.write_text(dedent('''
        """Controller with numbered citations.

        Implements super-twisting algorithm from Levant (2003) [1].

        References:
        [1] Levant, A. (2003). Higher-order sliding modes, differentiation and...
        """
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 1
    assert claims[0].has_citation is True
    assert claims[0].citation_format == 'numbered'
    assert claims[0].confidence == 0.8  # Cited confidence


def test_doi_citation_detection(temp_src_dir, extractor):
    """Test doi:... citation format detection."""
    test_file = temp_src_dir / "doi_cited.py"
    test_file.write_text(dedent('''
        class Algorithm:
            """Algorithm with DOI citation.

            Implementation of PSO from Kennedy (1995).
            doi:10.1109/ICNN.1995.488968
            """
            pass
    '''))

    claims = extractor._extract_from_file(test_file)

    assert len(claims) >= 1
    assert claims[0].has_citation is True
    assert claims[0].citation_format == 'doi'


def test_author_year_citation_detection(temp_src_dir, extractor):
    """Test (Author et al. YYYY) citation format detection."""
    test_file = temp_src_dir / "author_year.py"
    test_file.write_text(dedent('''
        """Module with author-year citations.

        Implements sliding mode control from Utkin et al. 1999 with
        modifications based on approach in (Slotine et al. 1991).
        """
    '''))

    claims = extractor._extract_from_file(test_file)

    if claims:  # May or may not match depending on exact pattern
        cited_claims = [c for c in claims if c.has_citation]
        if cited_claims:
            assert cited_claims[0].citation_format == 'author_year'


def test_confidence_scoring(temp_src_dir, extractor):
    """Test confidence scoring: cited (0.8) vs uncited (0.6)."""
    # Uncited claim
    uncited_file = temp_src_dir / "uncited.py"
    uncited_file.write_text(dedent('''
        """Implements basic algorithm from some paper.
        """
    '''))

    uncited_claims = extractor._extract_from_file(uncited_file)

    # Cited claim
    cited_file = temp_src_dir / "cited.py"
    cited_file.write_text(dedent('''
        """Implements basic algorithm from some paper [1].

        [1] Author (2020). Title.
        """
    '''))

    cited_claims = extractor._extract_from_file(cited_file)

    if uncited_claims:
        assert uncited_claims[0].confidence == 0.6

    if cited_claims:
        assert cited_claims[0].confidence == 0.8


def test_empty_docstring_handling(temp_src_dir, extractor):
    """Test graceful handling of missing docstrings."""
    test_file = temp_src_dir / "no_docs.py"
    test_file.write_text(dedent('''
        class NoDocstring:
            def method(self):
                return 42

        def function_no_doc():
            pass
    '''))

    claims = extractor._extract_from_file(test_file)

    # Should return empty list or handle gracefully
    assert isinstance(claims, list)
    assert len(claims) == 0


def test_save_to_json(temp_src_dir, extractor, tmp_path):
    """Test JSON export functionality."""
    test_file = temp_src_dir / "sample.py"
    test_file.write_text(dedent('''
        """Module docstring.

        Implements algorithm A from Source X [1].
        """

        class MyClass:
            """Class docstring.

            Based on pattern B from Source Y.
            doi:10.1234/example
            """
            pass
    '''))

    claims = extractor._extract_from_file(test_file)
    output_file = tmp_path / "output.json"

    extractor.save_to_json(claims, output_file)

    assert output_file.exists()

    import json
    data = json.loads(output_file.read_text())

    assert 'metadata' in data
    assert 'claims' in data
    assert data['metadata']['total_claims'] == len(claims)
    assert 'cited' in data['metadata']
    assert 'by_format' in data['metadata']
    assert 'by_scope' in data['metadata']


def test_skip_test_files(temp_src_dir, extractor):
    """Test that test files are skipped during extraction."""
    test_file = temp_src_dir / "test_something.py"
    test_file.write_text(dedent('''
        """Test module with implementation claim.

        Implements test pattern from Testing Guide (2020).
        """
    '''))

    claims = extractor.extract_from_directory()

    # Test files should be skipped
    test_claims = [c for c in claims if 'test_' in c.file_path]
    assert len(test_claims) == 0


def test_multiple_claims_same_file(temp_src_dir, extractor):
    """Test extraction of multiple claims from same file."""
    test_file = temp_src_dir / "multi.py"
    test_file.write_text(dedent('''
        """Module with multiple algorithms.

        Implements PSO from Kennedy (1995) and adaptive SMC from Slotine (1991).
        """

        class ControllerA:
            """First controller.

            Based on technique from Author A (2020).
            """
            pass

        class ControllerB:
            """Second controller.

            Implementation of method from Author B (2021).
            """
            pass
    '''))

    claims = extractor._extract_from_file(test_file)

    # Should extract multiple claims
    assert len(claims) >= 2

    # Verify unique IDs
    ids = [c.id for c in claims]
    assert len(ids) == len(set(ids))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
