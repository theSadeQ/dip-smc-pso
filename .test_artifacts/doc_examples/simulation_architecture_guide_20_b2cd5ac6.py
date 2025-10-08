# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 20
# Runnable: True
# Hash: b2cd5ac6

import numba

@numba.jit(nopython=True, cache=True)
def fast_dynamics_step(state, control, dt, params):
    """JIT-compiled dynamics for 100x speedup."""
    # Pure NumPy operations only
    M = compute_mass_matrix(state, params)
    C = compute_coriolis(state, params)
    G = compute_gravity(state, params)

    qdd = np.linalg.solve(M, control - C @ state[3:] - G)
    return state + dt * np.concatenate([state[3:], qdd])

# First call: ~100 ms (compilation)
# Subsequent calls: ~0.1 ms (compiled code)