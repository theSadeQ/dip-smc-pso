# Example from: docs\numerical_stability_guide.md
# Index: 23
# Runnable: False
# Hash: 0b52b293

# example-metadata:
# runnable: false

# Track where ill-conditioned matrices originate
def compute_inertia_matrix(state):
    """
    Compute inertia matrix M(q).

    Known conditioning issues:
    - Singular when theta1 = theta2 = 0 (upright equilibrium)
    - Condition number ~ 1e8 for typical trajectories
    - Requires adaptive regularization for robustness
    """
    # ... implementation ...