# Example from: docs\controllers\factory_system_guide.md
# Index: 11
# Runnable: False
# Hash: c203fda0

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class SMCConfig:
    """Clean configuration for all SMC controllers."""

    # Core parameters (common to all SMCs)
    gains: List[float]
    max_force: float = 100.0
    dt: float = 0.01

    # Optional dynamics model
    dynamics_model: Optional[Any] = None

    # Controller-specific parameters (use defaults if not specified)
    boundary_layer: float = 0.01
    damping_gain: float = 0.0

    # Adaptive SMC specific
    leak_rate: float = 0.1
    adapt_rate_limit: float = 100.0
    K_min: float = 0.1
    K_max: float = 100.0
    # ... additional parameters