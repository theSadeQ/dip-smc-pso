# Example from: docs\reference\interfaces\hil_plant_server.md
# Index: 2
# Runnable: True
# Hash: aad1acd0

from src.interfaces.hil import PlantServer
from src.plant.models.full import FullDIPDynamics

# Create high-fidelity dynamics model
dynamics = FullDIPDynamics(
    config=config,
    enable_monitoring=True,
    enable_validation=True
)

# Server with custom dynamics
server = PlantServer(
    cfg=config,
    bind_addr=("0.0.0.0", 5555),  # Listen on all interfaces
    dt=0.01
)

# Override dynamics model
server._dynamics = dynamics

server.start()