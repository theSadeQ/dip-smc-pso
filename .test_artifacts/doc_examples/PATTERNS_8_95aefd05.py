# Example from: docs\PATTERNS.md
# Index: 8
# Runnable: False
# Hash: 95aefd05

# example-metadata:
# runnable: false

# src/controllers/factory.py (lines 942-1012)

class PSOControllerWrapper:
    """Adapter for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller  # Wrapped legacy controller
        self.n_gains = n_gains
        self.controller_type = controller_type

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """Adapt legacy controller interface to PSO-compatible format."""
        # Legacy interface: compute_control(state, last_control, history)
        # PSO interface: compute_control(state) -> control_array

        result = self.controller.compute_control(state, (), {})

        # Extract and format control output for PSO
        if hasattr(result, 'u'):
            u = result.u
        else:
            u = result

        return np.array([u])  # Convert to numpy array