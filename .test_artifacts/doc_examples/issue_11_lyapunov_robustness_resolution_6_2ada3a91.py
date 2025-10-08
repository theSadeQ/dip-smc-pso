# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 6
# Runnable: True
# Hash: 2ada3a91

lyapunov_residual = A_to_solve.T @ P + P @ A_to_solve + Q
residual_norm = np.linalg.norm(lyapunov_residual, ord='fro')
residual_relative = residual_norm / (np.linalg.norm(Q, ord='fro') + 1e-15)

is_stable = is_positive_definite and residual_relative < 1e-6