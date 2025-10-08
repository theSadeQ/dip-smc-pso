# Example from: docs\api\factory_reference.md
# Index: 7
# Runnable: True
# Hash: 5e5b56bf

from src.controllers.factory import get_gain_bounds_for_pso, SMCType

lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
# Returns: ([1.0, 1.0, 1.0, 1.0, 5.0, 0.1], [30.0, 30.0, 20.0, 20.0, 50.0, 10.0])