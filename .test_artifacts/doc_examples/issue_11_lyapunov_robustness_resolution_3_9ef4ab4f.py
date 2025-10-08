# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 3
# Runnable: True
# Hash: 9ef4ab4f

cond_A = np.linalg.cond(A)
if not np.isfinite(cond_A) or cond_A > 1e14:
    A_reg = regularizer.regularize_matrix(A)  # Apply regularization
    A_to_solve = A_reg
else:
    A_to_solve = A  # Use original (fast path)