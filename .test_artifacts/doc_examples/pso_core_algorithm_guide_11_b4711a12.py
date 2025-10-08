# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 11
# Runnable: False
# Hash: b4711a12

# example-metadata:
# runnable: false

def check_convergence(self) -> Tuple[bool, str]:
    """Check if optimization has converged.

    Returns:
        Tuple of (converged flag, reason)
    """
    if self.iteration_count < 20:
        return False, "Insufficient iterations"

    # Check fitness stagnation
    recent_fitness = self.fitness_history[-20:]
    fitness_improvement = max(recent_fitness) - min(recent_fitness)

    if fitness_improvement < self.tolerance:
        return True, "Fitness stagnation"

    # Check diversity collapse
    if self.diversity_history[-1] < 0.01 * self.diversity_history[0]:
        if self.global_best_fitness > 10.0:  # Poor fitness
            return True, "Premature convergence"

    # Check iteration limit
    if self.iteration_count >= self.max_iterations:
        return True, "Maximum iterations reached"

    return False, "Continuing optimization"