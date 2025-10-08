# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 6
# Runnable: True
# Hash: d365faf5

from src.controllers.factory import list_available_controllers, get_default_gains

# Get all available controller types
available_types = list_available_controllers()
print(available_types)
# Output: ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

# Get default gains for any controller type
default_gains = get_default_gains('classical_smc')
print(default_gains)
# Output: [8.0, 6.0, 4.0, 3.0, 15.0, 2.0]