# Example from: docs\guides\api\optimization.md
# Index: 25
# Runnable: False
# Hash: 961924fa

# Expensive to evaluate one controller at a time
def slow_cost(gains):
    for ic in scenarios:  # Sequential
        result = runner.run(controller, initial_state=ic)
    return ...

# Fast: Evaluate all scenarios in parallel
def fast_cost(gains):
    from src.core.vector_sim import run_batch_simulation
    results = run_batch_simulation(controller, dynamics, scenarios, sim_params)
    return ...