# Example from: docs\api\factory_system_api_reference.md
# Index: 46
# Runnable: True
# Hash: 36b7cb76

from src.controllers.factory import create_controller

# Valid: 6 positive finite gains
gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
controller = create_controller('classical_smc', gains=gains)  # ✓ Success