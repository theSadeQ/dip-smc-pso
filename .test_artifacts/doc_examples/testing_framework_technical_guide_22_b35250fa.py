# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 22
# Runnable: False
# Hash: b35250fa

# tests/mocks/mock_controller.py

class MockController:
    """Mock controller for testing simulation framework."""

    def __init__(self, control_value=0.0):
        self.control_value = control_value
        self.call_count = 0

    def compute_control(self, state, state_vars, history):
        self.call_count += 1
        return {
            'control_output': self.control_value,
            'state_vars': state_vars,
            'history': history
        }

    def initialize_history(self):
        return {}


class MockDynamics:
    """Mock dynamics for testing controllers."""

    def __init__(self, dynamics_function=None):
        self.dynamics_function = dynamics_function or (lambda state, control: np.zeros(6))

    def dynamics(self, state, control):
        return self.dynamics_function(state, control)