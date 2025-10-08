# Example from: docs\factory\factory_api_reference.md
# Index: 18
# Runnable: True
# Hash: 1f78f1c2

from src.controllers.factory import SMCType, create_pso_controller_factory

# Create PSO factory for classical SMC
factory_func = create_pso_controller_factory(
    SMCType.CLASSICAL,
    max_force=150.0,
    boundary_layer=0.02
)

# Use in PSO optimization
optimized_gains = pso_optimizer.optimize(factory_func)