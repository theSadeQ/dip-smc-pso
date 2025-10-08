# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 17
# Runnable: False
# Hash: 420bc70a

def multi_start_pso(n_runs: int = 5) -> dict:
    """Run PSO multiple times and select best result.

    Args:
        n_runs: Number of independent PSO runs

    Returns:
        Dictionary with best result and all runs
    """
    results = []

    for run in range(n_runs):
        # Create fresh optimizer
        pso = ParticleSwarmOptimizer(
            parameter_space=param_space,
            population_size=30,
            max_iterations=100,
            adaptive_weights=True
        )

        # Run with different random seed
        np.random.seed(42 + run)
        result = pso.optimize(fitness_function)
        results.append(result)

        print(f"Run {run+1}/{n_runs}: Fitness = {result.best_fitness:.4f}")

    # Select best run
    best_result = min(results, key=lambda r: r.best_fitness)

    return {
        'best_result': best_result,
        'all_results': results,
        'mean_fitness': np.mean([r.best_fitness for r in results]),
        'std_fitness': np.std([r.best_fitness for r in results])
    }

# Run multi-start optimization
multi_result = multi_start_pso(n_runs=5)
print(f"\nBest overall fitness: {multi_result['best_result'].best_fitness:.4f}")
print(f"Mean ± std: {multi_result['mean_fitness']:.4f} ± {multi_result['std_fitness']:.4f}")