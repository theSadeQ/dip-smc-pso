# Example from: docs\reference\interfaces\hil___init__.md
# Index: 4
# Runnable: True
# Hash: 2861363f

from src.interfaces import hil

# Setup with logging
server = hil.PlantServer(cfg=config, bind_addr=("127.0.0.1", 5555), dt=0.01)
client = hil.HILControllerClient(
    cfg=config,
    plant_addr=("127.0.0.1", 5555),
    bind_addr=("127.0.0.1", 0),
    dt=0.01,
    steps=5000
)

# Add logger
logger = hil.DataLogger("hil_results.h5", format="hdf5")

# Attach to client
client.set_logger(logger)

# Run with logging
server.start()