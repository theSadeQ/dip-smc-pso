# Example from: docs\pso_factory_integration_patterns.md
# Index: 20
# Runnable: True
# Hash: b2e6a046

#!/usr/bin/env python3
"""Real-time PSO optimization with live monitoring."""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np

@dataclass
class OptimizationProgress:
    """Track optimization progress."""
    iteration: int
    best_fitness: float
    best_gains: np.ndarray
    population_diversity: float
    elapsed_time: float

def real_time_pso_optimization():
    """Real-time PSO optimization with live monitoring."""

    # Setup real-time monitoring
    progress_history: List[OptimizationProgress] = []

    def progress_callback(iteration: int, best_fitness: float,
                         best_gains: np.ndarray, population: np.ndarray) -> None:
        """Real-time progress monitoring callback."""

        # Compute population diversity
        diversity = np.std(population, axis=0).mean()
        elapsed_time = time.time() - start_time

        # Record progress
        progress = OptimizationProgress(
            iteration=iteration,
            best_fitness=best_fitness,
            best_gains=best_gains.copy(),
            population_diversity=diversity,
            elapsed_time=elapsed_time
        )
        progress_history.append(progress)

        # Live display
        print(f"Iteration {iteration:3d}: "
              f"fitness={best_fitness:.6f}, "
              f"diversity={diversity:.4f}, "
              f"time={elapsed_time:.1f}s")

        # Early stopping based on convergence
        if len(progress_history) >= 20:
            recent_improvements = [
                progress_history[-i].best_fitness for i in range(1, 11)
            ]

            improvement_rate = (max(recent_improvements) - min(recent_improvements)) / max(recent_improvements)

            if improvement_rate < 1e-4:
                print("Convergence detected. Early stopping.")
                return True  # Signal early stopping

        return False

    # Create factory and bounds
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

    # Enhanced fitness function with real-time monitoring
    evaluation_count = 0

    def monitored_fitness_function(gains: np.ndarray) -> float:
        nonlocal evaluation_count
        evaluation_count += 1

        try:
            controller = factory(gains)
            performance = evaluate_controller_performance(controller)

            # Log periodic updates
            if evaluation_count % 50 == 0:
                print(f"  Evaluated {evaluation_count} candidates")

            return performance['total_cost']

        except Exception as e:
            print(f"  Evaluation failed: {e}")
            return float('inf')

    # Run optimization with real-time monitoring
    start_time = time.time()

    tuner = PSOTuner(
        controller_factory=monitored_fitness_function,
        config=config,
        progress_callback=progress_callback
    )

    best_gains, best_fitness = tuner.optimize()

    total_time = time.time() - start_time

    # Generate real-time optimization report
    print(f"\nOptimization Summary:")
    print(f"Total time: {total_time:.1f}s")
    print(f"Total evaluations: {evaluation_count}")
    print(f"Evaluations per second: {evaluation_count/total_time:.1f}")
    print(f"Final fitness: {best_fitness:.6f}")
    print(f"Best gains: {best_gains}")

    # Plot convergence history
    plot_convergence_history(progress_history)

    return best_gains, best_fitness, progress_history

def plot_convergence_history(progress_history: List[OptimizationProgress]):
    """Plot real-time optimization convergence."""

    iterations = [p.iteration for p in progress_history]
    fitness_values = [p.best_fitness for p in progress_history]
    diversity_values = [p.population_diversity for p in progress_history]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Fitness convergence
    ax1.plot(iterations, fitness_values, 'b-', linewidth=2)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Best Fitness')
    ax1.set_title('PSO Convergence History')
    ax1.grid(True, alpha=0.3)

    # Population diversity
    ax2.plot(iterations, diversity_values, 'r-', linewidth=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Population Diversity')
    ax2.set_title('Population Diversity Evolution')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('pso_convergence_history.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    real_time_pso_optimization()