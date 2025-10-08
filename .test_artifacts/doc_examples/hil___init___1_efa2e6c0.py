# Example from: docs\reference\interfaces\hil___init__.md
# Index: 1
# Runnable: True
# Hash: efa2e6c0

from src.interfaces import hil

# Complete HIL system setup
config = hil.load_config("config.yaml")

# Start plant server
server = hil.PlantServer(
    cfg=config,
    bind_addr=("127.0.0.1", 5555),
    dt=0.01
)

# Start controller client
client = hil.HILControllerClient(
    cfg=config,
    plant_addr=("127.0.0.1", 5555),
    bind_addr=("127.0.0.1", 0),
    dt=0.01,
    steps=5000
)

# Run HIL simulation
server.start()  # Blocks until client connects