# Example from: docs\guides\api\controllers.md
# Index: 21
# Runnable: True
# Hash: e7f721cf

from src.optimizer import PSOTuner
from src.controllers import SMCType, get_gain_bounds_for_pso

bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
tuner = PSOTuner(controller_type=SMCType.CLASSICAL, bounds=bounds)

best_gains, best_cost = tuner.optimize()

# Use optimized controller
controller = create_smc_for_pso(SMCType.CLASSICAL, best_gains)
result = runner.run(controller)