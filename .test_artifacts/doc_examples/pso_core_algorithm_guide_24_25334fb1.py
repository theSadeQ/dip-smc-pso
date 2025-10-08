# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 24
# Runnable: True
# Hash: 25334fb1

if np.any(fitness > 1e6):
    print(f"WARNING: {np.sum(fitness > 1e6)} constraint violations")