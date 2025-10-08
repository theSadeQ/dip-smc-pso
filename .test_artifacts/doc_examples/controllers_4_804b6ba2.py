# Example from: docs\guides\api\controllers.md
# Index: 4
# Runnable: True
# Hash: 804b6ba2

from src.controllers import create_smc_for_pso, SMCType

# Minimal PSO-friendly creation
controller = create_smc_for_pso(
    smc_type=SMCType.CLASSICAL,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01  # Optional parameter
)

# Used in PSO fitness function
def fitness_function(gains_array):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains_array)
    result = simulate(controller)
    return result['cost']