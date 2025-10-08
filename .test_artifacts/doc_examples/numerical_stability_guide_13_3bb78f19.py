# Example from: docs\numerical_stability_guide.md
# Index: 13
# Runnable: True
# Hash: 3bb78f19

# Automatic conversion
if hasattr(config, 'regularization'):
    # Convert to fixed regularization mode
    regularizer = AdaptiveRegularizer(
        regularization_alpha=config.regularization,
        use_fixed_regularization=True
    )