# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 7
# Runnable: True
# Hash: a1d8a92e

# 1. Create controller factory
from src.controllers.factory import create_pso_controller_factory, SMCType
controller_factory = create_pso_controller_factory(SMCType.CLASSICAL, plant_config)

# 2. Initialize PSO tuner
from src.optimizer.pso_optimizer import PSOTuner
tuner = PSOTuner(controller_factory, config)

# 3. Run optimization
result = tuner.optimise()
optimal_gains = result['best_pos']