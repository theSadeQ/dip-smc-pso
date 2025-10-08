# Example from: docs\controllers\factory_system_guide.md
# Index: 4
# Runnable: True
# Hash: 4f0fe913

from src.controllers.factory import (
    create_controller,           # Main factory function
    list_available_controllers,  # Discovery
    get_default_gains,           # Gain specifications
    SMCType,                     # Enum for controller types
    SMCFactory,                  # Object-oriented interface
)