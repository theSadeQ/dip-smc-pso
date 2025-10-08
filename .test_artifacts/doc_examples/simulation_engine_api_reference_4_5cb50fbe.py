# Example from: docs\api\simulation_engine_api_reference.md
# Index: 4
# Runnable: False
# Hash: 5cb50fbe

# Legacy imports work unchanged
from src.simulation import run_simulation, step, get_step_fn, simulate

# Original function signatures preserved
t, x, u = run_simulation(controller=..., dynamics_model=..., sim_time=5.0, dt=0.01, ...)

# Legacy step function
x_next = step(x_current, u_current, dt)