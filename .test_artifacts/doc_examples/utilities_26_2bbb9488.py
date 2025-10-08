# Example from: docs\guides\api\utilities.md
# Index: 26
# Runnable: True
# Hash: 2bbb9488

from src.utils.analysis import (
    compute_confidence_interval,
    compare_controllers_statistical
)

# Run Monte Carlo
n_trials = 100
results = []

for i in range(n_trials):
    ic = np.random.normal(ic_mean, ic_std)
    result = runner.run(controller, initial_state=ic)
    results.append(result)

# Compute statistics
ise_values = [r['metrics']['ise'] for r in results]
mean_ise, ci_lower, ci_upper = compute_confidence_interval(ise_values)

print(f"ISE: {mean_ise:.4f} [{ci_lower:.4f}, {ci_upper:.4f}]")

# Compare with baseline
if baseline_results:
    comparison = compare_controllers_statistical(results, baseline_results)
    print(f"Improvement: {comparison['improvement_percent']:.1f}%")
    print(f"p-value: {comparison['p_value']:.4f}")