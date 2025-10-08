# Example from: docs\reference\interfaces\hil_simulation_bridge.md
# Index: 3
# Runnable: True
# Hash: ece8a6c5

from src.interfaces.hil.simulation_bridge import SimulationBridge
import numpy as np

# Bridge with interpolation
bridge = SimulationBridge(
    server_addr=("127.0.0.1", 5555),
    client_addr=("127.0.0.1", 6666)
)

# Enable state interpolation
bridge.enable_interpolation(method="linear")

# Custom interpolation
def custom_interpolator(state_buffer, t_req):
    # Find surrounding states
    t_prev, x_prev = state_buffer.get_before(t_req)
    t_next, x_next = state_buffer.get_after(t_req)

    # Linear interpolation
    alpha = (t_req - t_prev) / (t_next - t_prev)
    x_interp = x_prev + alpha * (x_next - x_prev)

    return x_interp

bridge.set_interpolator(custom_interpolator)
bridge.start()