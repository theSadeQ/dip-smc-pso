# Example from: docs\api\simulation_engine_api_reference.md
# Index: 25
# Runnable: True
# Hash: 9a35a0c4

from src.simulation import step

# Single dynamics step
x_next = step(x_current, u_current, dt=0.01)