# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 1
# Runnable: False
# Hash: 1b21fed2

@staticmethod
@njit
def _compute_inertia_matrix_numba(theta1, theta2, m0, m1, m2, ...):
    """JIT-compiled inertia matrix computation."""