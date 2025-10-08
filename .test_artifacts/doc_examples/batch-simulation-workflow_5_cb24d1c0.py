# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 5
# Runnable: True
# Hash: cb24d1c0

import numpy as np
import matplotlib.pyplot as plt

# From Monte Carlo results above
final_states = results[:, -1, :]

# Compute statistics
def analyze_monte_carlo(final_states, state_names):
    stats = {}
    for i, name in enumerate(state_names):
        values = final_states[:, i]
        stats[name] = {
            'mean': values.mean(),
            'std': values.std(),
            'min': values.min(),
            'max': values.max(),
            'p95': np.percentile(values, 95),
            'p05': np.percentile(values, 5)
        }
    return stats

state_names = ['x', 'theta1', 'theta2', 'xdot', 'theta1dot', 'theta2dot']
stats = analyze_monte_carlo(final_states, state_names)

# Print summary
for name, s in stats.items():
    print(f"{name:10s}: {s['mean']:8.4f} ± {s['std']:.4f}  "
          f"[{s['min']:8.4f}, {s['max']:8.4f}]  "
          f"(5%-95%: [{s['p05']:7.4f}, {s['p95']:7.4f}])")

# Plot distributions
fig, axes = plt.subplots(2, 3, figsize=(12, 6))
axes = axes.flat

for i, name in enumerate(state_names):
    axes[i].hist(final_states[:, i], bins=50, alpha=0.7, edgecolor='black')
    axes[i].set_xlabel(name)
    axes[i].set_ylabel('Count')
    axes[i].axvline(stats[name]['mean'], color='red', linestyle='--', label='Mean')
    axes[i].legend()

plt.tight_layout()
plt.savefig('monte_carlo_distributions.png', dpi=150)