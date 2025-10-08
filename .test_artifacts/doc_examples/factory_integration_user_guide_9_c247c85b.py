# Example from: docs\factory\factory_integration_user_guide.md
# Index: 9
# Runnable: True
# Hash: c247c85b

from src.controllers.factory import get_gain_bounds_for_pso, SMCType

# Automatic bounds for different controller types
classical_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
adaptive_bounds = get_gain_bounds_for_pso(SMCType.ADAPTIVE)
sta_bounds = get_gain_bounds_for_pso(SMCType.SUPER_TWISTING)

print(f"Classical SMC bounds: {classical_bounds}")
# Output: ([1.0, 1.0, 1.0, 1.0, 5.0, 0.1], [30.0, 30.0, 20.0, 20.0, 50.0, 10.0])