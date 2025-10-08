# Example from: docs\controllers\control_primitives_reference.md
# Index: 32
# Runnable: True
# Hash: ef245e78

from src.utils.control import saturate, smooth_sign
from src.utils.types import STAOutput
from src.utils.numerical_stability import safe_sqrt

class SuperTwistingSMC:
    def __init__(self, gains, dt, max_force):
        self.gains = gains
        self.dt = dt
        self.max_force = max_force

    def compute_control(self, state, state_vars, history):
        K1, K2, k1, k2, lam1, lam2 = self.gains
        z_prev, sigma_prev = state_vars if state_vars else (0.0, 0.0)

        # Compute sliding surface
        x, theta1, theta2, dx, dtheta1, dtheta2 = state
        sigma = lam1 * theta1 + lam2 * theta2 + k1 * dtheta1 + k2 * dtheta2

        # Super-twisting algorithm with safe operations
        u_proportional = -K1 * safe_sqrt(abs(sigma), min_value=1e-15) * smooth_sign(sigma)
        z_new = z_prev - K2 * smooth_sign(sigma) * self.dt
        u = u_proportional + z_new

        # Saturation
        u = np.clip(u, -self.max_force, self.max_force)

        return STAOutput(u=u, state=(z_new, sigma), history={})