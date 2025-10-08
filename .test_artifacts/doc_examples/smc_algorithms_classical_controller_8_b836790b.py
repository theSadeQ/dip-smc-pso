# Example from: docs\reference\controllers\smc_algorithms_classical_controller.md
# Index: 8
# Runnable: True
# Hash: b836790b

from src.controllers.factory import create_smc_for_pso, get_gain_bounds_for_pso
from src.controllers.factory import SMCType
from src.optimizer.pso_optimizer import PSOTuner

# Get optimization bounds
lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Define controller factory
def controller_factory(gains):
    return create_smc_for_pso(SMCType.CLASSICAL, gains, max_force=100.0)

# Configure PSO
pso_tuner = PSOTuner(
    controller_factory=controller_factory,
    bounds=(lower_bounds, upper_bounds),
    n_particles=30,
    max_iter=50
)

# Optimize
best_gains, best_cost = pso_tuner.optimize()
print(f"Optimized gains: {best_gains}")
print(f"Best fitness: {best_cost:.4f}")