# Example from: docs\PHASE_5_4_COMPLETION_REPORT.md
# Index: 1
# Runnable: False
# Hash: b8cf1950

# example-metadata:
# runnable: false

# Confidence Intervals (t-distribution)
def compute_statistics(data, metric='ise', confidence=0.95):
    mean, std = data.mean(), data.std()
    se = std / np.sqrt(len(data))
    t_critical = stats.t.ppf(1 - (1-confidence)/2, df=len(data)-1)
    ci = (mean - t_critical*se, mean + t_critical*se)
    return {'mean': mean, 'std': std, 'ci': ci}

# Hypothesis Testing (Welch's t-test)
t_stat, p_value = ttest_ind(classical, sta, equal_var=False)

# Effect Size (Cohen's d)
cohens_d = abs(classical.mean() - sta.mean()) / pooled_std

# Power Analysis (required sample size)
required_n = tt_solve_power(effect_size=0.68, alpha=0.05, power=0.80)