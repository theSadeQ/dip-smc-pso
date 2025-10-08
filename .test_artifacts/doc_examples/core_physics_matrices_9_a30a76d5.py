# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 9
# Runnable: True
# Hash: a30a76d5

import time

# Benchmark full physics
state_batch = np.random.randn(1000, 6)
start = time.perf_counter()
for state in state_batch:
    M = physics.compute_inertia_matrix(state)
full_time = time.perf_counter() - start

# Benchmark simplified physics
simplified_physics = SimplifiedDIPPhysicsMatrices(config)
start = time.perf_counter()
for state in state_batch:
    M_simp = simplified_physics.compute_inertia_matrix(state)
simplified_time = time.perf_counter() - start

print(f"Full physics: {full_time:.4f}s")
print(f"Simplified physics: {simplified_time:.4f}s")
print(f"Speedup: {full_time / simplified_time:.2f}×")