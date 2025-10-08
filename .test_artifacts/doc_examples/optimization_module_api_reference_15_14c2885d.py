# Example from: docs\api\optimization_module_api_reference.md
# Index: 15
# Runnable: False
# Hash: 14c2885d

# example-metadata:
# runnable: false

from src.optimization.validation.enhanced_convergence_analyzer import (
    EnhancedConvergenceAnalyzer,
    ConvergenceCriteria,
    ConvergenceStatus
)

# Initialize analyzer
criteria = ConvergenceCriteria(
    fitness_tolerance=1e-6,
    max_stagnation_iterations=50,
    enable_performance_prediction=True
)
analyzer = EnhancedConvergenceAnalyzer(
    criteria=criteria,
    controller_type=SMCType.CLASSICAL
)

# PSO optimization loop (pseudo-code)
for iteration in range(max_iterations):
    # ... PSO updates ...

    # Check convergence
    status, metrics = analyzer.check_convergence(
        iteration=iteration,
        best_fitness=current_best_fitness,
        mean_fitness=swarm_mean_fitness,
        fitness_std=swarm_fitness_std,
        swarm_positions=particle_positions
    )

    # Log metrics
    print(f"Iteration {iteration}:")
    print(f"  Status: {status.value}")
    print(f"  Best Fitness: {metrics.best_fitness:.6f}")
    print(f"  Convergence Velocity: {metrics.convergence_velocity:.6e}")
    print(f"  Diversity: {metrics.population_diversity:.6f}")
    print(f"  Predicted Iterations Remaining: {metrics.predicted_iterations_remaining}")

    # Early stopping
    if status == ConvergenceStatus.CONVERGED:
        print(f"Convergence detected at iteration {iteration}")
        break
    elif status == ConvergenceStatus.STAGNATED:
        print(f"Stagnation detected at iteration {iteration}")
        break