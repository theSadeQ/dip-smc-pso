# Example from: docs\controllers\control_primitives_reference.md
# Index: 16
# Runnable: True
# Hash: 1378ee2d

from src.utils.validation import require_positive

class ClassicalSMC:
    def __init__(self, gains, max_force, boundary_layer):
        # Validate stability-critical parameters
        self.max_force = require_positive(max_force, "max_force")
        self.boundary_layer = require_positive(boundary_layer, "boundary_layer")

        # Validate gains
        for i, gain in enumerate(gains):
            gains[i] = require_positive(gain, f"gains[{i}]", allow_zero=False)