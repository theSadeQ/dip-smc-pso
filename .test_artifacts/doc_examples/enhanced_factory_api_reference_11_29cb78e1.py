# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 11
# Runnable: False
# Hash: 29cb78e1

class PSOControllerWrapper:
    """Wrapper providing PSO-compatible interface for SMC controllers."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate gain particles for PSO optimization."""
        # Controller-specific validation logic

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        # Simplified interface for fitness evaluation