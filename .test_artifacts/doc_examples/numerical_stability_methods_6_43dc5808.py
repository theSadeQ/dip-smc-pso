# Example from: docs\theory\numerical_stability_methods.md
# Index: 6
# Runnable: True
# Hash: 43dc5808

if cond_num > 1e10:
    warnings.warn("Matrix approaching ill-conditioning")
    apply_regularization()

if cond_num > 1e14:
    raise NumericalInstabilityError("Matrix too ill-conditioned")