# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 17
# Runnable: True
# Hash: f6c56834

v_max = 0.2 * (bounds_upper - bounds_lower)
velocity = np.clip(velocity, -v_max, v_max)