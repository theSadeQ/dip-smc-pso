# Example from: docs\api\simulation_engine_api_reference.md
# Index: 27
# Runnable: True
# Hash: e181bacd

from src.simulation import get_step_fn

# Get configured step function
step_fn = get_step_fn()
x_next = step_fn(x, u, dt)