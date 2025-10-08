# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 21
# Runnable: True
# Hash: 9b4911ef

positions = np.random.uniform(
    low=bounds_lower,
    high=bounds_upper,
    size=(n_particles, n_dimensions)
)