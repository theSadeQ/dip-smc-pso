# Example from: docs\guides\how-to\running-simulations.md
# Index: 4
# Runnable: True
# Hash: c587443a

import multiprocessing as mp
from functools import partial

def run_single_simulation(ic, controller_gains):
    """Run simulation with specific initial condition."""
    config = load_config('config.yaml')
    config.simulation.initial_conditions = ic

    controller = create_controller(
        'classical_smc',
        config=config.controllers.classical_smc,
        gains=controller_gains
    )

    runner = SimulationRunner(config)
    result = runner.run(controller)

    return result['metrics']['ise']

# Define initial conditions
initial_conditions = [
    [0, 0, 0.1, 0, 0.15, 0],
    [0, 0, 0.2, 0, 0.25, 0],
    [0, 0, 0.3, 0, 0.35, 0],
]

# Define gains
gains = [10, 8, 15, 12, 50, 5]

# Run in parallel
with mp.Pool(4) as pool:
    run_func = partial(run_single_simulation, controller_gains=gains)
    ise_results = pool.map(run_func, initial_conditions)

print(f"Mean ISE: {np.mean(ise_results):.4f}")
print(f"Std ISE: {np.std(ise_results):.4f}")