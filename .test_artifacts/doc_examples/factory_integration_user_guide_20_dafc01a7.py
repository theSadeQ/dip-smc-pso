# Example from: docs\factory\factory_integration_user_guide.md
# Index: 20
# Runnable: True
# Hash: dafc01a7

import logging
from src.controllers.factory import create_controller

# Enable factory debug logging
logging.getLogger('src.controllers.factory').setLevel(logging.DEBUG)

# Create controller with detailed logging
controller = create_controller('classical_smc', gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0])