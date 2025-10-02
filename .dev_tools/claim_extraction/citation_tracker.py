"""
Citation Storage and Validation System

Tracks citation research progress, validates completeness, and generates reports.
Works with claims_research_tracker.csv to monitor completion.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict


@dataclass
class CitationStats:
    """Statistics for citation tracking."""
    total_claims: int
    researched_count: int
    completed_count: int
    in_progress_count: int
    not_started_count: int
    completion_percentage: float
    by_priority: Dict[str, Dict[str, int]]
    by_topic: Dict[str, Dict[str, int]]
    citations_found: int
    unique_citations: int
    reuse_rate: float


class CitationTracker:
    """Track and validate citation research progress."""

    def __init__(self, csv_path: Path):
        """Initialize tracker with research CSV."""
        self.csv_path = csv_path
        self.claims = self._load_csv()

    def _load_csv(self) -> List[Dict]:
        """Load claims from research CSV."""
        with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def get_research_status(self) -> Tuple[str, bool]:
        """Determine research status and validate fields for a claim."""
        def _validate_claim(claim: Dict) -> Tuple[str, bool]:
            status = claim.get('Research_Status', '').strip().lower()

            # Check if has citation data
            has_citation = bool(claim.get('Suggested_Citation', '').strip())
            has_bibtex = bool(claim.get('BibTeX_Key', '').strip())

            # Validation
            if status == 'completed':
                # Completed must have citation and bibtex
                is_valid = has_citation and has_bibtex
                return 'completed', is_valid
            elif status == 'in_progress' or status == 'in progress':
                return 'in_progress', True  # Valid as long as status is set
            else:
                # Empty or not started
                if has_citation or has_bibtex:
                    # Has data but no status - assume in progress
                    return 'in_progress', False  # Invalid - should update status
                return 'not_started', True

        return _validate_claim

    def calculate_statistics(self) -> CitationStats:
        """Calculate comprehensive statistics."""
        validator = self.get_research_status()

        # Overall counts
        completed = []
        in_progress = []
        not_started = []

        for claim in self.claims:
            status, is_valid = validator(claim)
            if status == 'completed':
                completed.append(claim)
            elif status == 'in_progress':
                in_progress.append(claim)
            else:
                not_started.append(claim)

        researched_count = len(completed) + len(in_progress)
        total = len(self.claims)

        # Priority breakdown
        priority_stats = defaultdict(lambda: {'completed': 0, 'in_progress': 0, 'not_started': 0, 'total': 0})
        for claim in self.claims:
            priority = claim.get('Priority', 'UNKNOWN')
            status, _ = validator(claim)
            priority_stats[priority][status] += 1
            priority_stats[priority]['total'] += 1

        # Topic breakdown (using CSV topic detection)
        topic_stats = self._calculate_topic_stats(completed, in_progress, not_started)

        # Citation reuse analysis
        citations = [c.get('Suggested_Citation', '').strip() for c in completed if c.get('Suggested_Citation', '').strip()]
        unique_citations_count = len(set(citations))
        citations_count = len(citations)
        reuse_rate = (citations_count - unique_citations_count) / citations_count * 100 if citations_count > 0 else 0.0

        return CitationStats(
            total_claims=total,
            researched_count=researched_count,
            completed_count=len(completed),
            in_progress_count=len(in_progress),
            not_started_count=len(not_started),
            completion_percentage=len(completed) / total * 100 if total > 0 else 0.0,
            by_priority=dict(priority_stats),
            by_topic=topic_stats,
            citations_found=citations_count,
            unique_citations=unique_citations_count,
            reuse_rate=reuse_rate
        )

    def _calculate_topic_stats(self, completed, in_progress, not_started) -> Dict:
        """Calculate statistics by topic (simplified from CSV Research_Description)."""
        # Simplified topic detection from description
        topics = {
            'SMC': ['sliding mode', 'smc', 'boundary layer', 'chattering'],
            'PSO': ['pso', 'particle swarm', 'optimization'],
            'Adaptive': ['adaptive', 'adaptation law'],
            'Numerical': ['numerical', 'matrix', 'regularization'],
            'Benchmarking': ['benchmark', 'metric', 'performance']
        }

        topic_stats = defaultdict(lambda: {'completed': 0, 'in_progress': 0, 'not_started': 0})

        def detect_topic(claim):
            desc = claim.get('Research_Description', '').lower()
            for topic, keywords in topics.items():
                if any(kw in desc for kw in keywords):
                    return topic
            return 'Other'

        for claim in completed:
            topic_stats[detect_topic(claim)]['completed'] += 1
        for claim in in_progress:
            topic_stats[detect_topic(claim)]['in_progress'] += 1
        for claim in not_started:
            topic_stats[detect_topic(claim)]['not_started'] += 1

        return dict(topic_stats)

    def find_successfully_cited_claims(self) -> List[Dict]:
        """Find all claims with completed citations."""
        validator = self.get_research_status()
        completed = []

        for claim in self.claims:
            status, is_valid = validator(claim)
            if status == 'completed' and is_valid:
                completed.append(claim)

        return completed

    def find_reusable_citations(self) -> Dict[str, List[str]]:
        """Find citations used multiple times (reuse opportunities)."""
        citation_to_claims = defaultdict(list)

        completed = self.find_successfully_cited_claims()
        for claim in completed:
            citation = claim.get('Suggested_Citation', '').strip()
            if citation:
                citation_to_claims[citation].append(claim['Claim_ID'])

        # Filter to citations used 2+ times
        reusable = {
            citation: claim_ids
            for citation, claim_ids in citation_to_claims.items()
            if len(claim_ids) >= 2
        }

        return dict(sorted(reusable.items(), key=lambda x: -len(x[1])))

    def generate_progress_report(self) -> str:
        """Generate human-readable progress report."""
        stats = self.calculate_statistics()

        report = []
        report.append("="*80)
        report.append("CITATION RESEARCH PROGRESS REPORT")
        report.append("="*80)

        report.append(f"\nOverall Progress:")
        report.append(f"  Total Claims: {stats.total_claims}")
        report.append(f"  Completed: {stats.completed_count} ({stats.completion_percentage:.1f}%)")
        report.append(f"  In Progress: {stats.in_progress_count}")
        report.append(f"  Not Started: {stats.not_started_count}")

        report.append(f"\nProgress Bar:")
        completed_bar = int(stats.completion_percentage / 2)  # 50 chars = 100%
        bar = "[" + "#" * completed_bar + "-" * (50 - completed_bar) + "]"
        report.append(f"  {bar} {stats.completion_percentage:.1f}%")

        report.append(f"\nBy Priority:")
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM']:
            if priority in stats.by_priority:
                p = stats.by_priority[priority]
                pct = p['completed'] / p['total'] * 100 if p['total'] > 0 else 0
                report.append(f"  {priority:12s}: {p['completed']:3d}/{p['total']:3d} ({pct:5.1f}%) | "
                             f"In progress: {p['in_progress']:3d} | Not started: {p['not_started']:3d}")

        report.append(f"\nCitation Reuse Analysis:")
        report.append(f"  Total Citations Found: {stats.citations_found}")
        report.append(f"  Unique Citations: {stats.unique_citations}")
        report.append(f"  Reuse Rate: {stats.reuse_rate:.1f}%")

        # Top reused citations
        reusable = self.find_reusable_citations()
        if reusable:
            report.append(f"\n  Top Reused Citations:")
            for i, (citation, claim_ids) in enumerate(list(reusable.items())[:5], 1):
                report.append(f"    {i}. {citation}: used {len(claim_ids)} times")

        report.append("\n" + "="*80)

        return "\n".join(report)

    def export_completed_citations(self, output_path: Path):
        """Export completed citations to JSON for Phase 2 integration."""
        completed = self.find_successfully_cited_claims()

        export_data = {
            'metadata': {
                'total_completed': len(completed),
                'export_date': '2025-10-02',
                'unique_citations': len(set(c.get('Suggested_Citation', '') for c in completed)),
            },
            'citations': []
        }

        for claim in completed:
            export_data['citations'].append({
                'claim_id': claim['Claim_ID'],
                'priority': claim['Priority'],
                'category': claim['Category'],
                'citation': claim['Suggested_Citation'],
                'bibtex_key': claim['BibTeX_Key'],
                'doi_url': claim.get('DOI_or_URL', ''),
                'reference_type': claim.get('Reference_Type', ''),
                'notes': claim.get('Research_Notes', ''),
                'file_path': claim['File_Path'],
                'line_number': claim['Line_Number']
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return len(completed)

    def find_incomplete_claims(self, priority: Optional[str] = None) -> List[Dict]:
        """Find claims that need research (not started or in progress)."""
        validator = self.get_research_status()
        incomplete = []

        for claim in self.claims:
            if priority and claim.get('Priority') != priority:
                continue

            status, _ = validator(claim)
            if status in ['not_started', 'in_progress']:
                incomplete.append({
                    'claim_id': claim['Claim_ID'],
                    'priority': claim['Priority'],
                    'status': status,
                    'description': claim.get('Research_Description', 'N/A')[:100],
                    'file_path': claim['File_Path']
                })

        return incomplete


def main():
    """Main execution - generate progress report."""
    project_root = Path(__file__).parent.parent.parent
    csv_path = project_root / "artifacts" / "claims_research_tracker.csv"

    if not csv_path.exists():
        print(f"Error: CSV not found at {csv_path}")
        print("Please ensure claims_research_tracker.csv exists in artifacts/")
        return

    tracker = CitationTracker(csv_path)

    # Print progress report
    print(tracker.generate_progress_report())

    # Export completed citations (if any)
    output_path = project_root / "artifacts" / "completed_citations.json"
    completed_count = tracker.export_completed_citations(output_path)

    if completed_count > 0:
        print(f"\nExported {completed_count} completed citations to: {output_path}")
    else:
        print("\nNo completed citations yet - start researching!")

    # Show incomplete CRITICAL claims (highest priority)
    print("\n" + "="*80)
    print("NEXT ACTIONS: CRITICAL Claims Needing Research")
    print("="*80)

    incomplete_critical = tracker.find_incomplete_claims(priority='CRITICAL')
    if incomplete_critical:
        print(f"\nFound {len(incomplete_critical)} CRITICAL claims to research:")
        for i, claim in enumerate(incomplete_critical[:5], 1):
            print(f"\n{i}. {claim['claim_id']} ({claim['status']})")
            print(f"   Description: {claim['description']}")
            print(f"   File: {claim['file_path']}")

        if len(incomplete_critical) > 5:
            print(f"\n... and {len(incomplete_critical) - 5} more CRITICAL claims")
    else:
        print("\nAll CRITICAL claims completed! Move to HIGH priority.")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
