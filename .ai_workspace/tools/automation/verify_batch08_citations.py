#!/usr/bin/env python3
"""
Comprehensive Batch 08 Citation Verification Tool

Systematically verifies all 314 citations by:
1. Reading actual source code context
2. Analyzing implementation content
3. Comparing against claimed citations
4. Identifying mismatches
5. Suggesting corrected citations
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class ClaimAnalysis:
    """Analysis results for a single claim."""
    claim_id: str
    file_path: str
    line_number: int
    context: str
    source_code: str = ""

    # Citation information
    claimed_citation: str = ""
    claimed_bibtex: str = ""

    # Analysis results
    actual_topic: str = ""
    confidence: str = "LOW"  # LOW, MEDIUM, HIGH
    is_mismatch: bool = False
    mismatch_severity: str = ""  # MINOR, MODERATE, SEVERE, CRITICAL

    # Recommendations
    suggested_citation: str = ""
    suggested_bibtex: str = ""
    rationale: str = ""

    # Code analysis
    detected_patterns: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


class CitationVerifier:
    """Verifies citations against actual code implementations."""

    def __init__(self, batch_dir: Path):
        self.batch_dir = batch_dir
        self.claims_file = batch_dir / "claims.json"
        self.sources_file = batch_dir / "chatgpt_sources.md"
        self.project_root = Path("D:/Projects/main")

        # Load citation mappings from chatgpt_sources.md
        self.citation_map = self._load_citation_mappings()

        # Results
        self.analyses: List[ClaimAnalysis] = []
        self.mismatch_count = 0
        self.severe_mismatch_count = 0

    def _load_citation_mappings(self) -> Dict[str, List[str]]:
        """Load citation-to-claims mapping from chatgpt_sources.md"""
        mapping = {
            'stone1978cross': ['CODE-IMPL-002', 'CODE-IMPL-003', 'CODE-IMPL-004', 'CODE-IMPL-005', 'CODE-IMPL-007',
                               'CODE-IMPL-214', 'CODE-IMPL-215', 'CODE-IMPL-216', 'CODE-IMPL-217', 'CODE-IMPL-218'],
            'barnett1994outliers': ['CODE-IMPL-012', 'CODE-IMPL-013', 'CODE-IMPL-014', 'CODE-IMPL-015', 'CODE-IMPL-016',
                                   'CODE-IMPL-219', 'CODE-IMPL-220', 'CODE-IMPL-221', 'CODE-IMPL-222', 'CODE-IMPL-223'],
            'efron1993bootstrap': ['CODE-IMPL-029', 'CODE-IMPL-032', 'CODE-IMPL-047', 'CODE-IMPL-052',
                                  'CODE-IMPL-224', 'CODE-IMPL-225', 'CODE-IMPL-226', 'CODE-IMPL-227', 'CODE-IMPL-228'],
            'demsar2006statistical': ['CODE-IMPL-053', 'CODE-IMPL-054', 'CODE-IMPL-055', 'CODE-IMPL-056', 'CODE-IMPL-057',
                                     'CODE-IMPL-229', 'CODE-IMPL-230', 'CODE-IMPL-231', 'CODE-IMPL-232', 'CODE-IMPL-233'],
            'wilcoxon1945individual': ['CODE-IMPL-058', 'CODE-IMPL-059', 'CODE-IMPL-060', 'CODE-IMPL-061', 'CODE-IMPL-062',
                                      'CODE-IMPL-234', 'CODE-IMPL-235', 'CODE-IMPL-236', 'CODE-IMPL-237', 'CODE-IMPL-238'],
            'shapiro1965analysis': ['CODE-IMPL-063', 'CODE-IMPL-064', 'CODE-IMPL-066', 'CODE-IMPL-068', 'CODE-IMPL-069',
                                   'CODE-IMPL-239', 'CODE-IMPL-240', 'CODE-IMPL-241', 'CODE-IMPL-242', 'CODE-IMPL-243'],
            'pearson1895note': ['CODE-IMPL-073', 'CODE-IMPL-074', 'CODE-IMPL-075', 'CODE-IMPL-077', 'CODE-IMPL-078',
                               'CODE-IMPL-244', 'CODE-IMPL-245', 'CODE-IMPL-246', 'CODE-IMPL-247', 'CODE-IMPL-248'],
            'cohen1988statistical': ['CODE-IMPL-079', 'CODE-IMPL-080', 'CODE-IMPL-081', 'CODE-IMPL-082', 'CODE-IMPL-083',
                                    'CODE-IMPL-249', 'CODE-IMPL-251', 'CODE-IMPL-252', 'CODE-IMPL-254'],
            'utkin1977variable': ['CODE-IMPL-085', 'CODE-IMPL-086', 'CODE-IMPL-090', 'CODE-IMPL-091', 'CODE-IMPL-106',
                                 'CODE-IMPL-255', 'CODE-IMPL-256', 'CODE-IMPL-257', 'CODE-IMPL-258', 'CODE-IMPL-259'],
            'levant2003higher': ['CODE-IMPL-107', 'CODE-IMPL-108', 'CODE-IMPL-109', 'CODE-IMPL-110', 'CODE-IMPL-111',
                                'CODE-IMPL-260', 'CODE-IMPL-261', 'CODE-IMPL-262', 'CODE-IMPL-263', 'CODE-IMPL-264'],
            'clerc2002particle': ['CODE-IMPL-114', 'CODE-IMPL-115', 'CODE-IMPL-117', 'CODE-IMPL-120', 'CODE-IMPL-121',
                                 'CODE-IMPL-265', 'CODE-IMPL-266', 'CODE-IMPL-267', 'CODE-IMPL-268', 'CODE-IMPL-269'],
            'storn1997differential': ['CODE-IMPL-122', 'CODE-IMPL-123', 'CODE-IMPL-132', 'CODE-IMPL-134', 'CODE-IMPL-135',
                                     'CODE-IMPL-270', 'CODE-IMPL-271', 'CODE-IMPL-272', 'CODE-IMPL-273', 'CODE-IMPL-274'],
            'nelder1965simplex': ['CODE-IMPL-146', 'CODE-IMPL-147', 'CODE-IMPL-150', 'CODE-IMPL-152', 'CODE-IMPL-155',
                                 'CODE-IMPL-275', 'CODE-IMPL-276', 'CODE-IMPL-277', 'CODE-IMPL-278', 'CODE-IMPL-279'],
            'nocedal2006numerical': ['CODE-IMPL-156', 'CODE-IMPL-157', 'CODE-IMPL-158', 'CODE-IMPL-159', 'CODE-IMPL-167',
                                    'CODE-IMPL-280', 'CODE-IMPL-281', 'CODE-IMPL-282', 'CODE-IMPL-283', 'CODE-IMPL-285'],
            'goldberg1989genetic': ['CODE-IMPL-168', 'CODE-IMPL-169', 'CODE-IMPL-173', 'CODE-IMPL-174', 'CODE-IMPL-175',
                                   'CODE-IMPL-286', 'CODE-IMPL-288', 'CODE-IMPL-289', 'CODE-IMPL-290', 'CODE-IMPL-291',
                                   'CODE-IMPL-292', 'CODE-IMPL-293'],
            'deb2001multiobjective': ['CODE-IMPL-178', 'CODE-IMPL-180', 'CODE-IMPL-181', 'CODE-IMPL-182', 'CODE-IMPL-183',
                                     'CODE-IMPL-294', 'CODE-IMPL-295', 'CODE-IMPL-296', 'CODE-IMPL-297', 'CODE-IMPL-298',
                                     'CODE-IMPL-335'],
            'camacho2013model': ['CODE-IMPL-186', 'CODE-IMPL-189', 'CODE-IMPL-190', 'CODE-IMPL-191', 'CODE-IMPL-192',
                                'CODE-IMPL-299', 'CODE-IMPL-300', 'CODE-IMPL-301', 'CODE-IMPL-302', 'CODE-IMPL-303'],
            'hairer1993solving': ['CODE-IMPL-193', 'CODE-IMPL-194', 'CODE-IMPL-195', 'CODE-IMPL-201', 'CODE-IMPL-204',
                                 'CODE-IMPL-304', 'CODE-IMPL-308', 'CODE-IMPL-312', 'CODE-IMPL-321', 'CODE-IMPL-322', 'CODE-IMPL-457'],
            'ogata2010modern': ['CODE-IMPL-206', 'CODE-IMPL-207', 'CODE-IMPL-209', 'CODE-IMPL-210', 'CODE-IMPL-213',
                               'CODE-IMPL-323', 'CODE-IMPL-325', 'CODE-IMPL-326', 'CODE-IMPL-327', 'CODE-IMPL-328'],
        }
        return mapping

    def _read_source_code(self, file_path: str, line_number: int, context_lines: int = 20) -> str:
        """Read source code around the specified line."""
        try:
            # Convert Windows path to Path object
            source_file = self.project_root / file_path.replace('\\', '/')
            if not source_file.exists():
                return f"[FILE NOT FOUND: {source_file}]"

            with open(source_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            start = max(0, line_number - context_lines)
            end = min(len(lines), line_number + context_lines)

            code_snippet = ''.join(lines[start:end])
            return code_snippet

        except Exception as e:
            return f"[ERROR READING FILE: {e}]"

    def _analyze_code_content(self, code: str, context: str, file_path: str) -> Tuple[str, List[str], str]:
        """Analyze code to determine actual topic and patterns."""
        code_lower = code.lower()
        context_lower = context.lower()
        path_lower = file_path.lower()

        patterns = []
        confidence = "LOW"

        # Statistical analysis patterns
        if any(kw in code_lower or kw in context_lower for kw in ['cross-validation', 'k-fold', 'kfold', 'train_test_split', 'validation']):
            patterns.append("CROSS_VALIDATION")
            confidence = "HIGH"
            return "Cross-Validation", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['outlier', 'iqr', 'z-score', 'percentile', 'quartile']):
            patterns.append("OUTLIER_DETECTION")
            confidence = "HIGH"
            return "Outlier Detection", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['bootstrap', 'resample', 'confidence interval']):
            patterns.append("BOOTSTRAP")
            confidence = "HIGH"
            return "Bootstrap Methods", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['wilcoxon', 'mann-whitney', 'rank-sum', 'non-parametric']):
            patterns.append("NONPARAMETRIC_TESTS")
            confidence = "HIGH"
            return "Non-parametric Tests", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['shapiro', 'normality', 'normal distribution']):
            patterns.append("NORMALITY_TESTING")
            confidence = "HIGH"
            return "Normality Testing", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['correlation', 'pearson', 'spearman']):
            patterns.append("CORRELATION")
            confidence = "HIGH"
            return "Correlation Analysis", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['effect size', 'cohen']):
            patterns.append("EFFECT_SIZE")
            confidence = "HIGH"
            return "Effect Size Analysis", patterns, confidence

        # Control theory patterns
        if any(kw in code_lower or kw in context_lower for kw in ['sliding mode', 'smc', 'sliding surface', 'reaching law']):
            patterns.append("SLIDING_MODE_CONTROL")
            confidence = "HIGH"
            return "Sliding Mode Control", patterns, confidence

        # Super-twisting requires explicit mention, not just Python's super()
        # Check file path AND explicit keywords to avoid false positives from super().__init__()
        is_super_twisting_file = 'super_twisting' in path_lower or 'sta_smc' in path_lower
        has_super_twisting_keyword = any(kw in code_lower or kw in context_lower
                                         for kw in ['super-twisting', 'super twisting', 'twisting algorithm', 'sta algorithm'])

        if is_super_twisting_file or (has_super_twisting_keyword and 'super()' not in code):
            patterns.append("SUPER_TWISTING")
            confidence = "HIGH"
            return "Super-Twisting Algorithm", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['mpc', 'model predictive', 'receding horizon']):
            patterns.append("MODEL_PREDICTIVE_CONTROL")
            confidence = "HIGH"
            return "Model Predictive Control", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['lyapunov', 'stability', 'convergence']):
            patterns.append("STABILITY_ANALYSIS")
            confidence = "MEDIUM"
            return "Stability Analysis", patterns, confidence

        # Optimization patterns
        if any(kw in code_lower or kw in context_lower for kw in ['pso', 'particle swarm', 'swarm']):
            patterns.append("PARTICLE_SWARM")
            confidence = "HIGH"
            return "Particle Swarm Optimization", patterns, confidence

        # Genetic algorithm requires file path OR strong keywords (avoid false positives from "population" alone)
        is_genetic_file = 'genetic' in path_lower or 'evolutionary' in path_lower
        has_ga_keywords = any(kw in code_lower or kw in context_lower
                              for kw in ['genetic algorithm', 'mutation', 'crossover', 'chromosome', 'fitness function'])

        if is_genetic_file or has_ga_keywords:
            patterns.append("GENETIC_ALGORITHM")
            confidence = "HIGH"
            return "Genetic Algorithm", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['differential evolution', 'de algorithm']):
            patterns.append("DIFFERENTIAL_EVOLUTION")
            confidence = "HIGH"
            return "Differential Evolution", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['nelder-mead', 'simplex method', 'simplex']):
            patterns.append("SIMPLEX_METHOD")
            confidence = "HIGH"
            return "Simplex Method", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['bfgs', 'gradient descent', 'quasi-newton']):
            patterns.append("GRADIENT_OPTIMIZATION")
            confidence = "HIGH"
            return "Gradient-Based Optimization", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['multi-objective', 'pareto', 'nsga']):
            patterns.append("MULTIOBJECTIVE")
            confidence = "HIGH"
            return "Multi-Objective Optimization", patterns, confidence

        # Numerical methods
        if any(kw in code_lower or kw in context_lower for kw in ['euler', 'runge-kutta', 'rk4', 'integration', 'integrator']):
            patterns.append("NUMERICAL_INTEGRATION")
            confidence = "HIGH"
            return "Numerical Integration", patterns, confidence

        # Software patterns
        if any(kw in code_lower or kw in context_lower for kw in ['factory', 'factory pattern', 'create_controller']):
            patterns.append("FACTORY_PATTERN")
            confidence = "MEDIUM"
            return "Software Design Pattern", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['threading', 'thread', 'lock', 'deadlock']):
            patterns.append("CONCURRENCY")
            confidence = "MEDIUM"
            return "Concurrency/Threading", patterns, confidence

        if any(kw in code_lower or kw in context_lower for kw in ['serialize', 'to_dict', 'from_dict', 'json']):
            patterns.append("SERIALIZATION")
            confidence = "MEDIUM"
            return "Serialization", patterns, confidence

        # Benchmarking/simulation
        if any(kw in code_lower or kw in context_lower for kw in ['trial', 'benchmark', 'simulation', 'monte carlo']):
            patterns.append("BENCHMARKING")
            confidence = "MEDIUM"
            return "Benchmarking/Simulation", patterns, confidence

        # Default
        patterns.append("UNKNOWN")
        return "Unknown/General Implementation", patterns, "LOW"

    def _determine_citation_mismatch(self, claim_id: str, actual_topic: str, confidence: str) -> Tuple[bool, str, str]:
        """Determine if citation is a mismatch and severity."""
        # Find which citation was claimed
        claimed_bibtex = None
        for bibtex, claim_ids in self.citation_map.items():
            if claim_id in claim_ids:
                claimed_bibtex = bibtex
                break

        if not claimed_bibtex:
            return False, "", "UNKNOWN_CLAIM"

        # Citation topic mappings
        citation_topics = {
            'stone1978cross': 'Cross-Validation',
            'barnett1994outliers': 'Outlier Detection',
            'efron1993bootstrap': 'Bootstrap Methods',
            'demsar2006statistical': 'Statistical Comparison',
            'wilcoxon1945individual': 'Non-parametric Tests',
            'shapiro1965analysis': 'Normality Testing',
            'pearson1895note': 'Correlation Analysis',
            'cohen1988statistical': 'Effect Size Analysis',
            'utkin1977variable': 'Sliding Mode Control',
            'levant2003higher': 'Super-Twisting Algorithm',
            'clerc2002particle': 'Particle Swarm Optimization',
            'storn1997differential': 'Differential Evolution',
            'nelder1965simplex': 'Simplex Method',
            'nocedal2006numerical': 'Gradient-Based Optimization',
            'goldberg1989genetic': 'Genetic Algorithm',
            'deb2001multiobjective': 'Multi-Objective Optimization',
            'camacho2013model': 'Model Predictive Control',
            'hairer1993solving': 'Numerical Integration',
            'ogata2010modern': 'Control Engineering',
        }

        claimed_topic = citation_topics.get(claimed_bibtex, "Unknown")

        # Check for mismatch
        is_mismatch = False
        severity = ""

        if confidence == "LOW":
            return False, claimed_bibtex, "UNCERTAIN"

        # Exact match
        if actual_topic.lower() in claimed_topic.lower() or claimed_topic.lower() in actual_topic.lower():
            return False, claimed_bibtex, ""

        # Critical mismatches (control theory vs software patterns)
        if actual_topic in ["Software Design Pattern", "Concurrency/Threading", "Serialization"] and \
           claimed_topic in ["Sliding Mode Control", "Super-Twisting Algorithm", "Model Predictive Control"]:
            return True, claimed_bibtex, "CRITICAL"

        # High severity (different methodologies)
        if actual_topic == "Cross-Validation" and claimed_topic == "Normality Testing":
            return True, claimed_bibtex, "SEVERE"

        if actual_topic == "Outlier Detection" and claimed_topic == "Bootstrap Methods":
            return True, claimed_bibtex, "SEVERE"

        if actual_topic == "Numerical Integration" and claimed_topic == "Particle Swarm Optimization":
            return True, claimed_bibtex, "SEVERE"

        if actual_topic == "Super-Twisting Algorithm" and claimed_topic == "Genetic Algorithm":
            return True, claimed_bibtex, "SEVERE"

        if actual_topic == "Sliding Mode Control" and claimed_topic == "Model Predictive Control":
            return True, claimed_bibtex, "SEVERE"

        # Moderate mismatches (related but different)
        if actual_topic in ["Benchmarking/Simulation", "Unknown/General Implementation"] and \
           claimed_topic in ["Sliding Mode Control", "Super-Twisting Algorithm"]:
            return True, claimed_bibtex, "MODERATE"

        # Default moderate for other mismatches
        return True, claimed_bibtex, "MODERATE"

    def verify_all_claims(self) -> None:
        """Verify all 314 claims."""
        print(f"Loading claims from {self.claims_file}...")
        with open(self.claims_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        claims = data['claims']
        print(f"Loaded {len(claims)} claims\n")

        for i, claim in enumerate(claims, 1):
            claim_id = claim['id']
            file_path = claim['file_path']
            line_number = int(claim['line_number'])
            context = claim['context']

            # Read source code
            source_code = self._read_source_code(file_path, line_number)

            # Analyze content
            actual_topic, patterns, confidence = self._analyze_code_content(source_code, context, file_path)

            # Determine mismatch
            is_mismatch, claimed_bibtex, severity = self._determine_citation_mismatch(claim_id, actual_topic, confidence)

            # Create analysis
            analysis = ClaimAnalysis(
                claim_id=claim_id,
                file_path=file_path,
                line_number=line_number,
                context=context,
                source_code=source_code[:500],  # First 500 chars
                claimed_bibtex=claimed_bibtex,
                actual_topic=actual_topic,
                confidence=confidence,
                is_mismatch=is_mismatch,
                mismatch_severity=severity,
                detected_patterns=patterns
            )

            self.analyses.append(analysis)

            if is_mismatch:
                self.mismatch_count += 1
                if severity in ["SEVERE", "CRITICAL"]:
                    self.severe_mismatch_count += 1

            # Progress indicator
            if i % 50 == 0:
                print(f"Processed {i}/{len(claims)} claims... (Mismatches: {self.mismatch_count})")

        print(f"\nVerification complete!")
        print(f"Total claims: {len(claims)}")
        print(f"Total mismatches: {self.mismatch_count}")
        print(f"Severe/Critical mismatches: {self.severe_mismatch_count}")

    def generate_report(self, output_file: Path) -> None:
        """Generate detailed mismatch report."""
        print(f"\nGenerating report to {output_file}...")

        # Group by severity
        critical = [a for a in self.analyses if a.mismatch_severity == "CRITICAL"]
        severe = [a for a in self.analyses if a.mismatch_severity == "SEVERE"]
        moderate = [a for a in self.analyses if a.mismatch_severity == "MODERATE"]
        correct = [a for a in self.analyses if not a.is_mismatch and a.confidence in ["HIGH", "MEDIUM"]]
        uncertain = [a for a in self.analyses if a.confidence == "LOW" or a.mismatch_severity == "UNCERTAIN"]

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Batch 08 Citation Verification Report\n\n")
            f.write(f"**Generated:** {Path(__file__).name}\n")
            f.write(f"**Total Claims Analyzed:** {len(self.analyses)}\n\n")

            f.write("## Executive Summary\n\n")
            f.write(f"- **✅ Correct Citations:** {len(correct)} ({len(correct)/len(self.analyses)*100:.1f}%)\n")
            f.write(f"- **❌ Total Mismatches:** {self.mismatch_count} ({self.mismatch_count/len(self.analyses)*100:.1f}%)\n")
            f.write(f"  - **CRITICAL:** {len(critical)}\n")
            f.write(f"  - **SEVERE:** {len(severe)}\n")
            f.write(f"  - **MODERATE:** {len(moderate)}\n")
            f.write(f"- **❓ Uncertain:** {len(uncertain)} ({len(uncertain)/len(self.analyses)*100:.1f}%)\n\n")

            f.write("---\n\n")

            # Critical mismatches
            if critical:
                f.write("## 🚨 CRITICAL Mismatches\n\n")
                f.write("Control theory papers cited for software implementation patterns:\n\n")
                for a in critical:
                    f.write(f"### {a.claim_id}\n")
                    f.write(f"- **File:** `{a.file_path}:{a.line_number}`\n")
                    f.write(f"- **Claimed Citation:** `{a.claimed_bibtex}`\n")
                    f.write(f"- **Actual Topic:** {a.actual_topic}\n")
                    f.write(f"- **Context:** {a.context[:150]}...\n")
                    f.write(f"- **Patterns:** {', '.join(a.detected_patterns)}\n\n")
                f.write("\n---\n\n")

            # Severe mismatches
            if severe:
                f.write("## ❌ SEVERE Mismatches\n\n")
                f.write("Completely different methodologies:\n\n")
                for a in severe:
                    f.write(f"### {a.claim_id}\n")
                    f.write(f"- **File:** `{a.file_path}:{a.line_number}`\n")
                    f.write(f"- **Claimed Citation:** `{a.claimed_bibtex}`\n")
                    f.write(f"- **Actual Topic:** {a.actual_topic}\n")
                    f.write(f"- **Context:** {a.context[:150]}...\n")
                    f.write(f"- **Patterns:** {', '.join(a.detected_patterns)}\n\n")
                f.write("\n---\n\n")

            # Moderate mismatches (summary only)
            if moderate:
                f.write("## ⚠️ MODERATE Mismatches\n\n")
                f.write(f"Total: {len(moderate)} claims\n\n")

                # Group by topic
                by_topic = defaultdict(list)
                for a in moderate:
                    by_topic[a.actual_topic].append(a)

                for topic, items in sorted(by_topic.items()):
                    f.write(f"### {topic} ({len(items)} claims)\n")
                    for a in items[:3]:  # Show first 3
                        f.write(f"- {a.claim_id}: `{a.file_path}:{a.line_number}` (claimed: {a.claimed_bibtex})\n")
                    if len(items) > 3:
                        f.write(f"- ... and {len(items)-3} more\n")
                    f.write("\n")
                f.write("\n---\n\n")

            # Correct citations (summary)
            if correct:
                f.write("## ✅ Correct Citations\n\n")
                f.write(f"Total: {len(correct)} claims appear correctly cited\n\n")

                # Group by citation
                by_citation = defaultdict(list)
                for a in correct:
                    by_citation[a.claimed_bibtex].append(a)

                for citation, items in sorted(by_citation.items()):
                    f.write(f"### {citation} ({len(items)} claims)\n")
                    topics = set(a.actual_topic for a in items)
                    f.write(f"Topics: {', '.join(topics)}\n\n")

                f.write("\n---\n\n")

            # Uncertain
            if uncertain:
                f.write("## ❓ Uncertain / Low Confidence\n\n")
                f.write(f"Total: {len(uncertain)} claims require manual review\n\n")
                f.write("These claims could not be automatically classified with high confidence.\n")
                f.write("Manual source code review recommended.\n\n")

        print(f"Report generated: {output_file}")


def main():
    batch_dir = Path("D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general")
    output_report = batch_dir / "CITATION_VERIFICATION_REPORT.md"

    verifier = CitationVerifier(batch_dir)
    verifier.verify_all_claims()
    verifier.generate_report(output_report)

    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print(f"\nDetailed report: {output_report}")
    print(f"\nSummary:")
    print(f"  ✅ Likely correct: {len([a for a in verifier.analyses if not a.is_mismatch and a.confidence in ['HIGH', 'MEDIUM']])}")
    print(f"  ❌ Mismatches: {verifier.mismatch_count}")
    print(f"  🚨 Severe/Critical: {verifier.severe_mismatch_count}")
    print(f"  ❓ Uncertain: {len([a for a in verifier.analyses if a.confidence == 'LOW'])}")


if __name__ == "__main__":
    main()
