# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 12
# Runnable: True
# Hash: 0b5512c6

import matplotlib.pyplot as plt

def plot_adaptation_history(history):
    """Visualize adaptive gain evolution."""

    fig, axes = plt.subplots(3, 1, figsize=(10, 8))

    # Adaptive gain evolution
    axes[0].plot(history['K'], label='K(t)')
    axes[0].axhline(y=controller.K_init, color='g', linestyle='--', label='K_init')
    axes[0].set_ylabel('Adaptive Gain K (N)')
    axes[0].legend()
    axes[0].grid(True)

    # Sliding surface
    axes[1].plot(history['sigma'], label='σ(t)')
    axes[1].axhline(y=controller.dead_zone, color='r', linestyle='--', alpha=0.5)
    axes[1].axhline(y=-controller.dead_zone, color='r', linestyle='--', alpha=0.5)
    axes[1].set_ylabel('Sliding Surface σ')
    axes[1].legend()
    axes[1].grid(True)

    # Gain rate of change
    axes[2].plot(history['dK'], label='dK/dt')
    axes[2].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    axes[2].set_ylabel('Gain Rate dK/dt (N/s)')
    axes[2].set_xlabel('Time Step')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    return fig