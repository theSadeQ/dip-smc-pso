# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 13
# Runnable: True
# Hash: f44034f7

from src.optimizer.pso_optimizer import PSOTuner

# Define PSO search space for hybrid controller
pso_bounds = [
    (1.0, 100.0),   # c1: First pendulum weight
    (1.0, 100.0),   # λ1: First pendulum damping
    (1.0, 20.0),    # c2: Second pendulum weight
    (1.0, 20.0),    # λ2: Second pendulum damping
]

# Run PSO optimization
tuner = PSOTuner(bounds=pso_bounds, n_particles=20, iters=200)
best_gains, best_cost = tuner.optimize(
    controller_type='hybrid_adaptive_sta_smc',
    dynamics=dynamics_model
)

print(f"Optimized gains: {best_gains}")
print(f"Best cost: {best_cost}")