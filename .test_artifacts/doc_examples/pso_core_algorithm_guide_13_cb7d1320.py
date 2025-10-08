# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 13
# Runnable: False
# Hash: cb7d1320

def log_iteration_statistics(self, iteration: int, fitness: np.ndarray) -> None:
    """Log statistics for current iteration.

    Args:
        iteration: Current iteration number
        fitness: Fitness values for all particles
    """
    # Best fitness
    best_fitness = np.min(fitness)
    self.fitness_history.append(best_fitness)

    # Average and worst fitness
    avg_fitness = np.mean(fitness)
    worst_fitness = np.max(fitness[fitness < np.inf])

    # Diversity
    diversity = self.compute_diversity()
    self.diversity_history.append(diversity)

    # Improvement rate
    if len(self.fitness_history) > 1:
        improvement = self.fitness_history[-2] - self.fitness_history[-1]
        improvement_pct = 100 * improvement / self.fitness_history[-2]
    else:
        improvement_pct = 0.0

    # Log to console/file
    self.logger.info(
        f"Iteration {iteration:3d}: "
        f"Best={best_fitness:8.4f}, "
        f"Avg={avg_fitness:8.4f}, "
        f"Diversity={diversity:.4f}, "
        f"Improvement={improvement_pct:+.2f}%"
    )