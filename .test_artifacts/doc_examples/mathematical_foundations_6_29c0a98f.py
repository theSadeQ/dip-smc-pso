# Example from: docs\technical\mathematical_foundations.md
# Index: 6
# Runnable: False
# Hash: 29c0a98f

# example-metadata:
# runnable: false

def compute_robustness_margin(controller, uncertainty_model):
    """Compute robustness margin for controller."""

    # Sample operating points
    test_points = generate_test_points()
    min_margin = float('inf')

    for x in test_points:
        # Compute local linearization
        A, B = linearize_dynamics(x)

        # Compute controller gain matrix
        K = compute_controller_gain_matrix(controller, x)

        # Closed-loop system
        A_cl = A + B @ K

        # Compute structured singular value
        mu = compute_structured_singular_value(A_cl, uncertainty_model)
        margin = 1.0 / mu if mu > 0 else float('inf')

        min_margin = min(min_margin, margin)

    return min_margin