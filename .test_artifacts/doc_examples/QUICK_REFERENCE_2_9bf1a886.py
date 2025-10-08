# Example from: docs\guides\QUICK_REFERENCE.md
# Index: 2
# Runnable: True
# Hash: 9bf1a886

from src.optimizer.pso_optimizer import PSOTuner
from src.controllers import create_smc_for_pso, get_gain_bounds_for_pso, SMCType

# Get bounds
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Create PSO tuner
tuner = PSOTuner(
    controller_type=SMCType.CLASSICAL,
    bounds=bounds,
    n_particles=30,
    iters=100
)

# Optimize
best_gains, best_cost = tuner.optimize()

print(f"Optimized gains: {best_gains}")
print(f"Final cost: {best_cost:.4f}")