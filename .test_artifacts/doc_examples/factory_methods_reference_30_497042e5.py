# Example from: docs\api\factory_methods_reference.md
# Index: 30
# Runnable: True
# Hash: 497042e5

# Pattern 1: Direct controller configuration
config.controllers.classical_smc.gains = [20, 15, 12, 8, 35, 5]

# Pattern 2: Controller defaults
config.controller_defaults.classical_smc.gains = [20, 15, 12, 8, 35, 5]

# Pattern 3: Dictionary-style access
config.controllers['classical_smc']['gains'] = [20, 15, 12, 8, 35, 5]