# Example from: docs\reference\controllers\smc_core_sliding_surface.md
# Index: 3
# Runnable: True
# Hash: 053537c1

from src.controllers.smc.core.sliding_surface import validate_sliding_surface_gains

# Valid gains (all positive)
gains_valid = [10.0, 8.0, 15.0, 12.0]
is_valid = validate_sliding_surface_gains(gains_valid)
print(f"Valid gains: {is_valid}")  # True

# Invalid gains (c2 negative)
gains_invalid = [10.0, -8.0, 15.0, 12.0]
try:
    surface_bad = LinearSlidingSurface(gains_invalid)
except ValueError as e:
    print(f"Validation error: {e}")