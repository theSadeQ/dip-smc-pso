# Example from: docs\guides\api\simulation.md
# Index: 27
# Runnable: True
# Hash: d1efc62a

# Sequential (slow)
results = []
for ic in initial_conditions:
    result = runner.run(controller, initial_state=ic)
    results.append(result)

# Batch (fast, Numba-accelerated)
batch_results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)