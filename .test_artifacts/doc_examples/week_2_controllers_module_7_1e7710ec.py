# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 7
# Runnable: True
# Hash: 1e7710ec

from controllers import create_smc_for_pso, SMCType

controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)