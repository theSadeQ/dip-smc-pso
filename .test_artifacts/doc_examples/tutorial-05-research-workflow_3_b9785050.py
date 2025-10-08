# Example from: docs\guides\tutorials\tutorial-05-research-workflow.md
# Index: 3
# Runnable: True
# Hash: b9785050

#!/usr/bin/env python
"""Generate publication-quality figures."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
sns.set_context("paper", font_scale=1.5)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'serif'

# Load data
df = pd.read_csv('experiments/robustness_study/results/monte_carlo_results.csv')

# Figure 1: Box plots - ISE across scenarios
fig, ax = plt.subplots()
df_pivot = df.pivot_table(values='ise', index='scenario', columns='controller')

df_pivot.plot(kind='bar', ax=ax, color=['tab:blue', 'tab:orange'])
ax.set_ylabel('ISE')
ax.set_xlabel('Parameter Scenario')
ax.set_title('Controller Performance Under Parameter Uncertainty')
ax.legend(['Classical SMC', 'Hybrid Adaptive STA-SMC'])
ax.grid(axis='y')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('experiments/robustness_study/figures/fig1_ise_comparison.pdf', dpi=300)
plt.savefig('experiments/robustness_study/figures/fig1_ise_comparison.png', dpi=300)
print("Saved: fig1_ise_comparison.pdf")

# Figure 2: Violin plots - Distribution comparison
fig, ax = plt.subplots()
sns.violinplot(data=df, x='scenario', y='ise', hue='controller', split=True, ax=ax)
ax.set_ylabel('ISE')
ax.set_xlabel('Parameter Scenario')
ax.set_title('ISE Distribution Comparison')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('experiments/robustness_study/figures/fig2_distribution.pdf', dpi=300)
print("Saved: fig2_distribution.pdf")

# Figure 3: Robustness index comparison
robustness = df.groupby(['controller', 'trial']).agg({'ise': 'std'}).reset_index()

fig, ax = plt.subplots()
sns.boxplot(data=robustness, x='controller', y='ise', ax=ax)
ax.set_ylabel('Robustness Index\n(ISE std dev across scenarios)')
ax.set_xlabel('Controller Type')
ax.set_title('Robustness Comparison (Lower is Better)')
ax.set_xticklabels(['Classical SMC', 'Hybrid Adaptive STA-SMC'])
plt.tight_layout()
plt.savefig('experiments/robustness_study/figures/fig3_robustness_index.pdf', dpi=300)
print("Saved: fig3_robustness_index.pdf")

print("\nAll figures saved to: experiments/robustness_study/figures/")