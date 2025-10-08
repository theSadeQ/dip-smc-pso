# Example from: docs\guides\api\README.md
# Index: 3
# Runnable: True
# Hash: a5fd9437

from src.optimizer import PSOTuner

tuner = PSOTuner(controller_type=SMCType.CLASSICAL, bounds=bounds)
best_gains, best_cost = tuner.optimize()