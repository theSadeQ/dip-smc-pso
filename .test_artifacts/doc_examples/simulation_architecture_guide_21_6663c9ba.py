# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 21
# Runnable: True
# Hash: 6663c9ba

import time
import cProfile

# Time measurement
start = time.perf_counter()
states = simulate(x0, u, dt)
elapsed = time.perf_counter() - start
print(f"Simulation time: {elapsed*1000:.2f} ms")

# Detailed profiling
profiler = cProfile.Profile()
profiler.enable()

for _ in range(100):
    states = simulate(x0, u, dt)

profiler.disable()
profiler.print_stats(sort='cumtime')

# Expected hot spots:
# 1. np.linalg.solve (30-40%)
# 2. dynamics evaluation (20-30%)
# 3. safety guards (5-10%)
# 4. array operations (10-20%)