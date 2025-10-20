#!/usr/bin/env python3
"""
Generate Table II: PSO Optimization Statistics (10 runs)

Aggregates statistics from 10 PSO runs with different seeds and formats
as publication-ready LaTeX table.

Input:
    - .artifacts/LT7_research_paper/experiments/results/results_seed*.json (10 files)

Output:
    - .artifacts/LT7_research_paper/tables/table2_pso_stats.tex
    - Console preview of table
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict
import numpy as np
from scipy import stats as scipy_stats

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent.parent
EXPERIMENTS_DIR = REPO_ROOT / ".artifacts" / "LT7_research_paper" / "experiments"
RESULTS_DIR = EXPERIMENTS_DIR / "results"
TABLES_DIR = REPO_ROOT / ".artifacts" / "LT7_research_paper" / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = [42, 123, 456, 789, 1011, 1314, 1617, 1920, 2223, 2526]


def load_pso_results(seeds: list = SEEDS) -> Dict:
    """Load PSO results from all seed runs.

    Args:
        seeds: List of random seeds used

    Returns:
        Dictionary with aggregated data

    Raises:
        FileNotFoundError: If result files don't exist
    """
    results = {
        'epsilon_min': [],
        'alpha': [],
        'fitness': [],
        'convergence_iteration': [],
        'seeds_found': []
    }

    missing_seeds = []

    for seed in seeds:
        result_file = RESULTS_DIR / f"results_seed{seed}.json"

        if not result_file.exists():
            missing_seeds.append(seed)
            continue

        with open(result_file, 'r') as f:
            data = json.load(f)

        # Extract parameters (handle multiple JSON formats)
        epsilon_min = (data.get('optimized_eps_min') or
                      data.get('epsilon_min') or
                      data.get('best_params', {}).get('epsilon_min'))
        alpha = (data.get('optimized_alpha') or
                data.get('alpha') or
                data.get('best_params', {}).get('alpha'))
        fitness = data.get('final_fitness') or data.get('best_fitness')
        conv_iter = data.get('convergence_iteration') or data.get('n_iterations', 30)

        if epsilon_min is not None:
            results['epsilon_min'].append(epsilon_min)
        if alpha is not None:
            results['alpha'].append(alpha)
        if fitness is not None:
            results['fitness'].append(fitness)
        if conv_iter is not None:
            results['convergence_iteration'].append(conv_iter)

        results['seeds_found'].append(seed)

    if missing_seeds:
        print(f"[WARN] Missing results for seeds: {missing_seeds}")
        print(f"[INFO] Loaded {len(results['seeds_found'])}/10 runs")

    if len(results['seeds_found']) == 0:
        raise FileNotFoundError(
            "No PSO result files found!\n"
            "Have you run the experiments yet? Execute:\n"
            "  cd .artifacts/LT7_research_paper/experiments\n"
            "  launch_all_experiments.bat"
        )

    return results


def compute_statistics(values: list) -> Dict:
    """Compute mean, std, and 95% confidence interval.

    Args:
        values: List of numerical values

    Returns:
        Dictionary with statistics
    """
    values = np.array(values)
    n = len(values)

    if n == 0:
        return {
            'mean': 0.0,
            'std': 0.0,
            'ci_lower': 0.0,
            'ci_upper': 0.0,
            'n': 0
        }

    mean = np.mean(values)
    std = np.std(values, ddof=1)  # Sample std (n-1)

    # 95% confidence interval using t-distribution
    if n > 1 and std > 0:
        se = std / np.sqrt(n)
        ci = scipy_stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
        ci_lower, ci_upper = ci
    else:
        # If std=0 (all values identical) or n=1, CI equals mean
        ci_lower = mean
        ci_upper = mean

    return {
        'mean': float(mean),
        'std': float(std),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n': int(n)
    }


def format_latex_table(stats: Dict, n_runs: int) -> str:
    """Format PSO statistics as LaTeX table.

    Args:
        stats: Dictionary with statistics for each parameter
        n_runs: Number of PSO runs

    Returns:
        LaTeX table string
    """
    latex = []

    # Table header
    latex.append(r"\begin{table}[t]")
    latex.append(r"\centering")
    latex.append(f"\\caption{{PSO Optimization Statistics ({n_runs} Independent Runs)}}")
    latex.append(r"\label{tab:pso_statistics}")
    latex.append(r"\begin{tabular}{lcccc}")
    latex.append(r"\hline")
    latex.append(r"Parameter & Mean & Std Dev & 95\% CI Lower & 95\% CI Upper \\")
    latex.append(r"\hline")

    # Epsilon_min row
    eps_stats = stats['epsilon_min']
    latex.append(
        f"$\\epsilon_{{\\min}}$ & "
        f"{eps_stats['mean']:.5f} & "
        f"{eps_stats['std']:.5f} & "
        f"{eps_stats['ci_lower']:.5f} & "
        f"{eps_stats['ci_upper']:.5f} \\\\"
    )

    # Alpha row
    alpha_stats = stats['alpha']
    latex.append(
        f"$\\alpha$ & "
        f"{alpha_stats['mean']:.4f} & "
        f"{alpha_stats['std']:.4f} & "
        f"{alpha_stats['ci_lower']:.4f} & "
        f"{alpha_stats['ci_upper']:.4f} \\\\"
    )

    # Fitness row
    fit_stats = stats['fitness']
    latex.append(
        f"Fitness & "
        f"{fit_stats['mean']:.2f} & "
        f"{fit_stats['std']:.2f} & "
        f"{fit_stats['ci_lower']:.2f} & "
        f"{fit_stats['ci_upper']:.2f} \\\\"
    )

    # Convergence iteration row
    conv_stats = stats['convergence_iteration']
    latex.append(
        f"Conv. Iteration & "
        f"{conv_stats['mean']:.1f} & "
        f"{conv_stats['std']:.1f} & "
        f"{int(conv_stats['ci_lower'])} & "
        f"{int(conv_stats['ci_upper'])} \\\\"
    )

    # Table footer
    latex.append(r"\hline")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")

    return "\n".join(latex)


def print_preview(stats: Dict, n_runs: int):
    """Print console preview of statistics.

    Args:
        stats: Dictionary with statistics
        n_runs: Number of runs
    """
    print("\n" + "=" * 90)
    print(f"TABLE II: PSO OPTIMIZATION STATISTICS ({n_runs} RUNS)")
    print("=" * 90)
    print(f"{'Parameter':<20} {'Mean':>12} {'Std':>12} {'95% CI Lower':>14} {'95% CI Upper':>14}")
    print("-" * 90)

    # Epsilon_min
    eps = stats['epsilon_min']
    print(f"{'ε_min':<20} {eps['mean']:>12.5f} {eps['std']:>12.5f} "
          f"{eps['ci_lower']:>14.5f} {eps['ci_upper']:>14.5f}")

    # Alpha
    alpha = stats['alpha']
    print(f"{'α':<20} {alpha['mean']:>12.4f} {alpha['std']:>12.4f} "
          f"{alpha['ci_lower']:>14.4f} {alpha['ci_upper']:>14.4f}")

    # Fitness
    fit = stats['fitness']
    print(f"{'Fitness':<20} {fit['mean']:>12.2f} {fit['std']:>12.2f} "
          f"{fit['ci_lower']:>14.2f} {fit['ci_upper']:>14.2f}")

    # Convergence iteration
    conv = stats['convergence_iteration']
    print(f"{'Convergence Iter':<20} {conv['mean']:>12.1f} {conv['std']:>12.1f} "
          f"{int(conv['ci_lower']):>14} {int(conv['ci_upper']):>14}")

    print("=" * 90)


def main():
    """Generate Table II: PSO statistics."""

    print("=" * 90)
    print("GENERATING TABLE II: PSO OPTIMIZATION STATISTICS")
    print("=" * 90)

    # Load PSO results
    print("\n[1/4] Loading PSO results from 10 runs...")
    try:
        results = load_pso_results(SEEDS)
        n_runs = len(results['seeds_found'])
        print(f"[OK] Loaded {n_runs} runs successfully")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Compute statistics
    print("\n[2/4] Computing statistics (mean, std, 95% CI)...")
    stats = {}
    for param in ['epsilon_min', 'alpha', 'fitness', 'convergence_iteration']:
        stats[param] = compute_statistics(results[param])
    print("[OK] Statistics computed")

    # Format LaTeX table
    print("\n[3/4] Formatting LaTeX table...")
    latex_table = format_latex_table(stats, n_runs)
    print("[OK] LaTeX table formatted")

    # Save to file
    print("\n[4/4] Saving table to file...")
    output_file = TABLES_DIR / "table2_pso_stats.tex"
    with open(output_file, 'w') as f:
        f.write(latex_table)
    print(f"[OK] Saved to: {output_file}")

    # Print preview
    print_preview(stats, n_runs)

    # LaTeX inclusion instructions
    print("\n" + "=" * 90)
    print("LaTeX Inclusion:")
    print("=" * 90)
    print(f"  \\input{{{output_file.name}}}")
    print("\nOr copy the table content directly into your manuscript.")
    print("=" * 90)

    # Save summary JSON for potential use by other scripts
    summary_file = TABLES_DIR / "table2_pso_stats_summary.json"
    summary = {
        'n_runs': n_runs,
        'seeds': results['seeds_found'],
        'statistics': stats
    }
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n[BONUS] Saved summary JSON: {summary_file}")


if __name__ == "__main__":
    main()
