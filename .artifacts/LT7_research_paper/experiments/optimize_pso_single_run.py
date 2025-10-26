"""Single PSO run with CLI arguments for batch processing.

Modified version of optimize_adaptive_boundary.py that accepts seed and output path
as command-line arguments for parallel execution.

Usage:
    python optimize_pso_single_run.py --seed 42 --output results_seed42.json
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import optimize_adaptive_boundary
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from optimize_adaptive_boundary import run_pso_optimization, validate_best_parameters
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Run PSO optimization with CLI arguments."""
    parser = argparse.ArgumentParser(description='Run PSO optimization for adaptive boundary layer')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--output', type=str, required=True, help='Output JSON file path')
    parser.add_argument('--n-particles', type=int, default=30, help='Swarm size (default: 30)')
    parser.add_argument('--n-iterations', type=int, default=30, help='Max iterations (default: 30)')
    parser.add_argument('--n-validation', type=int, default=100, help='Validation runs (default: 100)')
    parser.add_argument('--skip-validation', action='store_true', help='Skip validation step')

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info(f"PSO Optimization (Seed: {args.seed})")
    logger.info("=" * 80)

    # Step 1: Run PSO optimization
    logger.info("\nRunning PSO optimization...")
    logger.info(f"  Swarm size: {args.n_particles}")
    logger.info(f"  Max iterations: {args.n_iterations}")
    logger.info(f"  Random seed: {args.seed}")

    opt_result = run_pso_optimization(
        n_particles=args.n_particles,
        n_iterations=args.n_iterations,
        seed=args.seed
    )

    # Step 2: Validation (optional)
    validation_stats = None
    if not args.skip_validation:
        logger.info(f"\nValidating with {args.n_validation} Monte Carlo runs...")
        validation_stats = validate_best_parameters(
            epsilon_min=opt_result.best_epsilon_min,
            alpha=opt_result.best_alpha,
            n_runs=args.n_validation,
            seed=args.seed
        )

    # Step 3: Save results
    logger.info(f"\nSaving results to: {args.output}")

    output_data = {
        'seed': args.seed,
        'n_particles': args.n_particles,
        'n_iterations': args.n_iterations,
        'final_fitness': float(opt_result.best_fitness),
        'convergence_iteration': int(opt_result.convergence_iterations),
        'fitness_improvement': float(opt_result.fitness_improvement),
        'optimized_eps_min': float(opt_result.best_epsilon_min),
        'optimized_alpha': float(opt_result.best_alpha),
        'optimization_history': opt_result.optimization_history
    }

    if validation_stats is not None:
        output_data['validation'] = validation_stats

    # Save JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    logger.info("=" * 80)
    logger.info("COMPLETE")
    logger.info(f"Best fitness: {opt_result.best_fitness:.4f}")
    logger.info(f"Best params: eps_min={opt_result.best_epsilon_min:.6f}, alpha={opt_result.best_alpha:.4f}")
    logger.info(f"Converged at iteration: {opt_result.convergence_iterations}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
