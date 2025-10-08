# Example from: docs\reference\simulation\engines_vector_sim.md
# Index: 1
# Runnable: True
# Hash: a7a3c2aa

@numba.jit(nopython=True, parallel=True)
def batch_integrate(X, U, dt, N):
    for i in numba.prange(B):  # Parallel loop
        X[i] = integrate_single(X[i], U[i], dt, N)
    return X