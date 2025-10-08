# Example from: docs\controllers\index.md
# Index: 2
# Runnable: False
# Hash: 370d513c

# example-metadata:
# runnable: false

from src.controllers.factory import create_smc_for_pso, get_gain_bounds_for_pso
from src.controllers.factory import SMCType

lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

def controller_factory(gains):
    return create_smc_for_pso(SMCType.CLASSICAL, gains)

# Use with PSO tuner...