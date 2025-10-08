# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 4
# Runnable: False
# Hash: 9a7d5a53

# example-metadata:
# runnable: false

def log_space_pso_bounds(linear_bounds: tuple) -> tuple:
    """
    Convert linear bounds to log-space for better PSO exploration.

    Example: K ∈ [0.1, 100] → log(K) ∈ [-2.3, 4.6]
    """
    min_val, max_val = linear_bounds
    log_min = np.log10(min_val)
    log_max = np.log10(max_val)
    return (log_min, log_max)

# PSO operates in log-space, then transforms back:
def transform_gains_from_log(log_gains: np.ndarray) -> np.ndarray:
    return 10**log_gains