# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 13
# Runnable: True
# Hash: c6324b5d

import numpy as np
from src.plant.core import AdaptiveRegularizer

# Create ill-conditioned matrix
M = np.array([
    [1.0, 0.999999999, 0.5],
    [0.999999999, 1.0, 0.5],
    [0.5, 0.5, 0.3]
])

print(f"Original condition number: {np.linalg.cond(M):.2e}")  # ~1e13

# Regularize
regularizer = AdaptiveRegularizer()
M_reg = regularizer.regularize_matrix(M)

print(f"Regularized condition number: {np.linalg.cond(M_reg):.2e}")  # ~1e8