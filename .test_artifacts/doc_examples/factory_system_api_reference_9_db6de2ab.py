# Example from: docs\api\factory_system_api_reference.md
# Index: 9
# Runnable: True
# Hash: db6de2ab

from src.controllers.factory import create_controller, list_available_controllers
from src.config import load_config

config = load_config("config.yaml")

# Create all available controller types
controllers = {}
for controller_type in list_available_controllers():
    try:
        controllers[controller_type] = create_controller(controller_type, config)
        print(f"✓ Created {controller_type}")
    except Exception as e:
        print(f"✗ Failed to create {controller_type}: {e}")

# Run comparative simulation
for name, controller in controllers.items():
    cost = simulate_and_evaluate(controller)
    print(f"{name}: cost={cost:.3f}")