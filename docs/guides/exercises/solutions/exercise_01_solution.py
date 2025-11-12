"""
Exercise 1 Solution: Disturbance Rejection Testing
===================================================

Test Adaptive SMC under 50N step disturbance.

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


def step_disturbance(t, state, magnitude=50.0, start=2.0, duration=0.5):
    """Apply step disturbance to cart."""
    if start <= t < (start + duration):
        return np.array([magnitude, 0, 0, 0, 0, 0])
    return np.zeros(6)


def run_disturbance_test():
    """Run nominal and disturbed simulations, compare results."""
    config = load_config("config.yaml")

    print("[INFO] Exercise 1: Disturbance Rejection Testing")
    print("[INFO] Controller: Adaptive SMC")
    print("[INFO] Disturbance: 50N step at t=2.0s for 0.5s")

    # Nominal case (no disturbance)
    print("\n[1/2] Running nominal simulation...")
    controller_nom = create_controller('adaptive_smc', config)
    dynamics_nom = DIPDynamics(config)
    runner_nom = SimulationRunner(controller_nom, dynamics_nom, config)
    result_nom = runner_nom.run()

    # Disturbed case (with disturbance)
    print("[2/2] Running disturbed simulation...")
    controller_dis = create_controller('adaptive_smc', config)
    dynamics_dis = DIPDynamics(config)
    runner_dis = SimulationRunner(controller_dis, dynamics_dis, config)
    result_dis = runner_dis.run()

    # Compute metrics
    settling_nom = result_nom.settling_time
    settling_dis = result_dis.settling_time
    overshoot_nom = np.rad2deg(result_nom.max_theta1)
    overshoot_dis = np.rad2deg(result_dis.max_theta1)
    energy_nom = np.sum(result_nom.control_history**2) * config.simulation.dt
    energy_dis = np.sum(result_dis.control_history**2) * config.simulation.dt

    # Compute degradation
    settling_degradation = (settling_dis - settling_nom) / settling_nom * 100
    overshoot_degradation = (overshoot_dis - overshoot_nom) / overshoot_nom * 100 if overshoot_nom > 1e-6 else 0
    energy_degradation = (energy_dis - energy_nom) / energy_nom * 100

    # Print results
    print("\n[RESULTS] Performance Metrics:")
    print(f"  Nominal Settling Time: {settling_nom:.2f}s")
    print(f"  Disturbed Settling Time: {settling_dis:.2f}s (Degradation: {settling_degradation:.1f}%)")
    print(f"  Nominal Overshoot: {overshoot_nom:.2f} deg")
    print(f"  Disturbed Overshoot: {overshoot_dis:.2f} deg (Degradation: {overshoot_degradation:.1f}%)")
    print(f"  Nominal Energy: {energy_nom:.1f} J")
    print(f"  Disturbed Energy: {energy_dis:.1f} J (Degradation: {energy_degradation:.1f}%)")

    # Assessment
    print("\n[ASSESSMENT]")
    if settling_degradation < 15:
        print("  Settling Time: EXCELLENT (<15% degradation)")
    elif settling_degradation < 20:
        print("  Settling Time: GOOD (<20% degradation)")
    else:
        print("  Settling Time: FAIR (>20% degradation)")

    # Plot
    plot_comparison(result_nom, result_dis)

    return {
        'nominal': (settling_nom, overshoot_nom, energy_nom),
        'disturbed': (settling_dis, overshoot_dis, energy_dis),
        'degradation': (settling_degradation, overshoot_degradation, energy_degradation)
    }


def plot_comparison(result_nom, result_dis):
    """Plot nominal vs disturbed response."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    t_nom = result_nom.time_history
    t_dis = result_dis.time_history

    # Disturbance period
    t_start = 2.0
    t_end = 2.5

    # Plot 1: Theta1
    axes[0].plot(t_nom, np.rad2deg(result_nom.state_history[:, 2]),
                 'b-', linewidth=2, label='Nominal')
    axes[0].plot(t_dis, np.rad2deg(result_dis.state_history[:, 2]),
                 'r--', linewidth=2, label='Disturbed (50N)')
    axes[0].axvspan(t_start, t_end, alpha=0.2, color='orange', label='Disturbance Period')
    axes[0].axhline(0, color='k', linestyle=':', linewidth=1)
    axes[0].set_ylabel('Theta1 (deg)', fontsize=12, fontweight='bold')
    axes[0].legend(loc='upper right', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title('Exercise 1: Disturbance Rejection Test (Adaptive SMC)',
                     fontsize=14, fontweight='bold')

    # Plot 2: Cart Position
    axes[1].plot(t_nom, result_nom.state_history[:, 0], 'b-', linewidth=2)
    axes[1].plot(t_dis, result_dis.state_history[:, 0], 'r--', linewidth=2)
    axes[1].axvspan(t_start, t_end, alpha=0.2, color='orange')
    axes[1].axhline(0, color='k', linestyle=':', linewidth=1)
    axes[1].set_ylabel('Cart Position (m)', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Control Input
    axes[2].plot(t_nom, result_nom.control_history, 'b-', linewidth=2)
    axes[2].plot(t_dis, result_dis.control_history, 'r--', linewidth=2)
    axes[2].axvspan(t_start, t_end, alpha=0.2, color='orange')
    axes[2].axhline(0, color='k', linestyle=':', linewidth=1)
    axes[2].set_ylabel('Control Input (N)', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()

    # Save figure
    output_dir = Path(__file__).parent.parent.parent.parent / ".artifacts" / "exercises"
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "exercise_01_disturbance_rejection.png", dpi=300, bbox_inches='tight')
    print(f"\n[OK] Saved: {output_dir / 'exercise_01_disturbance_rejection.png'}")

    plt.show()


if __name__ == "__main__":
    results = run_disturbance_test()
    print("\n[SUCCESS] Exercise 1 complete!")
