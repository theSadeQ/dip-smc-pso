# Example from: docs\reference\utils\visualization___init__.md
# Index: 1
# Runnable: True
# Hash: b59c46b9

from src.utils.visualization import DIPAnimator
import numpy as np

# Create animator
animator = DIPAnimator(
    L1=0.3, L2=0.25,  # Pendulum lengths
    fps=30,  # 30 frames per second
    trail_length=50  # Show last 50 positions
)

# Animate simulation results
animator.animate(
    t=t,  # Time vector
    x=x,  # State trajectories
    save_path="simulation.mp4",
    dpi=120
)

print(f"Animation created at 30 FPS")
print(f"Frame interval: {1000/30:.2f} ms")