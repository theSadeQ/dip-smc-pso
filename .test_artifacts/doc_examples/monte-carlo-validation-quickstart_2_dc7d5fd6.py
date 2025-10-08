# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 2
# Runnable: True
# Hash: dc7d5fd6

import pandas as pd
import numpy as np
from scipy import stats

# Load results
df = pd.read_csv('monte_carlo_quick_test/results.csv')

def compute_statistics(data, metric='ise', confidence=0.95):
    """Compute mean, std, and confidence interval."""
    mean = data[metric].mean()
    std = data[metric].std()
    n = len(data)
    se = std / np.sqrt(n)  # Standard error

    # Confidence interval (t-distribution)
    alpha = 1 - confidence
    t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
    ci_lower = mean - t_critical * se
    ci_upper = mean + t_critical * se

    return {
        'mean': mean,
        'std': std,
        'se': se,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'n': n
    }

# Compute for each controller
for controller in df['controller'].unique():
    data = df[df['controller'] == controller]
    stats_ise = compute_statistics(data, metric='ise')

    print(f"\\n{controller}:")
    print(f"  ISE: {stats_ise['mean']:.4f} ± {stats_ise['std']:.4f}")
    print(f"  95% CI: [{stats_ise['ci_lower']:.4f}, {stats_ise['ci_upper']:.4f}]")
    print(f"  Samples: {stats_ise['n']}")