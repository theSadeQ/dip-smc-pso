# Example from: docs\api\optimization_module_api_reference.md
# Index: 32
# Runnable: False
# Hash: aab42467

#!/usr/bin/env python3
"""
Example 2: Real-Time Convergence Monitoring

Demonstrates:
- EnhancedConvergenceAnalyzer integration
- Multi-criteria convergence detection
- Real-time metric logging
- Early stopping based on convergence status
"""

import matplotlib.pyplot as plt
import numpy as np
from functools import partial

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.optimization.validation.enhanced_convergence_analyzer import (
    EnhancedConvergenceAnalyzer,
    ConvergenceCriteria,
    ConvergenceStatus
)
from src.controllers.factory import create_controller, SMCType
from src.config import load_config

# ============================================================================
# Configuration
# ============================================================================

CONFIG_PATH = "config.yaml"
CONTROLLER_TYPE = 'sta_smc'
SEED = 42

# ============================================================================
# Convergence Monitoring Callback
# ============================================================================

class ConvergenceMonitor:
    """Callback for real-time convergence monitoring."""

    def __init__(self, analyzer: EnhancedConvergenceAnalyzer):
        self.analyzer = analyzer
        self.metrics_history = []

    def __call__(self, iteration: int, best_fitness: float, mean_fitness: float,
                 fitness_std: float, swarm_positions: np.ndarray):
        """Check convergence at each iteration."""
        status, metrics = self.analyzer.check_convergence(
            iteration=iteration,
            best_fitness=best_fitness,
            mean_fitness=mean_fitness,
            fitness_std=fitness_std,
            swarm_positions=swarm_positions
        )

        self.metrics_history.append(metrics)

        # Log key metrics
        if iteration % 10 == 0:
            print(f"Iter {iteration:3d} | Status: {status.value:20s} | "
                  f"Best: {metrics.best_fitness:.6f} | "
                  f"Diversity: {metrics.population_diversity:.4f} | "
                  f"Conv. Velocity: {metrics.convergence_velocity:.4e} | "
                  f"Predicted Remaining: {metrics.predicted_iterations_remaining:3d}")

        # Early stopping
        if status == ConvergenceStatus.CONVERGED:
            print(f"\n>>> CONVERGENCE DETECTED at iteration {iteration} <<<")
            return True  # Signal early stop
        elif status == ConvergenceStatus.STAGNATED:
            print(f"\n>>> STAGNATION DETECTED at iteration {iteration} <<<")
            return True  # Signal early stop

        return False  # Continue

# ============================================================================
# Main
# ============================================================================

def main():
    # Load configuration
    config = load_config(CONFIG_PATH)

    # Initialize convergence analyzer with custom criteria
    criteria = ConvergenceCriteria(
        fitness_tolerance=1e-6,
        relative_improvement_threshold=1e-4,
        min_diversity_threshold=1e-3,
        max_stagnation_iterations=50,
        enable_performance_prediction=True,
        premature_convergence_detection=True
    )

    analyzer = EnhancedConvergenceAnalyzer(
        criteria=criteria,
        controller_type=SMCType.STA
    )

    monitor = ConvergenceMonitor(analyzer)

    # Create controller factory
    controller_factory = partial(
        create_controller,
        controller_type=CONTROLLER_TYPE,
        config=config
    )

    # Initialize PSO tuner
    tuner = PSOTuner(
        controller_factory=controller_factory,
        config=config,
        seed=SEED
    )

    # Run optimization with monitoring
    print(f"Running PSO optimization with real-time convergence monitoring...")
    print(f"{'='*120}")
    result = tuner.optimise()
    print(f"{'='*120}\n")

    # Plot convergence metrics
    metrics = monitor.metrics_history
    iterations = [m.iteration for m in metrics]
    best_fitness = [m.best_fitness for m in metrics]
    diversity = [m.population_diversity for m in metrics]
    conv_velocity = [m.convergence_velocity for m in metrics]

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Best fitness
    axes[0].plot(iterations, best_fitness, linewidth=2, color='blue')
    axes[0].set_ylabel('Best Fitness', fontsize=12)
    axes[0].set_yscale('log')
    axes[0].set_title('Convergence Monitoring - STA SMC', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    # Population diversity
    axes[1].plot(iterations, diversity, linewidth=2, color='green')
    axes[1].set_ylabel('Population Diversity', fontsize=12)
    axes[1].grid(True, alpha=0.3)

    # Convergence velocity
    axes[2].plot(iterations, conv_velocity, linewidth=2, color='red')
    axes[2].set_ylabel('Convergence Velocity', fontsize=12)
    axes[2].set_xlabel('Iteration', fontsize=12)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('pso_convergence_monitoring.png', dpi=300)
    print("Convergence monitoring plot saved: pso_convergence_monitoring.png")

if __name__ == "__main__":
    main()