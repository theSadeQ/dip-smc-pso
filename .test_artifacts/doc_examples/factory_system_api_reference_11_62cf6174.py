# Example from: docs\api\factory_system_api_reference.md
# Index: 11
# Runnable: True
# Hash: 62cf6174

from src.controllers.factory import create_controller

# All these create the same controller type ('sta_smc')
controller1 = create_controller('sta_smc')           # Canonical name
controller2 = create_controller('super_twisting')    # Alias
controller3 = create_controller('sta')               # Short alias

# Verify all are the same type
assert type(controller1) == type(controller2) == type(controller3)