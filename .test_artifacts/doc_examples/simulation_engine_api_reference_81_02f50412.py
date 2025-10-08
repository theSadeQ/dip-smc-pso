# Example from: docs\api\simulation_engine_api_reference.md
# Index: 81
# Runnable: False
# Hash: 02f50412

def _guard_bounds(state: np.ndarray, config: Any) -> None:
    """Check state within configured bounds."""
    bounds = config.safety.state_bounds  # [x_min, x_max, theta_min, theta_max, ...]

    for i, (val, (min_val, max_val)) in enumerate(zip(state, bounds)):
        if not (min_val <= val <= max_val):
            raise SafetyViolationError(
                f"State[{i}] = {val:.3f} outside bounds [{min_val}, {max_val}]"
            )