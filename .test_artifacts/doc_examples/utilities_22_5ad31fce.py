# Example from: docs\guides\api\utilities.md
# Index: 22
# Runnable: True
# Hash: 5ad31fce

from src.utils.visualization import DIPAnimator

animator = DIPAnimator(config.dip_params)

# Create animation
anim = animator.animate(
    result['t'],
    result['state'],
    save_path='simulation.mp4',
    fps=30
)