# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 9
# Runnable: False
# Hash: 2df3a462

class AdaptiveSMC(PSO_ControllerInterface):
    """Adaptive Sliding Mode Controller with uncertainty estimation."""

    def __init__(self, gains: np.ndarray, **kwargs) -> None:
        """Initialize Adaptive SMC.

        Mathematical Model:
        Sliding surface: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
        Adaptive control: u = -K̂(t)·sign(s)
        Adaptation law: K̇ = γ·|s| for |s| > δ, 0 otherwise

        Parameters
        ----------
        gains : np.ndarray, shape (5,)
            [c1, λ1, c2, λ2, γ]
        """
        if len(gains) != 5:
            raise ValueError(f"Adaptive SMC requires 5 gains, got {len(gains)}")

        self.c1, self.lambda1, self.c2, self.lambda2, self.gamma = gains
        self._max_force = kwargs.get('max_force', 150.0)

        # Adaptive gain initialization
        self.K_adaptive = kwargs.get('K_init', 1.0)
        self.K_min = kwargs.get('K_min', 0.1)
        self.K_max = kwargs.get('K_max', 100.0)
        self.dead_zone = kwargs.get('dead_zone', 0.05)

        # Validate adaptation parameters
        if self.gamma <= 0:
            raise ValueError("Adaptation rate must be positive")
        if self.lambda1 <= 0 or self.lambda2 <= 0:
            raise ValueError("Surface coefficients must be positive")

    @property
    def max_force(self) -> float:
        """Actuator saturation limit."""
        return self._max_force

    def compute_control(self, state: np.ndarray, dt: float = 0.001) -> float:
        """Compute adaptive SMC control.

        Mathematical Implementation:
        1. Sliding surface: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
        2. Adaptation law: K̇ = γ·|s| (outside dead zone)
        3. Control law: u = -K̂(t)·sign(s)
        """
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

        # Position and velocity errors
        e1, e2 = theta1, theta2
        e1_dot, e2_dot = theta1_dot, theta2_dot

        # Sliding surface
        s = self.lambda1 * e1 + self.lambda2 * e2 + e1_dot + e2_dot

        # Adaptive gain update (outside dead zone)
        if abs(s) > self.dead_zone:
            K_dot = self.gamma * abs(s)
            self.K_adaptive += K_dot * dt
            self.K_adaptive = np.clip(self.K_adaptive, self.K_min, self.K_max)

        # Control law
        if abs(s) <= self.dead_zone:
            sat_s = s / self.dead_zone
        else:
            sat_s = np.sign(s)

        u = -self.K_adaptive * sat_s

        return np.clip(u, -self.max_force, self.max_force)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate Adaptive SMC parameters."""
        n_particles = particles.shape[0]
        valid = np.ones(n_particles, dtype=bool)

        c1, lambda1, c2, lambda2, gamma = particles.T

        # Basic constraints
        valid &= (lambda1 > 0) & (lambda2 > 0)  # Surface stability
        valid &= (gamma > 0)                    # Adaptation positivity
        valid &= (c1 > 0) & (c2 > 0)          # Surface gains

        # Practical bounds
        valid &= (gamma < 10)  # Prevent excessive adaptation speed
        valid &= (lambda1 < 50) & (lambda2 < 50)  # Numerical stability

        return valid