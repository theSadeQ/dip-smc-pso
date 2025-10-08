# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 14
# Runnable: True
# Hash: 9ae3df90

from src.optimizer.pso_optimizer import PSOTuner

# Define PSO search space
pso_bounds = [
    (1.0, 50.0),   # k1: velocity gain 1
    (1.0, 50.0),   # k2: velocity gain 2
    (1.0, 100.0),  # lam1: position gain 1
    (1.0, 100.0),  # lam2: position gain 2
    (5.0, 200.0),  # K: switching gain
    (0.0, 50.0),   # kd: damping gain
]

# Run PSO optimization
tuner = PSOTuner(bounds=pso_bounds, n_particles=30, iters=200)
best_gains, best_cost = tuner.optimize(
    controller_type='classical_smc',
    dynamics=dynamics_model
)

print(f"Optimized gains: {best_gains}")
print(f"Best cost: {best_cost}")