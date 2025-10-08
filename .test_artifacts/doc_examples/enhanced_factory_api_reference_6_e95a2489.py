# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 6
# Runnable: True
# Hash: e95a2489

classical_params = {
    'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],  # [k1, k2, λ1, λ2, K, kd]
    'max_force': 150.0,             # Maximum control force [N]
    'boundary_layer': 0.02,         # Boundary layer thickness
    'dt': 0.001,                    # Time step [s]
    'switch_method': 'tanh'         # Switching function type
}