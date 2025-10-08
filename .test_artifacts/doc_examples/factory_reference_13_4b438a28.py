# Example from: docs\api\factory_reference.md
# Index: 13
# Runnable: True
# Hash: 4b438a28

from src.controllers.factory import create_smc_for_pso, SMCType
from src.optimizer.pso_optimizer import PSOTuner

def fitness_function(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    # Evaluate controller performance
    return performance_score

# Configure PSO optimization
tuner = PSOTuner()
best_gains = tuner.optimize(fitness_function, bounds=gain_bounds)