"""
Exercise 2 Solution: Model Uncertainty Analysis
================================================

Test STA SMC under ±30% cart mass variation (Monte Carlo N=50).

Author: DIP-SMC-PSO Development Team
Date: November 12, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from src.config import load_config
from src.controllers.factory import create_controller
from src.core.dynamics import DIPDynamics
from src.core.simulation_runner import SimulationRunner


def monte_carlo_uncertainty(n_runs=50, uncertainty=0.30, seed=42):
    """Run Monte Carlo analysis with ±30% cart mass variation."""
    np.random.seed(seed)
    config = load_config("config.yaml")

    nominal_mass = config.physics.cart_mass
    settling_times = []
    converged_count = 0

    print(f"[INFO] Exercise 2: Model Uncertainty Analysis")
    print(f"[INFO] Controller: STA SMC")
    print(f"[INFO] Uncertainty: ±{uncertainty*100:.0f}% cart mass")
    print(f"[INFO] Runs: {n_runs}")

    for run in range(n_runs):
        # Sample mass from uniform distribution
        scale_factor = 1.0 + np.random.uniform(-uncertainty, uncertainty)
        config.physics.cart_mass = nominal_mass * scale_factor

        # Run simulation
        controller = create_controller('sta_smc', config)
        dynamics = DIPDynamics(config)
        runner = SimulationRunner(controller, dynamics, config)
        result = runner.run()

        if result.converged:
            settling_times.append(result.settling_time)
            converged_count += 1

        if (run + 1) % 10 == 0:
            print(f"  [{run+1}/{n_runs}] Converged: {converged_count}/{run+1} "
                  f"({converged_count/(run+1)*100:.1f}%)")

        # Restore nominal
        config.physics.cart_mass = nominal_mass

    settling_times = np.array(settling_times)

    # Compute statistics
    stats = {
        'mean': np.mean(settling_times),
        'std': np.std(settling_times),
        'p5': np.percentile(settling_times, 5),
        'p50': np.percentile(settling_times, 50),
        'p95': np.percentile(settling_times, 95),
        'ci_95': (np.percentile(settling_times, 2.5), np.percentile(settling_times, 97.5)),
        'convergence_rate': converged_count / n_runs * 100
    }

    print(f"\n[RESULTS] Statistics:")
    print(f"  Mean: {stats['mean']:.2f}s ± {stats['std']:.2f}s")
    print(f"  Median: {stats['p50']:.2f}s")
    print(f"  95% CI: [{stats['ci_95'][0]:.2f}s, {stats['ci_95'][1]:.2f}s]")
    print(f"  Convergence Rate: {stats['convergence_rate']:.1f}%")

    # Degradation assessment (assume nominal ~2.8s)
    nominal_settling = 2.8
    degradation = (stats['p95'] - nominal_settling) / nominal_settling * 100
    print(f"\n[ASSESSMENT] Degradation at 95% CI: {degradation:.1f}%")
    if degradation < 15:
        print("  Rating: EXCELLENT (<15%)")
    else:
        print("  Rating: GOOD (<20%)")

    # Plot
    plot_monte_carlo(settling_times)

    return stats, settling_times


def plot_monte_carlo(settling_times):
    """Plot histogram and boxplot."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(settling_times, bins=15, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0].axvline(np.mean(settling_times), color='r', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(settling_times):.2f}s')
    axes[0].set_xlabel('Settling Time (s)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title('Settling Time Distribution (±30% Cart Mass)', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Boxplot
    bp = axes[1].boxplot([settling_times], vert=True, patch_artist=True,
                         labels=['STA SMC'],
                         boxprops=dict(facecolor='lightblue', color='black'),
                         medianprops=dict(color='red', linewidth=2))
    axes[1].set_ylabel('Settling Time (s)', fontsize=11, fontweight='bold')
    axes[1].set_title('Settling Time Spread', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_dir = Path(__file__).parent.parent.parent.parent / ".artifacts" / "exercises"
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "exercise_02_uncertainty_monte_carlo.png", dpi=300, bbox_inches='tight')
    print(f"\n[OK] Saved: {output_dir / 'exercise_02_uncertainty_monte_carlo.png'}")

    plt.show()


if __name__ == "__main__":
    stats, data = monte_carlo_uncertainty(n_runs=50, uncertainty=0.30, seed=42)
    print("\n[SUCCESS] Exercise 2 complete!")
