# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 14
# Runnable: True
# Hash: e1bea9dc

# Efficient: Vectorize over states
def compute_inertia_batch(physics, states):
    """Compute M(q) for batch of states."""
    batch_size = states.shape[0]
    M_batch = np.zeros((batch_size, 3, 3))
    for i in range(batch_size):
        M_batch[i] = physics.compute_inertia_matrix(states[i])
    return M_batch

# More efficient: Use Numba parallel loops (future enhancement)