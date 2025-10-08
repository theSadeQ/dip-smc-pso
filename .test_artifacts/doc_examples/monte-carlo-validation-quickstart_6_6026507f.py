# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 6
# Runnable: True
# Hash: 6026507f

#!/usr/bin/env python
"""Complete Monte Carlo validation workflow with statistical analysis."""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Step 1: Run Monte Carlo (assume already completed)
# Results in: monte_carlo_quick_test/results.csv

# Step 2: Load and validate data
df = pd.read_csv('monte_carlo_quick_test/results.csv')
print(f"Loaded {len(df)} trials")
print(f"Controllers: {df['controller'].unique()}")
print(f"Metrics: {[col for col in df.columns if col not in ['controller', 'trial', 'seed']]}")

# Step 3: Descriptive statistics
print("\\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)
print(df.groupby('controller').agg({
    'ise': ['count', 'mean', 'std', 'min', 'max']
}).round(4))

# Step 4: Hypothesis testing
print("\\n" + "="*60)
print("HYPOTHESIS TESTING")
print("="*60)

classical = df[df['controller'] == 'classical_smc']['ise'].values
sta = df[df['controller'] == 'sta_smc']['ise'].values

t_stat, p_value = stats.ttest_ind(classical, sta, equal_var=False)
print(f"Welch's t-test:")
print(f"  t = {t_stat:.4f}, p = {p_value:.4f}")
print(f"  Result: {'Significant' if p_value < 0.05 else 'Not significant'} at α=0.05")

# Step 5: Effect size
pooled_std = np.sqrt((classical.std()**2 + sta.std()**2) / 2)
cohens_d = abs(classical.mean() - sta.mean()) / pooled_std
print(f"\\nCohen's d: {cohens_d:.4f} ({interpret_cohens_d(cohens_d)})")

# Step 6: Confidence intervals
for ctrl in df['controller'].unique():
    data = df[df['controller'] == ctrl]['ise']
    ci = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
    print(f"\\n{ctrl}:")
    print(f"  Mean: {data.mean():.4f}")
    print(f"  95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")

# Step 7: Visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Box plot
df.boxplot(column='ise', by='controller', ax=axes[0])
axes[0].set_title('ISE Distribution by Controller')
axes[0].set_xlabel('Controller')
axes[0].set_ylabel('ISE')

# Bar plot with CI
controllers = df['controller'].unique()
means = [df[df['controller'] == c]['ise'].mean() for c in controllers]
cis = [stats.t.interval(0.95, len(df[df['controller'] == c])-1,
                         loc=df[df['controller'] == c]['ise'].mean(),
                         scale=stats.sem(df[df['controller'] == c]['ise']))
       for c in controllers]
ci_errors = np.array([[m - ci[0], ci[1] - m] for m, ci in zip(means, cis)]).T

x = np.arange(len(controllers))
axes[1].bar(x, means, alpha=0.7)
axes[1].errorbar(x, means, yerr=ci_errors, fmt='none', ecolor='black', capsize=5)
axes[1].set_xlabel('Controller')
axes[1].set_ylabel('Mean ISE')
axes[1].set_title('Mean ISE with 95% CI')
axes[1].set_xticks(x)
axes[1].set_xticklabels(controllers)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_quick_test/analysis_summary.png', dpi=150)
print("\\nPlot saved: monte_carlo_quick_test/analysis_summary.png")

def interpret_cohens_d(d):
    abs_d = abs(d)
    if abs_d < 0.2: return "Negligible"
    elif abs_d < 0.5: return "Small"
    elif abs_d < 0.8: return "Medium"
    else: return "Large"