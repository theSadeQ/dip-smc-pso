# Example from: docs\numerical_stability_guide.md
# Index: 16
# Runnable: True
# Hash: 3d79c836

# Well-conditioned matrix (cond ~ 1.25)
M = diag([1.0, 0.9, 0.8])
M_inv = matrix_inverter.invert_matrix(M)
error = max(abs((M @ M_inv) - I))
assert error < 1e-10  # High precision maintained