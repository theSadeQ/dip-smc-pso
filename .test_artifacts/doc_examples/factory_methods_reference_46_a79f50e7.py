# Example from: docs\api\factory_methods_reference.md
# Index: 46
# Runnable: True
# Hash: a79f50e7

#!/usr/bin/env python3
"""Basic factory usage examples."""

from src.controllers.factory import create_controller, list_available_controllers

def basic_factory_examples():
    """Demonstrate basic factory usage patterns."""

    # Check available controllers
    available = list_available_controllers()
    print(f"Available controllers: {available}")

    # Create controller with defaults
    controller = create_controller('classical_smc')
    print(f"Default gains: {controller.gains}")

    # Create with explicit gains
    custom_gains = [25.0, 20.0, 15.0, 10.0, 40.0, 6.0]
    controller = create_controller('classical_smc', gains=custom_gains)
    print(f"Custom gains: {controller.gains}")

    # Test controller functionality
    import numpy as np
    state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    control_output = controller.compute_control(state, 0.0, {})
    print(f"Control output: {control_output}")

if __name__ == "__main__":
    basic_factory_examples()