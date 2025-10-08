# Example from: docs\guides\tutorials\tutorial-05-research-workflow.md
# Index: 2
# Runnable: True
# Hash: 19020d06

#!/usr/bin/env python
"""Analyze Monte Carlo results with statistical rigor."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Load results
df = pd.read_csv('experiments/robustness_study/results/monte_carlo_results.csv')

# Compute summary statistics per controller × scenario
summary = df.groupby(['controller', 'scenario']).agg({
    'ise': ['mean', 'std', 'min', 'max'],
    'settling_time': ['mean', 'std'],
    'control_effort': ['mean', 'std']
}).round(4)

print("Summary Statistics:")
print(summary)
print("\n")

# Compute robustness index (coefficient of variation across scenarios)
robustness = df.groupby(['controller', 'trial']).agg({
    'ise': 'std'  # Standard deviation across scenarios (lower = more robust)
})

robustness_summary = robustness.groupby('controller').agg({
    'ise': ['mean', 'std']
})

print("Robustness Index (ISE std dev across scenarios):")
print(robustness_summary)
print("\n")

# Statistical hypothesis testing: Welch's t-test (unequal variances)
classical_robustness = robustness.loc['classical_smc']['ise'].values
hybrid_robustness = robustness.loc['hybrid_adaptive_sta_smc']['ise'].values

t_stat, p_value = stats.ttest_ind(classical_robustness, hybrid_robustness, equal_var=False)

print(f"Welch's t-test:")
print(f"  H₀: No difference in robustness")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.6f}")
print(f"  Significant (α=0.05): {'YES' if p_value < 0.05 else 'NO'}")
print("\n")

# Effect size (Cohen's d)
pooled_std = np.sqrt((classical_robustness.std()**2 + hybrid_robustness.std()**2) / 2)
cohens_d = (classical_robustness.mean() - hybrid_robustness.mean()) / pooled_std

print(f"Effect Size (Cohen's d): {cohens_d:.4f}")
print(f"  Interpretation: ", end="")
if abs(cohens_d) < 0.2:
    print("Small effect")
elif abs(cohens_d) < 0.5:
    print("Medium effect")
else:
    print("Large effect")
print("\n")

# 95% Confidence intervals
ci_classical = stats.t.interval(0.95, len(classical_robustness)-1,
                                 loc=classical_robustness.mean(),
                                 scale=classical_robustness.std()/np.sqrt(len(classical_robustness)))
ci_hybrid = stats.t.interval(0.95, len(hybrid_robustness)-1,
                              loc=hybrid_robustness.mean(),
                              scale=hybrid_robustness.std()/np.sqrt(len(hybrid_robustness)))

print(f"95% Confidence Intervals (Robustness Index):")
print(f"  Classical SMC: [{ci_classical[0]:.4f}, {ci_classical[1]:.4f}]")
print(f"  Hybrid SMC:    [{ci_hybrid[0]:.4f}, {ci_hybrid[1]:.4f}]")