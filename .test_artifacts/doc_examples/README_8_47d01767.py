# Example from: docs\guides\api\README.md
# Index: 8
# Runnable: True
# Hash: 47d01767

from src.optimizer import PSOTuner
from src.controllers import get_gain_bounds_for_pso, SMCType

# Get bounds for controller type
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