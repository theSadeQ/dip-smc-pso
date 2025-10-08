# Example from: docs\reference\interfaces\hil_simulation_bridge.md
# Index: 4
# Runnable: False
# Hash: b52ed7eb

# example-metadata:
# runnable: false

from src.interfaces.hil.simulation_bridge import SimulationBridge
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SimulationBridge')

# Bridge with fault tolerance
bridge = SimulationBridge(
    server_addr=("127.0.0.1", 5555),
    client_addr=("127.0.0.1", 6666),
    heartbeat_interval=1.0,  # 1 second heartbeat
    reconnect_attempts=5
)

# Monitor health
def health_callback(status):
    if status == "TIMEOUT":
        logger.warning("Connection timeout detected")
    elif status == "RECONNECTING":
        logger.info("Attempting reconnection...")
    elif status == "OK":
        logger.info("Connection healthy")

bridge.set_health_callback(health_callback)
bridge.start()