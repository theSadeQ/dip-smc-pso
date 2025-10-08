# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 1
# Runnable: True
# Hash: 81cff2dc

positions = np.random.uniform(
       low=bounds_lower,
       high=bounds_upper,
       size=(population_size, n_dimensions)
   )