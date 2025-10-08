# Example from: docs\controllers\factory_system_guide.md
# Index: 14
# Runnable: True
# Hash: 79c1d7d1

from src.controllers.factory import create_smc_for_pso, get_gain_bounds_for_pso

# Get PSO bounds for controller type
lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
# lower_bounds = [1.0, 1.0, 1.0, 1.0, 5.0, 0.1]
# upper_bounds = [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]

# PSO-friendly controller factory
def controller_factory(gains: np.ndarray):
    return create_smc_for_pso(
        smc_type=SMCType.CLASSICAL,
        gains=gains,
        max_force=100.0,
        dt=0.01
    )

# Use in PSO optimization
from src.optimizer.pso_optimizer import PSOTuner

tuner = PSOTuner(
    controller_factory=controller_factory,
    config='config.yaml',
    seed=42
)

best_gains, best_cost = tuner.optimize(
    lower_bounds=lower_bounds,
    upper_bounds=upper_bounds,
    n_particles=30,
    n_iterations=100
)