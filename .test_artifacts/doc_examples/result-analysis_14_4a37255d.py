# Example from: docs\guides\how-to\result-analysis.md
# Index: 14
# Runnable: True
# Hash: 4a37255d

import pandas as pd

# Load metrics from all controllers
metrics_data = []
for ctrl, label in zip(controllers, labels):
    with open(f'results_{ctrl}.json') as f:
        data = json.load(f)
        metrics_data.append({
            'Controller': label,
            'ISE': data['metrics']['ise'],
            'Settling Time': data['metrics']['settling_time'],
            'Overshoot': data['metrics']['overshoot']
        })

df = pd.DataFrame(metrics_data)

# Create bar chart
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# ISE
axes[0].bar(df['Controller'], df['ISE'], color=colors)
axes[0].set_ylabel('ISE', fontsize=12)
axes[0].set_title('Tracking Accuracy (ISE)', fontsize=14)
axes[0].grid(axis='y', alpha=0.3)

# Settling Time
axes[1].bar(df['Controller'], df['Settling Time'], color=colors)
axes[1].set_ylabel('Time (s)', fontsize=12)
axes[1].set_title('Settling Time', fontsize=14)
axes[1].grid(axis='y', alpha=0.3)

# Overshoot
axes[2].bar(df['Controller'], df['Overshoot'], color=colors)
axes[2].set_ylabel('Overshoot (%)', fontsize=12)
axes[2].set_title('Peak Overshoot', fontsize=14)
axes[2].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('metrics_comparison.png', dpi=300)
plt.show()