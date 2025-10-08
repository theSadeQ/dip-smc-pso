# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 12
# Runnable: True
# Hash: e88648c5

from src.controllers.smc.core.gain_validation import get_gain_bounds_for_controller

# Get recommended ranges for adaptive SMC
bounds = get_gain_bounds_for_controller("adaptive")

print("Adaptive SMC Gain Bounds:")
for gain_name, (min_val, max_val) in bounds.items():
    print(f"  {gain_name}: [{min_val}, {max_val}]")

# Output:
# k1: [0.1, 1000.0]
# k2: [0.1, 1000.0]
# lam1: [0.1, 1000.0]
# lam2: [0.1, 1000.0]
# gamma: [0.01, 10.0]