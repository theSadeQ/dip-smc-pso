# Example from: docs\factory\factory_integration_user_guide.md
# Index: 8
# Runnable: True
# Hash: 99f56e40

from src.optimization.integration.pso_factory_bridge import create_pso_controller_factory
from src.controllers.factory import SMCType

# Create PSO-optimized factory for Classical SMC
factory_func = create_pso_controller_factory(
    smc_type=SMCType.CLASSICAL,
    max_force=150.0,
    boundary_layer=0.02
)

# PSO optimization with enhanced factory
from src.optimizer.pso_optimizer import PSOTuner

bounds = [(1.0, 30.0), (1.0, 30.0), (1.0, 20.0),
          (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)]

tuner = PSOTuner(
    controller_factory=factory_func,
    bounds=bounds,
    n_particles=20,
    max_iterations=200
)

# Optimized gains with improved reliability
optimized_gains, best_cost = tuner.optimize()