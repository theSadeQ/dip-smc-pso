# Example from: docs\technical\configuration_schema_reference.md
# Index: 11
# Runnable: False
# Hash: c0b2a9d6

@dataclass(frozen=True)
class HybridSMCConfig:
    """Configuration for Hybrid Adaptive STA-SMC controller."""

    # Required Parameters
    hybrid_mode: HybridMode                      # Control mode selection
    dt: float                                   # Integration timestep [s]
    max_force: float                            # Control saturation limit [N]

    # Sub-Controller Configurations
    classical_config: ClassicalSMCConfig        # Classical SMC settings
    adaptive_config: AdaptiveSMCConfig          # Adaptive SMC settings

    # Hybrid-Specific Parameters
    k1_init: float = 4.0                       # Initial proportional gain
    k2_init: float = 0.4                       # Initial integral gain
    gamma1: float = 2.0                        # k1 adaptation rate
    gamma2: float = 0.5                        # k2 adaptation rate
    dead_zone: float = 0.05                    # Adaptation dead zone

    # Advanced Options
    enable_equivalent: bool = False             # Model-based equivalent control
    damping_gain: float = 3.0                  # Additional damping
    adapt_rate_limit: float = 5.0              # Rate limiting
    sat_soft_width: float = 0.05               # Soft saturation width