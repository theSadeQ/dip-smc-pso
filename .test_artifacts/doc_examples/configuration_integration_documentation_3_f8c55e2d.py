# Example from: docs\configuration_integration_documentation.md
# Index: 3
# Runnable: False
# Hash: f8c55e2d

# example-metadata:
# runnable: false

# Second priority - extracted from configuration objects
class CustomConfig:
    def __init__(self):
        self.controllers = {
            'classical_smc': {
                'gains': [18, 12, 10, 6, 30, 4],
                'max_force': 120.0,
                'boundary_layer': 0.015
            }
        }

config = CustomConfig()
controller = create_controller('classical_smc', config=config)