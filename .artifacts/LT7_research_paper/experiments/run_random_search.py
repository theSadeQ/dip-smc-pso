"""Random search baseline for comparison with PSO.

Random sampling of parameter space (600 samples to match PSO convergence budget).

Usage:
    python run_random_search.py [--n-samples 600] [--output results/random_search.json]
"""

import argparse
import json
import numpy as np
from pathlib import Path
import sys
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from optimize_adaptive_boundary import evaluate_single_run, generate_initial_conditions
from src.plant.models.dynamics import DIPParams

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_random_search(n_samples=600, n_ic_samples=10, seed=42):
    """Run random search over parameter space.

    Args:
        n_samples: Number of random parameter samples
        n_ic_samples: Number of initial conditions per parameter point
        seed: Random seed for reproducibility

    Returns:
        dict: Random search results with best parameters
    """
    logger.info("=" * 80)
    logger.info(f"Random Search: {n_samples} random samples")
    logger.info("=" * 80)

    # Set random seed
    rng = np.random.default_rng(seed)

    # Generate random parameter samples (uniform in parameter bounds)
    eps_min_samples = rng.uniform(0.001, 0.05, n_samples)
    alpha_samples = rng.uniform(0.1, 2.0, n_samples)

    logger.info(f"Parameter bounds:")
    logger.info(f"  epsilon_min: [0.001, 0.05]")
    logger.info(f"  alpha: [0.1, 2.0]")

    # Generate initial conditions
    dynamics_params = DIPParams()
    initial_conditions = generate_initial_conditions(n_ic_samples, seed=seed)
    logger.info(f"Initial conditions: {n_ic_samples} samples")

    # Evaluate each random sample
    fitness_values = []
    best_fitness = float('inf')
    best_eps = None
    best_alpha = None

    logger.info("\nEvaluating random samples...")
    for i, (eps, alpha) in enumerate(zip(eps_min_samples, alpha_samples)):
        if (i + 1) % 100 == 0:
            logger.info(f"  Progress: {i+1}/{n_samples} samples")

        # Evaluate on multiple initial conditions
        sample_fitness = []
        for ic in initial_conditions:
            metrics = evaluate_single_run(
                eps, alpha, ic, None, dynamics_params,
                dt=0.01, T=10.0
            )

            # Compute fitness (70-15-15 weighting)
            if metrics['success']:
                chat_norm = min(metrics['chattering_index'] / 2.0, 1.0)
                settle_norm = min(metrics['settling_time'] / 10.0, 1.0)
                over_norm = min(metrics['overshoot'] / 0.5, 1.0)
                fitness = 0.70 * chat_norm + 0.15 * settle_norm + 0.15 * over_norm
            else:
                fitness = 1e6

            sample_fitness.append(fitness)

        # Mean fitness for this parameter point
        mean_fitness = np.mean(sample_fitness)
        fitness_values.append(mean_fitness)

        # Update best
        if mean_fitness < best_fitness:
            best_fitness = mean_fitness
            best_eps = eps
            best_alpha = alpha

    logger.info("Random search complete!")
    logger.info(f"\nBest Parameters:")
    logger.info(f"  epsilon_min = {best_eps:.6f}")
    logger.info(f"  alpha = {best_alpha:.4f}")
    logger.info(f"  fitness = {best_fitness:.4f}")

    # Prepare results
    results = {
        'method': 'random_search',
        'n_samples': n_samples,
        'n_ic_samples': n_ic_samples,
        'seed': seed,
        'best_fitness': float(best_fitness),
        'best_eps_min': float(best_eps),
        'best_alpha': float(best_alpha),
        'all_fitness': fitness_values,
        'all_eps_min': eps_min_samples.tolist(),
        'all_alpha': alpha_samples.tolist()
    }

    return results


def main():
    """Main entry point for random search."""
    parser = argparse.ArgumentParser(description='Run random search for adaptive boundary layer optimization')
    parser.add_argument('--n-samples', type=int, default=600, help='Number of random samples (default: 600)')
    parser.add_argument('--n-ic', type=int, default=10, help='Initial conditions per point (default: 10)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--output', type=str, default='.artifacts/LT7_research_paper/experiments/results/random_search.json',
                       help='Output JSON file')

    args = parser.parse_args()

    # Run random search
    results = run_random_search(
        n_samples=args.n_samples,
        n_ic_samples=args.n_ic,
        seed=args.seed
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
