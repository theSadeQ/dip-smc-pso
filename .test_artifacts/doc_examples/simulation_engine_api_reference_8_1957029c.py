# Example from: docs\api\simulation_engine_api_reference.md
# Index: 8
# Runnable: True
# Hash: 1957029c

class MyController:
    def __call__(self, t: float, x: np.ndarray) -> float:
        """Compute control given time and state."""
        return control_value