# Example from: docs\configuration_integration_documentation.md
# Index: 6
# Runnable: True
# Hash: 1a9b5cb3

from dataclasses import dataclass, field
from typing import List, Optional, Literal
import numpy as np

@dataclass(frozen=True)
class ClassicalSMCConfig:
    """Type-safe configuration for Classical SMC controller."""

    # Required parameters
    gains: List[float] = field()                           # [k1, k2, λ1, λ2, K, kd]
    max_force: float = field()                             # Control saturation limit [N]
    boundary_layer: float = field()                        # Chattering reduction thickness

    # Optional parameters with defaults
    dt: float = field(default=0.01)                       # Control timestep [s]
    switch_method: Literal["tanh", "linear", "sign"] = field(default="tanh")
    regularization: float = field(default=1e-10)          # Matrix regularization
    boundary_layer_slope: float = field(default=0.0)      # Adaptive boundary layer
    controllability_threshold: Optional[float] = field(default=None)

    # Optional dynamics model
    dynamics_model: Optional[object] = field(default=None, compare=False)

    def __post_init__(self):
        """Validate configuration after creation."""
        self._validate_gains()
        self._validate_control_parameters()
        self._validate_stability_requirements()

    def _validate_gains(self):
        """Validate gain array for classical SMC."""
        if len(self.gains) != 6:
            raise ValueError("Classical SMC requires exactly 6 gains: [k1, k2, λ1, λ2, K, kd]")

        if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in self.gains):
            raise ValueError("All gains must be finite numbers")

        if not all(g > 0 for g in self.gains):
            raise ValueError("All gains must be positive for stability")

        k1, k2, lam1, lam2, K, kd = self.gains

        # Control theory constraints
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Surface coefficients λ1, λ2 must be positive (Hurwitz stability)")

        if K <= 0:
            raise ValueError("Switching gain K must be positive (reaching condition)")

        # Practical constraints
        if K > 200:
            raise ValueError("Switching gain K > 200 may cause excessive chattering")

        if lam1/k1 > 50 or lam2/k2 > 50:
            raise ValueError("Surface coefficient ratios too large (λ/k > 50)")

    def _validate_control_parameters(self):
        """Validate control-specific parameters."""
        if self.max_force <= 0:
            raise ValueError("max_force must be positive")

        if self.boundary_layer <= 0:
            raise ValueError("boundary_layer must be positive")

        if self.dt <= 0:
            raise ValueError("dt must be positive")

        if self.regularization <= 0:
            raise ValueError("regularization must be positive")

    def _validate_stability_requirements(self):
        """Validate control theory stability requirements."""
        k1, k2, lam1, lam2, K, kd = self.gains

        # Lyapunov stability condition: surface must be stable
        # For s = λ1*e1 + λ2*e2 + ė1 + ė2, we need λ1, λ2 > 0

        # Reaching condition: K must overcome uncertainties
        # Conservative estimate: K > max(k1, k2) for robustness
        min_K = max(k1, k2)
        if K < min_K:
            print(f"Warning: K={K} < max(k1,k2)={min_K}, may not satisfy reaching condition")

        # Chattering bound: K should not be excessively large
        if K > 10 * min_K:
            print(f"Warning: K={K} >> max(k1,k2)={min_K}, expect significant chattering")