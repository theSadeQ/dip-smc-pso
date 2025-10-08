# Example from: docs\api\simulation_engine_api_reference.md
# Index: 40
# Runnable: True
# Hash: eb332071

class LinearDynamicsModel(BaseDynamicsModel):
    """Base class for linear dynamics models."""

    def __init__(self, A: np.ndarray, B: np.ndarray, parameters: Any):
        """Initialize linear dynamics model."""
        super().__init__(parameters)
        self.A = A  # System matrix
        self.B = B  # Input matrix
        self._validate_matrices()