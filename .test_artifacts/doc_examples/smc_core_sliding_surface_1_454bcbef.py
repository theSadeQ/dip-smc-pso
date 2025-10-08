# Example from: docs\reference\controllers\smc_core_sliding_surface.md
# Index: 1
# Runnable: True
# Hash: 454bcbef

from src.controllers.smc.core.sliding_surface import LinearSlidingSurface
import numpy as np

# Define gains (c1, c2, λ1, λ2)
gains = [10.0, 8.0, 15.0, 12.0]
surface = LinearSlidingSurface(gains)

# Compute surface value for state
state = np.array([0.1, 0.0, 0.05, 0.1, 0.02, 0.05])  # [x, ẋ, θ₁, θ̇₁, θ₂, θ̇₂]
s = surface.compute(state)
print(f"Sliding surface value: {s:.4f}")