# Example from: docs\guides\QUICK_REFERENCE.md
# Index: 3
# Runnable: True
# Hash: 10321d41

import numpy as np

# Define initial conditions
initial_conditions = [
    [0, 0, 0.1, 0, 0.15, 0],
    [0, 0, 0.2, 0, 0.25, 0],
    [0, 0, 0.3, 0, 0.35, 0],
]

results = []
for ic in initial_conditions:
    config.simulation.initial_conditions = ic
    result = runner.run(controller)
    results.append(result['metrics']['ise'])

print(f"Mean ISE: {np.mean(results):.4f}")
print(f"Std ISE: {np.std(results):.4f}")