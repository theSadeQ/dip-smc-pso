# Example from: docs\factory_integration_documentation.md
# Index: 9
# Runnable: False
# Hash: 1876a3da

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class ClassicalSMCConfig:
    """Type-safe configuration for Classical SMC controller."""

    gains: List[float] = field()                           # [k1, k2, lam1, lam2, K, kd]
    max_force: float = field()                             # Control saturation limit
    boundary_layer: float = field()                        # Chattering reduction thickness
    dt: float = field(default=0.01)                       # Control timestep
    switch_method: Literal["tanh", "linear", "sign"] = field(default="tanh")

    def __post_init__(self):
        """Validate configuration after creation."""
        self._validate_gains()
        self._validate_control_parameters()
        self._validate_stability_requirements()