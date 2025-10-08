# Example from: docs\factory\factory_integration_user_guide.md
# Index: 5
# Runnable: False
# Hash: 51e4afe2

sta_config = {
    'gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
    'max_force': 150.0,
    'dt': 0.001,
    'power_exponent': 0.5,
    'regularization': 1e-6,
    'boundary_layer': 0.01,
    'switch_method': 'tanh'
}

controller = create_controller('sta_smc', **sta_config)