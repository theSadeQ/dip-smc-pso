# Example from: docs\guides\api\utilities.md
# Index: 21
# Runnable: True
# Hash: 53164341

from src.utils.visualization import (
    plot_state_trajectory,
    plot_control_signal,
    plot_phase_portrait,
    plot_sliding_surface
)

# State trajectory
fig1 = plot_state_trajectory(result['t'], result['state'])

# Control signal
fig2 = plot_control_signal(result['t'], result['control'], max_force=100)

# Phase portrait
fig3 = plot_phase_portrait(
    result['state'][:, 2],  # theta1
    result['state'][:, 3]   # dtheta1
)

# Sliding surface
if 'sliding_surface' in result:
    fig4 = plot_sliding_surface(result['t'], result['sliding_surface'])