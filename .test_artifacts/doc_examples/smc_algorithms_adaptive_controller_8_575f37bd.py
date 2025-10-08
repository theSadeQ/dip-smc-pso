# Example from: docs\reference\controllers\smc_algorithms_adaptive_controller.md
# Index: 8
# Runnable: True
# Hash: 575f37bd

from src.controllers.factory import create_smc_for_pso, SMCType
from src.optimizer.pso_optimizer import PSOTuner

# Adaptive SMC has 5 gains: [k1, k2, λ1, λ2, K₀]
bounds = [
    (0.1, 50.0),   # k1
    (0.1, 50.0),   # k2
    (0.1, 50.0),   # λ1
    (0.1, 50.0),   # λ2
    (1.0, 100.0)   # K₀
]

# Create controller factory
def controller_factory(gains):
    return create_smc_for_pso(SMCType.ADAPTIVE, gains, max_force=100.0)

# Run PSO optimization
tuner = PSOTuner(bounds, controller_factory)
best_gains, best_fitness = tuner.optimize(n_particles=30, iters=100)