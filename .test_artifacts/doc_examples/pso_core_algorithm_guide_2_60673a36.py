# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 2
# Runnable: True
# Hash: 60673a36

# Small random velocities (10% of range)
   velocity_range = 0.1 * (bounds_upper - bounds_lower)
   velocities = np.random.uniform(
       low=-velocity_range,
       high=velocity_range,
       size=(population_size, n_dimensions)
   )