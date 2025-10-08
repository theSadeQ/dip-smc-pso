# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 12
# Runnable: True
# Hash: 8f665af8

import time

# First call (includes compilation)
start = time.perf_counter()
M1 = physics.compute_inertia_matrix(state)
first_call = time.perf_counter() - start
print(f"First call: {first_call:.4f}s")

# Subsequent calls (compiled code)
start = time.perf_counter()
M2 = physics.compute_inertia_matrix(state)
subsequent_call = time.perf_counter() - start
print(f"Subsequent call: {subsequent_call:.6f}s")
print(f"Speedup: {first_call / subsequent_call:.0f}×")