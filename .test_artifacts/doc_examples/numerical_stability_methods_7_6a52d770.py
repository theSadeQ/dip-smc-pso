# Example from: docs\theory\numerical_stability_methods.md
# Index: 7
# Runnable: True
# Hash: 6a52d770

# Verify improved conditioning after regularization
kappa_reg = np.linalg.cond(M_reg)
if kappa_reg > 0.1 * kappa_original:
    # Less than 10× improvement - increase alpha
    alpha *= 10