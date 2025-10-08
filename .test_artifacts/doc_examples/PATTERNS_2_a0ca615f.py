# Example from: docs\PATTERNS.md
# Index: 2
# Runnable: True
# Hash: a0ca615f

from src.controllers.factory import create_controller

# Simple instantiation
controller = create_controller('classical_smc', gains=[10, 8, 15, 12, 50, 5])

# With configuration
controller = create_controller('adaptive_smc', config=app_config, gains=optimized_gains)