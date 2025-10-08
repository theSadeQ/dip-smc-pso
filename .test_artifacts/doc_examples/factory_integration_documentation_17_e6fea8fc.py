# Example from: docs\factory_integration_documentation.md
# Index: 17
# Runnable: True
# Hash: e6fea8fc

from src.controllers.factory import create_pso_controller_factory, SMCType
from src.optimization.algorithms.pso_optimizer import PSOTuner

# Create PSO-optimized factory
controller_factory = create_pso_controller_factory(
    SMCType.CLASSICAL,
    plant_config=config
)

# Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config
)

# Run optimization
best_gains, best_fitness = tuner.optimize()