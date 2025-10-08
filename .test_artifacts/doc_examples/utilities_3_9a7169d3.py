# Example from: docs\guides\api\utilities.md
# Index: 3
# Runnable: True
# Hash: 9a7169d3

from src.utils.validation import validate_physics_params

params = config.dip_params

try:
    validate_physics_params(params)
    print("Physics parameters valid")
except ValueError as e:
    print(f"Invalid parameters: {e}")

# Checks:
# - Masses > 0
# - Lengths > 0
# - Friction coefficients ≥ 0
# - Gravity ≈ 9.81 m/s²
# - Inertias > 0