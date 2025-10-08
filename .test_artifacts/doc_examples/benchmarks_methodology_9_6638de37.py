# Example from: docs\benchmarks_methodology.md
# Index: 9
# Runnable: True
# Hash: 6638de37

from scipy import stats

# Compare two controllers
ctrl1_ise = [trial['ise'] for trial in metrics_ctrl1]
ctrl2_ise = [trial['ise'] for trial in metrics_ctrl2]

# Welch's t-test (unequal variances)
t_stat, p_value = stats.ttest_ind(ctrl1_ise, ctrl2_ise, equal_var=False)

# Significant difference if p < 0.05
if p_value < 0.05:
    print(f"Controllers significantly different (p={p_value:.4f})")