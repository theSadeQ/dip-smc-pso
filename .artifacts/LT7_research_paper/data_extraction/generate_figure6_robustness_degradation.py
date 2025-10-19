#!/usr/bin/env python3
"""
Generate Figure 6: Robustness Degradation Analysis (2-column span)

Shows generalization failure when MT-6 optimized parameters are tested
under MT-7 challenging conditions (±0.3 rad vs ±0.05 rad).

Two subplots:
  A) Chattering distribution comparison
  B) Success rate breakdown

Input:
    - benchmarks/MT7_robustness_summary.json
    - benchmarks/MT6_adaptive_summary.json (for comparison)

Output:
    - .artifacts/LT7_research_paper/figures/fig6_robustness_degradation.pdf (300 DPI)
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent.parent
FIGURES_DIR = REPO_ROOT / ".artifacts" / "LT7_research_paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# IEEE format settings (2-column span)
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.figsize': (7.0, 2.5),  # Two-column span
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'lines.linewidth': 1.5,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.5,
})

def load_robustness_data():
    """Load MT-6 and MT-7 robustness data."""

    # Load MT-6 adaptive results
    mt6_path = REPO_ROOT / "benchmarks" / "MT6_adaptive_summary.json"
    with open(mt6_path, 'r') as f:
        mt6_data = json.load(f)

    # Load MT-7 robustness results
    mt7_path = REPO_ROOT / "benchmarks" / "MT7_robustness_summary.json"
    with open(mt7_path, 'r') as f:
        mt7_data = json.load(f)

    print(f"[OK] Loaded MT-6 adaptive results")
    print(f"[OK] Loaded MT-7 robustness results")

    return mt6_data, mt7_data

def create_robustness_degradation_plot(mt6_data, mt7_data):
    """Create 2-subplot figure showing robustness degradation."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.5))

    # Extract statistics
    mt6_chattering_mean = mt6_data['statistics']['chattering_index']['mean']
    mt6_chattering_std = mt6_data['statistics']['chattering_index']['std']
    mt6_success_rate = mt6_data['configuration']['success_rate']

    mt7_chattering_mean = mt7_data['global_statistics']['mean']
    mt7_chattering_std = mt7_data['global_statistics']['std']
    mt7_success_rate = (mt7_data['global_statistics']['n_total'] / 500) * 100  # 49/500

    # Subplot A: Chattering distribution comparison
    categories = ['MT-6\n(±0.05 rad)', 'MT-7\n(±0.3 rad)']
    means = [mt6_chattering_mean, mt7_chattering_mean]
    stds = [mt6_chattering_std, mt7_chattering_std]

    x_pos = np.arange(len(categories))
    bars = ax1.bar(x_pos, means, yerr=stds, capsize=5,
                   color=['lightblue', 'salmon'],
                   edgecolor='black', linewidth=0.8,
                   error_kw={'linewidth': 1.0, 'ecolor': 'black'})

    # Add degradation annotation
    degradation = mt7_chattering_mean / mt6_chattering_mean
    ax1.annotate(f'{degradation:.1f}× worse',
                 xy=(1, mt7_chattering_mean), xytext=(0.5, mt7_chattering_mean * 0.7),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                 fontsize=10, color='red', weight='bold')

    ax1.set_ylabel('Chattering Index', fontsize=10, weight='bold')
    ax1.set_xlabel('Test Condition', fontsize=10, weight='bold')
    ax1.set_title('(A) Chattering Degradation', fontsize=10, weight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories)
    ax1.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)

    # Subplot B: Success rate comparison
    success_rates = [mt6_success_rate, mt7_success_rate]
    colors_success = ['green' if sr >= 50 else 'red' for sr in success_rates]

    bars2 = ax2.bar(x_pos, success_rates, color=colors_success, alpha=0.7,
                    edgecolor='black', linewidth=0.8)

    # Add percentage labels on bars
    for i, (bar, rate) in enumerate(zip(bars2, success_rates)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=9, weight='bold')

    # Add failure annotation
    ax2.annotate(f'{mt6_success_rate - mt7_success_rate:.1f}% drop',
                 xy=(1, mt7_success_rate), xytext=(0.5, 50),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                 fontsize=10, color='red', weight='bold')

    ax2.set_ylabel('Success Rate (%)', fontsize=10, weight='bold')
    ax2.set_xlabel('Test Condition', fontsize=10, weight='bold')
    ax2.set_title('(B) Success Rate Degradation', fontsize=10, weight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(categories)
    ax2.set_ylim([0, 110])
    ax2.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)

    plt.tight_layout()

    print(f"\nRobustness Statistics:")
    print(f"  MT-6 Chattering: {mt6_chattering_mean:.2f} ± {mt6_chattering_std:.2f}")
    print(f"  MT-7 Chattering: {mt7_chattering_mean:.2f} ± {mt7_chattering_std:.2f}")
    print(f"  Degradation: {degradation:.1f}×")
    print(f"  MT-6 Success Rate: {mt6_success_rate:.1f}%")
    print(f"  MT-7 Success Rate: {mt7_success_rate:.1f}%")
    print(f"  Success Rate Drop: {mt6_success_rate - mt7_success_rate:.1f}%")

    return fig

def main():
    """Generate Figure 6: Robustness degradation."""

    print("="*60)
    print("Figure 6: Robustness Degradation Analysis")
    print("="*60)

    # Load data
    mt6_data, mt7_data = load_robustness_data()

    # Create plot
    fig = create_robustness_degradation_plot(mt6_data, mt7_data)

    # Save figure
    pdf_path = FIGURES_DIR / "fig6_robustness_degradation.pdf"
    png_path = FIGURES_DIR / "fig6_robustness_degradation.png"

    fig.savefig(pdf_path, format='pdf', dpi=300, bbox_inches='tight')
    fig.savefig(png_path, format='png', dpi=300, bbox_inches='tight')

    print(f"\n[OK] Saved PDF: {pdf_path}")
    print(f"[OK] Saved PNG: {png_path}")
    print(f"\nFigure ready for LaTeX inclusion (2-column span):")
    print(f"  \\begin{{figure*}}[t]")
    print(f"  \\includegraphics[width=\\textwidth]{{{pdf_path.name}}}")
    print(f"  \\caption{{...}}")
    print(f"  \\end{{figure*}}")

    plt.close(fig)

if __name__ == "__main__":
    main()
