# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 11
# Runnable: False
# Hash: 2306d233

@dataclass(frozen=True)
class SuperTwistingSMCConfig:
    """Configuration for Super-Twisting (STA) SMC controller."""

    # Required Parameters
    gains: List[float]              # [K1, K2, k1, k2, λ1, λ2] - 6 elements
    max_force: float               # Control saturation limit

    # STA Algorithm Parameters
    K1: float = 4.0               # Proportional-like STA gain
    K2: float = 0.4               # Integral-like STA gain
    power_exponent: float = 0.5    # STA convergence exponent (0 < α < 1)

    # Optional Parameters
    dt: float = 0.001             # Integration timestep
    damping_gain: float = 0.0     # Additional damping
    regularization: float = 1e-6   # Numerical stability
    dynamics_model: Optional[object] = None