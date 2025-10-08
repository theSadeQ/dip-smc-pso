# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 9
# Runnable: True
# Hash: b444b379

from src.core.vector_sim import run_batch_simulation

results = run_batch_simulation(
    controller, dynamics, initial_conditions, sim_params
)