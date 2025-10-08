# Example from: docs\api\factory_reference.md
# Index: 6
# Runnable: True
# Hash: 09800cfa

from src.controllers.factory import create_smc_for_pso, SMCType
import numpy as np

# Create PSO-optimized controller
wrapper = create_smc_for_pso(SMCType.CLASSICAL, [20.0, 15.0, 12.0, 8.0, 35.0, 5.0])

# Use in PSO fitness function
state = np.array([0.1, 0.0, 0.05, 0.0, 0.1, 0.0])
control_output = wrapper.compute_control(state)