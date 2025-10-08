# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 5
# Runnable: False
# Hash: cab0e550

# example-metadata:
# runnable: false

class ClassicalSMC(PSO_ControllerInterface):
    """Classical Sliding Mode Controller with PSO interface."""

    def __init__(self, gains: np.ndarray, **kwargs) -> None:
        """Initialize Classical SMC.

        Mathematical Model:
        Sliding surface: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
        Control law: u = -K·sign(s) - kd·ṡ

        Parameters
        ----------
        gains : np.ndarray, shape (6,)
            [c1, λ1, c2, λ2, K, kd]
        """
        if len(gains) != 6:
            raise ValueError(f"Classical SMC requires 6 gains, got {len(gains)}")

        self.c1, self.lambda1, self.c2, self.lambda2, self.K, self.kd = gains
        self._max_force = kwargs.get('max_force', 150.0)
        self.boundary_layer = kwargs.get('boundary_layer', 0.02)

        # Validate stability conditions
        if self.lambda1 <= 0 or self.lambda2 <= 0:
            raise ValueError("Sliding surface coefficients must be positive")
        if self.K <= 0:
            raise ValueError("Control gain must be positive")

    @property
    def max_force(self) -> float:
        """Actuator saturation limit."""
        return self._max_force

    def compute_control(self, state: np.ndarray, dt: float = 0.001) -> float:
        """Compute classical SMC control.

        Mathematical Implementation:
        1. Compute position errors: e₁ = θ₁, e₂ = θ₂
        2. Compute velocity errors: ė₁ = θ̇₁, ė₂ = θ̇₂
        3. Sliding surface: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
        4. Control law: u = -K·sat(s/ε) - kd·ṡ
        """
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

        # Position errors (target is upright: θ₁ = θ₂ = 0)
        e1 = theta1
        e2 = theta2

        # Velocity errors (target velocities are zero)
        e1_dot = theta1_dot
        e2_dot = theta2_dot

        # Sliding surface
        s = self.lambda1 * e1 + self.lambda2 * e2 + e1_dot + e2_dot

        # Boundary layer saturation function
        if abs(s) <= self.boundary_layer:
            sat_s = s / self.boundary_layer
        else:
            sat_s = np.sign(s)

        # Control law
        u = -self.K * sat_s - self.kd * s

        # Apply actuator saturation
        return np.clip(u, -self.max_force, self.max_force)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Validate Classical SMC gain combinations.

        Stability Requirements:
        1. λ₁, λ₂ > 0 (sliding surface stability)
        2. K > 0 (control authority)
        3. Reasonable gain ratios to prevent numerical issues
        """
        n_particles = particles.shape[0]
        valid = np.ones(n_particles, dtype=bool)

        # Extract gain components
        c1, lambda1, c2, lambda2, K, kd = particles.T

        # Stability conditions
        valid &= (lambda1 > 0) & (lambda2 > 0)  # Surface coefficients
        valid &= (K > 0)                        # Control gain
        valid &= (kd >= 0)                      # Derivative gain

        # Numerical stability bounds
        valid &= (lambda1 < 100) & (lambda2 < 100)  # Prevent excessive stiffness
        valid &= (K < 1000)                         # Prevent actuator abuse

        return valid