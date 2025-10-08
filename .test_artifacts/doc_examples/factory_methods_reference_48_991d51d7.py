# Example from: docs\api\factory_methods_reference.md
# Index: 48
# Runnable: True
# Hash: 991d51d7

#!/usr/bin/env python3
"""Advanced configuration examples."""

from src.controllers.factory import create_controller
from src.config import load_config
import numpy as np

def advanced_configuration_example():
    """Demonstrate advanced configuration patterns."""

    # Load configuration from file
    config = load_config("config.yaml")

    # Create controllers with various configuration methods
    controllers = {}

    # Method 1: Configuration file only
    controllers['config_only'] = create_controller('classical_smc', config=config)

    # Method 2: Override gains from config
    custom_gains = [30.0, 25.0, 18.0, 12.0, 45.0, 8.0]
    controllers['override_gains'] = create_controller(
        'classical_smc',
        config=config,
        gains=custom_gains  # Overrides config gains
    )

    # Method 3: Different controller types
    for controller_type in ['classical_smc', 'adaptive_smc', 'sta_smc']:
        try:
            controllers[controller_type] = create_controller(controller_type, config=config)
        except ImportError as e:
            print(f"Skipping {controller_type}: {e}")

    # Compare controller properties
    for name, controller in controllers.items():
        print(f"{name}:")
        print(f"  Gains: {controller.gains}")
        print(f"  Max force: {getattr(controller, 'max_force', 'N/A')}")

        # Test control computation
        test_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
        try:
            control_output = controller.compute_control(test_state, 0.0, {})
            control_value = control_output.u if hasattr(control_output, 'u') else control_output
            print(f"  Control output: {control_value:.3f}")
        except Exception as e:
            print(f"  Control computation failed: {e}")

        print()

if __name__ == "__main__":
    advanced_configuration_example()