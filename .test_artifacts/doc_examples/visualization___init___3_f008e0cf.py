# Example from: docs\reference\utils\visualization___init__.md
# Index: 3
# Runnable: True
# Hash: f008e0cf

from src.utils.visualization import MultiSystemAnimator

# Create comparison animator
animator = MultiSystemAnimator(
    systems=['Classical SMC', 'Adaptive SMC', 'STA SMC'],
    L1=0.3, L2=0.25,
    layout='horizontal'  # Side-by-side comparison
)

# Animate multiple controllers
animator.animate_comparison(
    t=t,
    states=[x_classical, x_adaptive, x_sta],
    save_path="comparison.mp4",
    fps=30
)