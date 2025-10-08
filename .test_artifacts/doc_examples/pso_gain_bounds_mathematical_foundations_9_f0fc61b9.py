# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 9
# Runnable: True
# Hash: f0fc61b9

CLASSICAL_SMC_BOUNDS = {
    'c1': (1.0, 100.0),      # Position error weighting
    'lambda1': (1.0, 20.0),  # Damping coefficient
    'c2': (1.0, 100.0),      # Position error weighting
    'lambda2': (1.0, 20.0),  # Damping coefficient
    'K': (5.0, 150.0),       # Switching gain
    'kd': (0.1, 10.0)        # Derivative gain
}