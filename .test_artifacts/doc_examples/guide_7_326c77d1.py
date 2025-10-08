# Example from: docs\optimization_simulation\guide.md
# Index: 7
# Runnable: True
# Hash: 326c77d1

def _guard_no_nan(state: np.ndarray, step_idx: int) -> None:
    """Raise error if state contains NaN or Inf values."""
    if not np.all(np.isfinite(state)):
        raise ValueError(f"Non-finite state detected at step {step_idx}")