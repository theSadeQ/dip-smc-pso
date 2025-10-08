# Example from: docs\guides\api\optimization.md
# Index: 17
# Runnable: False
# Hash: 33e5eab3

def tune_pso_hyperparameters():
    """Find best PSO settings for your problem."""
    best_overall_cost = float('inf')
    best_config = None

    # Grid search over PSO parameters
    for n_particles in [20, 30, 50]:
        for w in [0.5, 0.7, 0.9]:
            for c1 in [1.0, 1.5, 2.0]:
                c2 = c1  # Keep symmetric

                tuner = PSOTuner(
                    SMCType.CLASSICAL,
                    bounds=bounds,
                    n_particles=n_particles,
                    iters=50,
                    w=w,
                    c1=c1,
                    c2=c2
                )

                _, cost = tuner.optimize()

                if cost < best_overall_cost:
                    best_overall_cost = cost
                    best_config = {
                        'n_particles': n_particles,
                        'w': w,
                        'c1': c1,
                        'c2': c2
                    }

    return best_config, best_overall_cost

optimal_pso_config, best_cost = tune_pso_hyperparameters()
print(f"Optimal PSO config: {optimal_pso_config}")