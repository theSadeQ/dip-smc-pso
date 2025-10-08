# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 24
# Runnable: True
# Hash: 445d1138

# Pre-compile frequent calculations
@functools.lru_cache(maxsize=128)
def cached_matrix_operations(state_tuple):
    """Cache expensive matrix operations."""
    return compute_physics_matrices(np.array(state_tuple))

# Vectorized operations where possible
def vectorized_adaptation(s_values, gamma_values):
    """Batch adaptive gain updates."""
    return gamma_values * np.abs(s_values)