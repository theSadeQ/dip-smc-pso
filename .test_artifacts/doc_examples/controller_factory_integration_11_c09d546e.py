# Example from: docs\technical\controller_factory_integration.md
# Index: 11
# Runnable: False
# Hash: c09d546e

def validate_inputs(controller_type, config, gains):
    """Validate factory inputs before processing."""

    # Controller type validation
    if not isinstance(controller_type, str):
        raise TypeError("controller_type must be string")

    # Gains validation
    if gains is not None:
        if not isinstance(gains, (list, np.ndarray)):
            raise TypeError("gains must be list or numpy array")
        if not all(isinstance(g, (int, float)) for g in gains):
            raise ValueError("gains must contain numeric values")
        if any(not np.isfinite(g) for g in gains):
            raise ValueError("gains contain NaN or infinite values")