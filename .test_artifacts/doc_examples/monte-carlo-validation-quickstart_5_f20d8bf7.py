# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 5
# Runnable: True
# Hash: f20d8bf7

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('monte_carlo_quick_test/results.csv')

# Compute statistics for each controller
controllers = df['controller'].unique()
stats_data = []

for ctrl in controllers:
    data = df[df['controller'] == ctrl]['ise'].values
    mean = data.mean()
    ci = stats.t.interval(0.95, len(data)-1,
                           loc=mean,
                           scale=stats.sem(data))
    stats_data.append({
        'controller': ctrl,
        'mean': mean,
        'ci_lower': ci[0],
        'ci_upper': ci[1]
    })

stats_df = pd.DataFrame(stats_data)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(controllers))
means = stats_df['mean'].values
ci_errors = np.array([stats_df['mean'] - stats_df['ci_lower'],
                       stats_df['ci_upper'] - stats_df['mean']])

ax.bar(x, means, alpha=0.7, color=['blue', 'orange'])
ax.errorbar(x, means, yerr=ci_errors, fmt='none', ecolor='black',
             capsize=5, capthick=2, label='95% CI')

ax.set_xlabel('Controller')
ax.set_ylabel('ISE (Integral Squared Error)')
ax.set_title('Controller Performance Comparison\\n(N=10 trials, 95% confidence intervals)')
ax.set_xticks(x)
ax.set_xticklabels(controllers, rotation=15)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_quick_test/performance_comparison.png', dpi=150)
print("\\nPlot saved: monte_carlo_quick_test/performance_comparison.png")