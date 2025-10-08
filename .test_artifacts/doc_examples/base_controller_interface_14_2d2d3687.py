# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 14
# Runnable: True
# Hash: 2d2d3687

from src.controllers.base.controller_interface import Controller
from abc import ABC

class MyCustomSMC(Controller):
    """Custom SMC implementation."""

    def __init__(self, gains, max_force):
        self.gains = gains
        self.max_force = max_force

    def compute_control(self, state, state_vars, history):
        # Custom control law
        theta1, theta2 = state[2], state[4]
        theta1_dot, theta2_dot = state[3], state[5]

        # Custom sliding surface
        s = self.gains[0] * theta1 + self.gains[1] * theta1_dot

        # Custom switching law
        u = -self.gains[2] * np.sign(s)
        u = np.clip(u, -self.max_force, self.max_force)

        return u, state_vars, history

    def initialize_history(self):
        return {'states': [], 'times': []}

# Use custom controller with existing simulation infrastructure
custom_controller = MyCustomSMC(gains=[10.0, 5.0, 50.0], max_force=100.0)
result = simulate(custom_controller, duration=5.0)  # Works!