# Example from: docs\hil_quickstart.md
# Index: 4
# Runnable: True
# Hash: 1fe7650b

from src.fault_detection.fdi import FaultDetector
from src.interfaces.hil.plant_server import PlantServer

# Create FDI system with HIL-specific fault types
fdi = FaultDetector(
    fault_types=['sensor_failure', 'actuator_saturation', 'network_timeout']
)

# Initialize HIL with FDI monitoring
plant_server = PlantServer(config, fault_detector=fdi)

# FDI automatically monitors:
# - Sensor value bounds and rate limits
# - Network packet integrity and timing
# - Control signal saturation and discontinuities