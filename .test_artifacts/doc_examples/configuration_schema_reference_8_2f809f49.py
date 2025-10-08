# Example from: docs\technical\configuration_schema_reference.md
# Index: 8
# Runnable: False
# Hash: 2f809f49

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class AdaptiveSMCConfig:
    """Configuration for Adaptive SMC with parameter estimation."""

    # Required Parameters
    gains: List[float]                           # [k1, k2, λ1, λ2, γ]
    max_force: float                            # Control saturation limit [N]
    dt: float                                   # Integration timestep [s]

    # Adaptation Parameters
    leak_rate: float = 0.01                     # Parameter drift prevention σ
    dead_zone: float = 0.05                     # Adaptation dead zone width
    adapt_rate_limit: float = 10.0              # Maximum adaptation rate
    K_min: float = 0.1                          # Minimum adaptive gain
    K_max: float = 100.0                        # Maximum adaptive gain
    K_init: float = 10.0                        # Initial adaptive gain
    alpha: float = 0.5                          # Adaptation smoothing factor

    # Control Parameters
    boundary_layer: float = 0.01                # Smooth switching layer
    smooth_switch: bool = True                  # Enable smooth switching

    # Optional dynamics model
    dynamics_model: Optional[object] = None