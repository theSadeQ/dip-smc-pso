# Example from: docs\technical\controller_factory_integration.md
# Index: 16
# Runnable: False
# Hash: a22d3ae6

class PSOControllerWrapper:
    """Wrapper for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        result = self.controller.compute_control(state, (), {})

        # Extract and normalize control value
        if hasattr(result, 'u'):
            u = result.u
        elif isinstance(result, dict) and 'u' in result:
            u = result['u']
        else:
            u = result

        return np.array([u]) if isinstance(u, (int, float)) else u