# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 7
# Runnable: True
# Hash: a26bb60b

def _guard_bounds(state: np.ndarray, lower: Any, upper: Any, t: float) -> None:
    """Check state bounds."""
    if lower is not None and np.any(state < lower):
        raise ValueError(f"Lower bound violation at t={t:.3f}")
    if upper is not None and np.any(state > upper):
        raise ValueError(f"Upper bound violation at t={t:.3f}")