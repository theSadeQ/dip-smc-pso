"""Grid search over adaptive boundary layer parameter space.

Exhaustive grid search over epsilon_min × alpha space (30×30 = 900 evaluations).
Outputs best fitness for comparison with PSO in Table III.

Usage:
    python run_grid_search.py [--n-grid 30] [--output results/grid_search.json]
"""

import argparse
import json
import numpy as np
from pathlib import Path
from multiprocessing import Pool
import sys
import logging
from functools import partial

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from optimize_adaptive_boundary import evaluate_single_run, generate_initial_conditions
from src.plant.models.dynamics import DIPParams

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def evaluate_parameter_point(eps_alpha_tuple, initial_conditions, dynamics_params):
    """Evaluate fitness for a single (epsilon_min, alpha) parameter point.

    Args:
        eps_alpha_tuple: Tuple of (epsilon_min, alpha)
        initial_conditions: Array of initial conditions for evaluation
        dynamics_params: DIP physical parameters

    Returns:
        float: Average fitness across all initial conditions
    """
    epsilon_min, alpha = eps_alpha_tuple

    # Evaluate on multiple initial conditions (like PSO does)
    fitness_values = []

    for ic in initial_conditions:
        metrics = evaluate_single_run(
            epsilon_min, alpha, ic, None, dynamics_params,
            dt=0.01, T=10.0
        )

        # Compute fitness (same weighting as PSO: 70-15-15)
        if metrics['success']:
            # Normalize metrics (simple min-max based on expected ranges)
            chat_norm = min(metrics['chattering_index'] / 2.0, 1.0)  # chattering in [0, 2]
            settle_norm = min(metrics['settling_time'] / 10.0, 1.0)  # settling in [0, 10s]
            over_norm = min(metrics['overshoot'] / 0.5, 1.0)  # overshoot in [0, 0.5 rad]

            fitness = 0.70 * chat_norm + 0.15 * settle_norm + 0.15 * over_norm
        else:
            fitness = 1e6  # Penalty for failure

        fitness_values.append(fitness)

    # Return mean fitness
    return np.mean(fitness_values)


def run_grid_search(n_grid=30, n_ic_samples=10, seed=42, n_processes=12):
    """Run exhaustive grid search over parameter space.

    Args:
        n_grid: Grid resolution (n_grid × n_grid total evaluations)
        n_ic_samples: Number of initial conditions per parameter point
        seed: Random seed for reproducibility
        n_processes: Number of parallel processes

    Returns:
        dict: Grid search results with best parameters and all fitness values
    """
    logger.info("=" * 80)
    logger.info(f"Grid Search: {n_grid}×{n_grid} = {n_grid**2} evaluations")
    logger.info("=" * 80)

    # Define parameter bounds (same as PSO)
    eps_min_vals = np.linspace(0.001, 0.05, n_grid)
    alpha_vals = np.linspace(0.1, 2.0, n_grid)

    # Create grid points
    param_grid = [(eps, alpha) for eps in eps_min_vals for alpha in alpha_vals]
    logger.info(f"Total evaluations: {len(param_grid)}")
    logger.info(f"Parallel processes: {n_processes}")

    # Generate initial conditions (shared across all parameter evaluations)
    dynamics_params = DIPParams()
    initial_conditions = generate_initial_conditions(n_ic_samples, seed=seed)
    logger.info(f"Initial conditions: {n_ic_samples} samples")

    # Parallel evaluation
    logger.info("\nStarting parallel grid search...")
    eval_func = partial(
        evaluate_parameter_point,
        initial_conditions=initial_conditions,
        dynamics_params=dynamics_params
    )

    with Pool(processes=n_processes) as pool:
        fitness_values = pool.map(eval_func, param_grid)

    logger.info("Grid search complete!")

    # Find best parameters
    best_idx = np.argmin(fitness_values)
    best_eps, best_alpha = param_grid[best_idx]
    best_fitness = fitness_values[best_idx]

    logger.info(f"\nBest Parameters:")
    logger.info(f"  epsilon_min = {best_eps:.6f}")
    logger.info(f"  alpha = {best_alpha:.4f}")
    logger.info(f"  fitness = {best_fitness:.4f}")

    # Prepare results
    results = {
        'method': 'grid_search',
        'n_grid': n_grid,
        'total_evaluations': len(param_grid),
        'n_ic_samples': n_ic_samples,
        'seed': seed,
        'best_fitness': float(best_fitness),
        'best_eps_min': float(best_eps),
        'best_alpha': float(best_alpha),
        'grid_points': {
            'eps_min': eps_min_vals.tolist(),
            'alpha': alpha_vals.tolist()
        },
        'fitness_grid': np.array(fitness_values).reshape(n_grid, n_grid).tolist()
    }

    return results


def main():
    """Main entry point for grid search."""
    parser = argparse.ArgumentParser(description='Run grid search for adaptive boundary layer optimization')
    parser.add_argument('--n-grid', type=int, default=30, help='Grid resolution (default: 30)')
    parser.add_argument('--n-ic', type=int, default=10, help='Initial conditions per point (default: 10)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--n-processes', type=int, default=12, help='Parallel processes (default: 12)')
    parser.add_argument('--output', type=str, default='.artifacts/LT7_research_paper/experiments/results/grid_search.json',
                       help='Output JSON file')

    args = parser.parse_args()

    # Run grid search
    results = run_grid_search(
        n_grid=args.n_grid,
        n_ic_samples=args.n_ic,
        seed=args.seed,
        n_processes=args.n_processes
    )

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info(f"\nResults saved to: {output_path}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
