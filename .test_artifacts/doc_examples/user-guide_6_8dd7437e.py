# Example from: docs\guides\user-guide.md
# Index: 6
# Runnable: False
# Hash: 8dd7437e

# example-metadata:
# runnable: false

# parallel_batch.py
from multiprocessing import Pool
import subprocess

def run_simulation(params):
    ctrl, ic_idx, ic = params
    cmd = [
        'python', 'simulate.py',
        '--ctrl', ctrl,
        '--override', f'simulation.initial_conditions={ic}',
        '--save', f'results_{ctrl}_ic{ic_idx}.json'
    ]
    subprocess.run(cmd)
    return f'results_{ctrl}_ic{ic_idx}.json'

# Define experiments
experiments = [
    ('classical_smc', 0, [0, 0, 0.1, 0, 0.15, 0]),
    ('classical_smc', 1, [0, 0, 0.2, 0, 0.25, 0]),
    ('sta_smc', 0, [0, 0, 0.1, 0, 0.15, 0]),
    # ... add all combinations
]

# Run in parallel (4 processes)
with Pool(4) as pool:
    result_files = pool.map(run_simulation, experiments)

print("Batch complete!")
print(f"Generated {len(result_files)} result files")