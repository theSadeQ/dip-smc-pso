# Example from: docs\api\factory_system_api_reference.md
# Index: 19
# Runnable: False
# Hash: 96213313

from src.controllers.factory import get_default_gains

# Get baseline gains
default_gains = get_default_gains('classical_smc')
print(f"Baseline gains: {default_gains}")
# Output: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]

# Use as PSO initial guess
from src.optimization.algorithms.pso_optimizer import PSOTuner
tuner = PSOTuner(...)
optimized_gains = tuner.optimize(initial_guess=default_gains)