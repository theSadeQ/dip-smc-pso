# Example from: docs\configuration_integration_documentation.md
# Index: 11
# Runnable: False
# Hash: ef157b8c

# example-metadata:
# runnable: false

# Nested dictionary configuration
config = {
    'controllers': {
        'classical_smc': {
            'gains': [18, 12, 10, 6, 30, 4],
            'max_force': 120.0,
            'boundary_layer': 0.015,
            'dt': 0.001
        },
        'adaptive_smc': {
            'gains': [22, 16, 12, 8, 3.5],
            'max_force': 140.0,
            'dt': 0.001,
            'leak_rate': 0.015
        }
    }
}

# Use with factory
controller = create_controller('classical_smc', config=config)