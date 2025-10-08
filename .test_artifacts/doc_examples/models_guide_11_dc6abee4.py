# Example from: docs\plant\models_guide.md
# Index: 11
# Runnable: False
# Hash: dc6abee4

from numba import njit

@njit
def compute_simplified_dynamics_numba(
    state, u,
    m0, m1, m2,           # Masses
    L1, L2, Lc1, Lc2,     # Lengths
    I1, I2,               # Inertias
    g, c0, c1, c2,        # Gravity and friction
    reg_alpha, min_reg    # Regularization
):
    """JIT-compiled dynamics computation."""
    # Inline matrix computation and solution
    # ... optimized implementation ...
    return state_derivative