# Example from: docs\controllers\control_primitives_reference.md
# Index: 18
# Runnable: True
# Hash: 9a2f314b

from src.utils.validation import require_finite

def compute_control_law(state, gains):
    # Validate intermediate computations
    sigma = compute_sliding_surface(state)
    sigma = require_finite(sigma, "sliding_surface")

    u = -gains[4] * saturate(sigma, epsilon=0.01)
    u = require_finite(u, "control_input")

    return u