# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 4
# Runnable: False
# Hash: aa936ffc

# example-metadata:
# runnable: false

# Classical SMC bounds
CLASSICAL_BOUNDS = {
    'k1': (0.1, 50.0),      # Surface gain 1
    'k2': (0.1, 50.0),      # Surface gain 2
    'lam1': (0.1, 50.0),    # Sliding surface parameter 1
    'lam2': (0.1, 50.0),    # Sliding surface parameter 2
    'K': (1.0, 200.0),      # Switching gain
    'kd': (0.0, 50.0)       # Damping gain (can be zero)
}

# Adaptive SMC bounds
ADAPTIVE_BOUNDS = {
    'k1': (0.1, 50.0),      # Surface gain 1
    'k2': (0.1, 50.0),      # Surface gain 2
    'lam1': (0.1, 50.0),    # Sliding surface parameter 1
    'lam2': (0.1, 50.0),    # Sliding surface parameter 2
    'gamma': (0.01, 10.0)   # Adaptation rate
}