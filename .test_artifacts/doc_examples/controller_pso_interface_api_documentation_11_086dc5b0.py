# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 11
# Runnable: False
# Hash: 086dc5b0

class HybridAdaptiveSTASMC(PSO_ControllerInterface):
    """Hybrid Adaptive Super-Twisting SMC with dual adaptation."""

    def __init__(self, gains: np.ndarray, **kwargs) -> None:
        """Initialize Hybrid Adaptive STA-SMC.

        Mathematical Model:
        Combines adaptive gain estimation with super-twisting algorithm.
        Sliding surface: s = c₁θ₁ + c₂θ₂ + λ₁∫θ₁dt + λ₂∫θ₂dt
        Adaptive STA: u = -k₁(t)·|s|^(1/2)·sign(s) + u₂
        where k₁(t) adapts based on sliding surface magnitude.

        Parameters
        ----------
        gains : np.ndarray, shape (4,)
            [c1, λ1, c2, λ2]
        """
        if len(gains) != 4:
            raise ValueError(f"Hybrid Adaptive STA-SMC requires 4 gains, got {len(gains)}")

        self.c1, self.lambda1, self.c2, self.lambda2 = gains
        self._max_force = kwargs.get('max_force', 150.0)

        # Adaptive parameters
        self.k1_adaptive = kwargs.get('k1_init', 4.0)
        self.k2_adaptive = kwargs.get('k2_init', 0.4)
        self.k1_adapt_rate = kwargs.get('k1_adapt_rate', 0.5)
        self.k2_adapt_rate = kwargs.get('k2_adapt_rate', 0.05)

        # Internal states
        self.theta1_integral = 0.0
        self.theta2_integral = 0.0
        self.u2_integral = 0.0
        self.dt = kwargs.get('dt', 0.001)

        # Validation
        if any(g <= 0 for g in gains):
            raise ValueError("All gains must be positive")

    @property
    def max_force(self) -> float:
        """Actuator saturation limit."""
        return self._max_force

    def compute_control(self, state: np.ndarray, dt: float = 0.001) -> float:
        """Compute hybrid adaptive STA control.

        Mathematical Implementation:
        1. Update integral terms
        2. Compute sliding surface with integral action
        3. Adapt gains based on sliding surface
        4. Apply super-twisting algorithm
        """
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

        # Update integral terms
        self.theta1_integral += theta1 * dt
        self.theta2_integral += theta2 * dt

        # Sliding surface with integral action
        s = (self.c1 * theta1 + self.c2 * theta2 +
             self.lambda1 * self.theta1_integral +
             self.lambda2 * self.theta2_integral)

        # Adaptive gain updates
        if abs(s) > 0.01:  # Dead zone
            self.k1_adaptive += self.k1_adapt_rate * abs(s) * dt
            self.k2_adaptive += self.k2_adapt_rate * abs(s) * dt

        # Bound adaptive gains
        self.k1_adaptive = np.clip(self.k1_adaptive, 0.1, 50.0)
        self.k2_adaptive = np.clip(self.k2_adaptive, 0.01, 5.0)

        # Super-twisting control
        u1 = -self.k1_adaptive * np.sqrt(abs(s)) * np.sign(s)
        u2_dot = -self.k2_adaptive * np.sign(s)
        self.u2_integral += u2_dot * dt

        u = u1 + self.u2_integral

        return np.clip(u, -self.max_force, self.max_force)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate Hybrid Adaptive STA-SMC gains."""
        n_particles = particles.shape[0]
        valid = np.ones(n_particles, dtype=bool)

        c1, lambda1, c2, lambda2 = particles.T

        # All gains must be positive
        valid &= (c1 > 0) & (lambda1 > 0) & (c2 > 0) & (lambda2 > 0)

        # Practical bounds for stability
        valid &= (c1 < 100) & (c2 < 100)
        valid &= (lambda1 < 50) & (lambda2 < 50)

        return valid