# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 25
# Runnable: True
# Hash: 6a81d76c

plt.scatter(positions[:, 0], positions[:, 1], alpha=0.5)
plt.scatter(global_best_position[0], global_best_position[1],
           c='red', marker='*', s=200)