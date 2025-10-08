# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 36
# Runnable: True
# Hash: 627e8b59

# Old way - still works
from src.controllers.factory import create_classical_smc_controller

controller = create_classical_smc_controller(
    config=config,
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
)