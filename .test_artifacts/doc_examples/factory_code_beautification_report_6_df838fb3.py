# Example from: docs\reports\factory_code_beautification_report.md
# Index: 6
# Runnable: False
# Hash: df838fb3

class PSOControllerWrapper:
    """Wrapper for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller: ControllerProtocol, n_gains: int, controller_type: str) -> None:
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate gain particles for PSO optimization."""
        # Controller-specific validation logic

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        # Safe control computation with fallback