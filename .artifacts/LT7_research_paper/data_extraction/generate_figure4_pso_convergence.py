#!/usr/bin/env python3
"""
Generate Figure 4: PSO Convergence Curve

Shows fitness function convergence during PSO optimization of adaptive
boundary layer parameters (MT-6).

Input:
    - benchmarks/MT6_adaptive_optimization.csv

Output:
    - .artifacts/LT7_research_paper/figures/fig4_pso_convergence.pdf (300 DPI)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent.parent
FIGURES_DIR = REPO_ROOT / ".artifacts" / "LT7_research_paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# IEEE format settings
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.figsize': (3.5, 2.5),  # Single column
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'lines.linewidth': 1.5,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.5,
})

def load_pso_convergence():
    """Load PSO convergence data."""

    csv_path = REPO_ROOT / "benchmarks" / "MT6_adaptive_optimization.csv"
    df = pd.read_csv(csv_path)

    print(f"[OK] Loaded PSO optimization data: {len(df)} iterations")
    print(f"    Columns: {list(df.columns)}")

    return df

def create_pso_convergence_plot(df):
    """Create PSO convergence plot."""

    fig, ax = plt.subplots(figsize=(3.5, 2.5))

    # Plot best fitness over iterations
    ax.plot(df['iteration'], df['best_fitness'],
            color='blue', linewidth=1.5, label='Best Fitness')

    # Mark final optimum
    final_iter = df['iteration'].iloc[-1]
    final_fitness = df['best_fitness'].iloc[-1]
    ax.plot(final_iter, final_fitness, 'r*', markersize=10,
            label=f'Optimum: {final_fitness:.4f}', zorder=5)

    # Labels and formatting
    ax.set_xlabel('Iteration', fontsize=10, weight='bold')
    ax.set_ylabel('Best Fitness', fontsize=10, weight='bold')
    ax.set_title('PSO Convergence for Adaptive Boundary Layer',
                 fontsize=10, weight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.legend(loc='upper right', framealpha=0.9)

    # Set y-axis to show improvement clearly
    ax.set_ylim([final_fitness * 0.95, df['best_fitness'].max() * 1.05])

    plt.tight_layout()

    print(f"\nConvergence Stats:")
    print(f"  Initial fitness: {df['best_fitness'].iloc[0]:.4f}")
    print(f"  Final fitness: {final_fitness:.4f}")
    print(f"  Improvement: {(df['best_fitness'].iloc[0] - final_fitness) / df['best_fitness'].iloc[0] * 100:.1f}%")
    print(f"  Total iterations: {final_iter}")

    return fig

def main():
    """Generate Figure 4: PSO convergence."""

    print("="*60)
    print("Figure 4: PSO Convergence Curve")
    print("="*60)

    # Load data
    df = load_pso_convergence()

    # Create plot
    fig = create_pso_convergence_plot(df)

    # Save figure
    pdf_path = FIGURES_DIR / "fig4_pso_convergence.pdf"
    png_path = FIGURES_DIR / "fig4_pso_convergence.png"

    fig.savefig(pdf_path, format='pdf', dpi=300, bbox_inches='tight')
    fig.savefig(png_path, format='png', dpi=300, bbox_inches='tight')

    print(f"\n[OK] Saved PDF: {pdf_path}")
    print(f"[OK] Saved PNG: {png_path}")
    print(f"\nFigure ready for LaTeX inclusion:")
    print(f"  \\includegraphics[width=\\columnwidth]{{{pdf_path.name}}}")

    plt.close(fig)

if __name__ == "__main__":
    main()
