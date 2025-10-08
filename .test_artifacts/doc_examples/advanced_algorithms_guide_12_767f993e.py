# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 12
# Runnable: True
# Hash: 767f993e

import numba

@numba.jit(nopython=True, cache=True)
def fast_dynamics_update(state, control, dt, params):
    """Compiled dynamics integration."""
    # Pure NumPy operations, no Python objects
    M = compute_mass_matrix(state, params)
    C = compute_coriolis(state, params)
    G = compute_gravity(state, params)

    # Solve: M * qdd = tau - C * qd - G
    qdd = np.linalg.solve(M, control - C @ state[3:] - G)

    return state + dt * np.concatenate([state[3:], qdd])

# First call: ~100 ms (compilation overhead)
# Subsequent calls: ~0.1 ms (compiled code)