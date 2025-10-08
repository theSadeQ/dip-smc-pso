# Example from: docs\reference\controllers\smc_core_switching_functions.md
# Index: 1
# Runnable: True
# Hash: 036e65c0

from src.utils.control.saturation import saturate
import numpy as np

# Sliding surface value
s = 0.05  # rad

# Boundary layer parameters
epsilon = 0.01  # rad
beta = 3.0  # Slope parameter

# Compute tanh switching
u_sw = saturate(s, epsilon, method='tanh', slope=beta)
print(f"Switching control: {u_sw:.4f}")

# For s >> epsilon, u_sw → 1.0
# For s << -epsilon, u_sw → -1.0
# For |s| < epsilon, smooth transition