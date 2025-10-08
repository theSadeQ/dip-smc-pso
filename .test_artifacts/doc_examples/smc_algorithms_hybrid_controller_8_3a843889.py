# Example from: docs\reference\controllers\smc_algorithms_hybrid_controller.md
# Index: 8
# Runnable: True
# Hash: 3a843889

from src.controllers.factory import create_smc_for_pso, SMCType

# Hybrid SMC has 4 gains (surface only, internal switching)
bounds = [
    (1.0, 50.0),   # k1
    (1.0, 50.0),   # k2
    (1.0, 50.0),   # λ1
    (1.0, 50.0),   # λ2
]

def controller_factory(gains):
    return create_smc_for_pso(SMCType.HYBRID, gains, max_force=100.0)

# Optimize for robustness
tuner = PSOTuner(bounds, controller_factory, metric='robustness_index')
best_gains, best_robustness = tuner.optimize(n_particles=35, iters=120)