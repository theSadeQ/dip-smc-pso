# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 2
# Runnable: True
# Hash: 0719bc92

from typing import Protocol, Optional, Union, Any
import numpy as np

class PSO_ControllerInterface(Protocol):
    """PSO-compatible controller interface protocol."""

    def __init__(self, gains: np.ndarray, **kwargs) -> None:
        """Initialize controller with PSO-optimized gains.

        Parameters
        ----------
        gains : np.ndarray, shape (n,)
            Controller gain vector from PSO particle
            - Classical SMC: [c1, λ1, c2, λ2, K, kd] ∈ ℝ⁶
            - STA-SMC: [K1, K2, k1, k2, λ1, λ2] ∈ ℝ⁶
            - Adaptive SMC: [c1, λ1, c2, λ2, γ] ∈ ℝ⁵
            - Hybrid Adaptive: [c1, λ1, c2, λ2] ∈ ℝ⁴
        **kwargs
            Additional controller-specific parameters
        """

    @property
    def max_force(self) -> float:
        """Actuator saturation limit [N].

        Required for PSO simulation bounds.
        Typical range: [50.0, 200.0] N
        """

    def compute_control(self,
                       state: np.ndarray,
                       dt: float = 0.001,
                       **kwargs) -> float:
        """Compute control command for current state.

        Parameters
        ----------
        state : np.ndarray, shape (6,)
            System state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
        dt : float, optional
            Sampling time [s]

        Returns
        -------
        float
            Control command u(t) ∈ [-max_force, max_force]
        """

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Optional: Pre-filter invalid particles.

        Parameters
        ----------
        particles : np.ndarray, shape (n_particles, n_gains)
            Swarm particle matrix

        Returns
        -------
        np.ndarray, shape (n_particles,), dtype=bool
            Boolean mask indicating valid particles

        Notes
        -----
        This method enables early rejection of unstable gain combinations
        before expensive simulation evaluation.
        """