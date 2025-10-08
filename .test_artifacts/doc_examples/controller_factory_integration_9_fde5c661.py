# Example from: docs\technical\controller_factory_integration.md
# Index: 9
# Runnable: True
# Hash: fde5c661

class ControllerInterface:
    def compute_control(
        self,
        state: np.ndarray,
        last_control: Any,
        history: dict
    ) -> ControlResult:
        """Compute control action for given state."""
        pass