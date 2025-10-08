# Example from: docs\theory\numerical_stability_methods.md
# Index: 11
# Runnable: False
# Hash: b2010734

# Simulation parameters
DT_VALUES = [0.001, 0.005, 0.01, 0.02]  # Time steps to test
SIM_TIME = 10.0  # Simulation duration (seconds)
N_MONTE_CARLO = 5000  # Monte Carlo samples

# Conditioning thresholds
COND_THRESHOLD = 1e12  # Ill-conditioning threshold
REG_ALPHA = 1e-4  # Regularization parameter

# PSO configuration
N_PARTICLES = 30
N_ITERATIONS = 50