# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 37
# Runnable: True
# Hash: c3f99df9

# New way - enhanced capabilities
from src.controllers.factory import create_controller

controller = create_controller(
    controller_type='classical_smc',
    config=config,
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
)