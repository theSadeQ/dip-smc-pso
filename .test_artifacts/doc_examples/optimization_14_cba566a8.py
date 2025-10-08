# Example from: docs\guides\api\optimization.md
# Index: 14
# Runnable: True
# Hash: cba566a8

# Ensure stability margins
physics_constrained_bounds = [
    (0.1, 50),     # k1 > 0 (positive definite)
    (0.1, 50),     # k2 > 0
    (0.1, 50),     # λ1 > 0
    (0.1, 50),     # λ2 > 0
    (10.0, 200),   # K: minimum switching gain for robustness
    (0.1, 50),     # ε: minimum boundary layer to prevent chattering
]