# Example from: docs\guides\api\controllers.md
# Index: 1
# Runnable: True
# Hash: 51e84d3b

from src.controllers import create_controller, create_smc_for_pso

# Option 1: Full configuration (recommended for general use)
controller = create_controller(
    controller_type='classical_smc',
    config=config.controllers.classical_smc
)

# Option 2: PSO-optimized (recommended for optimization workflows)
controller = create_smc_for_pso(
    smc_type=SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)