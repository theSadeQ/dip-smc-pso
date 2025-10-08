# Example from: docs\configuration_integration_documentation.md
# Index: 7
# Runnable: False
# Hash: 30fe8206

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class AdaptiveSMCConfig:
    """Type-safe configuration for Adaptive SMC controller."""

    # Required parameters
    gains: List[float] = field()                           # [k1, k2, λ1, λ2, γ]
    max_force: float = field()                             # Control saturation limit
    dt: float = field()                                    # Control timestep

    # Adaptive parameters
    leak_rate: float = field(default=0.01)                 # σ-modification leak rate
    dead_zone: float = field(default=0.05)                 # Adaptation dead zone
    adapt_rate_limit: float = field(default=10.0)          # Maximum adaptation rate
    K_min: float = field(default=0.1)                      # Minimum adaptive gain
    K_max: float = field(default=100.0)                    # Maximum adaptive gain
    K_init: float = field(default=10.0)                    # Initial adaptive gain
    alpha: float = field(default=0.5)                      # Adaptation smoothing
    boundary_layer: float = field(default=0.01)            # Chattering reduction
    smooth_switch: bool = field(default=True)              # Smooth switching

    # Optional dynamics model
    dynamics_model: Optional[object] = field(default=None, compare=False)

    def __post_init__(self):
        """Validate adaptive SMC configuration."""
        self._validate_gains()
        self._validate_adaptive_parameters()
        self._validate_adaptation_stability()

    def _validate_gains(self):
        """Validate gain array for adaptive SMC."""
        if len(self.gains) != 5:
            raise ValueError("Adaptive SMC requires exactly 5 gains: [k1, k2, λ1, λ2, γ]")

        if not all(g > 0 for g in self.gains):
            raise ValueError("All gains must be positive")

        k1, k2, lam1, lam2, gamma = self.gains

        # Adaptation rate constraints
        if gamma <= 0:
            raise ValueError("Adaptation rate γ must be positive")

        if gamma > 50:
            raise ValueError("Adaptation rate γ > 50 may cause instability")

        # Surface stability
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Surface coefficients must be positive")

    def _validate_adaptive_parameters(self):
        """Validate adaptation-specific parameters."""
        if not 0 < self.leak_rate < 1:
            raise ValueError("leak_rate must be in (0, 1)")

        if self.dead_zone <= 0:
            raise ValueError("dead_zone must be positive")

        if self.adapt_rate_limit <= 0:
            raise ValueError("adapt_rate_limit must be positive")

        if not 0 < self.K_min < self.K_max:
            raise ValueError("Must have 0 < K_min < K_max")

        if not self.K_min <= self.K_init <= self.K_max:
            raise ValueError("K_init must be in [K_min, K_max]")

    def _validate_adaptation_stability(self):
        """Validate adaptation stability requirements."""
        k1, k2, lam1, lam2, gamma = self.gains

        # Ensure adaptation is not too aggressive relative to surface dynamics
        surface_time_constant = min(1/lam1, 1/lam2)
        adaptation_time_constant = 1/gamma

        if adaptation_time_constant < 0.1 * surface_time_constant:
            print(f"Warning: Fast adaptation (τ_adapt={adaptation_time_constant:.3f}) "
                  f"relative to surface dynamics (τ_surface={surface_time_constant:.3f})")