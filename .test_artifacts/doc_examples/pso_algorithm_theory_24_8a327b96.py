# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 24
# Runnable: True
# Hash: 8a327b96

from multiprocessing import Pool

with Pool(processes=8) as pool:
    fitness = pool.map(evaluate_fitness, positions)