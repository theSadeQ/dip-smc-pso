# Example from: docs\reference\controllers\smc_core_sliding_surface.md
# Index: 5
# Runnable: True
# Hash: a8ef97a1

from src.controllers.smc.core.sliding_surface import HigherOrderSlidingSurface

# Define 6 gains for 2nd order surface
gains_ho = [25.0, 10.0, 15.0, 12.0, 20.0, 15.0]
surface_ho = HigherOrderSlidingSurface(gains_ho)

# Compute surface and its derivative
s_ho = surface_ho.compute(state)
s_dot_ho = surface_ho.compute_derivative(state, state_dot)

print(f"Higher-order surface: s={s_ho:.4f}, ṡ={s_dot_ho:.4f}")