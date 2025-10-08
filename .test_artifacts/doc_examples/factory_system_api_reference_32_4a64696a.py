# Example from: docs\api\factory_system_api_reference.md
# Index: 32
# Runnable: True
# Hash: 4a64696a

from src.controllers.factory import SMCType, create_pso_controller_factory
from src.optimization.algorithms.pso_optimizer import PSOTuner

# Create factory for PSO optimization
controller_factory = create_pso_controller_factory(
    smc_type=SMCType.CLASSICAL,
    max_force=150.0,
    dt=0.001
)

# Factory has PSO-required attributes
print(f"Gain dimension: {controller_factory.n_gains}")  # 6

# Use with PSO tuner
tuner = PSOTuner(controller_factory=controller_factory, config=config)
result = tuner.optimise()
optimized_gains = result['best_pos']