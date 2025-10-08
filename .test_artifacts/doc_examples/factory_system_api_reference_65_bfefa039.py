# Example from: docs\api\factory_system_api_reference.md
# Index: 65
# Runnable: True
# Hash: bfefa039

"""
Example 1: Basic Factory Usage
Demonstrates the simplest controller creation patterns.
"""

from src.controllers.factory import create_controller, list_available_controllers, get_default_gains
from src.config import load_config
import numpy as np

def main():
    # Query available controllers
    print("Available controllers:")
    for controller_type in list_available_controllers():
        defaults = get_default_gains(controller_type)
        print(f"  - {controller_type}: {len(defaults)} gains")

    # Load configuration
    config = load_config("config.yaml")

    # Create controller with config defaults
    controller = create_controller('classical_smc', config)
    print(f"\nCreated classical_smc with gains: {controller.gains}")

    # Use controller in simulation
    state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
    result = controller.compute_control(state, 0.0, {})

    if hasattr(result, 'u'):
        control = result.u
    elif isinstance(result, dict):
        control = result['u']
    else:
        control = result

    print(f"Control output: {control:.3f} N")

if __name__ == '__main__':
    main()