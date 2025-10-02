#!/usr/bin/env python3
"""
Claim Triage Tool - Automated Citation Necessity Detection

Categorizes claims into:
- Category A: REQUIRES CITATION (Algorithmic Theory)
- Category B: REQUIRES CITATION (Foundational Concepts)
- Category C: NO CITATION NEEDED (Pure Implementation)
- Category D: UNCERTAIN (Manual Review Required)

Based on file path analysis, keyword detection, and code pattern recognition.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import argparse


@dataclass
class TriageResult:
    """Triage result for a single claim."""
    claim_id: str
    category: str  # A, B, C, D
    confidence: str  # LOW, MEDIUM, HIGH
    rationale: str
    detected_patterns: List[str] = field(default_factory=list)
    needs_citation: bool = True
    suggested_action: str = ""


class ClaimTriager:
    """Triages claims to determine citation necessity."""

    def __init__(self, batch_dir: Path):
        self.batch_dir = batch_dir
        self.claims_file = batch_dir / "claims.json"
        self.results: List[TriageResult] = []

    def triage_all_claims(self) -> None:
        """Triage all claims in batch."""
        print(f"Loading claims from {self.claims_file}...")
        with open(self.claims_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        claims = data['claims']
        print(f"Loaded {len(claims)} claims\n")

        for i, claim in enumerate(claims, 1):
            result = self.triage_claim(claim)
            self.results.append(result)

            if i % 50 == 0:
                print(f"Processed {i}/{len(claims)} claims...")

        print(f"\nTriage complete!")

    def triage_claim(self, claim: Dict) -> TriageResult:
        """Triage a single claim."""
        claim_id = claim['id']
        file_path = claim['file_path'].lower()
        context = claim['context'].lower()
        description = claim.get('description', '').lower()

        # Combine for analysis
        text = f"{file_path} {context} {description}"

        # Check patterns in order of priority
        category, confidence, rationale, patterns = self._analyze_patterns(text, file_path)

        # Determine needs_citation
        needs_citation = category in ['A', 'B']

        # Suggested action
        if category == 'C':
            suggested_action = 'Mark "no citation needed" in CSV'
        elif category == 'D':
            suggested_action = 'Manual code review required'
        else:
            suggested_action = 'Research appropriate citation'

        return TriageResult(
            claim_id=claim_id,
            category=category,
            confidence=confidence,
            rationale=rationale,
            detected_patterns=patterns,
            needs_citation=needs_citation,
            suggested_action=suggested_action
        )

    def _analyze_patterns(self, text: str, file_path: str) -> Tuple[str, str, str, List[str]]:
        """Analyze text to determine category."""
        patterns = []

        # Category C: Pure Implementation (HIGH CONFIDENCE)
        # Software patterns
        if any(kw in text for kw in ['factory', 'singleton', 'observer', 'strategy pattern', 'design pattern']):
            if 'factory' in file_path or 'pattern' in file_path:
                patterns.append("FACTORY_PATTERN")
                return 'C', 'HIGH', 'Software design pattern (factory)', patterns

        # Initialization/constructors
        if any(kw in text for kw in ['__init__', 'constructor', 'initialize', 'reset state', 'reset method']):
            if any(kw in text for kw in ['reset internal', 'initial values', 'clear state', 'reset controller']):
                patterns.append("INITIALIZATION")
                return 'C', 'HIGH', 'Initialization/reset method (pure implementation)', patterns

        # Serialization
        if any(kw in text for kw in ['to_dict', 'from_dict', 'serialize', 'deserialize', 'json', 'to_json']):
            patterns.append("SERIALIZATION")
            return 'C', 'HIGH', 'Serialization/deserialization (pure implementation)', patterns

        # Threading/concurrency
        if any(kw in text for kw in ['threading', 'lock', 'mutex', 'deadlock', 'thread safe', 'concurrent']):
            if 'algorithm' not in text:  # Avoid false positives for concurrent algorithms
                patterns.append("THREADING")
                return 'C', 'HIGH', 'Threading/concurrency primitives (pure implementation)', patterns

        # Interface definitions
        if any(kw in text for kw in ['interface', 'abstract', 'protocol', 'abc.', 'typing.protocol']):
            patterns.append("INTERFACE")
            return 'C', 'MEDIUM', 'Interface/protocol definition (pure implementation)', patterns

        # Configuration/file I/O
        if any(kw in text for kw in ['config', 'parse yaml', 'load config', 'file i/o', 'read file', 'write file']):
            if 'algorithm' not in text:
                patterns.append("CONFIG_IO")
                return 'C', 'MEDIUM', 'Configuration/file I/O (pure implementation)', patterns

        # Data structures (simple)
        if any(kw in text for kw in ['dataclass', 'namedtuple', 'dict', 'list comprehension']):
            if not any(kw in text for kw in ['algorithm', 'method', 'analysis']):
                patterns.append("DATA_STRUCTURE")
                return 'C', 'MEDIUM', 'Data structure definition (pure implementation)', patterns

        # Category A: Algorithmic Theory (HIGH CONFIDENCE)
        # Control algorithms
        if any(kw in text for kw in ['sliding mode', 'super-twisting', 'lyapunov', 'reaching law', 'sliding surface']):
            patterns.append("SMC_THEORY")
            return 'A', 'HIGH', 'Sliding mode control theory (requires citation)', patterns

        if any(kw in text for kw in ['model predictive', 'mpc', 'receding horizon', 'optimization horizon']):
            patterns.append("MPC_THEORY")
            return 'A', 'HIGH', 'Model predictive control theory (requires citation)', patterns

        # Optimization algorithms
        if any(kw in text for kw in ['particle swarm', 'pso', 'swarm intelligence']):
            if 'optimizer' in file_path or 'pso' in file_path:
                patterns.append("PSO_ALGORITHM")
                return 'A', 'HIGH', 'Particle swarm optimization algorithm (requires citation)', patterns

        if any(kw in text for kw in ['genetic algorithm', 'mutation', 'crossover', 'chromosome', 'evolution']):
            if 'genetic' in file_path or 'evolutionary' in file_path:
                patterns.append("GENETIC_ALGORITHM")
                return 'A', 'HIGH', 'Genetic algorithm (requires citation)', patterns

        if any(kw in text for kw in ['differential evolution', 'de algorithm']):
            patterns.append("DIFFERENTIAL_EVOLUTION")
            return 'A', 'HIGH', 'Differential evolution algorithm (requires citation)', patterns

        if any(kw in text for kw in ['nelder-mead', 'simplex method', 'simplex optimization']):
            patterns.append("SIMPLEX_METHOD")
            return 'A', 'HIGH', 'Simplex optimization method (requires citation)', patterns

        # Statistical methods
        if any(kw in text for kw in ['cross-validation', 'k-fold', 'cross validation', 'train test split']):
            if 'validation' in file_path or 'cross' in file_path:
                patterns.append("CROSS_VALIDATION")
                return 'A', 'HIGH', 'Cross-validation method (requires citation)', patterns

        if any(kw in text for kw in ['bootstrap', 'resampling', 'bootstrap confidence']):
            patterns.append("BOOTSTRAP")
            return 'A', 'HIGH', 'Bootstrap resampling method (requires citation)', patterns

        if any(kw in text for kw in ['shapiro', 'normality test', 'anderson-darling', 'kolmogorov-smirnov']):
            patterns.append("NORMALITY_TEST")
            return 'A', 'HIGH', 'Normality testing (requires citation)', patterns

        if any(kw in text for kw in ['wilcoxon', 'mann-whitney', 'rank-sum', 'kruskal-wallis']):
            patterns.append("NONPARAMETRIC_TEST")
            return 'A', 'HIGH', 'Non-parametric statistical test (requires citation)', patterns

        if any(kw in text for kw in ['outlier detection', 'iqr', 'interquartile', 'z-score outlier']):
            patterns.append("OUTLIER_DETECTION")
            return 'A', 'HIGH', 'Outlier detection method (requires citation)', patterns

        # Numerical methods
        if any(kw in text for kw in ['euler', 'runge-kutta', 'rk4', 'rk45', 'numerical integration']):
            if 'integrat' in text:
                patterns.append("NUMERICAL_INTEGRATION")
                return 'A', 'HIGH', 'Numerical integration method (requires citation)', patterns

        # Category B: Foundational Concepts (MEDIUM CONFIDENCE)
        # Performance metrics
        if any(kw in text for kw in ['overshoot', 'settling time', 'rise time', 'ise', 'iae', 'integral error']):
            patterns.append("PERFORMANCE_METRIC")
            return 'B', 'MEDIUM', 'Performance metric definition (requires textbook citation)', patterns

        if any(kw in text for kw in ['stability', 'convergence', 'asymptotic', 'bounded']):
            if any(kw in text for kw in ['analysis', 'metric', 'measure', 'index']):
                patterns.append("STABILITY_METRIC")
                return 'B', 'MEDIUM', 'Stability analysis concept (requires textbook citation)', patterns

        # Category D: Uncertain (LOW CONFIDENCE)
        # Ambiguous cases
        if any(kw in text for kw in ['adaptive', 'threshold', 'parameter', 'tuning']):
            patterns.append("UNCERTAIN_ADAPTIVE")
            return 'D', 'LOW', 'Unclear if novel or standard (manual review needed)', patterns

        # Generic implementation without clear algorithmic content
        if len(text) < 50:  # Very short description
            patterns.append("VAGUE_DESCRIPTION")
            return 'D', 'LOW', 'Insufficient information (manual review needed)', patterns

        # Default: Uncertain
        patterns.append("UNCLASSIFIED")
        return 'D', 'LOW', 'Could not classify (manual review needed)', patterns

    def generate_report(self, output_file: Path) -> None:
        """Generate triage report."""
        # Group by category
        by_category = defaultdict(list)
        for result in self.results:
            by_category[result.category].append(result)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Claim Triage Report\n\n")
            f.write(f"**Total Claims:** {len(self.results)}\n\n")

            # Summary
            f.write("## Summary\n\n")
            f.write("| Category | Count | Percentage | Needs Citation |\n")
            f.write("|----------|-------|------------|----------------|\n")
            for cat in ['A', 'B', 'C', 'D']:
                count = len(by_category[cat])
                pct = count / len(self.results) * 100 if self.results else 0
                needs = "Yes" if cat in ['A', 'B'] else "No" if cat == 'C' else "TBD"
                f.write(f"| {cat} | {count} | {pct:.1f}% | {needs} |\n")
            f.write("\n")

            # Category descriptions
            f.write("## Category Descriptions\n\n")
            f.write("- **Category A:** Algorithmic theory (requires peer-reviewed citation)\n")
            f.write("- **Category B:** Foundational concepts (requires textbook citation)\n")
            f.write("- **Category C:** Pure implementation (no citation needed)\n")
            f.write("- **Category D:** Uncertain (manual review required)\n\n")

            # Detailed results
            for cat in ['A', 'B', 'C', 'D']:
                if not by_category[cat]:
                    continue

                f.write(f"## Category {cat} ({len(by_category[cat])} claims)\n\n")

                # Group by rationale
                by_rationale = defaultdict(list)
                for result in by_category[cat]:
                    by_rationale[result.rationale].append(result)

                for rationale, results in sorted(by_rationale.items()):
                    f.write(f"### {rationale} ({len(results)} claims)\n\n")
                    for result in results[:5]:  # Show first 5
                        f.write(f"- {result.claim_id} (confidence: {result.confidence})\n")
                    if len(results) > 5:
                        f.write(f"- ... and {len(results)-5} more\n")
                    f.write("\n")

            # Action items
            f.write("## Action Items\n\n")
            f.write(f"1. **Category A ({len(by_category['A'])} claims):** Research peer-reviewed citations\n")
            f.write(f"2. **Category B ({len(by_category['B'])} claims):** Research textbook citations\n")
            f.write(f"3. **Category C ({len(by_category['C'])} claims):** Mark 'no citation needed' in CSV\n")
            f.write(f"4. **Category D ({len(by_category['D'])} claims):** Manual code review to determine category\n\n")

        print(f"\nTriage report generated: {output_file}")

    def export_json(self, output_file: Path) -> None:
        """Export triage results to JSON."""
        data = {
            'batch_id': self.batch_dir.name,
            'total_claims': len(self.results),
            'summary': {
                cat: len([r for r in self.results if r.category == cat])
                for cat in ['A', 'B', 'C', 'D']
            },
            'results': [
                {
                    'claim_id': r.claim_id,
                    'category': r.category,
                    'confidence': r.confidence,
                    'rationale': r.rationale,
                    'needs_citation': r.needs_citation,
                    'suggested_action': r.suggested_action,
                    'detected_patterns': r.detected_patterns
                }
                for r in self.results
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"JSON export complete: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Triage claims for citation necessity')
    parser.add_argument('--batch', required=True, help='Batch directory name (e.g., 08_HIGH_implementation_general)')
    parser.add_argument('--output', default='triage_report.md', help='Output report filename')
    args = parser.parse_args()

    batch_dir = Path(f"D:/Projects/main/artifacts/research_batches/{args.batch}")
    if not batch_dir.exists():
        print(f"ERROR: Batch directory not found: {batch_dir}")
        return

    triager = ClaimTriager(batch_dir)
    triager.triage_all_claims()

    # Generate reports
    report_file = batch_dir / args.output
    json_file = batch_dir / "claims_triaged.json"

    triager.generate_report(report_file)
    triager.export_json(json_file)

    print("\n" + "="*70)
    print("TRIAGE SUMMARY")
    print("="*70)

    summary = {cat: len([r for r in triager.results if r.category == cat]) for cat in ['A', 'B', 'C', 'D']}
    print(f"Category A (requires citation): {summary['A']}")
    print(f"Category B (requires citation): {summary['B']}")
    print(f"Category C (no citation needed): {summary['C']}")
    print(f"Category D (manual review): {summary['D']}")
    print(f"\nTotal requiring citations: {summary['A'] + summary['B']}")
    print(f"Total NOT requiring citations: {summary['C']}")
    print("="*70)


if __name__ == "__main__":
    main()
