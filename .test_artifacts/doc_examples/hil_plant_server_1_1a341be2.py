# Example from: docs\reference\interfaces\hil_plant_server.md
# Index: 1
# Runnable: True
# Hash: 1a341be2

from src.interfaces.hil import PlantServer
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# Initialize server
server = PlantServer(
    cfg=config,
    bind_addr=("127.0.0.1", 5555),
    dt=0.01,  # 10 ms control period
    extra_latency_ms=5,  # 5 ms network latency
    sensor_noise_std=0.01,  # 1% sensor noise
    max_steps=5000  # 50 seconds simulation
)

# Start server (blocks until client connects)
server.start()

# Server runs until client disconnects or max_steps reached
server.close()