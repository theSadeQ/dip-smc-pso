# Example from: docs\reference\plant\core___init__.md
# Index: 3
# Runnable: False
# Hash: da7a3cda

# example-metadata:
# runnable: false

@njit(cache=True, fastmath=True)
def compute_physics_matrices_numba(q, q_dot, params):
    # Hot loop - compiled to machine code
    ...