# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 7
# Runnable: True
# Hash: ae8d31e1

sta_params = {
    'gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],  # [K1, K2, k1, k2, λ1, λ2]
    'max_force': 150.0,             # Maximum control force [N]
    'dt': 0.001,                    # Time step [s]
    'power_exponent': 0.5,          # Super-twisting power
    'regularization': 1e-6,         # Numerical regularization
    'boundary_layer': 0.01,         # Small boundary layer for implementation
    'switch_method': 'tanh'         # Continuous switching function
}