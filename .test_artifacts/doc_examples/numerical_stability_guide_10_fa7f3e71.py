# Example from: docs\numerical_stability_guide.md
# Index: 10
# Runnable: True
# Hash: fa7f3e71

# For well-conditioned systems or debugging
regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-6,           # Single parameter
    use_fixed_regularization=True        # Disable adaptive scaling
)