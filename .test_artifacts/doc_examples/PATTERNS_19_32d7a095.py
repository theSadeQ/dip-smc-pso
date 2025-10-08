# Example from: docs\PATTERNS.md
# Index: 19
# Runnable: True
# Hash: 32d7a095

from numba import jit

@jit(nopython=True, cache=True)
def compute_sliding_surface_batch(states, k1, k2, lam1, lam2):
    """JIT-compiled sliding surface computation (1000× faster)."""
    n = states.shape[0]
    surfaces = np.zeros(n)

    for i in range(n):
        x, x_dot, theta1, theta1_dot, theta2, theta2_dot = states[i]
        surfaces[i] = (k1 * x + lam1 * x_dot +
                      k2 * theta1 + lam2 * theta1_dot)

    return surfaces