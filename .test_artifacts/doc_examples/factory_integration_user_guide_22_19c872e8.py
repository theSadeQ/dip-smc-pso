# Example from: docs\factory\factory_integration_user_guide.md
# Index: 22
# Runnable: True
# Hash: 19c872e8

from src.controllers.factory import (
    CONTROLLER_REGISTRY,
    list_available_controllers,
    get_default_gains
)

# Inspect available controllers
print("Available controllers:", list_available_controllers())

# Get controller specifications
for controller_type in list_available_controllers():
    info = CONTROLLER_REGISTRY[controller_type]
    print(f"{controller_type}:")
    print(f"  Description: {info['description']}")
    print(f"  Gain count: {info['gain_count']}")
    print(f"  Default gains: {get_default_gains(controller_type)}")
    print()