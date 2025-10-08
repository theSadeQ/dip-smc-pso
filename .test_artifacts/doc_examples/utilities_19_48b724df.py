# Example from: docs\guides\api\utilities.md
# Index: 19
# Runnable: True
# Hash: 48b724df

from src.utils.analysis import profile_simulation

def run_simulation():
    return runner.run(controller)

profile = profile_simulation(run_simulation, n_runs=100)

print(f"Average time: {profile['mean_time']:.4f} s")
print(f"Std dev: {profile['std_time']:.4f} s")
print(f"Min time: {profile['min_time']:.4f} s")
print(f"Max time: {profile['max_time']:.4f} s")