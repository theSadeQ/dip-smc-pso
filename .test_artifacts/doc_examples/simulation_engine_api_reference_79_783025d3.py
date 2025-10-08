# Example from: docs\api\simulation_engine_api_reference.md
# Index: 79
# Runnable: True
# Hash: 783025d3

def _guard_no_nan(state: np.ndarray) -> None:
    """Check for NaN or Inf values."""
    if not np.all(np.isfinite(state)):
        raise SafetyViolationError("State contains NaN or Inf")