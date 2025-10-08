# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 10
# Runnable: True
# Hash: 70feb0f7

from src.optimizer.pso_optimizer import PSOTuner

# Define PSO search space for 5 gains
pso_bounds = [
    (1.0, 50.0),   # k1
    (1.0, 50.0),   # k2
    (1.0, 100.0),  # lam1
    (1.0, 100.0),  # lam2
    (0.1, 5.0),    # gamma
]

# Run PSO optimization
tuner = PSOTuner(bounds=pso_bounds, n_particles=30, iters=200)
best_gains, best_cost = tuner.optimize(
    controller_type='adaptive_smc',
    dynamics=dynamics_model
)

print(f"Optimized gains: {best_gains}")
print(f"Best cost: {best_cost}")