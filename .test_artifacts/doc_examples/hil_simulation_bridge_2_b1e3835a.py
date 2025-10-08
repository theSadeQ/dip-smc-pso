# Example from: docs\reference\interfaces\hil_simulation_bridge.md
# Index: 2
# Runnable: True
# Hash: b1e3835a

from src.interfaces.hil.simulation_bridge import SimulationBridge

# TCP server, UDP client
bridge = SimulationBridge(
    server_addr=("127.0.0.1", 5555),
    client_addr=("127.0.0.1", 6666),
    server_protocol="tcp",
    client_protocol="udp"
)

bridge.start()