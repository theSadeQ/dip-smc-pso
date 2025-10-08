# Example from: docs\factory_integration_documentation.md
# Index: 19
# Runnable: True
# Hash: a9b5e399

from src.controllers.factory import create_controller
from src.hil.controller_client import ControllerClient

# Create controller
controller = create_controller('adaptive_smc', gains=optimized_gains)

# HIL integration
hil_client = ControllerClient(
    controller=controller,
    host='localhost',
    port=8888
)

hil_client.run()