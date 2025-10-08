# Example from: docs\optimization_simulation\guide.md
# Index: 9
# Runnable: True
# Hash: f537de8f

def _guard_bounds(state: np.ndarray, bounds: Tuple, t: float) -> None:
    """Verify state within per-dimension bounds."""
    lower, upper = bounds
    if lower is not None and np.any(state < lower):
        raise ValueError(f"State below lower bound at t={t:.3f}")
    if upper is not None and np.any(state > upper):
        raise ValueError(f"State above upper bound at t={t:.3f}")