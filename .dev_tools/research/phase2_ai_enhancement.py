#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/phase2_ai_enhancement.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Phase 2: AI-Enhanced Research Pipeline.

Workflow:
1. Analyze Phase 1 results (identify low-quality citations)
2. Generate AI queries for weak claims
3. Re-run research with enhanced queries
4. Merge improved results with Phase 1
5. Generate Phase 2 report

Usage:
    # Analyze Phase 1 results
    python phase2_ai_enhancement.py --analyze artifacts/research/research_results.json

    # Run full Phase 2 enhancement
    python phase2_ai_enhancement.py --input artifacts/research/research_results.json --output artifacts/research/phase2_enhanced.json
"""

import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class Phase2Orchestrator:
    """Orchestrate AI-enhanced research refinement."""

    def __init__(
        self,
        phase1_results: Path,
        claims_inventory: Path = Path(".artifacts/claims_inventory.json")
    ):
        """
        Initialize Phase 2 orchestrator.

        Args:
            phase1_results: Path to Phase 1 research_results.json
            claims_inventory: Path to original claims inventory
        """
        self.phase1_results = phase1_results
        self.claims_inventory = claims_inventory

        # Load data
        with open(phase1_results, 'r', encoding='utf-8') as f:
            self.results = json.load(f)

        with open(claims_inventory, 'r', encoding='utf-8') as f:
            self.inventory = json.load(f)

        # Build claim lookup
        self.claims_by_id = {c['id']: c for c in self.inventory['claims']}

    def analyze_phase1_quality(self) -> Dict:
        """
        Analyze Phase 1 results to identify low-quality citations.

        Returns:
            Analysis report with weak claims identified
        """
        weak_claims = []
        good_claims = []
        zero_citation_claims = []

        for claim_id, result in self.results.items():
            citation_count = result.get('citation_count', 0)
            queries = result.get('queries_generated', [])

            # Quality criteria
            is_weak = False
            reason = []

            if citation_count == 0:
                is_weak = True
                reason.append("zero_citations")
                zero_citation_claims.append(claim_id)

            # Check for empty queries
            if not queries or all(not q.strip() for q in queries):
                is_weak = True
                reason.append("empty_queries")

            # Check for generic queries
            if queries:
                generic_terms = ['professional', 'framework', 'system', 'application']
                if any(all(term in q.lower() for term in ['professional', 'framework']) for q in queries):
                    is_weak = True
                    reason.append("generic_queries")

            if is_weak:
                weak_claims.append({
                    'claim_id': claim_id,
                    'citation_count': citation_count,
                    'reasons': reason,
                    'queries': queries
                })
            else:
                good_claims.append(claim_id)

        # Statistics
        total = len(self.results)
        weak_count = len(weak_claims)
        zero_count = len(zero_citation_claims)
        weak_pct = (weak_count / total * 100) if total else 0

        analysis = {
            'total_claims': total,
            'weak_claims': weak_count,
            'weak_percentage': weak_pct,
            'zero_citations': zero_count,
            'good_claims': len(good_claims),
            'weak_claim_details': weak_claims[:20],  # Sample for report
            'weak_claim_ids': [c['claim_id'] for c in weak_claims],
            'zero_citation_ids': zero_citation_claims
        }

        return analysis

    def create_weak_claims_batch(
        self,
        analysis: Dict,
        output_file: Path
    ) -> Path:
        """
        Create batch file with weak claims for re-research.

        Args:
            analysis: Output from analyze_phase1_quality()
            output_file: Path to save batch file

        Returns:
            Path to created batch file
        """
        weak_ids = analysis['weak_claim_ids']

        # Extract full claim objects
        weak_claims = [
            self.claims_by_id[claim_id]
            for claim_id in weak_ids
            if claim_id in self.claims_by_id
        ]

        # Count by priority
        by_priority = defaultdict(int)
        for claim in weak_claims:
            priority = claim.get('priority', 'UNKNOWN')
            by_priority[priority] += 1

        # Build batch structure
        batch = {
            'metadata': {
                'phase': 2,
                'description': 'Weak claims from Phase 1 requiring AI-enhanced queries',
                'total_claims': len(weak_claims),
                'by_priority': dict(by_priority),
                'ai_enhanced': False  # Will be set to True after AI query generation
            },
            'claims': weak_claims
        }

        # Save
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)

        print(f"Created weak claims batch: {output_file}")
        print(f"  Total weak claims: {len(weak_claims)}")
        print(f"  By priority: {dict(by_priority)}")

        return output_file

    def generate_ai_queries(
        self,
        input_batch: Path,
        output_batch: Path,
        api_key: str = None
    ) -> Path:
        """
        Generate AI queries for weak claims.

        Args:
            input_batch: Batch file with weak claims
            output_batch: Output batch with ai_queries added
            api_key: Anthropic API key (optional)

        Returns:
            Path to enhanced batch file
        """
        cmd = [
            'python',
            '.dev_tools/research/ai_query_generator.py',
            '--input', str(input_batch),
            '--output', str(output_batch)
        ]

        if api_key:
            cmd.extend(['--api-key', api_key])

        print("\nGenerating AI queries for weak claims...")
        subprocess.run(cmd, check=True)

        return output_batch

    def run_phase2_research(
        self,
        enhanced_batch: Path,
        output_prefix: str = 'phase2'
    ) -> Dict:
        """
        Run research pipeline with AI-enhanced queries.

        Args:
            enhanced_batch: Batch file with ai_queries
            output_prefix: Prefix for output files

        Returns:
            Research results summary
        """
        cmd = [
            'python',
            '.dev_tools/research/research_pipeline.py',
            '--claims-file', str(enhanced_batch),
            '--priority', 'HIGH',  # Most weak claims are HIGH
            '--verbose'
        ]

        print("\nRunning Phase 2 research with AI-enhanced queries...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error running Phase 2 research:\n{result.stderr}")
            return None

        print(result.stdout)

        # Load results
        results_file = Path('artifacts/research/research_results.json')
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    def merge_phase1_phase2(
        self,
        phase1_results: Dict,
        phase2_results: Dict,
        output_file: Path
    ) -> Dict:
        """
        Merge Phase 1 and Phase 2 results, preferring Phase 2 for conflicts.

        Args:
            phase1_results: Original results
            phase2_results: AI-enhanced results
            output_file: Path to save merged results

        Returns:
            Merged results dict
        """
        merged = phase1_results.copy()

        # Update with Phase 2 results (overwrites Phase 1 for same claims)
        improvements = 0
        for claim_id, p2_result in phase2_results.items():
            p1_result = phase1_results.get(claim_id, {})
            p1_citations = p1_result.get('citation_count', 0)
            p2_citations = p2_result.get('citation_count', 0)

            if p2_citations > p1_citations:
                improvements += 1

            merged[claim_id] = p2_result

        # Save merged results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        print(f"\nMerged Phase 1 + Phase 2 results:")
        print(f"  Total claims: {len(merged)}")
        print(f"  Claims improved in Phase 2: {improvements}")
        print(f"  Output: {output_file}")

        return {
            'total_claims': len(merged),
            'improvements': improvements,
            'output_file': str(output_file)
        }

    def run_full_phase2(
        self,
        output_file: Path,
        api_key: str = None
    ) -> Dict:
        """
        Run complete Phase 2 workflow.

        Args:
            output_file: Final output file for merged results
            api_key: Anthropic API key (optional)

        Returns:
            Phase 2 summary report
        """
        print("=" * 80)
        print("PHASE 2: AI-ENHANCED RESEARCH PIPELINE")
        print("=" * 80)

        # Step 1: Analyze Phase 1
        print("\n[1/5] Analyzing Phase 1 results...")
        analysis = self.analyze_phase1_quality()

        print(f"\nPhase 1 Quality Analysis:")
        print(f"  Total claims: {analysis['total_claims']}")
        print(f"  Weak claims: {analysis['weak_claims']} ({analysis['weak_percentage']:.1f}%)")
        print(f"  Zero citations: {analysis['zero_citations']}")

        if analysis['weak_claims'] == 0:
            print("\nNo weak claims found. Phase 1 results are sufficient!")
            return {'status': 'skipped', 'reason': 'no_weak_claims'}

        # Step 2: Create weak claims batch
        print("\n[2/5] Creating weak claims batch...")
        weak_batch = self.create_weak_claims_batch(
            analysis,
            Path('artifacts/research/phase2_weak_claims.json')
        )

        # Step 3: Generate AI queries
        print("\n[3/5] Generating AI-enhanced queries...")
        enhanced_batch = self.generate_ai_queries(
            weak_batch,
            Path('artifacts/research/phase2_enhanced_claims.json'),
            api_key=api_key
        )

        # Step 4: Run Phase 2 research
        print("\n[4/5] Running Phase 2 research...")
        phase2_results = self.run_phase2_research(enhanced_batch)

        if not phase2_results:
            print("Error: Phase 2 research failed")
            return {'status': 'failed', 'reason': 'research_failed'}

        # Step 5: Merge results
        print("\n[5/5] Merging Phase 1 + Phase 2 results...")
        merge_stats = self.merge_phase1_phase2(
            self.results,
            phase2_results,
            output_file
        )

        # Final report
        report = {
            'status': 'complete',
            'phase1_analysis': analysis,
            'phase2_research': {
                'claims_researched': len(phase2_results),
                'improvements': merge_stats['improvements']
            },
            'output_file': str(output_file)
        }

        print("\n" + "=" * 80)
        print("PHASE 2 COMPLETE")
        print("=" * 80)
        print(f"Claims improved: {merge_stats['improvements']}")
        print(f"Final output: {output_file}")

        return report


def main():
    parser = argparse.ArgumentParser(
        description="Phase 2: AI-Enhanced Research Pipeline"
    )
    parser.add_argument(
        '--analyze',
        type=str,
        help='Analyze Phase 1 results (path to research_results.json)'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Phase 1 results file (research_results.json)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for merged Phase 1 + Phase 2 results'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Analysis-only mode
    if args.analyze:
        orchestrator = Phase2Orchestrator(Path(args.analyze))
        analysis = orchestrator.analyze_phase1_quality()

        print("=" * 80)
        print("PHASE 1 QUALITY ANALYSIS")
        print("=" * 80)
        print(f"Total claims: {analysis['total_claims']}")
        print(f"Weak claims: {analysis['weak_claims']} ({analysis['weak_percentage']:.1f}%)")
        print(f"Zero citations: {analysis['zero_citations']}")
        print(f"Good claims: {analysis['good_claims']}")

        print(f"\nSample weak claims ({min(10, len(analysis['weak_claim_details']))}):")
        for weak in analysis['weak_claim_details'][:10]:
            print(f"  {weak['claim_id']}: {weak['citation_count']} citations - {', '.join(weak['reasons'])}")

        return 0

    # Full Phase 2 mode
    if not args.input or not args.output:
        print("Error: --input and --output required for Phase 2 execution")
        print("Use --analyze for analysis-only mode")
        return 1

    orchestrator = Phase2Orchestrator(Path(args.input))
    report = orchestrator.run_full_phase2(
        Path(args.output),
        api_key=args.api_key
    )

    # Save report
    report_file = Path('artifacts/research/phase2_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nPhase 2 report saved: {report_file}")

    return 0


if __name__ == '__main__':
    exit(main())
