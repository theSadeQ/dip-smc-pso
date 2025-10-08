# Example from: docs\api\factory_methods_reference.md
# Index: 49
# Runnable: True
# Hash: 7a12f551

#!/usr/bin/env python3
"""Error handling examples."""

from src.controllers.factory import create_controller, list_available_controllers
import logging

logging.basicConfig(level=logging.INFO)

def error_handling_example():
    """Demonstrate robust error handling patterns."""

    test_cases = [
        # Valid cases
        ('classical_smc', [20, 15, 12, 8, 35, 5], "Valid classical SMC"),
        ('adaptive_smc', [25, 18, 15, 10, 4], "Valid adaptive SMC"),

        # Error cases
        ('invalid_controller', None, "Unknown controller type"),
        ('classical_smc', [1, 2, 3], "Invalid gain count"),
        ('classical_smc', [-20, 15, 12, 8, 35, 5], "Negative gains"),
        ('mpc_controller', None, "Potentially missing dependencies"),
    ]

    for controller_type, gains, description in test_cases:
        print(f"Testing: {description}")

        try:
            if gains is not None:
                controller = create_controller(controller_type, gains=gains)
            else:
                controller = create_controller(controller_type)

            print(f"  ✅ Success: {controller_type} created")
            print(f"     Gains: {controller.gains}")

        except ValueError as e:
            print(f"  ❌ Configuration Error: {e}")

        except ImportError as e:
            print(f"  ⚠️  Import Error: {e}")
            available = list_available_controllers()
            print(f"     Available: {available}")

        except Exception as e:
            print(f"  💥 Unexpected Error: {e}")

        print()

if __name__ == "__main__":
    error_handling_example()