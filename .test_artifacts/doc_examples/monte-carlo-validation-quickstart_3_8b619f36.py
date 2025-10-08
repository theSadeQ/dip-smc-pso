# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 3
# Runnable: True
# Hash: 8b619f36

from scipy.stats import ttest_ind

# Load data
df = pd.read_csv('monte_carlo_quick_test/results.csv')

classical = df[df['controller'] == 'classical_smc']['ise'].values
sta = df[df['controller'] == 'sta_smc']['ise'].values

# Welch's t-test (unequal variances)
t_stat, p_value = ttest_ind(classical, sta, equal_var=False)

# Effect size (Cohen's d)
pooled_std = np.sqrt((classical.std()**2 + sta.std()**2) / 2)
cohens_d = (classical.mean() - sta.mean()) / pooled_std

# Interpret results
alpha = 0.05
significant = p_value < alpha

print("\\nHypothesis Test Results:")
print(f"  H₀: No difference between controllers")
print(f"  H₁: Controllers have different performance")
print(f"  \\n  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Significance level (α): {alpha}")
print(f"  Result: {'REJECT H₀' if significant else 'FAIL TO REJECT H₀'} (p {'<' if significant else '>='} {alpha})")
print(f"  \\n  Effect size (Cohen's d): {cohens_d:.4f}")
print(f"  Interpretation: {interpret_cohens_d(cohens_d)}")

def interpret_cohens_d(d):
    """Interpret Cohen's d effect size."""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "Negligible"
    elif abs_d < 0.5:
        return "Small"
    elif abs_d < 0.8:
        return "Medium"
    else:
        return "Large"