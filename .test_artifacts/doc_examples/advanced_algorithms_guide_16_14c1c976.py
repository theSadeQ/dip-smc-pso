# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 16
# Runnable: True
# Hash: 14c1c976

import time

start = time.time()
result = tuner.optimise(iters_override=100, n_particles_override=30)
elapsed = time.time() - start

evaluations = 100 * 30  # iters * particles
evals_per_second = evaluations / elapsed

print(f"Optimization time: {elapsed:.2f} s")
print(f"Evaluations/second: {evals_per_second:.1f}")
print(f"Cost per evaluation: {1000 * elapsed / evaluations:.2f} ms")