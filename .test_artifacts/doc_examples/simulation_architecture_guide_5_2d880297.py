# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 5
# Runnable: True
# Hash: 2d880297

def _guard_no_nan(state: np.ndarray, t: float, dt: float) -> None:
    """Detect and raise error for NaN values."""
    if not np.all(np.isfinite(state)):
        raise ValueError(f"NaN/Inf detected at t={t:.3f}")