# Example from: docs\numerical_stability_guide.md
# Index: 3
# Runnable: True
# Hash: 5737f27b

# Matrix with singular value ratio 2e-9
M = U @ diag([1.0, 2e-8, 2e-9]) @ V.T
# Regularization: λ = 1e-4 * 1.0 * 100000 = 10.0