# Example from: docs\factory\README.md
# Index: 2
# Runnable: True
# Hash: c467797d

from src.controllers.factory import create_pso_controller_factory, SMCType

# Create PSO-optimized factory
factory_func = create_pso_controller_factory(SMCType.CLASSICAL)

# Use in optimization
from src.optimizer.pso_optimizer import PSOTuner
tuner = PSOTuner(controller_factory=factory_func, bounds=bounds)
optimized_gains, cost = tuner.optimize()