# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 2
# Runnable: False
# Hash: 1caf58bc

# example-metadata:
# runnable: false

#======================================================================================\\\
#======================== src/controllers/smc/terminal_smc.py ========================\\\
#======================================================================================\\\

"""
Terminal Sliding Mode Controller for double-inverted pendulum.

Implements nonlinear terminal sliding surface for finite-time convergence.
"""

import numpy as np
import logging
import weakref
from typing import TYPE_CHECKING, List, Tuple, Dict, Optional, Union, Sequence

from ...utils import saturate, TerminalSMCOutput

if TYPE_CHECKING:
    from ...plant.models.dynamics import DoubleInvertedPendulum

logger = logging.getLogger(__name__)


class TerminalSMC:
    """
    Terminal Sliding Mode Controller with finite-time convergence.

    Uses nonlinear terminal sliding surface with fractional exponents
    to achieve faster convergence than classical SMC.

    Parameters
    ----------
    gains : array-like
        [k1, k2, λ1, λ2, K, α, β]
        - k1, k2, λ1, λ2: sliding surface gains (positive)
        - K: switching gain (positive)
        - α, β: terminal exponents in (0, 1) for finite-time convergence
    max_force : float
        Maximum control force (N)
    boundary_layer : float
        Boundary layer thickness for chattering reduction
    dynamics_model : DoubleInvertedPendulum, optional
        Dynamics model for equivalent control (if None, uses robust control only)
    singularity_epsilon : float, default=1e-3
        Small value to avoid singularity when velocities near zero
    """

    def __init__(
        self,
        gains: Union[Sequence[float], np.ndarray],
        max_force: float,
        boundary_layer: float,
        dynamics_model: Optional["DoubleInvertedPendulum"] = None,
        singularity_epsilon: float = 1e-3,
        switch_method: str = "tanh",
    ):
        # Validate gain count
        if len(gains) != 7:
            raise ValueError(
                f"Terminal SMC requires 7 gains [k1,k2,λ1,λ2,K,α,β], got {len(gains)}"
            )

        # Extract and validate gains
        self.k1, self.k2, self.lam1, self.lam2, self.K, self.alpha, self.beta = gains

        # Validate gain constraints
        if self.k1 <= 0 or self.k2 <= 0 or self.lam1 <= 0 or self.lam2 <= 0:
            raise ValueError("Surface gains k1, k2, λ1, λ2 must be positive")

        if self.K <= 0:
            raise ValueError("Switching gain K must be positive")

        if not (0 < self.alpha < 1):
            raise ValueError(f"Terminal exponent α must be in (0,1), got {self.alpha}")

        if not (0 < self.beta < 1):
            raise ValueError(f"Terminal exponent β must be in (0,1), got {self.beta}")

        # Store parameters
        self.max_force = max_force
        self.boundary_layer = boundary_layer
        self.singularity_epsilon = singularity_epsilon
        self.switch_method = switch_method

        # Store dynamics model reference (weakref to avoid circular reference)
        if dynamics_model is not None:
            self._dynamics_ref = weakref.ref(dynamics_model)
        else:
            self._dynamics_ref = lambda: None

        logger.info(
            f"Initialized Terminal SMC: gains={gains}, max_force={max_force}, "
            f"boundary_layer={boundary_layer}"
        )

    @property
    def dyn(self):
        """Access dynamics model via weakref."""
        if self._dynamics_ref is not None:
            return self._dynamics_ref()
        return None

    def compute_sliding_surface(self, state: np.ndarray) -> float:
        """
        Compute terminal sliding surface.

        s = k₁·θ₁ + k₂·sign(dθ₁)·|dθ₁|^α + λ₁·θ₂ + λ₂·sign(dθ₂)·|dθ₂|^β

        Parameters
        ----------
        state : np.ndarray
            [x, dx, θ₁, dθ₁, θ₂, dθ₂]

        Returns
        -------
        s : float
            Sliding surface value
        """
        _, _, theta1, dtheta1, theta2, dtheta2 = state

        # Terminal terms with singularity avoidance
        # Add small epsilon to avoid division by zero
        term1 = np.sign(dtheta1) * np.abs(dtheta1 + self.singularity_epsilon) ** self.alpha
        term2 = np.sign(dtheta2) * np.abs(dtheta2 + self.singularity_epsilon) ** self.beta

        # Sliding surface
        s = self.k1 * theta1 + self.k2 * term1 + self.lam1 * theta2 + self.lam2 * term2

        return s

    def switching_function(self, s: float) -> float:
        """
        Continuous approximation to sign function.

        Parameters
        ----------
        s : float
            Sliding surface value

        Returns
        -------
        switch : float
            Switching function output in [-1, 1]
        """
        if self.switch_method == "tanh":
            return np.tanh(s / self.boundary_layer)
        elif self.switch_method == "linear":
            return saturate(s / self.boundary_layer, -1.0, 1.0)
        else:
            raise ValueError(f"Unknown switch method: {self.switch_method}")

    def compute_control(
        self,
        state: np.ndarray,
        state_vars: Optional[Dict] = None,
        history: Optional[Dict] = None,
    ) -> Tuple[float, Dict, Dict]:
        """
        Compute terminal SMC control law.

        Parameters
        ----------
        state : np.ndarray
            State vector [x, dx, θ₁, dθ₁, θ₂, dθ₂]
        state_vars : dict, optional
            Controller internal state (unused for terminal SMC)
        history : dict, optional
            Historical data (unused for terminal SMC)

        Returns
        -------
        control : float
            Control input (force)
        state_vars : dict
            Updated state variables
        history : dict
            Updated history
        """
        # Initialize if None
        if state_vars is None:
            state_vars = {}
        if history is None:
            history = self.initialize_history()

        # Compute sliding surface
        s = self.compute_sliding_surface(state)

        # Compute switching function
        switch = self.switching_function(s)

        # Control law: u = -K·switch(s)
        # (Simplified: no equivalent control for tutorial simplicity)
        control = -self.K * switch

        # Saturate to max force
        control = saturate(control, -self.max_force, self.max_force)

        # Log for debugging
        logger.debug(f"Terminal SMC: s={s:.4f}, switch={switch:.4f}, u={control:.4f}")

        return control, state_vars, history

    def initialize_history(self) -> Dict:
        """Initialize empty history (terminal SMC is memoryless)."""
        return {}

    def cleanup(self):
        """Clean up resources."""
        self._dynamics_ref = None
        logger.debug("Terminal SMC cleaned up")

    def __del__(self):
        """Destructor for automatic cleanup."""
        self.cleanup()