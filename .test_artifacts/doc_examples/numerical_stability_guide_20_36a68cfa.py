# Example from: docs\numerical_stability_guide.md
# Index: 20
# Runnable: True
# Hash: 36a68cfa

# Recommended defaults for production
regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-4,
    max_condition_number=1e14,
    min_regularization=1e-10,
    use_fixed_regularization=False
)