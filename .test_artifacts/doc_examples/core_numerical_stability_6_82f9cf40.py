# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 6
# Runnable: True
# Hash: 82f9cf40

if regularizer.check_conditioning(M):
    # Direct inversion safe
    M_inv = np.linalg.inv(M)
else:
    # Regularization needed
    M_reg = regularizer.regularize_matrix(M)
    M_inv = np.linalg.inv(M_reg)