"""Aggregate statistics from 10 PSO runs for Table II.

Computes mean, std, min, max, 95% CI for:
- Final fitness
- Convergence iteration
- Optimized epsilon_min
- Optimized alpha

Usage:
    python aggregate_pso_stats.py
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def compute_stats(values):
    """Compute mean, std, min, max, 95% CI for a list of values.

    Args:
        values: List or array of numeric values

    Returns:
        dict: Statistics dictionary
    """
    values = np.array(values)
    mean = np.mean(values)
    std = np.std(values, ddof=1)  # Sample standard deviation
    min_val = np.min(values)
    max_val = np.max(values)

    # 95% confidence interval (t-distribution, df=n-1)
    n = len(values)
    se = std / np.sqrt(n)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)

    return {
        'mean': float(mean),
        'std': float(std),
        'min': float(min_val),
        'max': float(max_val),
        'ci_lower': float(ci[0]),
        'ci_upper': float(ci[1]),
        'n_samples': int(n)
    }


def aggregate_pso_results(results_dir=None):
    """Aggregate 10 PSO runs into Table II statistics.

    Args:
        results_dir: Directory containing results_seed*.json files
                    (default: .artifacts/LT7_research_paper/experiments/results)

    Returns:
        dict: Table II statistics
    """
    if results_dir is None:
        results_dir = Path(".artifacts/LT7_research_paper/experiments/results")
    else:
        results_dir = Path(results_dir)

    logger.info("=" * 80)
    logger.info("Aggregating PSO Statistics (Table II)")
    logger.info("=" * 80)

    seeds = [42, 123, 456, 789, 1011, 1314, 1617, 1920, 2223, 2526]

    final_fitness = []
    convergence_iters = []
    eps_min_opt = []
    alpha_opt = []

    logger.info(f"\nReading results from: {results_dir}")

    for seed in seeds:
        result_file = results_dir / f"results_seed{seed}.json"

        if not result_file.exists():
            logger.warning(f"  Missing: results_seed{seed}.json (skipping)")
            continue

        with open(result_file) as f:
            data = json.load(f)

        final_fitness.append(data['final_fitness'])
        convergence_iters.append(data['convergence_iteration'])
        eps_min_opt.append(data['optimized_eps_min'])
        alpha_opt.append(data['optimized_alpha'])

        logger.info(f"  Loaded: seed={seed}, fitness={data['final_fitness']:.4f}")

    logger.info(f"\nTotal runs loaded: {len(final_fitness)}")

    if len(final_fitness) == 0:
        logger.error("No results found! Run PSO optimization first.")
        return None

    # Compute statistics
    table_ii = {
        'final_fitness': compute_stats(final_fitness),
        'convergence_iter': compute_stats(convergence_iters),
        'eps_min_opt': compute_stats(eps_min_opt),
        'alpha_opt': compute_stats(alpha_opt),
        'seeds': seeds[:len(final_fitness)]
    }

    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("TABLE II: PSO CONVERGENCE STATISTICS ({} runs)".format(len(final_fitness)))
    logger.info("=" * 80)

    for metric_name, metric_key in [
        ('Final Fitness', 'final_fitness'),
        ('Convergence Iteration', 'convergence_iter'),
        ('Optimized ε_min', 'eps_min_opt'),
        ('Optimized α', 'alpha_opt')
    ]:
        stats_dict = table_ii[metric_key]
        logger.info(f"\n{metric_name}:")
        logger.info(f"  Mean: {stats_dict['mean']:.6f}")
        logger.info(f"  Std Dev: {stats_dict['std']:.6f}")
        logger.info(f"  Min: {stats_dict['min']:.6f}")
        logger.info(f"  Max: {stats_dict['max']:.6f}")
        logger.info(f"  95% CI: [{stats_dict['ci_lower']:.6f}, {stats_dict['ci_upper']:.6f}]")

    # Print LaTeX table
    logger.info("\n" + "=" * 80)
    logger.info("LATEX TABLE II")
    logger.info("=" * 80)
    logger.info("\\begin{table}[h]")
    logger.info("\\centering")
    logger.info("\\caption{PSO Convergence Statistics (10 runs)}")
    logger.info("\\label{tab:pso_stats}")
    logger.info("\\begin{tabular}{lcccc}")
    logger.info("\\hline")
    logger.info("Metric & Mean & Std Dev & Min & Max \\\\")
    logger.info("\\hline")

    f = table_ii['final_fitness']
    logger.info(f"Final Fitness & {f['mean']:.2f} & {f['std']:.2f} & {f['min']:.2f} & {f['max']:.2f} \\\\")

    c = table_ii['convergence_iter']
    logger.info(f"Convergence Iter & {c['mean']:.1f} & {c['std']:.1f} & {int(c['min'])} & {int(c['max'])} \\\\")

    e = table_ii['eps_min_opt']
    logger.info(f"$\\epsilon_{{\\min}}^*$ & {e['mean']:.5f} & {e['std']:.5f} & {e['min']:.5f} & {e['max']:.5f} \\\\")

    a = table_ii['alpha_opt']
    logger.info(f"$\\alpha^*$ & {a['mean']:.3f} & {a['std']:.3f} & {a['min']:.3f} & {a['max']:.3f} \\\\")

    logger.info("\\hline")
    logger.info("\\end{tabular}")
    logger.info("\\end{table}")

    return table_ii


def main():
    """Main entry point."""
    results_dir = Path(".artifacts/LT7_research_paper/experiments/results")

    # Aggregate statistics
    table_ii = aggregate_pso_results(results_dir)

    if table_ii is not None:
        # Save Table II
        output_file = results_dir / "table_ii_pso_statistics.json"
        with open(output_file, 'w') as f:
            json.dump(table_ii, f, indent=2)

        logger.info(f"\n\nTable II saved to: {output_file}")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
