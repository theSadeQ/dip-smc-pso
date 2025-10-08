# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 9
# Runnable: True
# Hash: f211f513

from numba import jit

@jit(nopython=True, cache=True)
def compute_control_numba(state, gains):
    """Compiled controller - 10-50x faster"""
    k1, k2, k3, k4, k5, k6 = gains
    # Control law implementation
    u = -k1 * state[0] - k2 * state[1] - k3 * state[2]
    return np.clip(u, -MAX_TORQUE, MAX_TORQUE)