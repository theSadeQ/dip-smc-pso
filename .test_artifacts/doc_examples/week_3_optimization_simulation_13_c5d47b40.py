# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 13
# Runnable: False
# Hash: c5d47b40

# example-metadata:
# runnable: false

def plot_fitness_landscape(optimizer, fixed_gains, vary_indices):
    """Visualize fitness function in 2D slice."""
    k1_range = np.linspace(0.1, 50, 50)
    k2_range = np.linspace(0.1, 50, 50)

    fitness_grid = np.zeros((len(k1_range), len(k2_range)))

    for i, k1 in enumerate(k1_range):
        for j, k2 in enumerate(k2_range):
            gains = fixed_gains.copy()
            gains[vary_indices[0]] = k1
            gains[vary_indices[1]] = k2
            fitness_grid[i, j] = optimizer.evaluate_fitness(gains)

    plt.contourf(k1_range, k2_range, fitness_grid)
    plt.xlabel(f'Gain {vary_indices[0]}')
    plt.ylabel(f'Gain {vary_indices[1]}')
    plt.colorbar(label='Fitness')