# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 11
# Runnable: True
# Hash: ca3ce9ee

ADAPTIVE_SMC_BOUNDS = {
    'c1': (1.0, 100.0),      # Position error weighting
    'lambda1': (1.0, 20.0),  # Damping coefficient
    'c2': (1.0, 100.0),      # Position error weighting
    'lambda2': (1.0, 20.0),  # Damping coefficient
    'gamma': (0.1, 10.0)     # Adaptation rate
}