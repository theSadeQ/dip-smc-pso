#!/usr/bin/env python3
#======================================================================================\\\
#======================== .dev_tools/citation_validator.py ============================\\\
#======================================================================================\\\

"""
Citation Validation for DIP-SMC-PSO Project.

This module validates that discovered citations meet all requirements
for the apply_chatgpt_citations.py script, ensuring:
- Complete fields for each category
- Valid DOI/ISBN formats
- Algorithm/concept name matching
- Proper reference types
"""

from typing import Dict, List, Tuple
import re


class ValidationError:
    """Represents a validation error."""

    def __init__(self, claim_id: str, field: str, message: str, severity: str = "ERROR"):
        self.claim_id = claim_id
        self.field = field
        self.message = message
        self.severity = severity  # ERROR, WARNING, INFO

    def __repr__(self):
        return f"{self.severity}: {self.claim_id} - {self.field}: {self.message}"


class CitationValidator:
    """Validates citations against apply_chatgpt_citations.py requirements."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def validate_complete_output(self, claims: List[Dict]) -> Tuple[bool, List[ValidationError]]:
        """
        Validate complete ChatGPT output for all claims.

        Args:
            claims: List of claim dicts with citations

        Returns:
            Tuple of (is_valid, errors_list)
        """
        self.errors = []
        self.warnings = []

        # Check basic structure
        if not isinstance(claims, list):
            self.errors.append(ValidationError("STRUCTURE", "root", "Output must be JSON array"))
            return False, self.errors

        if len(claims) != 108:
            self.errors.append(
                ValidationError("STRUCTURE", "length", f"Expected 108 claims, got {len(claims)}")
            )

        # Validate each claim
        for claim in claims:
            self.validate_claim(claim)

        # Report summary
        has_errors = len(self.errors) > 0
        all_issues = self.errors + self.warnings

        return not has_errors, all_issues

    def validate_claim(self, claim: Dict) -> None:
        """
        Validate a single claim.

        Args:
            claim: Claim dict to validate
        """
        claim_id = claim.get('claim_id', 'UNKNOWN')

        # Required fields for all claims
        required_base_fields = ['claim_id', 'category', 'confidence', 'rationale', 'code_summary']

        for field in required_base_fields:
            if field not in claim or not claim[field]:
                self.errors.append(
                    ValidationError(claim_id, field, f"Missing required field '{field}'")
                )

        # Category-specific validation
        category = claim.get('category')

        if category not in ['A', 'B', 'C']:
            self.errors.append(
                ValidationError(claim_id, 'category', f"Invalid category '{category}' (must be A, B, or C)")
            )
            return

        if category == 'A':
            self.validate_category_a(claim)
        elif category == 'B':
            self.validate_category_b(claim)
        elif category == 'C':
            self.validate_category_c(claim)

    def validate_category_a(self, claim: Dict) -> None:
        """
        Validate Category A (algorithm paper) citation.

        Required fields:
        - doi_or_url (valid DOI format)
        - paper_title (mentions algorithm)
        - suggested_citation
        - reference_type (journal/conference/arxiv)
        """
        claim_id = claim.get('claim_id')

        # Required fields
        required_fields = [
            'algorithm_name',
            'suggested_citation',
            'bibtex_key',
            'doi_or_url',
            'paper_title',
            'reference_type'
        ]

        for field in required_fields:
            if field not in claim or not claim[field]:
                self.errors.append(
                    ValidationError(claim_id, field, f"Category A missing required field '{field}'")
                )

        # Validate DOI format
        doi = claim.get('doi_or_url', '')
        if doi and not self.is_valid_doi_or_isbn(doi):
            self.errors.append(
                ValidationError(claim_id, 'doi_or_url', f"Invalid DOI/ISBN format: '{doi}'")
            )

        # Validate reference type
        ref_type = claim.get('reference_type', '')
        if ref_type not in ['journal', 'conference', 'arxiv', 'book']:
            self.errors.append(
                ValidationError(claim_id, 'reference_type',
                              f"Invalid reference type '{ref_type}' (must be journal/conference/arxiv/book)")
            )

        # Validate paper title mentions algorithm
        algorithm = claim.get('algorithm_name', '').lower()
        title = claim.get('paper_title', '').lower()

        if algorithm and title:
            if not self.title_matches_algorithm(title, algorithm):
                self.warnings.append(
                    ValidationError(claim_id, 'paper_title',
                                  f"Paper title may not match algorithm '{algorithm}'", severity="WARNING")
                )

    def validate_category_b(self, claim: Dict) -> None:
        """
        Validate Category B (textbook concept) citation.

        Required fields:
        - isbn (valid ISBN format)
        - book_title
        - suggested_citation
        - reference_type (must be 'book')
        """
        claim_id = claim.get('claim_id')

        # Required fields
        required_fields = [
            'concept',
            'suggested_citation',
            'bibtex_key',
            'isbn',
            'book_title',
            'reference_type'
        ]

        for field in required_fields:
            if field not in claim or not claim[field]:
                self.errors.append(
                    ValidationError(claim_id, field, f"Category B missing required field '{field}'")
                )

        # Validate ISBN format
        isbn = claim.get('isbn', '')
        if isbn and not self.is_valid_isbn(isbn):
            self.errors.append(
                ValidationError(claim_id, 'isbn', f"Invalid ISBN format: '{isbn}'")
            )

        # Validate reference type must be 'book'
        ref_type = claim.get('reference_type', '')
        if ref_type != 'book':
            self.errors.append(
                ValidationError(claim_id, 'reference_type',
                              f"Category B reference type must be 'book', got '{ref_type}'")
            )

    def validate_category_c(self, claim: Dict) -> None:
        """
        Validate Category C (no citation needed).

        Should have empty citation fields.
        """
        claim_id = claim.get('claim_id')

        # Citation fields should be empty or absent
        citation_fields = [
            'suggested_citation', 'bibtex_key', 'doi_or_url', 'isbn',
            'paper_title', 'book_title', 'reference_type'
        ]

        for field in citation_fields:
            value = claim.get(field, '')
            if value and value != '':
                self.warnings.append(
                    ValidationError(claim_id, field,
                                  f"Category C should have empty '{field}', got: '{value}'",
                                  severity="WARNING")
                )

    def is_valid_doi_or_isbn(self, identifier: str) -> bool:
        """
        Check if identifier is valid DOI or ISBN.

        Args:
            identifier: DOI or ISBN string

        Returns:
            True if valid format, False otherwise
        """
        return self.is_valid_doi(identifier) or self.is_valid_isbn(identifier)

    def is_valid_doi(self, doi: str) -> bool:
        """
        Validate DOI format.

        Valid formats:
        - 10.xxxx/yyyy (standard)
        - https://doi.org/10.xxxx/yyyy (URL)
        - arxiv:xxxx.xxxxx (arXiv)

        Args:
            doi: DOI string to validate

        Returns:
            True if valid, False otherwise
        """
        if not doi:
            return False

        # Standard DOI pattern
        doi_pattern = r'^10\.\d{4,}/[^\s]+$'
        if re.match(doi_pattern, doi):
            return True

        # DOI URL pattern
        doi_url_pattern = r'^https?://doi\.org/10\.\d{4,}/[^\s]+$'
        if re.match(doi_url_pattern, doi):
            return True

        # arXiv pattern
        arxiv_pattern = r'^(arxiv:)?\d{4}\.\d{4,5}(v\d+)?$'
        if re.match(arxiv_pattern, doi, re.IGNORECASE):
            return True

        return False

    def is_valid_isbn(self, isbn: str) -> bool:
        """
        Validate ISBN format (ISBN-10 or ISBN-13).

        Args:
            isbn: ISBN string to validate

        Returns:
            True if valid, False otherwise
        """
        if not isbn:
            return False

        # Remove hyphens and spaces
        cleaned = re.sub(r'[-\s]', '', isbn)

        # ISBN-13 pattern
        if re.match(r'^97[89]\d{10}$', cleaned):
            return True

        # ISBN-10 pattern
        if re.match(r'^\d{9}[\dX]$', cleaned):
            return True

        return False

    def title_matches_algorithm(self, title: str, algorithm: str) -> bool:
        """
        Check if paper title reasonably matches algorithm name.

        Args:
            title: Paper title (lowercase)
            algorithm: Algorithm name (lowercase)

        Returns:
            True if match is reasonable, False otherwise
        """
        # Direct substring match
        if algorithm in title:
            return True

        # Word overlap check
        algorithm_words = set(algorithm.split())
        title_words = set(title.split())

        overlap = algorithm_words.intersection(title_words)
        overlap_ratio = len(overlap) / len(algorithm_words) if algorithm_words else 0

        # Require at least 40% word overlap
        return overlap_ratio >= 0.4

    def generate_report(self) -> str:
        """
        Generate human-readable validation report.

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("CITATION VALIDATION REPORT")
        report_lines.append("="*80)
        report_lines.append("")

        # Summary
        error_count = len(self.errors)
        warning_count = len(self.warnings)

        if error_count == 0 and warning_count == 0:
            report_lines.append("✓ VALIDATION PASSED: No errors or warnings")
            report_lines.append("")
            report_lines.append("Ready to apply citations with apply_chatgpt_citations.py")
        else:
            report_lines.append(f"ERRORS: {error_count}")
            report_lines.append(f"WARNINGS: {warning_count}")
            report_lines.append("")

            if error_count > 0:
                report_lines.append("ERRORS (must fix before applying):")
                report_lines.append("-" * 80)
                for error in self.errors:
                    report_lines.append(f"  {error}")
                report_lines.append("")

            if warning_count > 0:
                report_lines.append("WARNINGS (review recommended):")
                report_lines.append("-" * 80)
                for warning in self.warnings:
                    report_lines.append(f"  {warning}")
                report_lines.append("")

        report_lines.append("="*80)
        return "\n".join(report_lines)


# ===========================================================================================
# MAIN VALIDATION INTERFACE
# ===========================================================================================

def validate_citations_file(json_path: str) -> Tuple[bool, str]:
    """
    Validate a complete citations JSON file.

    Args:
        json_path: Path to chatgpt_output_108_citations.json

    Returns:
        Tuple of (is_valid, report_text)
    """
    import json
    from pathlib import Path

    # Load JSON
    path = Path(json_path)
    if not path.exists():
        return False, f"ERROR: File not found: {json_path}"

    try:
        with open(path, 'r', encoding='utf-8') as f:
            claims = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"ERROR: Invalid JSON: {e}"

    # Validate
    validator = CitationValidator()
    is_valid, issues = validator.validate_complete_output(claims)

    # Generate report
    report = validator.generate_report()

    return is_valid, report


def validate_single_claim(claim: Dict) -> List[ValidationError]:
    """
    Validate a single claim and return any errors/warnings.

    Args:
        claim: Claim dict to validate

    Returns:
        List of ValidationError objects
    """
    validator = CitationValidator()
    validator.validate_claim(claim)
    return validator.errors + validator.warnings


# ===========================================================================================
# CLI INTERFACE
# ===========================================================================================

def main():
    """Command-line interface for citation validation."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Validate ChatGPT citations output")
    parser.add_argument(
        'json_file',
        nargs='?',
        default='artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_citations.json',
        help='Path to chatgpt_output_108_citations.json'
    )
    args = parser.parse_args()

    print(f"Validating: {args.json_file}")
    print("")

    is_valid, report = validate_citations_file(args.json_file)
    print(report)

    # Exit code
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
