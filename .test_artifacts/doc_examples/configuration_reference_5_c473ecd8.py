# Example from: docs\factory\configuration_reference.md
# Index: 5
# Runnable: True
# Hash: c473ecd8

# Classical SMC parameters with boundary layer chattering reduction
config_params = {
    'gains': controller_gains,           # [k1, k2, λ1, λ2, K, kd]
    'max_force': 150.0,                 # Control saturation limit
    'dt': 0.001,                        # Sampling time
    'boundary_layer': 0.02,             # Required for chattering reduction
    'dynamics_model': dynamics_model     # Optional plant model
}