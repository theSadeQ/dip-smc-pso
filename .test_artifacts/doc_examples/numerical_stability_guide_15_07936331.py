# Example from: docs\numerical_stability_guide.md
# Index: 15
# Runnable: True
# Hash: 07936331

# High condition matrix
M = diag([1.0, 1e-6, 1e-13])  # cond ~ 1e13
# Automatic regularization triggered -> No LinAlgError