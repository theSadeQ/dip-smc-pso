# Example from: docs\factory\parameter_interface_specification.md
# Index: 7
# Runnable: False
# Hash: 263eb840

# example-metadata:
# runnable: false

def validate_parameter_ranges(
    gains: List[float],
    controller_type: str,
    bounds: Optional[List[Tuple[float, float]]] = None
) -> None:
    """Validate parameters against acceptable ranges."""

    if bounds is None:
        bounds = get_default_bounds(controller_type)

    for i, (gain, (min_val, max_val)) in enumerate(zip(gains, bounds)):
        if not (min_val <= gain <= max_val):
            gain_name = get_gain_name(controller_type, i)
            raise ValueError(
                f"Parameter {gain_name}[{i}] = {gain} outside valid range "
                f"[{min_val}, {max_val}] for {controller_type}"
            )

def get_default_bounds(controller_type: str) -> List[Tuple[float, float]]:
    """Get default parameter bounds for controller type."""
    bounds_map = {
        'classical_smc': [(0.1, 50.0)] * 4 + [(1.0, 200.0)] + [(0.0, 50.0)],
        'adaptive_smc': [(0.1, 50.0)] * 4 + [(0.01, 10.0)],
        'sta_smc': [(1.0, 100.0)] * 2 + [(0.1, 50.0)] * 4,
        'hybrid_adaptive_sta_smc': [(0.1, 50.0)] * 4
    }
    return bounds_map.get(controller_type, [(0.1, 100.0)] * 6)