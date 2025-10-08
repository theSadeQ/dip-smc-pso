# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 9
# Runnable: False
# Hash: f58ea931

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class ClassicalSMCConfig:
    """Type-safe configuration for Classical SMC controller."""

    # Required Parameters
    gains: List[float]              # [k1, k2, λ1, λ2, K, kd] - Must be 6 elements
    max_force: float               # Control saturation limit (Newtons)
    boundary_layer: float          # Chattering reduction thickness

    # Optional Parameters with Defaults
    dt: float = 0.01              # Control timestep (seconds)
    boundary_layer_slope: float = 0.0    # Adaptive boundary layer slope
    switch_method: Literal["tanh", "linear", "sign"] = "tanh"
    regularization: float = 1e-10          # Matrix regularization
    controllability_threshold: Optional[float] = None
    dynamics_model: Optional[object] = None