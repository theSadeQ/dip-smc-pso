# Example from: docs\reference\controllers\smc_algorithms_super_twisting_controller.md
# Index: 9
# Runnable: True
# Hash: c6c654f8

import numpy as np

# Theoretical convergence time: t_c ≈ 2|s(0)|/(K₁√K₂)
K1, K2 = 20.0, 15.0
s0 = 0.1

theoretical_time = 2 * abs(s0) / (K1 * np.sqrt(K2))
print(f"Theoretical convergence: {theoretical_time:.3f}s")

# Run simulation and measure actual convergence
result = runner.run(initial_state=[0.1, 0, 0, 0, 0, 0], duration=5.0)
actual_time = np.argmax(np.abs(result.surface_history) < 0.01) * 0.01
print(f"Actual convergence: {actual_time:.3f}s")