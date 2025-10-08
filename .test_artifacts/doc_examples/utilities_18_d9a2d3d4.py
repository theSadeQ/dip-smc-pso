# Example from: docs\guides\api\utilities.md
# Index: 18
# Runnable: True
# Hash: d9a2d3d4

from src.utils.analysis import compare_controllers_statistical

# Compare two controller results
controller_a_results = monte_carlo_results_a
controller_b_results = monte_carlo_results_b

comparison = compare_controllers_statistical(
    controller_a_results,
    controller_b_results,
    metric='ise'
)

print(f"t-statistic: {comparison['t_statistic']:.4f}")
print(f"p-value: {comparison['p_value']:.4f}")

if comparison['p_value'] < 0.05:
    print("Statistically significant difference")