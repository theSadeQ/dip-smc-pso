#==========================================================================================\\\
#================== .dev_tools/claim_extraction/code_extractor.py ======================\\\
#==========================================================================================\\\

"""Code claim extractor for implementation claims in Python source code.

Extracts implementation claims from docstrings using AST parsing, detects various
citation formats, and tracks scope hierarchy for accurate attribution.

Performance target: ≥66 files/sec (165 files in ≤2.5s)
"""

import ast
import re
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from collections import Counter


@dataclass
class CodeClaim:
    """Represents an implementation claim extracted from source code.

    Attributes:
        id: Unique identifier (e.g., "CODE-IMPL-001")
        type: Claim type (always "implementation")
        scope: Hierarchical scope (e.g., "module:class:Foo:function:bar")
        claim_text: Full claim text from docstring
        algorithm_name: Extracted algorithm/technique name
        source_attribution: Source reference if mentioned
        file_path: Source file path
        line_number: Line number where claim appears
        has_citation: Whether claim includes proper citation
        citation_format: Citation format type (numbered, doi, author_year, null)
        confidence: Confidence score (0.6-0.8)
    """
    id: str
    type: str
    scope: str
    claim_text: str
    algorithm_name: Optional[str]
    source_attribution: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    citation_format: Optional[str]
    confidence: float


class CodeClaimExtractor(ast.NodeVisitor):
    """Extract implementation claims from Python source code using AST parsing.

    Visits module, class, and function definitions to extract implementation
    claims from docstrings. Tracks scope hierarchy and detects multiple
    citation formats.
    """

    # Implementation claim patterns (EXPANDED - Phase 1 Fix)
    # Now detects 7 common attribution patterns instead of just 3
    IMPLEMENTS_PATTERN = re.compile(
        r'(?:Implements?|Implementation of|Based on|Following|According to|'
        r'Adapted from|Derived from|Uses?|Employs?)\s+'
        r'(?P<what>[^,\.]+?)\s+'
        r'(?:from|in|by|of)\s+'
        r'(?P<source>[^\.\n]+)',
        re.IGNORECASE
    )

    # Citation format patterns
    # CRITICAL FIX: Added bracket citation pattern 【...】 used throughout codebase
    BRACKET_CITATION = re.compile(r'【([^】]+)】')  # Special format: 66 occurrences in code!
    NUMBERED_CITATION = re.compile(r'\[(\d+)\]')
    DOI_CITATION = re.compile(r'doi:([^\s]+)', re.IGNORECASE)
    AUTHOR_YEAR_CITATION = re.compile(r'\(([A-Z][a-z]+ et al\.\s+\d{4})\)')
    CITE_BACKTICK = re.compile(r'\{cite\}`([^`]+)`')  # MyST markdown {cite}`key` format

    # Phase 2: Algorithm/technique keywords for comprehensive extraction
    ALGORITHM_KEYWORDS = [
        'algorithm', 'method', 'approach', 'technique', 'implements', 'implementation',
        'based on', 'following', 'according to', 'adapted from', 'derived from',
        'uses', 'employs', 'applies', 'utilizes', 'procedure', 'strategy'
    ]

    def __init__(self, src_dir: Path):
        """Initialize extractor with source code directory.

        Args:
            src_dir: Root directory containing Python source files
        """
        self.src_dir = Path(src_dir)
        self.claims: List[CodeClaim] = []
        self._claim_counter = 0
        self._scope_stack: List[str] = []
        self._current_file: Optional[Path] = None

    def extract_from_directory(self, src_dir: Optional[Path] = None) -> List[CodeClaim]:
        """Extract all code claims from source directory.

        Args:
            src_dir: Source directory to scan (uses self.src_dir if None)

        Returns:
            List of CodeClaim objects sorted by file path and line number
        """
        if src_dir is None:
            src_dir = self.src_dir

        py_files = sorted(src_dir.rglob('*.py'))
        all_claims: List[CodeClaim] = []

        for py_file in py_files:
            # Skip test files and __pycache__
            if '__pycache__' in str(py_file) or 'test_' in py_file.name:
                continue

            file_claims = self._extract_from_file(py_file)
            all_claims.extend(file_claims)

        self.claims = all_claims
        return all_claims

    def _extract_from_file(self, file_path: Path) -> List[CodeClaim]:
        """Extract claims from a single Python file.

        Args:
            file_path: Path to Python source file

        Returns:
            List of CodeClaim objects found in the file
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
        except (IOError, SyntaxError, UnicodeDecodeError):
            return []

        self._current_file = file_path
        self._scope_stack = ['module']
        file_claims: List[CodeClaim] = []

        # Visit AST nodes
        self.visit(tree)

        # Collect claims from this file
        file_claims = [c for c in self.claims if c.file_path == str(file_path.relative_to(self.src_dir.parent))]

        return file_claims

    def visit_Module(self, node: ast.Module) -> None:
        """Visit module node and extract module-level docstring claims.

        Args:
            node: AST Module node
        """
        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_from_docstring(docstring, scope='module', line_number=1)

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition and extract class docstring claims.

        Args:
            node: AST ClassDef node
        """
        # Push class onto scope stack
        self._scope_stack.append(f'class:{node.name}')

        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_from_docstring(
                docstring,
                scope=':'.join(self._scope_stack),
                line_number=node.lineno
            )

        # Visit class body
        self.generic_visit(node)

        # Pop class from scope stack
        self._scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function/method definition and extract docstring claims.

        Args:
            node: AST FunctionDef node
        """
        # Push function onto scope stack
        self._scope_stack.append(f'function:{node.name}')

        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_from_docstring(
                docstring,
                scope=':'.join(self._scope_stack),
                line_number=node.lineno
            )

        # Visit function body
        self.generic_visit(node)

        # Pop function from scope stack
        self._scope_stack.pop()

    def _extract_from_docstring(self, docstring: str, scope: str, line_number: int) -> None:
        """Extract implementation claims from docstring text.

        UPDATED (Phase 2): Now extracts from ALL docstrings with citations OR keywords,
        not just those matching IMPLEMENTS_PATTERN.

        Args:
            docstring: Docstring text to parse
            scope: Current scope hierarchy
            line_number: Line number of docstring
        """
        # Phase 1: Extract structured claims via IMPLEMENTS_PATTERN (preferred)
        pattern_matches = list(self.IMPLEMENTS_PATTERN.finditer(docstring))

        for match in pattern_matches:
            self._claim_counter += 1

            algorithm_name = match.group('what').strip()
            source_attribution = match.group('source').strip()
            claim_text = match.group(0)

            # Detect citation format
            has_citation = self._has_proper_citation(docstring)
            citation_format = self._detect_citation_format(docstring)

            # Calculate confidence
            confidence = 0.8 if has_citation else 0.6

            # Generate ID
            claim_id = f"CODE-IMPL-{self._claim_counter:03d}"

            claim = CodeClaim(
                id=claim_id,
                type='implementation',
                scope=scope,
                claim_text=claim_text,
                algorithm_name=algorithm_name,
                source_attribution=source_attribution,
                file_path=str(self._current_file.relative_to(self.src_dir.parent)),
                line_number=line_number,
                has_citation=has_citation,
                citation_format=citation_format,
                confidence=confidence
            )

            self.claims.append(claim)

        # Phase 2: Extract from docstrings with citations OR keywords (no pattern match)
        # Skip if already extracted via pattern (avoid duplicates)
        if not pattern_matches:
            has_citation = self._has_proper_citation(docstring)
            has_keywords = self._has_algorithm_keywords(docstring)

            if has_citation or has_keywords:
                self._claim_counter += 1

                # Extract first meaningful sentence as claim text
                claim_text = self._extract_claim_text(docstring)

                # Try to extract algorithm name and source from citation context
                algorithm_name, source_attribution = self._extract_algorithm_and_source(docstring)

                citation_format = self._detect_citation_format(docstring)

                # Confidence based on citation presence and keyword strength
                if has_citation:
                    confidence = 0.75  # Has citation but no clear pattern
                elif has_keywords:
                    confidence = 0.65  # Has keywords only
                else:
                    confidence = 0.6   # Fallback

                claim_id = f"CODE-IMPL-{self._claim_counter:03d}"

                claim = CodeClaim(
                    id=claim_id,
                    type='implementation',
                    scope=scope,
                    claim_text=claim_text,
                    algorithm_name=algorithm_name,
                    source_attribution=source_attribution,
                    file_path=str(self._current_file.relative_to(self.src_dir.parent)),
                    line_number=line_number,
                    has_citation=has_citation,
                    citation_format=citation_format,
                    confidence=confidence
                )

                self.claims.append(claim)

    def _has_proper_citation(self, docstring: str) -> bool:
        """Check if docstring contains a proper citation.

        UPDATED (Phase 1): Now checks 5 citation formats including bracket citations.

        Args:
            docstring: Docstring text to check

        Returns:
            True if proper citation detected, False otherwise
        """
        return bool(
            self.BRACKET_CITATION.search(docstring) or
            self.CITE_BACKTICK.search(docstring) or
            self.NUMBERED_CITATION.search(docstring) or
            self.DOI_CITATION.search(docstring) or
            self.AUTHOR_YEAR_CITATION.search(docstring)
        )

    def _detect_citation_format(self, docstring: str) -> Optional[str]:
        """Detect the format of citation used in docstring.

        UPDATED (Phase 1): Now detects 5 citation formats including bracket citations.

        Args:
            docstring: Docstring text to analyze

        Returns:
            Citation format: 'bracket', 'cite_backtick', 'numbered', 'doi', 'author_year', or None
        """
        # Priority order: Check most specific formats first
        if self.BRACKET_CITATION.search(docstring):
            return 'bracket'  # 【...】 format (66 occurrences in codebase!)
        elif self.CITE_BACKTICK.search(docstring):
            return 'cite_backtick'  # {cite}`key` MyST format
        elif self.NUMBERED_CITATION.search(docstring):
            return 'numbered'  # [1] format
        elif self.DOI_CITATION.search(docstring):
            return 'doi'  # doi:10.xxxx format
        elif self.AUTHOR_YEAR_CITATION.search(docstring):
            return 'author_year'  # (Author et al. YYYY) format
        return None

    def _has_algorithm_keywords(self, docstring: str) -> bool:
        """Check if docstring contains algorithm/technique keywords.

        NEW (Phase 2): Enables extraction from docstrings without explicit pattern match.

        Args:
            docstring: Docstring text to check

        Returns:
            True if algorithm keywords detected, False otherwise
        """
        docstring_lower = docstring.lower()
        return any(keyword in docstring_lower for keyword in self.ALGORITHM_KEYWORDS)

    def _extract_claim_text(self, docstring: str) -> str:
        """Extract first meaningful sentence as claim text from docstring.

        NEW (Phase 2): Extracts claim text when no pattern match exists.

        Args:
            docstring: Docstring text

        Returns:
            First meaningful sentence (up to 200 chars)
        """
        # Remove leading/trailing whitespace and normalize
        text = docstring.strip()

        # Extract first sentence (up to first period or newline)
        sentences = re.split(r'[.\n]', text)
        for sentence in sentences:
            sentence = sentence.strip()
            # Skip empty or very short sentences (likely not meaningful)
            if len(sentence) > 20:
                # Limit to 200 chars for readability
                return sentence[:200] if len(sentence) > 200 else sentence

        # Fallback: return first 200 chars of docstring
        return text[:200]

    def _extract_algorithm_and_source(self, docstring: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract algorithm name and source attribution from citation context.

        NEW (Phase 2): Best-effort extraction when no pattern match exists.

        Args:
            docstring: Docstring text

        Returns:
            Tuple of (algorithm_name, source_attribution)
        """
        algorithm_name = None
        source_attribution = None

        # Try to extract from citation context
        # Pattern: "... <algorithm> ... 【source】" or "{cite}`source`"
        bracket_match = self.BRACKET_CITATION.search(docstring)
        cite_match = self.CITE_BACKTICK.search(docstring)

        if bracket_match:
            source_attribution = bracket_match.group(1).strip()
            # Try to find algorithm name before citation
            text_before = docstring[:bracket_match.start()].strip()
            words = text_before.split()
            if len(words) >= 3:
                # Take last 3 words before citation as potential algorithm name
                algorithm_name = ' '.join(words[-3:])

        elif cite_match:
            source_attribution = cite_match.group(1).strip()
            text_before = docstring[:cite_match.start()].strip()
            words = text_before.split()
            if len(words) >= 3:
                algorithm_name = ' '.join(words[-3:])

        # Fallback: extract from keyword context
        if not algorithm_name:
            for keyword in ['algorithm', 'method', 'approach', 'technique']:
                pattern = re.compile(rf'{keyword}\s+(\w+(?:\s+\w+){{0,2}})', re.IGNORECASE)
                match = pattern.search(docstring)
                if match:
                    algorithm_name = match.group(1).strip()
                    break

        return algorithm_name, source_attribution

    def save_to_json(self, claims: List[CodeClaim], output_path: Path) -> None:
        """Save extracted claims to JSON file with metadata.

        Args:
            claims: List of CodeClaim objects
            output_path: Output JSON file path
        """
        # Calculate metadata
        cited = sum(1 for c in claims if c.has_citation)
        format_counts = Counter(
            c.citation_format if c.citation_format else 'null'
            for c in claims
        )
        scope_counts = Counter(c.scope.split(':')[0] for c in claims)

        output = {
            "metadata": {
                "total_claims": len(claims),
                "cited": cited,
                "by_format": dict(format_counts),
                "by_scope": dict(scope_counts)
            },
            "claims": [asdict(c) for c in claims]
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2), encoding='utf-8')


def extract_from_directory(src_dir: Path) -> List[CodeClaim]:
    """Convenience function to extract claims from directory.

    Args:
        src_dir: Source directory to scan

    Returns:
        List of extracted CodeClaim objects
    """
    extractor = CodeClaimExtractor(src_dir)
    return extractor.extract_from_directory()


def main() -> None:
    """CLI entry point for code claim extraction."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract implementation claims from Python source code'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('src'),
        help='Input source directory (default: src)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('artifacts/code_claims.json'),
        help='Output JSON file (default: artifacts/code_claims.json)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Extract claims
    extractor = CodeClaimExtractor(args.input)

    if args.verbose:
        print(f"Scanning {args.input} for implementation claims...")

    import time
    start = time.time()
    claims = extractor.extract_from_directory()
    elapsed = time.time() - start

    # Save results
    args.output.parent.mkdir(parents=True, exist_ok=True)
    extractor.save_to_json(claims, args.output)

    # Report results
    if args.verbose:
        print(f"\nExtracted {len(claims)} claims in {elapsed:.2f}s")
        py_files = len(list(args.input.rglob('*.py')))
        print(f"Performance: {py_files/elapsed:.1f} files/sec")
        print(f"Output saved to: {args.output}")

        cited = sum(1 for c in claims if c.has_citation)
        print(f"\nCitation coverage: {cited}/{len(claims)} ({100*cited/len(claims):.1f}%)" if claims else "\nNo claims found")


if __name__ == '__main__':
    main()
