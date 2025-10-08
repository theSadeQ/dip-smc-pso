# Example from: docs\api\simulation_engine_api_reference.md
# Index: 29
# Runnable: True
# Hash: 1cb4a85c

class DynamicsResult(NamedTuple):
    """Result of dynamics computation."""
    state_derivative: np.ndarray  # dx/dt vector
    success: bool                 # Whether computation succeeded
    info: Dict[str, Any]         # Additional diagnostic information