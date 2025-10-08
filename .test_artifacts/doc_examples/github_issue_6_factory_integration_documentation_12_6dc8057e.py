# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 12
# Runnable: False
# Hash: 6dc8057e

@dataclass(frozen=True)
class SMCConfig:
    """
    Complete configuration for SMC controllers.

    Attributes:
        gains: Controller gain parameters (varies by type)
        max_force: Maximum control force saturation [N]
        dt: Control timestep [s]
        boundary_layer: Boundary layer thickness for chattering reduction

    Controller-Specific Parameters:
        # Adaptive SMC
        leak_rate: Parameter drift prevention rate
        adapt_rate_limit: Maximum adaptation rate

        # Hybrid SMC
        k1_init, k2_init: Initial adaptive gains
        gamma1, gamma2: Adaptation rates
    """
    gains: List[float]
    max_force: float = 100.0
    dt: float = 0.01
    boundary_layer: float = 0.01

    # Adaptive SMC parameters
    leak_rate: float = 0.1
    adapt_rate_limit: float = 100.0

    # Hybrid SMC parameters
    k1_init: float = 5.0
    k2_init: float = 3.0
    gamma1: float = 0.5
    gamma2: float = 0.3