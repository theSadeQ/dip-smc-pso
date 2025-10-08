# Example from: docs\controllers\control_primitives_reference.md
# Index: 34
# Runnable: True
# Hash: 862da74d

def compute_control(self, state):
    sigma = compute_sliding_surface(state)

    # Validate critical quantities in debug builds
    if __debug__:
        sigma = require_finite(sigma, "sliding_surface")