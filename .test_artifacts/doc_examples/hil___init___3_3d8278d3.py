# Example from: docs\reference\interfaces\hil___init__.md
# Index: 3
# Runnable: True
# Hash: 3d8278d3

from src.interfaces import hil

# Setup with fault injection
server = hil.PlantServer(cfg=config, bind_addr=("127.0.0.1", 5555), dt=0.01)

# Add fault injector
injector = hil.FaultInjector()
injector.add_fault(
    fault_type=hil.FaultType.SENSOR_BIAS,
    target="theta1",
    bias=0.1,
    start_time=5.0
)

# Attach to server
server.set_fault_injector(injector)

server.start()