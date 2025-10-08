# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 14
# Runnable: True
# Hash: ecd73619

import matplotlib.pyplot as plt
from matplotlib import cm

# Fix other gains
fixed_gains = [15, 12, 8, 35, 5]  # k2, λ1, λ2, K, kd

# Vary K and k1
K_range = np.linspace(10, 200, 30)
k1_range = np.linspace(0.1, 50, 30)
K_grid, k1_grid = np.meshgrid(K_range, k1_range)

fitness_grid = np.zeros_like(K_grid)
for i in range(K_grid.shape[0]):
    for j in range(K_grid.shape[1]):
        gains = [k1_grid[i,j]] + fixed_gains
        fitness_grid[i,j] = evaluate_fitness(gains)

# 3D surface plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(K_grid, k1_grid, fitness_grid, cmap=cm.viridis)
ax.set_xlabel('K (Switching Gain)')
ax.set_ylabel('k1 (Surface Gain)')
ax.set_zlabel('Fitness')
plt.colorbar(surf)
plt.title('Fitness Landscape: K vs k1 Interaction')