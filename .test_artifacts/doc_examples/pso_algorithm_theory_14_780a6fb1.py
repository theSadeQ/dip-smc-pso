# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 14
# Runnable: True
# Hash: 780a6fb1

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.semilogy(fitness_history['iteration'], fitness_history['best_fitness'])
plt.xlabel('Iteration')
plt.ylabel('Best Fitness (log scale)')
plt.title('PSO Convergence Curve')
plt.grid(True)