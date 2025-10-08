# Example from: docs\controllers\factory_system_guide.md
# Index: 16
# Runnable: False
# Hash: 026ab7d1

# example-metadata:
# runnable: false

class PSOControllerWrapper:
    """PSO-friendly wrapper that simplifies the control interface."""

    def __init__(self, controller: SMCProtocol):
        self.controller = controller
        self._history = {}

        # Initialize state_vars based on controller type
        controller_name = type(controller).__name__
        if 'SuperTwisting' in controller_name:
            self._state_vars = (0.0, 0.0)  # (z, sigma)
        elif 'Hybrid' in controller_name:
            self._state_vars = (k1_init, k2_init, 0.0)
        else:
            self._state_vars = ()

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """Simplified compute_control for PSO fitness evaluation."""
        result = self.controller.compute_control(state, self._state_vars, self._history)

        # Extract control value and return as numpy array
        if hasattr(result, 'u'):
            control_value = result.u
        elif isinstance(result, dict) and 'u' in result:
            control_value = result['u']
        else:
            control_value = result

        return np.array([control_value])