# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 22
# Runnable: True
# Hash: 5340f1a7

from scipy.stats import qmc

sampler = qmc.LatinHypercube(d=n_dimensions)
samples = sampler.random(n=n_particles)

# Scale to bounds
positions = bounds_lower + samples * (bounds_upper - bounds_lower)