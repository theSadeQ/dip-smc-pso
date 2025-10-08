# Example from: docs\factory\factory_api_reference.md
# Index: 20
# Runnable: True
# Hash: 33c73762

from src.controllers.factory import SMCType, get_gain_bounds_for_pso

bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
lower, upper = bounds
print(f"Lower bounds: {lower}")
print(f"Upper bounds: {upper}")