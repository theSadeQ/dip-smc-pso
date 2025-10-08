# Example from: docs\api\factory_system_api_reference.md
# Index: 27
# Runnable: True
# Hash: 9f8ff4ae

from src.controllers.factory import CONTROLLER_REGISTRY

# Get metadata for a controller type
classical_info = CONTROLLER_REGISTRY['classical_smc']
print(f"Description: {classical_info['description']}")
print(f"Gain count: {classical_info['gain_count']}")
print(f"Default gains: {classical_info['default_gains']}")
print(f"Required params: {classical_info['required_params']}")

# Check if controller supports dynamics model
if classical_info['supports_dynamics']:
    print("Controller can use dynamics model for feedforward control")

# Iterate over all registered controllers
for controller_type, info in CONTROLLER_REGISTRY.items():
    if info['class'] is not None:
        print(f"{controller_type}: {info['gain_count']} gains")