# Example from: docs\api\simulation_engine_api_reference.md
# Index: 21
# Runnable: True
# Hash: d4b0a2dc

def run_simulation(
    self,
    initial_state: np.ndarray,
    controller: Optional[Any] = None,
    reference: Optional[np.ndarray] = None,
    **kwargs: Any
) -> dict[str, Any]:
    """Run simulation using functional API."""