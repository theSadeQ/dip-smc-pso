# Example from: docs\technical\configuration_schema_reference.md
# Index: 6
# Runnable: False
# Hash: c0f0e974

@dataclass(frozen=True)
class SuperTwistingSMCConfig:
    """Configuration for Super-Twisting (STA) SMC controller."""

    # Required Parameters
    gains: List[float]                           # [K1, K2, k1, k2, λ1, λ2]
    max_force: float                            # Control saturation limit [N]
    dt: float                                   # Integration timestep [s]

    # Optional STA Algorithm Parameters
    power_exponent: float = 0.5                 # STA convergence exponent α ∈ (0,1)
    regularization: float = 1e-6                # Numerical stability
    boundary_layer: float = 0.01                # Chattering reduction
    switch_method: str = "tanh"                 # Switching function type
    damping_gain: float = 0.0                   # Additional damping

    # Optional dynamics model
    dynamics_model: Optional[object] = None