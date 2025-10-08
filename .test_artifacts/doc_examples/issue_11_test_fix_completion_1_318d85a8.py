# Example from: docs\issue_11_test_fix_completion.md
# Index: 1
# Runnable: False
# Hash: 318d85a8

# System from test (lines 313-321)
A = [[0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 1],
     [-2, -1, 0, -1, 0, 0],
     [0, -3, -1, 0, -1, 0],
     [0, 0, -2, 0, 0, -1]]

B = [0, 0, 0, 1, 0, 0]

# LQR design parameters
Q = 100 * I₆  # Strong state penalty for fast convergence
R = 1         # Control effort weight

# Optimal gains via CARE
K_optimal = [8.20, -0.91, -0.01, 9.83, -0.05, -0.01]