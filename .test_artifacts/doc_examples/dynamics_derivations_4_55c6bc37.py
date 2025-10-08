# Example from: docs\mathematical_foundations\dynamics_derivations.md
# Index: 4
# Runnable: False
# Hash: 55c6bc37

import numba

@numba.jit(nopython=True)
def compute_mass_matrix(theta1, theta2, params):
    """JIT-compiled mass matrix computation."""
    m1, m2, L1, L2, I1, I2, M = params
    s12 = np.sin(theta2 - theta1)
    c12 = np.cos(theta2 - theta1)

    # ... matrix computation ...

    return M