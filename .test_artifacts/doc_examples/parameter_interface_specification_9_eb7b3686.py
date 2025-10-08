# Example from: docs\factory\parameter_interface_specification.md
# Index: 9
# Runnable: True
# Hash: eb7b3686

def normalize_parameter_types(params: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize parameter types for consistent processing."""

    normalized = {}

    for key, value in params.items():
        if key == 'gains':
            # Convert gains to list of floats
            if isinstance(value, np.ndarray):
                normalized[key] = value.tolist()
            elif isinstance(value, (list, tuple)):
                normalized[key] = [float(g) for g in value]
            else:
                raise TypeError(f"Invalid gains type: {type(value)}")

        elif key in ['max_force', 'dt', 'boundary_layer', 'leak_rate']:
            # Convert numeric parameters
            normalized[key] = float(value)

        elif key in ['smooth_switch']:
            # Convert boolean parameters
            normalized[key] = bool(value)

        elif key == 'hybrid_mode':
            # Convert enum parameters
            if isinstance(value, str):
                from src.controllers.smc.algorithms.hybrid.config import HybridMode
                normalized[key] = HybridMode(value)
            else:
                normalized[key] = value

        else:
            # Pass through other parameters
            normalized[key] = value

    return normalized