# Example from: docs\guides\how-to\running-simulations.md
# Index: 7
# Runnable: True
# Hash: 1e13ddd7

import multiprocessing as mp
import subprocess

def run_simulation(params):
    """Run simulation with specific parameters."""
    ctrl, ic_idx, ic = params
    cmd = [
        'python', 'simulate.py',
        '--ctrl', ctrl,
        '--override', f'simulation.initial_conditions={ic}',
        '--save', f'results_{ctrl}_ic{ic_idx}.json'
    ]
    subprocess.run(cmd, check=True)
    return f'results_{ctrl}_ic{ic_idx}.json'

# Define parameter combinations
controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
initial_conditions = [
    [0, 0, 0.1, 0, 0.15, 0],
    [0, 0, 0.2, 0, 0.25, 0],
]

# Create all combinations
experiments = [
    (ctrl, i, ic)
    for ctrl in controllers
    for i, ic in enumerate(initial_conditions)
]

# Run in parallel (4 processes)
with mp.Pool(4) as pool:
    result_files = pool.map(run_simulation, experiments)

print(f"Generated {len(result_files)} result files")