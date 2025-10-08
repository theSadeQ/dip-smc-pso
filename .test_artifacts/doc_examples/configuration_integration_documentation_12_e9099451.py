# Example from: docs\configuration_integration_documentation.md
# Index: 12
# Runnable: False
# Hash: e9099451

class AttributeConfig:
    """Configuration using attributes."""

    def __init__(self):
        # Create controller configurations as attributes
        self.classical_smc = type('Config', (), {
            'gains': [25, 20, 15, 10, 40, 6],
            'max_force': 160.0,
            'boundary_layer': 0.025,
            'dt': 0.001
        })()

        self.adaptive_smc = type('Config', (), {
            'gains': [30, 22, 18, 12, 5.0],
            'max_force': 160.0,
            'dt': 0.001,
            'leak_rate': 0.02
        })()

# Initialize controllers namespace
config = type('Config', (), {})()
config.controllers = AttributeConfig()

controller = create_controller('classical_smc', config=config)