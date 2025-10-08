# Example from: docs\controllers\factory_system_guide.md
# Index: 3
# Runnable: False
# Hash: a5d629ae

class PSOControllerWrapper:
    """PSO-friendly wrapper that simplifies the control interface."""

    def __init__(self, controller: SMCProtocol):
        self.controller = controller
        self._history = {}
        self._state_vars = ()  # Controller-specific state

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """Simplified interface for PSO fitness evaluation."""
        # Full interface: compute_control(state, state_vars, history)
        # PSO interface: compute_control(state) -> np.ndarray
        result = self.controller.compute_control(state, self._state_vars, self._history)
        return np.array([self._extract_control_value(result)])