# Example from: docs\guides\how-to\result-analysis.md
# Index: 7
# Runnable: True
# Hash: 3ca70ea6

from scipy import stats

# Perform Welch's t-test
t_stat, p_value = stats.ttest_ind(
    ise_classical_trials,
    ise_sta_trials,
    equal_var=False  # Welch's t-test
)

print(f"\nWelch's t-test:")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value:     {p_value:.6f}")

if p_value < 0.05:
    print("  Result: Statistically significant difference (p < 0.05)")
else:
    print("  Result: No statistically significant difference")