# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 27
# Runnable: False
# Hash: 218c3349

# example-metadata:
# runnable: false

class IsolatedControllerWrapper:
    """Wrapper to ensure controller state isolation."""

    def __init__(self, controller):
        self._controller = controller
        self._state_lock = threading.RLock()
        self._initial_state = self._capture_state()

    def _capture_state(self):
        """Capture controller's initial state."""
        state = {}

        # Capture gains
        if hasattr(self._controller, 'gains'):
            state['gains'] = self._controller.gains.copy()

        # Capture configuration
        if hasattr(self._controller, 'config'):
            state['config'] = self._controller.config

        # Controller-specific state
        if hasattr(self._controller, '_adaptive_gains'):
            state['adaptive_gains'] = self._controller._adaptive_gains.copy()

        return state

    def reset_state(self):
        """Reset controller to initial state."""
        with self._state_lock:
            # Reset gains
            if 'gains' in self._initial_state:
                self._controller.gains = self._initial_state['gains'].copy()

            # Reset adaptive state
            if hasattr(self._controller, '_adaptive_gains') and 'adaptive_gains' in self._initial_state:
                self._controller._adaptive_gains = self._initial_state['adaptive_gains'].copy()

            # Call controller's reset method
            if hasattr(self._controller, 'reset'):
                self._controller.reset()

    def compute_control(self, state, last_control=0.0, history=None):
        """Thread-safe control computation."""
        with self._state_lock:
            # Ensure clean state
            if history is None:
                history = {}

            # Compute control
            result = self._controller.compute_control(state, last_control, history)

            return result

    def __getattr__(self, name):
        """Delegate other attributes to wrapped controller."""
        return getattr(self._controller, name)

# Usage with thread safety
def create_isolated_controller(controller_type, **kwargs):
    """Create controller with state isolation."""

    base_controller = create_controller(controller_type, **kwargs)
    return IsolatedControllerWrapper(base_controller)

# PSO with isolated controllers
def isolated_fitness_function(gains):
    """PSO fitness function with isolated controllers."""

    controller = create_isolated_controller('classical_smc', gains=gains)

    try:
        performance = evaluate_controller_performance(controller)
        return performance['total_cost']
    finally:
        # Ensure clean state for next use
        controller.reset_state()