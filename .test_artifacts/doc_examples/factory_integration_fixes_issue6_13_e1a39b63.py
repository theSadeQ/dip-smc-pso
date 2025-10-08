# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 13
# Runnable: False
# Hash: e1a39b63

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class AdaptiveSMCConfig:
    """Configuration for Adaptive SMC with parameter estimation."""

    # Required Parameters
    gains: List[float]              # [k1, k2, λ1, λ2, γ] - 5 elements
    max_force: float               # Control saturation

    # Adaptation Parameters
    leak_rate: float = 0.01        # Parameter drift prevention (σ)
    dead_zone: float = 0.05        # Adaptation dead zone width
    adapt_rate_limit: float = 10.0  # Maximum adaptation rate
    K_min: float = 0.1             # Minimum adaptive gain
    K_max: float = 100.0           # Maximum adaptive gain
    gamma: float = 2.0             # Adaptation rate (γ)

    # Control Parameters
    boundary_layer: float = 0.1     # Smooth switching layer
    smooth_switch: bool = True      # Enable smooth switching
    dt: float = 0.001              # Integration timestep
    dynamics_model: Optional[object] = None