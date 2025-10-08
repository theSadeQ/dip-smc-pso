# Example from: docs\controllers\control_primitives_reference.md
# Index: 31
# Runnable: True
# Hash: 6fda69e4

from src.utils.control import saturate, dead_zone
from src.utils.types import AdaptiveSMCOutput
from src.utils.numerical_stability import safe_divide

class AdaptiveSMC:
    def __init__(self, gains, dt, max_force, leak_rate, dead_zone_threshold):
        self.gains = gains
        self.dt = dt
        self.max_force = max_force
        self.leak_rate = leak_rate
        self.dead_zone = dead_zone_threshold
        self.K_init = 10.0

    def compute_control(self, state, state_vars, history):
        K_prev = state_vars[0] if state_vars else self.K_init

        # Compute sliding surface
        k1, k2, lam1, lam2, gamma = self.gains
        x, theta1, theta2, dx, dtheta1, dtheta2 = state
        sigma = lam1 * theta1 + lam2 * theta2 + k1 * dtheta1 + k2 * dtheta2

        # Adaptive gain update with dead zone
        if abs(sigma) <= self.dead_zone:
            dK = 0.0  # Freeze inside dead zone
        else:
            sigma_active = dead_zone(sigma, self.dead_zone)
            dK = gamma * abs(sigma_active) - self.leak_rate * (K_prev - self.K_init)

        K_new = K_prev + dK * self.dt
        K_new = np.clip(K_new, 0.1, 100.0)  # Saturation

        # Control law
        u = -K_new * saturate(sigma, epsilon=0.01, method='tanh')
        u = np.clip(u, -self.max_force, self.max_force)

        return AdaptiveSMCOutput(u=u, state=(K_new,), history={}, sigma=sigma)