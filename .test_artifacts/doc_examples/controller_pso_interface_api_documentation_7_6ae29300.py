# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 7
# Runnable: False
# Hash: 6ae29300

# example-metadata:
# runnable: false

class STASMC(PSO_ControllerInterface):
    """Super-Twisting Algorithm Sliding Mode Controller."""

    def __init__(self, gains: np.ndarray, **kwargs) -> None:
        """Initialize STA-SMC.

        Mathematical Model:
        Sliding surface: s = k₁θ₁ + k₂θ₂ + λ₁θ̇₁ + λ₂θ̇₂
        Super-twisting control:
        u̇ = -K₂·sign(s)
        u = -K₁·|s|^(1/2)·sign(s) + ∫u̇dt

        Parameters
        ----------
        gains : np.ndarray, shape (6,)
            [K1, K2, k1, k2, λ1, λ2]
        """
        if len(gains) != 6:
            raise ValueError(f"STA-SMC requires 6 gains, got {len(gains)}")

        self.K1, self.K2, self.k1, self.k2, self.lambda1, self.lambda2 = gains
        self._max_force = kwargs.get('max_force', 150.0)
        self.dt = kwargs.get('dt', 0.001)

        # Internal states for super-twisting algorithm
        self.u_integral = 0.0
        self.boundary_layer = kwargs.get('boundary_layer', 0.05)

        # Validate super-twisting stability conditions
        if self.K1 <= 0 or self.K2 <= 0:
            raise ValueError("Super-twisting gains must be positive")
        if self.lambda1 <= 0 or self.lambda2 <= 0:
            raise ValueError("Surface coefficients must be positive")

    @property
    def max_force(self) -> float:
        """Actuator saturation limit."""
        return self._max_force

    def compute_control(self, state: np.ndarray, dt: float = 0.001) -> float:
        """Compute super-twisting SMC control.

        Mathematical Implementation:
        1. Sliding surface: s = k₁θ₁ + k₂θ₂ + λ₁θ̇₁ + λ₂θ̇₂
        2. First-order term: u₁ = -K₁·|s|^(1/2)·sign(s)
        3. Second-order term: u̇₂ = -K₂·sign(s)
        4. Total control: u = u₁ + u₂
        """
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

        # Sliding surface computation
        s = (self.k1 * theta1 + self.k2 * theta2 +
             self.lambda1 * theta1_dot + self.lambda2 * theta2_dot)

        # Super-twisting algorithm
        if abs(s) <= self.boundary_layer:
            # Boundary layer approximation
            u1 = -self.K1 * (abs(s) / self.boundary_layer)**0.5 * s / self.boundary_layer
            u2_dot = -self.K2 * s / self.boundary_layer
        else:
            # Traditional super-twisting
            u1 = -self.K1 * np.sqrt(abs(s)) * np.sign(s)
            u2_dot = -self.K2 * np.sign(s)

        # Integrate second-order term
        self.u_integral += u2_dot * dt

        # Total control
        u = u1 + self.u_integral

        # Apply actuator saturation
        return np.clip(u, -self.max_force, self.max_force)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate STA-SMC gain combinations.

        Super-Twisting Stability Conditions:
        1. K₁, K₂ > 0 (algorithmic gains)
        2. λ₁, λ₂ > 0 (surface coefficients)
        3. Sufficient condition: K₁ > L, K₂ > K₁·C (where L, C are bounds)
        """
        n_particles = particles.shape[0]
        valid = np.ones(n_particles, dtype=bool)

        # Extract gains
        K1, K2, k1, k2, lambda1, lambda2 = particles.T

        # Basic positivity
        valid &= (K1 > 0) & (K2 > 0)
        valid &= (k1 > 0) & (k2 > 0)
        valid &= (lambda1 > 0) & (lambda2 > 0)

        # Super-twisting stability condition (simplified)
        valid &= (K2 > K1 * 0.5)  # Simplified sufficient condition

        # Practical bounds to prevent excessive oscillations
        valid &= (K1 < 50) & (K2 < 50)
        valid &= (lambda1 < 20) & (lambda2 < 20)

        return valid