# Example from: docs\api\factory_reference.md
# Index: 1
# Runnable: True
# Hash: f21aaf13

from src.controllers.factory import create_controller

# Basic creation with default gains
controller = create_controller('classical_smc')

# Creation with custom gains
controller = create_controller('adaptive_smc', gains=[25.0, 18.0, 15.0, 10.0, 4.0])

# Creation with configuration
controller = create_controller('sta_smc', config=my_config)