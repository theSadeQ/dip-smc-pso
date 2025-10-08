# Example from: docs\reference\controllers\smc_core_equivalent_control.md
# Index: 5
# Runnable: True
# Hash: bfe4c3f9

import time

# Benchmark equivalent control computation
n_iterations = 1000
start = time.time()

for _ in range(n_iterations):
    u_eq = eq_control.compute(state)

elapsed = time.time() - start
time_per_call = (elapsed / n_iterations) * 1e6  # microseconds

print(f"Equivalent control time: {time_per_call:.2f} μs per call")
print(f"Can achieve ~{1e6 / time_per_call:.0f} Hz control rate")