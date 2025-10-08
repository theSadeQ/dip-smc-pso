# Example from: docs\factory\configuration_reference.md
# Index: 7
# Runnable: False
# Hash: b23b3fc2

# Super-Twisting Algorithm (STA) SMC
config_params = {
    'gains': controller_gains,           # [K1, K2, k1, k2, λ1, λ2]
    'max_force': 150.0,
    'dt': 0.001,
    'power_exponent': 0.5,              # STA convergence exponent
    'regularization': 1e-6,             # Numerical regularization
    'boundary_layer': 0.01,             # Chattering reduction
    'switch_method': 'tanh',            # Switching function type
    'damping_gain': 0.0                 # Additional damping
}