# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 15
# Runnable: True
# Hash: 1c2555bd

from src.utils.validation.parameter_validators import require_positive
from src.utils.validation.range_validators import require_in_range

class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, u_max: float):
        """Initialize PID controller with validated parameters."""
        # Gains must be positive
        self.kp = require_positive(kp, "proportional_gain")
        self.ki = require_positive(ki, "integral_gain")
        self.kd = require_positive(kd, "derivative_gain")

        # Saturation limit must be positive and reasonable
        self.u_max = require_in_range(
            u_max, "control_saturation",
            minimum=1.0, maximum=500.0
        )