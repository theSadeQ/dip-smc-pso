# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 15
# Runnable: True
# Hash: f82ee37e

# Inefficient: Creates new arrays each call
for i in range(10000):
    M = physics.compute_inertia_matrix(state)

# Efficient: Reuse pre-allocated arrays
M = np.zeros((3, 3))
for i in range(10000):
    M[:] = physics.compute_inertia_matrix(state)  # In-place update