# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 4
# Runnable: True
# Hash: be3f619a

personal_best_positions = positions.copy()
   personal_best_fitness = fitness.copy()

   global_best_idx = np.argmin(fitness)
   global_best_position = positions[global_best_idx]
   global_best_fitness = fitness[global_best_idx]