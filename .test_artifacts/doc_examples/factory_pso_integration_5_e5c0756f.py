# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 5
# Runnable: False
# Hash: e5c0756f

# example-metadata:
# runnable: false

# PSO with convergence callback
def convergence_callback(iteration, best_fitness, diversity):
    print(f"Iteration {iteration:3d}: "
          f"Fitness={best_fitness:.4f}, "
          f"Diversity={diversity:.4f}")

    # Early stopping if fitness stagnant
    if iteration > 20:
        fitness_history = pso.get_fitness_history()
        improvement = abs(fitness_history[-1] - fitness_history[-10]) / fitness_history[-10]
        if improvement < 1e-4:
            print("Early stopping: convergence detected")
            return True  # Stop optimization
    return False

pso = PSOTuner(
    n_particles=30,
    bounds=bounds,
    fitness_function=fitness_function,
    convergence_callback=convergence_callback
)

best_gains, _ = pso.optimize(max_iterations=200)