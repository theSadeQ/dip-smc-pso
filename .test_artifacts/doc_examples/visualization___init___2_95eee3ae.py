# Example from: docs\reference\utils\visualization___init__.md
# Index: 2
# Runnable: True
# Hash: 95eee3ae

from src.utils.visualization import ControlPlotter
import matplotlib.pyplot as plt

# Create plotter
plotter = ControlPlotter()

# Create comprehensive plot layout
fig, axes = plotter.plot_comprehensive(
    t=t, x=x, u=u,
    reference=np.zeros_like(x),
    title="Classical SMC Performance"
)

# Customize appearance
plotter.set_style('seaborn-v0_8-paper')
plotter.add_grid(axes, alpha=0.3)

plt.savefig('performance.png', dpi=300, bbox_inches='tight')