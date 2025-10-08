# Example from: docs\reference\utils\visualization___init__.md
# Index: 5
# Runnable: True
# Hash: 1bfcabb1

from src.utils.visualization import ControlPlotter
import numpy as np

# Define perceptually uniform color scheme
colors = {
    'state': '#1f77b4',  # Blue
    'control': '#ff7f0e',  # Orange
    'reference': '#2ca02c',  # Green
    'error': '#d62728'  # Red
}

plotter = ControlPlotter(color_scheme=colors)

# Plot with consistent colors
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

axes[0].plot(t, x[:, 1], color=colors['state'], label='θ₁')
axes[0].plot(t, ref, color=colors['reference'],
            linestyle='--', label='Reference')

axes[1].plot(t, u, color=colors['control'], label='Control')
axes[1].axhline(0, color='gray', linestyle=':', alpha=0.5)

for ax in axes:
    ax.legend()
    ax.grid(alpha=0.3)

plt.tight_layout()