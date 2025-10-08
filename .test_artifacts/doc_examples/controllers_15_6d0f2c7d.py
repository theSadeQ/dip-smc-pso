# Example from: docs\guides\api\controllers.md
# Index: 15
# Runnable: True
# Hash: 6d0f2c7d

# my_custom_controller.py
import numpy as np
from src.controllers.base import BaseController

class TerminalSMC(BaseController):
    """Terminal sliding mode controller with finite-time convergence."""

    def __init__(self, gains, max_force=100.0, alpha=0.5):
        """
        Parameters
        ----------
        gains : list[float]
            [k1, k2, λ1, λ2, K, p, q] where p/q < 1
        max_force : float
            Control saturation limit
        alpha : float
            Terminal attractor exponent
        """
        super().__init__(max_force=max_force)

        if len(gains) != 7:
            raise ValueError("Terminal SMC requires 7 gains")

        self.k1, self.k2, self.lam1, self.lam2 = gains[:4]
        self.K, self.p, self.q = gains[4:]
        self.alpha = alpha

    def compute_control(self, state, state_vars, history):
        """Compute terminal SMC control law."""
        x, dx, theta1, dtheta1, theta2, dtheta2 = state

        # Terminal sliding surface
        s = (self.k1 * theta1 + self.k2 * dtheta1 +
             self.lam1 * theta2 + self.lam2 * dtheta2)

        # Terminal attractor term
        terminal_term = np.sign(s) * np.abs(s)**(self.p / self.q)

        # Control law
        u = -self.K * (s + self.alpha * terminal_term)

        # Saturate
        u = np.clip(u, -self.max_force, self.max_force)

        # Update history
        history['sliding_surface'].append(s)
        history['control'].append(u)

        return u, state_vars, history

    def initialize_history(self):
        """Initialize history tracking."""
        return {
            'sliding_surface': [],
            'control': []
        }