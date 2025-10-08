# Example from: docs\factory\factory_integration_user_guide.md
# Index: 4
# Runnable: True
# Hash: 05323777

classical_config = {
    'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    'max_force': 150.0,
    'boundary_layer': 0.02,
    'dt': 0.001
}

controller = create_controller('classical_smc', **classical_config)