# Example from: docs\analysis\controller_memory_patterns.md
# Index: 3
# Runnable: False
# Hash: 8cd8c953

# example-metadata:
# runnable: false

@numba.njit(cache=True)
def _sta_smc_control_numba(
    state: np.ndarray,
    z: float,
    alg_gain_K1: float,
    # ... other parameters
) -> Tuple[float, float, float]:
    # Numba automatically optimizes array access
    _, th1, th2, _, th1dot, th2dot = state

    # Ultra-fast compiled operations
    sigma = surf_gain_k1 * (th1dot + surf_lam1 * th1) + \
            surf_gain_k2 * (th2dot + surf_lam2 * th2)