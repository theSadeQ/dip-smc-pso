# Example from: docs\reference\controllers\smc_algorithms_super_twisting_controller.md
# Index: 8
# Runnable: True
# Hash: 3e3b299b

from src.controllers.factory import create_smc_for_pso, SMCType

# STA requires 6 gains: [k1, k2, λ1, λ2, K₁, K₂]
# STA stability: K₁ > K₂ for finite-time convergence
bounds = [
    (1.0, 50.0),    # k1
    (1.0, 50.0),    # k2
    (1.0, 50.0),    # λ1
    (1.0, 50.0),    # λ2
    (10.0, 100.0),  # K₁ (proportional)
    (5.0, 50.0),    # K₂ (integral)
]

def controller_factory(gains):
    return create_smc_for_pso(SMCType.SUPER_TWISTING, gains, max_force=100.0)

# Optimize for convergence time
tuner = PSOTuner(bounds, controller_factory, metric='convergence_time')
best_gains, best_time = tuner.optimize(n_particles=40, iters=150)