# Example from: docs\api\simulation_engine_api_reference.md
# Index: 19
# Runnable: True
# Hash: 4a1c7afe

class SimulationRunner:
    """Object-oriented wrapper around run_simulation function."""

    def __init__(self, dynamics_model: Any, dt: float = 0.01, max_time: float = 10.0):
        """Initialize simulation runner."""