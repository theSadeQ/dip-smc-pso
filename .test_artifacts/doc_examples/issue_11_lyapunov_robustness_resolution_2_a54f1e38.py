# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 2
# Runnable: True
# Hash: a54f1e38

regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-6,   # Minimal for accuracy
    max_condition_number=1e12,   # Accept modest ill-conditioning
    min_regularization=1e-12,    # Very small minimum
    use_fixed_regularization=False
)