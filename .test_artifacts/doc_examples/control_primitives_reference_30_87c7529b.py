# Example from: docs\controllers\control_primitives_reference.md
# Index: 30
# Runnable: True
# Hash: 87c7529b

from src.utils.control import saturate
from src.utils.types import ClassicalSMCOutput
from src.utils.validation import require_positive

class ClassicalSMC:
    def __init__(self, gains, max_force, boundary_layer):
        # Parameter validation
        self.gains = [require_positive(g, f"gains[{i}]") for i, g in enumerate(gains)]
        self.max_force = require_positive(max_force, "max_force")
        self.boundary_layer = require_positive(boundary_layer, "boundary_layer")

    def compute_control(self, state, state_vars, history):
        # Extract state
        x, theta1, theta2, dx, dtheta1, dtheta2 = state

        # Compute sliding surface
        k1, k2, lam1, lam2, K, kd = self.gains
        sigma = lam1 * theta1 + lam2 * theta2 + k1 * dtheta1 + k2 * dtheta2

        # Continuous control law with saturation
        u_switch = -K * saturate(sigma, self.boundary_layer, method='tanh', slope=3.0)
        u_damping = -kd * saturate(sigma, self.boundary_layer, method='tanh', slope=3.0)
        u = np.clip(u_switch + u_damping, -self.max_force, self.max_force)

        # Return structured output
        return ClassicalSMCOutput(u=u, state=(), history={})