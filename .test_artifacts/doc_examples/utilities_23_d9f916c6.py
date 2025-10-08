# Example from: docs\guides\api\utilities.md
# Index: 23
# Runnable: True
# Hash: d9f916c6

from src.utils.visualization import plot_controller_comparison

results_dict = {
    'Classical SMC': result_classical,
    'STA-SMC': result_sta,
    'Adaptive SMC': result_adaptive
}

fig = plot_controller_comparison(
    results_dict,
    metrics=['ise', 'settling_time', 'control_effort']
)
plt.savefig('controller_comparison.png')