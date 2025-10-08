# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 4
# Runnable: True
# Hash: 2e510a4d

try:
    P = linalg.solve_lyapunov(A_to_solve.T, -Q)  # Fast direct method
except (np.linalg.LinAlgError, ValueError):
    P = self._solve_lyapunov_svd(A_to_solve, Q, regularizer)  # Robust fallback