# Example from: docs\factory\configuration_reference.md
# Index: 6
# Runnable: False
# Hash: 36de03ac

# Adaptive SMC with parameter estimation
config_params = {
    'gains': controller_gains,           # [k1, k2, λ1, λ2, γ]
    'max_force': 150.0,
    'dt': 0.001,
    'leak_rate': 0.01,                  # Parameter estimation leak
    'adapt_rate_limit': 10.0,           # Adaptation rate bounds
    'K_min': 0.1, 'K_max': 100.0,      # Adaptive gain bounds
    'K_init': 10.0,                     # Initial adaptive gain
    'alpha': 0.5,                       # Adaptation law exponent
    'boundary_layer': 0.01,             # Smooth switching
    'smooth_switch': True               # Enable smooth switching
}