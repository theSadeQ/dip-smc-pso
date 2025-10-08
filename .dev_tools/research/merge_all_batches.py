#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/merge_all_batches.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Merge multiple batch research results into unified files.

Combines all batch results, deduplicates BibTeX entries, and validates
the merged bibliography.

Usage:
    python merge_all_batches.py --results artifacts/research/batch*.json \
                                 --output artifacts/research/phase2_complete.json \
                                 --bibtex artifacts/research/enhanced_bibliography_phase2.bib

    python merge_all_batches.py --auto  # Auto-detect all batch files
"""

import json
import argparse
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime


def load_batch_results(result_files: List[str]) -> Tuple[List[Dict], Dict]:
    """
    Load all batch result files.

    Args:
        result_files: List of result JSON file paths

    Returns:
        Tuple of (all_results, merged_progress)
    """
    all_results = []
    merged_progress = {
        "total_claims": 0,
        "claims_processed": 0,
        "claims_successful": 0,
        "claims_failed": 0,
        "sessions": [],
        "errors": [],
    }

    for result_file in result_files:
        path = Path(result_file)
        if not path.exists():
            print(f"Warning: Skipping non-existent file: {result_file}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Merge results
        all_results.extend(data.get("results", []))

        # Merge progress
        progress = data.get("progress", {})
        merged_progress["total_claims"] += progress.get("total_claims", 0)
        merged_progress["claims_processed"] += progress.get("claims_processed", 0)
        merged_progress["claims_successful"] += progress.get("claims_successful", 0)
        merged_progress["claims_failed"] += progress.get("claims_failed", 0)
        merged_progress["errors"].extend(progress.get("errors", []))

        # Track session info
        if "session_id" in data:
            merged_progress["sessions"].append(
                {
                    "session_id": data["session_id"],
                    "batch": data.get("progress", {}).get("current_batch", "unknown"),
                    "claims": progress.get("total_claims", 0),
                }
            )

    return all_results, merged_progress


def extract_bibtex_entries(results: List[Dict]) -> List[Dict[str, Any]]:
    """
    Extract all BibTeX entries from results.

    Args:
        results: List of claim results with selected_citations

    Returns:
        List of BibTeX entry dictionaries with metadata
    """
    entries = []

    for result in results:
        claim_id = result.get("claim_id", "unknown")

        for citation in result.get("selected_citations", []):
            entry = {
                "key": citation.get("key", ""),
                "entry_type": citation.get("entry_type", "article"),
                "fields": citation.get("fields", {}),
                "claim_id": claim_id,
                "raw_bibtex": citation.get("bibtex", ""),
            }
            entries.append(entry)

    return entries


def deduplicate_bibtex(entries: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
    """
    Deduplicate BibTeX entries.

    Strategy:
    1. Remove exact duplicate keys
    2. Detect duplicate papers (same DOI or title+year)
    3. Keep first occurrence

    Args:
        entries: List of BibTeX entry dictionaries

    Returns:
        Tuple of (unique_entries, duplicates_removed)
    """
    seen_keys = set()
    seen_papers = set()  # (doi, title, year) tuples
    unique = []
    duplicates = []

    for entry in entries:
        key = entry["key"]
        fields = entry["fields"]

        # Check key duplication
        if key in seen_keys:
            duplicates.append(entry)
            continue

        # Check paper duplication (by DOI)
        doi = fields.get("doi", "").strip()
        if doi and doi in seen_papers:
            duplicates.append(entry)
            continue

        # Check paper duplication (by title + year)
        title = fields.get("title", "").strip().lower()
        year = fields.get("year", "")
        paper_sig = (title, year)

        if paper_sig in seen_papers and title:
            duplicates.append(entry)
            continue

        # Add to unique set
        seen_keys.add(key)
        if doi:
            seen_papers.add(doi)
        if title:
            seen_papers.add(paper_sig)

        unique.append(entry)

    return unique, duplicates


def generate_bibtex_file(entries: List[Dict[str, Any]], output_path: str) -> None:
    """
    Generate BibTeX file from entries.

    Args:
        entries: List of unique BibTeX entries
        output_path: Path to save .bib file
    """
    header = """% ═══════════════════════════════════════════════════════════════════════════
% Enhanced Bibliography - Phase 2 Complete
% ═══════════════════════════════════════════════════════════════════════════
%
% This file contains IEEE-formatted citations extracted from academic databases.
% Generated by: .dev_tools/research/merge_all_batches.py
% Format: IEEE
%
% Key Convention: topic_authorYear_shortTitle
%   Examples:
%     - smc_slotine1991_applied_nonlinear_control
%     - pso_kennedy1995_particle_swarm
%     - dip_khalil2002_nonlinear_systems
%
% ═══════════════════════════════════════════════════════════════════════════

"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)

        for entry in entries:
            # Use raw_bibtex if available, otherwise construct
            if entry.get("raw_bibtex"):
                f.write(entry["raw_bibtex"])
                f.write("\n\n")
            else:
                # Fallback: construct from fields
                entry_type = entry["entry_type"]
                key = entry["key"]
                fields = entry["fields"]

                f.write(f"@{entry_type}{{{key},\n")
                for field_name, field_value in fields.items():
                    f.write(f"    {field_name} = {{{field_value}}},\n")
                f.write("}\n\n")


def create_merged_results_file(
    results: List[Dict],
    progress: Dict,
    output_path: str,
) -> Dict[str, Any]:
    """
    Create merged results JSON file.

    Args:
        results: All merged claim results
        progress: Merged progress metadata
        output_path: Path to save merged results

    Returns:
        Merged data structure
    """
    merged = {
        "session_id": f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "source": "merge_all_batches.py",
        "progress": progress,
        "results": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    return merged


def main():
    parser = argparse.ArgumentParser(
        description="Merge batch research results and deduplicate BibTeX"
    )
    parser.add_argument(
        "--results",
        type=str,
        nargs="+",
        help="Batch result JSON files (supports wildcards)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="artifacts/research/phase2_complete.json",
        help="Output path for merged results (default: artifacts/research/phase2_complete.json)",
    )
    parser.add_argument(
        "--bibtex",
        type=str,
        default="artifacts/research/enhanced_bibliography_phase2.bib",
        help="Output path for merged BibTeX (default: artifacts/research/enhanced_bibliography_phase2.bib)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-detect batch result files in artifacts/research/",
    )

    args = parser.parse_args()

    # Auto-detect mode
    if args.auto:
        research_dir = Path("artifacts/research")
        if not research_dir.exists():
            print(f"Error: Research directory not found: {research_dir}")
            return 1

        # Find all batch result files
        result_files = [
            str(f)
            for f in research_dir.glob("batch_*.json")
            if "validation" not in f.name and "checkpoint" not in str(f)
        ]

        # Also include the CRITICAL batch
        critical_result = research_dir / "research_results.json"
        if critical_result.exists():
            result_files.insert(0, str(critical_result))

        if not result_files:
            print(f"Error: No batch result files found in {research_dir}")
            return 1

        print(f"Auto-detected {len(result_files)} batch result files:")
        for f in result_files:
            print(f"  - {f}")
        print()

    else:
        if not args.results:
            print("Error: Must specify --results or use --auto")
            return 1
        result_files = args.results

    # Load all batch results
    print("Loading batch results...")
    all_results, merged_progress = load_batch_results(result_files)

    if not all_results:
        print("Error: No results found in batch files")
        return 1

    print(f"Loaded {len(all_results)} claim results from {len(result_files)} batches")

    # Extract BibTeX entries
    print("Extracting BibTeX entries...")
    all_entries = extract_bibtex_entries(all_results)
    print(f"Extracted {len(all_entries)} total BibTeX entries")

    # Deduplicate
    print("Deduplicating BibTeX entries...")
    unique_entries, duplicates = deduplicate_bibtex(all_entries)
    print(
        f"Deduplicated: {len(unique_entries)} unique, {len(duplicates)} duplicates removed"
    )

    # Generate merged BibTeX file
    print(f"Writing merged BibTeX to {args.bibtex}...")
    Path(args.bibtex).parent.mkdir(parents=True, exist_ok=True)
    generate_bibtex_file(unique_entries, args.bibtex)

    # Create merged results file
    print(f"Writing merged results to {args.output}...")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    merged_data = create_merged_results_file(all_results, merged_progress, args.output)

    # Print summary
    print("\n" + "=" * 70)
    print("MERGE COMPLETE")
    print("=" * 70)
    print(f"Total claims processed: {merged_progress['claims_processed']}")
    print(f"Successful: {merged_progress['claims_successful']}")
    print(f"Failed: {merged_progress['claims_failed']}")
    print(f"Batches merged: {len(merged_progress['sessions'])}")
    print(f"\nBibTeX entries:")
    print(f"  Total extracted: {len(all_entries)}")
    print(f"  Unique: {len(unique_entries)}")
    print(f"  Duplicates removed: {len(duplicates)}")
    print(f"\nOutput files:")
    print(f"  Results: {args.output}")
    print(f"  BibTeX: {args.bibtex}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    exit(main())
