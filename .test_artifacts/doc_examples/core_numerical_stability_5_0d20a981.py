# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 5
# Runnable: True
# Hash: 0d20a981

import numpy as np

# Ill-conditioned matrix (κ ≈ 1e13)
M = np.array([
    [1.0, 0.99999999, 0.5],
    [0.99999999, 1.0, 0.5],
    [0.5, 0.5, 0.3]
])

print(f"Original condition number: {np.linalg.cond(M):.2e}")

# Apply adaptive regularization
regularizer = AdaptiveRegularizer()
M_reg = regularizer.regularize_matrix(M)

print(f"Regularized condition number: {np.linalg.cond(M_reg):.2e}")