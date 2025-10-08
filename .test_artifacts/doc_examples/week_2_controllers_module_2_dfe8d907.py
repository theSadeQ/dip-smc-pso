# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 2
# Runnable: True
# Hash: dfe8d907

from controllers import create_smc_for_pso, get_gain_bounds_for_pso

controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)