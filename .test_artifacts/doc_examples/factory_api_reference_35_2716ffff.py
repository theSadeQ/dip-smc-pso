# Example from: docs\factory\factory_api_reference.md
# Index: 35
# Runnable: True
# Hash: 2716ffff

from src.controllers.factory import (
    create_controller,
    SMCType,
    get_gain_bounds_for_pso,
    create_pso_controller_factory
)
from src.optimizer.pso_optimizer import PSOTuner

# 1. Create initial controller
controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)

# 2. Set up PSO optimization
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
factory_func = create_pso_controller_factory(SMCType.CLASSICAL)

tuner = PSOTuner(
    controller_factory=factory_func,
    bounds=bounds,
    n_particles=20,
    max_iterations=200
)

# 3. Optimize controller gains
optimized_gains, best_cost = tuner.optimize()

# 4. Create optimized controller
optimized_controller = create_controller(
    'classical_smc',
    gains=optimized_gains
)

print(f"Optimization improved cost from {initial_cost} to {best_cost}")