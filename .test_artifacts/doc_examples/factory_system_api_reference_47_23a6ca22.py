# Example from: docs\api\factory_system_api_reference.md
# Index: 47
# Runnable: True
# Hash: 23a6ca22

from src.controllers.factory import create_controller

# Invalid: Wrong number of gains
gains = [20.0, 15.0, 12.0]  # Only 3 gains, need 6
try:
    controller = create_controller('classical_smc', gains=gains)
except ValueError as e:
    print(e)
    # Output: "Controller 'Classical sliding mode controller with boundary layer'
    #          requires 6 gains, got 3"