# Example from: docs\theory\numerical_stability_methods.md
# Index: 10
# Runnable: True
# Hash: 43746865

U, s, Vt = np.linalg.svd(M_reg)
s_inv = np.where(s > 1e-10 * s[0], 1/s, 0)  # Threshold small singular values
M_pinv = (Vt.T * s_inv) @ U.T
accelerations = M_pinv @ forcing