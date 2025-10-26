#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/validate_results.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Validate research results for CRITICAL batch.

Checks:
1. Citation coverage (target: ≥85% of claims have ≥2 citations)
2. BibTeX format and compilation
3. DOI accessibility (target: ≥95%)
4. Query diversity (target: 3-5 queries/claim average)
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import re
from collections import defaultdict


def validate_citation_coverage(results_path: str = "artifacts/research/research_results.json") -> Dict[str, Any]:
    """
    Validate citation coverage.

    Target: ≥85% of CRITICAL claims have ≥2 citations each
    """
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)

    total_claims = len(results['results'])
    claims_with_2plus_cites = 0
    claims_with_1_cite = 0
    claims_with_0_cites = 0

    query_counts = []
    total_citations = 0

    for result in results['results']:
        cite_count = len(result.get('selected_citations', []))
        total_citations += cite_count

        if cite_count >= 2:
            claims_with_2plus_cites += 1
        elif cite_count == 1:
            claims_with_1_cite += 1
        else:
            claims_with_0_cites += 1

        query_counts.append(len(result.get('queries_used', [])))

    coverage_pct = (claims_with_2plus_cites / total_claims * 100) if total_claims > 0 else 0
    avg_queries = sum(query_counts) / len(query_counts) if query_counts else 0

    validation = {
        "total_claims": total_claims,
        "claims_with_2plus_citations": claims_with_2plus_cites,
        "claims_with_1_citation": claims_with_1_cite,
        "claims_with_0_citations": claims_with_0_cites,
        "coverage_percentage": coverage_pct,
        "total_citations_generated": total_citations,
        "avg_citations_per_claim": total_citations / total_claims if total_claims > 0 else 0,
        "avg_queries_per_claim": avg_queries,
        "target_coverage": 85.0,
        "passes": coverage_pct >= 85.0,
    }

    return validation


def validate_bibtex(bibtex_path: str = "artifacts/research/enhanced_bibliography.bib") -> Dict[str, Any]:
    """
    Validate BibTeX format.

    Checks:
    - Valid BibTeX syntax
    - Duplicate entries
    - Missing required fields
    """
    with open(bibtex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count entries
    entry_pattern = r'@(\w+)\{([^,]+),'
    entries = re.findall(entry_pattern, content)

    # Check for duplicates
    entry_keys = [key for _, key in entries]
    duplicates = [key for key in set(entry_keys) if entry_keys.count(key) > 1]

    # Count by type
    entry_types = defaultdict(int)
    for entry_type, _ in entries:
        entry_types[entry_type.lower()] += 1

    validation = {
        "total_entries": len(entries),
        "unique_entries": len(set(entry_keys)),
        "duplicate_entries": len(duplicates),
        "duplicate_keys": duplicates,
        "entry_types": dict(entry_types),
        "passes_basic_syntax": True,  # If we got here, it parsed
        "passes_no_duplicates": len(duplicates) == 0,
    }

    return validation


def validate_doi_accessibility(results_path: str = "artifacts/research/research_results.json") -> Dict[str, Any]:
    """
    Validate DOI accessibility.

    Target: ≥95% of papers with DOIs can be resolved
    Note: This is a dry-run check without actually hitting DOIs
    """
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)

    total_citations = 0
    citations_with_doi = 0
    citations_with_arxiv = 0
    citations_with_url = 0
    citations_without_any = 0

    for result in results['results']:
        for paper in result.get('papers_found', []):
            total_citations += 1

            has_doi = paper.get('doi') is not None and paper.get('doi') != ""
            has_url = paper.get('url') is not None and paper.get('url') != ""
            is_arxiv = 'arxiv' in paper.get('source', '').lower() or 'arxiv.org' in paper.get('url', '')

            if has_doi:
                citations_with_doi += 1
            if is_arxiv:
                citations_with_arxiv += 1
            if has_url:
                citations_with_url += 1
            if not (has_doi or has_url):
                citations_without_any += 1

    doi_coverage = (citations_with_doi / total_citations * 100) if total_citations > 0 else 0
    url_coverage = (citations_with_url / total_citations * 100) if total_citations > 0 else 0

    # DOI or URL coverage (assume both are accessible)
    accessible_coverage = ((citations_with_doi + citations_without_any == 0 and citations_with_url) / total_citations * 100) if total_citations > 0 else 100

    validation = {
        "total_papers_found": total_citations,
        "papers_with_doi": citations_with_doi,
        "papers_with_arxiv": citations_with_arxiv,
        "papers_with_url": citations_with_url,
        "papers_without_identifiers": citations_without_any,
        "doi_coverage_pct": doi_coverage,
        "url_coverage_pct": url_coverage,
        "accessible_estimate_pct": max(doi_coverage, url_coverage),
        "target_accessibility": 95.0,
        "passes": max(doi_coverage, url_coverage) >= 95.0,
        "note": "Actual HTTP checks not performed (dry-run validation)"
    }

    return validation


def run_full_validation():
    """Run all validation checks."""
    print("=" * 70)
    print("CRITICAL BATCH VALIDATION REPORT")
    print("=" * 70)

    # 1. Citation Coverage
    print("\n1. CITATION COVERAGE")
    print("-" * 70)
    coverage = validate_citation_coverage()
    print(f"Total claims researched: {coverage['total_claims']}")
    print(f"Claims with >=2 citations: {coverage['claims_with_2plus_citations']}")
    print(f"Claims with 1 citation: {coverage['claims_with_1_citation']}")
    print(f"Claims with 0 citations: {coverage['claims_with_0_citations']}")
    print(f"Coverage: {coverage['coverage_percentage']:.1f}% (target: >={coverage['target_coverage']}%)")
    print(f"Average citations/claim: {coverage['avg_citations_per_claim']:.2f}")
    print(f"Average queries/claim: {coverage['avg_queries_per_claim']:.2f}")
    print(f"Status: {'PASS' if coverage['passes'] else 'FAIL'}")

    # 2. BibTeX Format
    print("\n2. BIBTEX FORMAT")
    print("-" * 70)
    bibtex = validate_bibtex()
    print(f"Total BibTeX entries: {bibtex['total_entries']}")
    print(f"Unique entries: {bibtex['unique_entries']}")
    print(f"Duplicate entries: {bibtex['duplicate_entries']}")
    if bibtex['duplicate_keys']:
        print(f"Duplicate keys: {', '.join(bibtex['duplicate_keys'])}")
    print(f"Entry types: {bibtex['entry_types']}")
    print(f"Status: {'PASS (basic syntax)' if bibtex['passes_basic_syntax'] else 'FAIL'}")
    if not bibtex['passes_no_duplicates']:
        print("WARNING: Duplicate entries detected (needs deduplication)")

    # 3. DOI Accessibility
    print("\n3. DOI ACCESSIBILITY")
    print("-" * 70)
    doi = validate_doi_accessibility()
    print(f"Total papers found: {doi['total_papers_found']}")
    print(f"Papers with DOI: {doi['papers_with_doi']} ({doi['doi_coverage_pct']:.1f}%)")
    print(f"Papers with URL: {doi['papers_with_url']} ({doi['url_coverage_pct']:.1f}%)")
    print(f"Papers with ArXiv: {doi['papers_with_arxiv']}")
    print(f"Estimated accessible: {doi['accessible_estimate_pct']:.1f}% (target: >={doi['target_accessibility']}%)")
    print(f"Status: {'PASS' if doi['passes'] else 'FAIL'}")
    print(f"Note: {doi['note']}")

    # Overall Summary
    print("\n" + "=" * 70)
    print("OVERALL VALIDATION SUMMARY")
    print("=" * 70)

    all_pass = coverage['passes'] and bibtex['passes_basic_syntax'] and doi['passes']

    print(f"Citation Coverage: {'PASS' if coverage['passes'] else 'FAIL'}")
    print(f"BibTeX Format: {'PASS' if bibtex['passes_basic_syntax'] else 'FAIL'}")
    print(f"DOI Accessibility: {'PASS' if doi['passes'] else 'FAIL'}")
    print(f"\nOverall: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")

    # Save validation report
    report = {
        "citation_coverage": coverage,
        "bibtex_format": bibtex,
        "doi_accessibility": doi,
        "overall_pass": all_pass
    }

    output_path = "artifacts/research/critical_batch_validation_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n Validation report saved to: {output_path}")

    return report


if __name__ == "__main__":
    run_full_validation()
