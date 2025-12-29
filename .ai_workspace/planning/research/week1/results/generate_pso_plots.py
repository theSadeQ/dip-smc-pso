"""
Generate example PSO convergence plots for Week 1 Task QW-3.

Since we don't have full history data from the baseline PSO run,
this script generates synthetic example plots demonstrating the
visualization capabilities.
"""

import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.visualization.pso_plots import plot_convergence, plot_diversity, plot_pso_summary

# Generate synthetic PSO convergence data (typical behavior)
n_iters = 200
n_particles = 40
n_dims = 6

# Typical PSO convergence: exponential decay with noise
iterations = np.arange(n_iters)
base_cost = 100.0 * np.exp(-iterations / 30.0) + 0.01
noise = np.random.randn(n_iters) * 0.1 * np.exp(-iterations / 40.0)
fitness_history = np.maximum(base_cost + noise, 0.0)

# Swarm diversity: decreases as particles converge
diversity_base = 10.0 * np.exp(-iterations / 50.0) + 0.5
diversity_noise = np.random.randn(n_iters) * 0.2
diversity = np.maximum(diversity_base + diversity_noise, 0.1)

# Simulate position history (simplified - just use diversity as proxy)
position_history = np.zeros((n_iters, n_dims))
for i in range(n_iters):
    position_history[i, :] = np.random.randn(n_dims) * diversity[i]

print("Generating PSO visualization plots...")
print(f"  Iterations: {n_iters}")
print(f"  Particles: {n_particles}")
print(f"  Dimensions: {n_dims}")
print()

# Generate plots
output_dir = Path(__file__).parent

# 1. Convergence plot
print("1. Generating convergence plot...")
plot_convergence(
    fitness_history,
    save_path=str(output_dir / "pso_convergence.png"),
    show=False,
    title="PSO Convergence - Classical SMC Gain Optimization"
)

# 2. Diversity plot
print("2. Generating diversity plot...")
plot_diversity(
    position_history,
    save_path=str(output_dir / "pso_diversity.png"),
    show=False,
    title="PSO Swarm Diversity - Position Spread Over Time"
)

# 3. Summary plot
print("3. Generating summary plot...")
plot_pso_summary(
    fitness_history,
    position_history,
    save_path=str(output_dir / "pso_convergence_summary.png"),
    show=False
)

print()
print("✓ All plots generated successfully!")
print(f"  Output directory: {output_dir}")
print()
print("Generated files:")
print("  - pso_convergence.png (convergence only)")
print("  - pso_diversity.png (diversity only)")
print("  - pso_convergence_summary.png (combined)")
