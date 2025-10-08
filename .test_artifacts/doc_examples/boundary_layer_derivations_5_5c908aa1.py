# Example from: docs\mathematical_foundations\boundary_layer_derivations.md
# Index: 5
# Runnable: True
# Hash: 5c908aa1

def saturate_with_hysteresis(sigma, epsilon0, hysteresis_ratio, method="tanh"):
    """Saturation function with hysteresis dead-band."""
    dead_band = hysteresis_ratio * epsilon0

    if abs(sigma) < dead_band:
        return 0.0
    else:
        return saturate(sigma, epsilon0, method)