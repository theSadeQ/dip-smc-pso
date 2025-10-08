# Example from: docs\reference\interfaces\hil_controller_client.md
# Index: 2
# Runnable: True
# Hash: ab2ae924

from src.interfaces.hil import HILControllerClient
from src.controllers import ClassicalSMC

# Create custom controller
controller = ClassicalSMC(
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0,
    boundary_layer=0.01
)

# Client with custom controller
client = HILControllerClient(
    cfg=config,
    plant_addr=("192.168.1.100", 5555),  # Remote server
    bind_addr=("0.0.0.0", 6666),
    dt=0.01,
    steps=10000
)

# Override controller
client._controller = controller

# Run simulation
client.run()