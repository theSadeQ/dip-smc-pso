# Example from: docs\reference\plant\core___init__.md
# Index: 3
# Runnable: False
# Hash: 8100743a

@njit(cache=True, fastmath=True)
def compute_physics_matrices_numba(q, q_dot, params):
    # Hot loop - compiled to machine code
    ...