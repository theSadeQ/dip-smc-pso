# Example from: docs\api\factory_system_api_reference.md
# Index: 68
# Runnable: True
# Hash: c03dd3d7

"""
Example 4: Custom Configuration Override
Demonstrates programmatic configuration overrides.
"""

from src.controllers.factory import create_controller
from src.config import load_config
import numpy as np

class CustomConfig:
    """Custom configuration object."""
    def __init__(self):
        self.controllers = {
            'classical_smc': {
                'gains': [30.0, 20.0, 15.0, 12.0, 45.0, 7.0],
                'max_force': 200.0,
                'boundary_layer': 0.5,
                'dt': 0.001
            },
            'sta_smc': {
                'gains': [35.0, 20.0, 25.0, 15.0, 10.0, 8.0],
                'max_force': 200.0,
                'dt': 0.001
            }
        }

def main():
    print("Demonstrating custom configuration overrides\n")

    # Method 1: Load base config and override gains
    print("Method 1: Override gains only")
    config = load_config("config.yaml")
    custom_gains = [35.0, 25.0, 18.0, 14.0, 50.0, 8.0]
    controller1 = create_controller('classical_smc', config, gains=custom_gains)
    print(f"  Gains: {controller1.gains}")
    print(f"  Max force: {controller1.max_force:.1f} N\n")

    # Method 2: Use custom configuration object
    print("Method 2: Custom configuration object")
    custom_config = CustomConfig()
    controller2 = create_controller('classical_smc', custom_config)
    print(f"  Gains: {controller2.gains}")
    print(f"  Max force: {controller2.max_force:.1f} N\n")

    # Method 3: Override both config and gains
    print("Method 3: Override config and gains")
    override_gains = [40.0, 28.0, 20.0, 16.0, 55.0, 9.0]
    controller3 = create_controller('classical_smc', custom_config, gains=override_gains)
    print(f"  Gains: {controller3.gains}")  # Uses override_gains
    print(f"  Max force: {controller3.max_force:.1f} N")  # From custom_config

    # Verify different configurations produce different controllers
    print("\nVerifying configuration differences:")
    state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])

    u1 = controller1.compute_control(state, 0.0, {})
    u2 = controller2.compute_control(state, 0.0, {})
    u3 = controller3.compute_control(state, 0.0, {})

    # Extract control values
    def get_control(result):
        if hasattr(result, 'u'):
            return result.u
        elif isinstance(result, dict):
            return result['u']
        else:
            return result

    print(f"  Controller 1: u = {get_control(u1):.3f} N")
    print(f"  Controller 2: u = {get_control(u2):.3f} N")
    print(f"  Controller 3: u = {get_control(u3):.3f} N")

if __name__ == '__main__':
    main()