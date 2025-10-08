# Example from: docs\mathematical_foundations\boundary_layer_derivations.md
# Index: 4
# Runnable: True
# Hash: 66ad1f2f

def compute_boundary_layer(sigma, epsilon0, epsilon1):
    """Compute adaptive boundary layer thickness."""
    return epsilon0 + epsilon1 * abs(sigma)

def saturate_adaptive(sigma, epsilon0, epsilon1, method="tanh"):
    """Saturation with adaptive boundary layer."""
    eps_adaptive = compute_boundary_layer(sigma, epsilon0, epsilon1)
    return saturate(sigma, eps_adaptive, method)