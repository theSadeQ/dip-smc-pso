# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 18
# Runnable: True
# Hash: b5b8fd17

from src.utils.validation.parameter_validators import require_positive

class SimulationConfig:
    def __init__(self, duration: float, dt: float,
                 atol: float = 1e-8, rtol: float = 1e-6):
        """Initialize simulation configuration with validation."""
        # Time parameters must be positive
        self.duration = require_positive(duration, "simulation_duration")
        self.dt = require_positive(dt, "time_step")

        # Tolerances must be positive and small
        self.atol = require_positive(atol, "absolute_tolerance")
        self.rtol = require_positive(rtol, "relative_tolerance")

        # Sanity check: dt should be much smaller than duration
        if self.dt >= self.duration:
            raise ValueError(
                f"time_step ({self.dt}) must be smaller than "
                f"simulation_duration ({self.duration})"
            )