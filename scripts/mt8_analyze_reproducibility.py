#!/usr/bin/env python
"""
MT-8 Reproducibility Analysis: Statistical Validation of PSO Optimization
================================================================================

Analyzes reproducibility test results from multiple random seeds to compute:
- Fitness reproducibility (mean, std, CV)
- Gain reproducibility (mean, std, RSD per parameter)
- Improvement reproducibility (comparison with original MT-8)
- Success criteria assessment

Generates a complete reproducibility report with pass/fail assessment.

Author: MT-8 Reproducibility Team
Created: December 15, 2025
"""

import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ControllerReproducibilityMetrics:
    """Reproducibility metrics for a single controller."""
    controller_name: str

    # Fitness metrics
    fitness_mean: float
    fitness_std: float
    fitness_cv: float  # Coefficient of variation (%)

    # Gain metrics (per parameter)
    gains_mean: List[float]
    gains_std: List[float]
    gains_rsd: List[float]  # Relative standard deviation (%)

    # Improvement metrics
    improvement_mean: float
    improvement_std: float
    baseline_cost_mean: float

    # Raw data from each seed
    fitness_values: List[float]
    gains_values: List[List[float]]
    improvement_values: List[float]
    seeds: List[int]

    # Pass/fail
    fitness_cv_pass: bool  # CV < 5%
    gains_rsd_pass: bool  # All RSD < 20%
    improvement_match_pass: bool  # Within ±10% of original MT-8


def load_reproducibility_results(
    seeds: List[int],
    prefix: str = "mt8_repro_seed"
) -> Dict[str, List[Dict]]:
    """
    Load reproducibility test results for all seeds.

    Args:
        seeds: List of random seeds used in testing
        prefix: File prefix for result files

    Returns:
        Dictionary mapping controller names to list of results (one per seed)
    """
    results = {
        'classical_smc': [],
        'sta_smc': [],
        'adaptive_smc': [],
        'hybrid_adaptive_sta_smc': []
    }

    for seed in seeds:
        for controller in results.keys():
            result_file = Path(f"optimization_results/{prefix}{seed}_{controller}.json")
            if result_file.exists():
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    results[controller].append(data)
                logger.info(f"Loaded: {result_file.name}")
            else:
                logger.warning(f"Missing result file: {result_file}")

    return results


def compute_reproducibility_metrics(
    controller_name: str,
    results: List[Dict],
    original_mt8_improvement: float
) -> ControllerReproducibilityMetrics:
    """
    Compute reproducibility metrics for a single controller.

    Args:
        controller_name: Name of controller
        results: List of optimization results (one per seed)
        original_mt8_improvement: Original MT-8 improvement percentage

    Returns:
        ControllerReproducibilityMetrics with statistical analysis
    """
    # Extract data
    seeds = [r['random_seed'] for r in results]
    fitness_values = [r['robust_cost'] for r in results]
    gains_values = [r['gains'] for r in results]
    improvement_values = [r['improvement_pct'] for r in results]
    baseline_costs = [r['baseline_cost'] for r in results]

    # Fitness metrics
    fitness_mean = np.mean(fitness_values)
    fitness_std = np.std(fitness_values, ddof=1)  # Sample std
    fitness_cv = (fitness_std / fitness_mean) * 100.0 if fitness_mean > 0 else 0.0

    # Gain metrics (per parameter)
    gains_array = np.array(gains_values)  # Shape: (n_seeds, n_gains)
    gains_mean = np.mean(gains_array, axis=0).tolist()
    gains_std = np.std(gains_array, axis=0, ddof=1).tolist()
    gains_rsd = [
        (std / mean) * 100.0 if mean != 0 else 0.0
        for mean, std in zip(gains_mean, gains_std)
    ]

    # Improvement metrics
    improvement_mean = np.mean(improvement_values)
    improvement_std = np.std(improvement_values, ddof=1)
    baseline_cost_mean = np.mean(baseline_costs)

    # Pass/fail criteria
    fitness_cv_pass = fitness_cv < 5.0
    gains_rsd_pass = all(rsd < 20.0 for rsd in gains_rsd)
    improvement_match_pass = abs(improvement_mean - original_mt8_improvement) / original_mt8_improvement * 100.0 < 10.0

    return ControllerReproducibilityMetrics(
        controller_name=controller_name,
        fitness_mean=fitness_mean,
        fitness_std=fitness_std,
        fitness_cv=fitness_cv,
        gains_mean=gains_mean,
        gains_std=gains_std,
        gains_rsd=gains_rsd,
        improvement_mean=improvement_mean,
        improvement_std=improvement_std,
        baseline_cost_mean=baseline_cost_mean,
        fitness_values=fitness_values,
        gains_values=gains_values,
        improvement_values=improvement_values,
        seeds=seeds,
        fitness_cv_pass=fitness_cv_pass,
        gains_rsd_pass=gains_rsd_pass,
        improvement_match_pass=improvement_match_pass
    )


def generate_reproducibility_report(
    metrics: Dict[str, ControllerReproducibilityMetrics],
    original_mt8_improvements: Dict[str, float],
    output_file: str = "benchmarks/MT8_REPRODUCIBILITY_REPORT.md"
) -> None:
    """
    Generate complete reproducibility report.

    Args:
        metrics: Dictionary mapping controller names to reproducibility metrics
        original_mt8_improvements: Original MT-8 improvement percentages
        output_file: Output markdown file path
    """
    report = []

    # Header
    report.append("# MT-8 Reproducibility Validation Report")
    report.append("")
    report.append(f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("**Test Type:** PSO Optimization Reproducibility")
    report.append("**Seeds Tested:** 42, 123, 456 (N=3)")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")

    overall_pass = all(
        m.fitness_cv_pass and m.gains_rsd_pass and m.improvement_match_pass
        for m in metrics.values()
    )

    if overall_pass:
        report.append("**Status:** [OK] REPRODUCIBILITY VALIDATED")
        report.append("")
        report.append("All controllers passed reproducibility criteria:")
        report.append("- Fitness CV < 5% (acceptable variation)")
        report.append("- Gain RSD < 20% (consistent parameter values)")
        report.append("- Improvement within ±10% of original MT-8 results")
    else:
        report.append("**Status:** [WARNING] REPRODUCIBILITY CONCERNS DETECTED")
        report.append("")
        report.append("Some controllers failed reproducibility criteria. See detailed analysis below.")

    report.append("")
    report.append("---")
    report.append("")

    # Detailed Results by Controller
    report.append("## Detailed Reproducibility Results")
    report.append("")

    for controller_name, m in metrics.items():
        report.append(f"### {controller_name}")
        report.append("")

        # Status badge
        status = "[OK] PASS" if (m.fitness_cv_pass and m.gains_rsd_pass and m.improvement_match_pass) else "[WARNING] FAIL"
        report.append(f"**Overall Status:** {status}")
        report.append("")

        # Fitness reproducibility
        report.append("#### Fitness Reproducibility")
        report.append("")
        report.append(f"| Metric | Value | Criterion | Pass |")
        report.append(f"|--------|-------|-----------|------|")
        report.append(f"| Mean Fitness | {m.fitness_mean:.4f} | - | - |")
        report.append(f"| Std Deviation | {m.fitness_std:.4f} | - | - |")
        cv_pass_str = "[OK] PASS" if m.fitness_cv_pass else "[ERROR] FAIL"
        report.append(f"| Coefficient of Variation (CV) | {m.fitness_cv:.2f}% | < 5% | {cv_pass_str} |")
        report.append("")
        report.append(f"**Fitness by seed:** {', '.join([f'Seed {s}: {f:.4f}' for s, f in zip(m.seeds, m.fitness_values)])}")
        report.append("")

        # Gain reproducibility
        report.append("#### Gain Reproducibility")
        report.append("")
        report.append(f"| Parameter | Mean | Std | RSD | Pass |")
        report.append(f"|-----------|------|-----|-----|------|")
        for i, (mean, std, rsd) in enumerate(zip(m.gains_mean, m.gains_std, m.gains_rsd)):
            rsd_pass = "[OK] PASS" if rsd < 20.0 else "[ERROR] FAIL"
            report.append(f"| Gain {i+1} | {mean:.3f} | {std:.3f} | {rsd:.1f}% | {rsd_pass} |")
        report.append("")

        gains_pass_str = "[OK] PASS" if m.gains_rsd_pass else "[ERROR] FAIL"
        report.append(f"**All gains RSD < 20%:** {gains_pass_str}")
        report.append("")

        # Improvement reproducibility
        report.append("#### Improvement Reproducibility")
        report.append("")
        original_imp = original_mt8_improvements.get(controller_name, 0.0)
        deviation = abs(m.improvement_mean - original_imp) / original_imp * 100.0 if original_imp > 0 else 0.0
        imp_pass_str = "[OK] PASS" if m.improvement_match_pass else "[ERROR] FAIL"

        report.append(f"| Metric | Value |")
        report.append(f"|--------|-------|")
        report.append(f"| Mean Improvement | {m.improvement_mean:.2f}% |")
        report.append(f"| Std Deviation | {m.improvement_std:.2f}% |")
        report.append(f"| Original MT-8 Improvement | {original_imp:.2f}% |")
        report.append(f"| Deviation from Original | {deviation:.1f}% |")
        report.append(f"| Within ±10% of Original | {imp_pass_str} |")
        report.append("")
        report.append(f"**Improvement by seed:** {', '.join([f'Seed {s}: {i:.2f}%' for s, i in zip(m.seeds, m.improvement_values)])}")
        report.append("")
        report.append("---")
        report.append("")

    # Summary statistics
    report.append("## Summary Statistics")
    report.append("")

    avg_cv = np.mean([m.fitness_cv for m in metrics.values()])
    avg_improvement = np.mean([m.improvement_mean for m in metrics.values()])

    report.append(f"| Metric | Value |")
    report.append(f"|--------|-------|")
    report.append(f"| Average CV across controllers | {avg_cv:.2f}% |")
    report.append(f"| Average improvement (reproducibility test) | {avg_improvement:.2f}% |")
    report.append(f"| Original MT-8 average improvement | {np.mean(list(original_mt8_improvements.values())):.2f}% |")
    report.append("")

    # Pass/fail summary
    report.append("## Pass/Fail Summary")
    report.append("")
    report.append(f"| Controller | Fitness CV Pass | Gains RSD Pass | Improvement Match Pass | Overall |")
    report.append(f"|------------|-----------------|----------------|------------------------|---------|")
    for controller_name, m in metrics.items():
        cv_icon = "[OK]" if m.fitness_cv_pass else "[ERROR]"
        rsd_icon = "[OK]" if m.gains_rsd_pass else "[ERROR]"
        imp_icon = "[OK]" if m.improvement_match_pass else "[ERROR]"
        overall_icon = "[OK]" if (m.fitness_cv_pass and m.gains_rsd_pass and m.improvement_match_pass) else "[ERROR]"
        report.append(f"| {controller_name} | {cv_icon} | {rsd_icon} | {imp_icon} | {overall_icon} |")
    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")

    if overall_pass:
        report.append("### Reproducibility Validated [OK]")
        report.append("")
        report.append("1. **Document reproducibility** in LT-7 research paper as evidence of robust methodology")
        report.append("2. **Use mean gains** across seeds as \"ensemble\" production gains (optional)")
        report.append("3. **Cite this validation** in research publications as methodological rigor")
        report.append("4. **Maintain current PSO parameters** (30 particles, 50 iterations)")
    else:
        report.append("### Reproducibility Concerns Detected [WARNING]")
        report.append("")
        report.append("Controllers with failures:")
        for controller_name, m in metrics.items():
            if not (m.fitness_cv_pass and m.gains_rsd_pass and m.improvement_match_pass):
                report.append(f"- **{controller_name}:** ", end="")
                issues = []
                if not m.fitness_cv_pass:
                    issues.append(f"High CV ({m.fitness_cv:.1f}%)")
                if not m.gains_rsd_pass:
                    issues.append("High gain RSD")
                if not m.improvement_match_pass:
                    issues.append("Improvement mismatch")
                report.append(", ".join(issues))
        report.append("")
        report.append("**Recommended actions:**")
        report.append("1. Run additional seeds (4-5 total) for tighter confidence bounds")
        report.append("2. Consider increasing PSO particles (50-100) or iterations (100-200)")
        report.append("3. Document PSO stochasticity as research finding")
        report.append("4. Use ensemble approach: run multiple seeds, select best or average")

    report.append("")
    report.append("---")
    report.append("")

    # Methodology
    report.append("## Methodology")
    report.append("")
    report.append("### Test Configuration")
    report.append("- **Seeds:** 42, 123, 456 (N=3)")
    report.append("- **PSO Algorithm:** PySwarms GlobalBestPSO")
    report.append("- **Particles:** 30")
    report.append("- **Iterations:** 50")
    report.append("- **Fitness Function:** 50% nominal + 50% disturbed")
    report.append("- **Disturbances:** Step (10N @ t=2s), Impulse (30N @ t=2s, 0.1s)")
    report.append("")
    report.append("### Success Criteria")
    report.append("1. **Fitness CV < 5%:** Acceptable variation for stochastic optimization")
    report.append("2. **Gain RSD < 20%:** PSO stochasticity expected, but gains should cluster")
    report.append("3. **Improvement within ±10% of original MT-8:** Validates original results")
    report.append("")
    report.append("### Statistical Definitions")
    report.append("- **CV (Coefficient of Variation):** (std / mean) × 100%")
    report.append("- **RSD (Relative Standard Deviation):** (std / mean) × 100% per parameter")
    report.append("- **Sample Standard Deviation:** Used (ddof=1) for unbiased estimates")
    report.append("")

    # References
    report.append("## References")
    report.append("")
    report.append("- **Original MT-8 Report:** `benchmarks/MT8_COMPLETE_REPORT.md`")
    report.append("- **Test Protocol:** `benchmarks/MT8_REPRODUCIBILITY_TEST_PROTOCOL.md`")
    report.append("- **Test Script:** `scripts/mt8_reproducibility_test.py`")
    report.append("- **Analysis Script:** `scripts/mt8_analyze_reproducibility.py`")
    report.append("")
    report.append("---")
    report.append("")
    report.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("**Status:** Reproducibility Validation Complete")

    # Write report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))

    logger.info(f"[OK] Reproducibility report saved: {output_path}")


def main():
    """Main analysis execution."""
    import argparse
    parser = argparse.ArgumentParser(description='MT-8: Reproducibility Analysis')
    parser.add_argument('--seeds', type=int, nargs='+', default=[42, 123, 456],
                        help='Random seeds to analyze')
    parser.add_argument('--prefix', type=str, default='mt8_repro_seed',
                        help='File prefix for result files')
    parser.add_argument('--output', type=str, default='benchmarks/MT8_REPRODUCIBILITY_REPORT.md',
                        help='Output report file')
    args = parser.parse_args()

    logger.info("="*80)
    logger.info("MT-8: Reproducibility Analysis")
    logger.info(f"Seeds: {args.seeds}")
    logger.info("="*80)

    # Original MT-8 improvements (from November 8, 2025)
    original_mt8_improvements = {
        'classical_smc': 2.15,
        'sta_smc': 1.38,
        'adaptive_smc': 0.47,
        'hybrid_adaptive_sta_smc': 21.39
    }

    # Load results
    logger.info("\nLoading reproducibility test results...")
    results = load_reproducibility_results(args.seeds, args.prefix)

    # Check if all results loaded
    for controller, res_list in results.items():
        if len(res_list) != len(args.seeds):
            logger.warning(f"{controller}: Expected {len(args.seeds)} results, got {len(res_list)}")

    # Compute metrics for each controller
    logger.info("\nComputing reproducibility metrics...")
    metrics = {}
    for controller_name, res_list in results.items():
        if len(res_list) == 0:
            logger.warning(f"Skipping {controller_name}: No results found")
            continue

        m = compute_reproducibility_metrics(
            controller_name,
            res_list,
            original_mt8_improvements[controller_name]
        )
        metrics[controller_name] = m
        logger.info(f"  {controller_name}: CV={m.fitness_cv:.2f}%, Mean Improvement={m.improvement_mean:.2f}%")

    # Generate report
    logger.info("\nGenerating reproducibility report...")
    generate_reproducibility_report(metrics, original_mt8_improvements, args.output)

    # Print summary
    logger.info(f"\n{'='*80}")
    logger.info("ANALYSIS COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"\nReport saved: {args.output}")
    logger.info("\nQuick Summary:")
    for controller_name, m in metrics.items():
        status = "[OK]" if (m.fitness_cv_pass and m.gains_rsd_pass and m.improvement_match_pass) else "[WARNING]"
        logger.info(f"  {controller_name}: {status} (CV={m.fitness_cv:.1f}%, Improvement={m.improvement_mean:.1f}%)")
    logger.info(f"{'='*80}")


if __name__ == '__main__':
    main()
