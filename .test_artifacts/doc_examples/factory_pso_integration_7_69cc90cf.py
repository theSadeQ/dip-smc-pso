# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 7
# Runnable: True
# Hash: 69cc90cf

from joblib import Parallel, delayed

# Parallel fitness evaluation
def batch_fitness(gains_population):
    """Evaluate all particles in parallel."""

    def eval_single(gains):
        controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
        result = simulate(controller, duration=5.0)
        return result.itae

    # Parallel execution (8 cores)
    fitness_values = Parallel(n_jobs=8)(
        delayed(eval_single)(gains) for gains in gains_population
    )

    return np.array(fitness_values)

# PSO with batch evaluation
pso = PSOTuner(
    n_particles=30,
    bounds=bounds,
    fitness_function=batch_fitness,  # Pass batch function
    batch_mode=True
)

best_gains, _ = pso.optimize(max_iterations=50)
print(f"Speedup: ~8x using parallel evaluation")