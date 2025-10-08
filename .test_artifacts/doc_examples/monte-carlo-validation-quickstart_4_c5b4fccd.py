# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 4
# Runnable: True
# Hash: c5b4fccd

from statsmodels.stats.power import ttest_power

# Calculate required sample size for desired power
effect_size = 0.68  # From Cohen's d above
alpha = 0.05
power = 0.80  # Desired power (80%)

# Compute required sample size per group
from statsmodels.stats.power import tt_solve_power

required_n = tt_solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative='two-sided'
)

print(f"\\nPower Analysis:")
print(f"  Effect size (d): {effect_size}")
print(f"  Significance level (α): {alpha}")
print(f"  Desired power: {power}")
print(f"  Required sample size per group: {np.ceil(required_n):.0f}")
print(f"  \\n  Current sample size: 10")
print(f"  Recommendation: Increase to {np.ceil(required_n):.0f} trials per controller")