# Example from: docs\factory_integration_documentation.md
# Index: 5
# Runnable: False
# Hash: 89db4d06

class PSOControllerWrapper:
    """Wrapper for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate gain particles for PSO optimization."""
        # Domain-specific validation logic
        return valid_mask

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        # Standardized interface for PSO fitness evaluation
        return control_output