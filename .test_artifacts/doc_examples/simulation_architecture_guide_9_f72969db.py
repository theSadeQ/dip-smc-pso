# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 9
# Runnable: True
# Hash: f72969db

from src.simulation.engines.simulation_runner import step, get_step_fn

# Automatic dispatch based on config
# config.simulation.use_full_dynamics = True/False

x_next = step(x_current, u, dt)

# Manual selection
full_step_fn = _load_full_step()      # Full nonlinear model
lowrank_step_fn = _load_lowrank_step()  # Low-rank approximation

x_next_full = full_step_fn(x, u, dt)
x_next_lr = lowrank_step_fn(x, u, dt)