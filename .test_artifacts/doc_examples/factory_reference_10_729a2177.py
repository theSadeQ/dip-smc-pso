# Example from: docs\api\factory_reference.md
# Index: 10
# Runnable: True
# Hash: 729a2177

from src.controllers.factory import create_controller, ConfigValueError

try:
    controller = create_controller('invalid_type')
except ValueError as e:
    print(f"Invalid controller: {e}")

try:
    controller = create_controller('sta_smc', gains=[15.0, 25.0, 20.0, 12.0, 8.0, 6.0])  # K1 < K2
except ValueError as e:
    print(f"Constraint violation: {e}")