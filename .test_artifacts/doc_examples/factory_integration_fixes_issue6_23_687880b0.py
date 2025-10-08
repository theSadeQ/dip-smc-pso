# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 23
# Runnable: False
# Hash: 687880b0

# Use correct controller type names
controller = create_controller('classical_smc', gains=[...])

# Or use aliases
controller = create_controller('classic_smc', gains=[...])

# Check available types
from src.controllers.factory import list_available_controllers
print(list_available_controllers())