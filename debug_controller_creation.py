"""Debug: Check if controller factory creates dynamics model."""

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller

# Load config
config = load_config("config.yaml")

print("=" * 80)
print("Controller Creation Diagnostic")
print("=" * 80)

# Create controller through factory
gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
print(f"Creating controller with config type: {type(config)}")
print(f"Config has physics: {hasattr(config, 'physics')}")
print(f"Config has controllers: {hasattr(config, 'controllers')}")
controller = create_controller(
    'classical_smc',
    config=config,
    gains=gains
)

print(f"Controller type: {type(controller).__name__}")
print(f"Has dynamics_model attr: {hasattr(controller, 'dynamics_model')}")
print(f"Has dyn attr: {hasattr(controller, 'dyn')}")
print(f"Has _dynamics_ref attr: {hasattr(controller, '_dynamics_ref')}")
print()

if hasattr(controller, 'dyn'):
    dyn = controller.dyn
    print(f"controller.dyn: {dyn}")
    print(f"Type: {type(dyn)}")

    if dyn is not None:
        print(f"Has step method: {hasattr(dyn, 'step')}")
        if hasattr(dyn, 'state_dim'):
            print(f"State dim: {dyn.state_dim}")
    else:
        print("[ERROR] controller.dyn is None!")

print()
print("Checking config.physics:")
if hasattr(config, 'physics'):
    print(f"config.physics exists: {config.physics}")
else:
    print("[ERROR] config.physics does NOT exist!")
