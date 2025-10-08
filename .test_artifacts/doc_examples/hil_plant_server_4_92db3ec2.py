# Example from: docs\reference\interfaces\hil_plant_server.md
# Index: 4
# Runnable: False
# Hash: 92db3ec2

from src.interfaces.hil import PlantServer
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='hil_server.log'
)

# Server with logging
server = PlantServer(
    cfg=config,
    bind_addr=("127.0.0.1", 5555),
    dt=0.01,
    extra_latency_ms=5,
    sensor_noise_std=0.01
)

# Enable detailed monitoring
logger = logging.getLogger('HIL.PlantServer')
logger.info("Starting HIL plant server...")

try:
    server.start()
except Exception as e:
    logger.error(f"Server error: {e}")
finally:
    server.close()
    logger.info("Server shutdown complete")