#!/usr/bin/env python3
"""
Generate Figure VI-2: Normality Validation for MT-6 Data

This script validates the normality assumption for chattering distributions
using Shapiro-Wilk tests and Q-Q plots. Normality is required for parametric
statistical tests (Welch's t-test) used in Chapter 6.

Panel (a): Q-Q plot for Fixed baseline (n=100)
Panel (b): Q-Q plot for Adaptive validation (n=100)

Statistical Tests:
- Shapiro-Wilk test: H0: data is normally distributed
- Significance level: α = 0.05
- Reject H0 if p < 0.05 (non-normal)
- Accept H0 if p >= 0.05 (approximately normal)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Set publication-quality defaults
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

print('=== NORMALITY VALIDATION ===\n')

# Load MT-6 data
fixed_df = pd.read_csv('benchmarks/MT6_fixed_baseline.csv')
adaptive_df = pd.read_csv('benchmarks/MT6_adaptive_validation.csv')

fixed_chat = fixed_df['chattering_index'].values
adaptive_chat = adaptive_df['chattering_index'].values

print(f'Data loaded:')
print(f'  Fixed baseline: n={len(fixed_chat)}')
print(f'  Adaptive validation: n={len(adaptive_chat)}')
print()

# Shapiro-Wilk test
print('Shapiro-Wilk Normality Test:')
print('  H0: Data is normally distributed')
print('  Significance level: α = 0.05')
print('  Decision: Reject H0 if p < 0.05\n')

# Fixed baseline
stat_fixed, p_fixed = stats.shapiro(fixed_chat)
print(f'Fixed Baseline:')
print(f'  W-statistic: {stat_fixed:.4f}')
print(f'  p-value:     {p_fixed:.4f}')
if p_fixed >= 0.05:
    print(f'  Decision:    Accept H0 (approximately normal)')
else:
    print(f'  Decision:    Reject H0 (non-normal)')
print()

# Adaptive validation
stat_adaptive, p_adaptive = stats.shapiro(adaptive_chat)
print(f'Adaptive Validation:')
print(f'  W-statistic: {stat_adaptive:.4f}')
print(f'  p-value:     {p_adaptive:.4f}')
if p_adaptive >= 0.05:
    print(f'  Decision:    Accept H0 (approximately normal)')
else:
    print(f'  Decision:    Reject H0 (non-normal)')
print()

# Additional normality metrics
print('Normality Metrics:')
print(f'Fixed Baseline:')
print(f'  Skewness:    {stats.skew(fixed_chat):.4f} (ideal: 0)')
print(f'  Kurtosis:    {stats.kurtosis(fixed_chat):.4f} (ideal: 0, excess)')
print()
print(f'Adaptive Validation:')
print(f'  Skewness:    {stats.skew(adaptive_chat):.4f} (ideal: 0)')
print(f'  Kurtosis:    {stats.kurtosis(adaptive_chat):.4f} (ideal: 0, excess)')
print()

# Create Q-Q plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3))

# Panel (a): Fixed baseline Q-Q plot
stats.probplot(fixed_chat, dist="norm", plot=ax1)
ax1.set_title('(a) Fixed Baseline')
ax1.set_xlabel('Theoretical Quantiles')
ax1.set_ylabel('Sample Quantiles')
ax1.grid(True, alpha=0.3)

# Add Shapiro-Wilk result as text
ax1.text(0.05, 0.95, f'W = {stat_fixed:.4f}\np = {p_fixed:.4f}',
         transform=ax1.transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Panel (b): Adaptive validation Q-Q plot
stats.probplot(adaptive_chat, dist="norm", plot=ax2)
ax2.set_title('(b) Adaptive Validation')
ax2.set_xlabel('Theoretical Quantiles')
ax2.set_ylabel('Sample Quantiles')
ax2.grid(True, alpha=0.3)

# Add Shapiro-Wilk result as text
ax2.text(0.05, 0.95, f'W = {stat_adaptive:.4f}\np = {p_adaptive:.4f}',
         transform=ax2.transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Tight layout and save
plt.tight_layout()

# Create output directories
Path('.artifacts/LT7_research_paper/figures').mkdir(parents=True, exist_ok=True)

# Save figure
pdf_path = '.artifacts/LT7_research_paper/figures/figure_vi2_normality.pdf'
png_path = '.artifacts/LT7_research_paper/figures/figure_vi2_normality.png'

plt.savefig(pdf_path, dpi=300, bbox_inches='tight')
plt.savefig(png_path, dpi=300, bbox_inches='tight')

print(f'=== FIGURE VI-2 SAVED ===')
print(f'PDF: {pdf_path}')
print(f'PNG: {png_path}')
print()

# Summary
print('Interpretation:')
if p_fixed >= 0.05 and p_adaptive >= 0.05:
    print('  - Both distributions approximately normal (p >= 0.05)')
    print('  - Parametric tests (Welch\'s t-test) are valid')
    print('  - Q-Q plots show good agreement with theoretical normal quantiles')
elif p_fixed >= 0.05:
    print('  - Fixed baseline approximately normal (p >= 0.05)')
    print('  - Adaptive validation shows deviation from normality (p < 0.05)')
    print('  - Consider non-parametric tests (Mann-Whitney U) as alternative')
elif p_adaptive >= 0.05:
    print('  - Adaptive validation approximately normal (p >= 0.05)')
    print('  - Fixed baseline shows deviation from normality (p < 0.05)')
    print('  - Consider non-parametric tests (Mann-Whitney U) as alternative')
else:
    print('  - Both distributions deviate from normality (p < 0.05)')
    print('  - Non-parametric tests (Mann-Whitney U) recommended')
    print('  - However, t-test is robust to moderate deviations with n=100')

print()
print('Technical Note:')
print('  - Shapiro-Wilk is sensitive to large sample sizes (n>50)')
print('  - Q-Q plots provide visual assessment of normality')
print('  - Central Limit Theorem ensures approximate normality for means with n=100')
print('  - Welch\'s t-test is robust to moderate departures from normality')
print()
print('=== VALIDATION COMPLETE ===')
