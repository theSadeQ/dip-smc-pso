# Example from: docs\guides\api\plant-models.md
# Index: 7
# Runnable: True
# Hash: 070ce28b

from src.core.dynamics_full import FullDynamics
import numpy as np

class CoulombFrictionDynamics(FullDynamics):
    """Full dynamics with Coulomb friction model."""

    def __init__(self, params, mu_coulomb=0.2):
        """
        Parameters
        ----------
        params : DIPParams
            Physics parameters
        mu_coulomb : float
            Coulomb friction coefficient
        """
        super().__init__(params)
        self.mu_coulomb = mu_coulomb

    def compute_dynamics(self, state, control):
        """Compute state derivatives with Coulomb friction."""
        x, dx, theta1, dtheta1, theta2, dtheta2 = state

        # Coulomb friction force
        F_coulomb = self.mu_coulomb * self.params.m0 * self.params.g * np.sign(dx)

        # Apply Coulomb friction to control input
        effective_control = control - F_coulomb

        # Use parent class dynamics with modified control
        return super().compute_dynamics(state, effective_control)