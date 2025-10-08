# Example from: docs\factory\factory_integration_user_guide.md
# Index: 10
# Runnable: True
# Hash: 0091e55d

from src.controllers.factory import create_controller

try:
    # Invalid gains array (wrong length)
    controller = create_controller(
        'classical_smc',
        gains=[10.0, 5.0, 8.0]  # Only 3 gains instead of 6
    )
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: Controller 'Classical sliding mode controller' requires 6 gains, got 3

try:
    # Invalid parameter values
    controller = create_controller(
        'adaptive_smc',
        gains=[25.0, 18.0, 15.0, 10.0, -2.0]  # Negative gamma
    )
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: All gains must be positive