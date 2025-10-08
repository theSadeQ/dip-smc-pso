# Example from: docs\api\simulation_engine_api_reference.md
# Index: 11
# Runnable: True
# Hash: 2352e727

class MyDynamics:
    def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
        """Integrate dynamics forward one timestep."""
        return next_state