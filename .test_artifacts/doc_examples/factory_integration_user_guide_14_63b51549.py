# Example from: docs\factory\factory_integration_user_guide.md
# Index: 14
# Runnable: False
# Hash: 63b51549

# example-metadata:
# runnable: false

# Good: Complete parameter specification
controller_config = {
    'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    'max_force': 150.0,
    'boundary_layer': 0.02,
    'dt': 0.001
}

# Avoid: Relying on implicit defaults
controller_config = {
    'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
    # Missing required parameters
}