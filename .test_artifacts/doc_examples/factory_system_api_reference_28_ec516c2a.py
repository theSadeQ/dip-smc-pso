# Example from: docs\api\factory_system_api_reference.md
# Index: 28
# Runnable: False
# Hash: ec516c2a

class PSOControllerWrapper:
    """Wrapper for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)
        self.dynamics_model = getattr(controller, 'dynamics_model', None)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate gain particles for PSO optimization."""
        # Checks gain count, finiteness, positivity, and controller-specific constraints
        ...

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        # Simplified interface for PSO fitness evaluation
        ...