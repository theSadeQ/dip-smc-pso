# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 17
# Runnable: True
# Hash: 51316325

from src.utils.validation.parameter_validators import require_positive
from src.utils.validation.range_validators import require_probability

class PSOConfig:
    def __init__(self, n_particles: int, iters: int,
                 c1: float, c2: float, w: float):
        """Initialize PSO configuration with validation."""
        # Population and iterations must be positive integers
        self.n_particles = int(require_positive(n_particles, "population_size"))
        self.iters = int(require_positive(iters, "max_iterations"))

        # Acceleration coefficients (typically ~2.0, but allow flexibility)
        self.c1 = require_in_range(c1, "cognitive_coefficient",
                                   minimum=0.1, maximum=5.0)
        self.c2 = require_in_range(c2, "social_coefficient",
                                   minimum=0.1, maximum=5.0)

        # Inertia weight (typically 0.4-0.9)
        self.w = require_in_range(w, "inertia_weight",
                                  minimum=0.1, maximum=1.5)