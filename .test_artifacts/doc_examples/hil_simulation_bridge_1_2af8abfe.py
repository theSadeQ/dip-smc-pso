# Example from: docs\reference\interfaces\hil_simulation_bridge.md
# Index: 1
# Runnable: True
# Hash: 2af8abfe

from src.interfaces.hil.simulation_bridge import SimulationBridge

# Initialize bridge
bridge = SimulationBridge(
    server_addr=("127.0.0.1", 5555),
    client_addr=("127.0.0.1", 6666),
    protocol="tcp"
)

# Start bridge
bridge.start()

# Bridge runs until shutdown
bridge.stop()