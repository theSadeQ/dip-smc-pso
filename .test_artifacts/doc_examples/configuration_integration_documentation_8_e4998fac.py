# Example from: docs\configuration_integration_documentation.md
# Index: 8
# Runnable: False
# Hash: e4998fac

@dataclass(frozen=True)
class SuperTwistingSMCConfig:
    """Type-safe configuration for Super-Twisting SMC controller."""

    # Required parameters
    gains: List[float] = field()                           # [K1, K2, k1, k2, λ1, λ2]
    max_force: float = field()                             # Control saturation limit
    dt: float = field()                                    # Control timestep

    # Super-twisting specific parameters
    power_exponent: float = field(default=0.5)             # Fractional power (0 < α < 1)
    regularization: float = field(default=1e-6)            # Singularity avoidance
    boundary_layer: float = field(default=0.01)            # Chattering reduction
    switch_method: Literal["tanh", "linear", "sign"] = field(default="tanh")
    damping_gain: float = field(default=0.0)               # Additional damping

    # Optional dynamics model
    dynamics_model: Optional[object] = field(default=None, compare=False)

    def __post_init__(self):
        """Validate super-twisting configuration."""
        self._validate_gains()
        self._validate_twisting_parameters()
        self._validate_convergence_conditions()

    def _validate_gains(self):
        """Validate gain array for super-twisting SMC."""
        if len(self.gains) != 6:
            raise ValueError("Super-twisting SMC requires 6 gains: [K1, K2, k1, k2, λ1, λ2]")

        if not all(g > 0 for g in self.gains):
            raise ValueError("All gains must be positive")

        K1, K2, k1, k2, lam1, lam2 = self.gains

        # Super-twisting stability conditions
        if K1 <= 0 or K2 <= 0:
            raise ValueError("Algorithmic gains K1, K2 must be positive")

        # Surface gains
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Surface coefficients must be positive")

    def _validate_twisting_parameters(self):
        """Validate super-twisting specific parameters."""
        if not 0 < self.power_exponent < 1:
            raise ValueError("Power exponent must be in (0, 1) for finite-time convergence")

        if self.regularization <= 0:
            raise ValueError("Regularization must be positive")

        if self.boundary_layer <= 0:
            raise ValueError("Boundary layer must be positive")

        if self.damping_gain < 0:
            raise ValueError("Damping gain must be non-negative")

    def _validate_convergence_conditions(self):
        """Validate finite-time convergence conditions."""
        K1, K2, k1, k2, lam1, lam2 = self.gains

        # Super-twisting convergence requires specific gain relationships
        # Sufficient condition: K1 > √(2)*uncertainty_bound
        # and K2 > uncertainty_bound for some uncertainty bound

        # Check gain ratios for practical convergence
        if K2 > 2 * K1:
            print(f"Warning: K2={K2} > 2*K1={2*K1}, may cause oscillations")

        if K1 < max(k1, k2):
            print(f"Warning: K1={K1} < max(k1,k2), may not achieve finite-time convergence")