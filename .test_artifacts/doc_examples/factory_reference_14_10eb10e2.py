# Example from: docs\api\factory_reference.md
# Index: 14
# Runnable: True
# Hash: 10eb10e2

# Legacy pattern (still supported)
from src.controllers.factory import create_classical_smc_controller
controller = create_classical_smc_controller(gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0])

# Modern pattern (recommended)
from src.controllers.factory import create_controller
controller = create_controller('classical_smc', gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0])