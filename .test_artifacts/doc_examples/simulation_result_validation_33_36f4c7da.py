# Example from: docs\validation\simulation_result_validation.md
# Index: 33
# Runnable: True
# Hash: 36f4c7da

# After fitting (e.g., lognormal)
from scipy import stats

dist_params = result.data['distribution_analysis']['distribution_fits']['lognormal']['parameters']
dist = stats.lognorm(*dist_params)

# Probability of exceeding threshold
prob_exceed = 1 - dist.cdf(threshold)
print(f"P(settling time > 3s) = {prob_exceed:.4f}")

# 95th percentile
percentile_95 = dist.ppf(0.95)
print(f"95% of scenarios have settling time < {percentile_95:.2f}s")