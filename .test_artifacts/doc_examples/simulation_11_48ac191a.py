# Example from: docs\guides\api\simulation.md
# Index: 11
# Runnable: True
# Hash: 48ac191a

from src.core.dynamics import BaseDynamics
import numpy as np

class FrictionEnhancedDynamics(BaseDynamics):
    """Dynamics with enhanced friction model."""

    def __init__(self, params, friction_model='coulomb'):
        super().__init__(params)
        self.friction_model = friction_model

    def compute_dynamics(self, state, control):
        """
        Compute state derivatives with enhanced friction.

        Parameters
        ----------
        state : np.ndarray, shape (6,)
            Current state [x, dx, θ₁, dθ₁, θ₂, dθ₂]
        control : float
            Control force (N)

        Returns
        -------
        state_dot : np.ndarray, shape (6,)
            State derivatives
        """
        x, dx, theta1, dtheta1, theta2, dtheta2 = state

        # Apply friction model
        if self.friction_model == 'coulomb':
            friction = self._coulomb_friction(dx)
        elif self.friction_model == 'viscous':
            friction = self._viscous_friction(dx)
        else:
            friction = 0.0

        # Base dynamics computation
        base_dynamics = super().compute_dynamics(state, control)

        # Add friction effects
        state_dot = base_dynamics.copy()
        state_dot[1] -= friction  # Apply friction to cart velocity

        return state_dot

    def _coulomb_friction(self, velocity):
        """Coulomb friction model."""
        mu_c = 0.2  # Coulomb friction coefficient
        return mu_c * np.sign(velocity)

    def _viscous_friction(self, velocity):
        """Viscous friction model."""
        b = 0.5  # Viscous friction coefficient
        return b * velocity