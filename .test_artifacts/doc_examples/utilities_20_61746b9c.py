# Example from: docs\guides\api\utilities.md
# Index: 20
# Runnable: True
# Hash: 61746b9c

from src.utils.visualization import plot_results

# Plot state trajectories and control
fig, axes = plot_results(result, show=True)

# Customize plots
fig, axes = plot_results(
    result,
    plot_types=['state', 'control', 'phase'],
    figsize=(15, 10),
    show=False
)
plt.savefig('simulation_results.png', dpi=300)