# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 16
# Runnable: True
# Hash: 3315225d

from src.utils.validation.parameter_validators import require_positive, require_finite

class DoublePendulumParams:
    def __init__(self, m1: float, m2: float, l1: float, l2: float,
                 b1: float, b2: float, g: float = 9.81):
        """Initialize physics parameters with validation."""
        # Masses must be positive
        self.m1 = require_positive(m1, "cart_mass")
        self.m2 = require_positive(m2, "pendulum1_mass")

        # Lengths must be positive
        self.l1 = require_positive(l1, "pendulum1_length")
        self.l2 = require_positive(l2, "pendulum2_length")

        # Friction can be zero
        self.b1 = require_positive(b1, "joint1_friction", allow_zero=True)
        self.b2 = require_positive(b2, "joint2_friction", allow_zero=True)

        # Gravity is finite (can be negative for upside-down tests)
        self.g = require_finite(g, "gravity")