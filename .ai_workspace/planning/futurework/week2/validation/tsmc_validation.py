#======================================================================================\\
#================ .ai/planning/research/week2/validation/tsmc_validation.py ===========\\
#======================================================================================\\

"""
Terminal SMC Validation Script

Compares Terminal SMC against Classical SMC to validate:
1. Finite-time convergence (30-50% faster settling)
2. Reduced chattering (smoother control)
3. Robustness to parameter variations

Based on MT-1.5: Terminal SMC validation and documentation (1h)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.controllers.factory import create_controller
from src.core.dynamics import DoublePendulumDynamics
from src.config import load_config

def run_comparison_simulation(
    controller_type: str,
    initial_state: np.ndarray,
    duration: float = 5.0,
    dt: float = 0.001
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run simulation with specified controller."""

    # Load config and create controller
    config = load_config('config.yaml')
    controller = create_controller(controller_type)

    # Create dynamics
    dynamics = DoublePendulumDynamics(
        m0=config.physics.cart_mass,
        m1=config.physics.pendulum1_mass,
        m2=config.physics.pendulum2_mass,
        L1=config.physics.pendulum1_length,
        L2=config.physics.pendulum2_length,
        g=config.physics.gravity,
        b0=config.physics.cart_friction,
        b1=config.physics.joint1_friction,
        b2=config.physics.joint2_friction
    )

    # Initialize
    steps = int(duration / dt)
    time = np.zeros(steps)
    states = np.zeros((steps, 6))
    controls = np.zeros(steps)

    state = initial_state.copy()
    history = controller.initialize_history()

    # Simulate
    for i in range(steps):
        time[i] = i * dt
        states[i] = state

        # Compute control
        output = controller.compute_control(state, 0.0, history)
        u = output.u
        controls[i] = u

        # Update history
        if hasattr(output, 'history') and output.history:
            history.update(output.history)

        # Dynamics step (simple Euler for validation)
        x_dot = dynamics.compute_dynamics(state, u)
        state = state + x_dot * dt

    return time, states, controls


def compute_performance_metrics(
    time: np.ndarray,
    states: np.ndarray,
    controls: np.ndarray
) -> Dict[str, float]:
    """Compute performance metrics for validation."""

    # Settling time (2% criterion for both angles)
    settling_threshold = 0.02  # 2% of initial error
    theta1_settled = np.where(np.abs(states[:, 1]) < settling_threshold)[0]
    theta2_settled = np.where(np.abs(states[:, 2]) < settling_threshold)[0]

    t_settle_theta1 = time[theta1_settled[0]] if len(theta1_settled) > 0 else time[-1]
    t_settle_theta2 = time[theta2_settled[0]] if len(theta2_settled) > 0 else time[-1]
    t_settle = max(t_settle_theta1, t_settle_theta2)

    # ISE (Integral Square Error)
    dt = time[1] - time[0]
    ise = np.sum(states[:, 1]**2 + states[:, 2]**2) * dt

    # Control effort
    control_effort = np.sum(np.abs(controls)) * dt

    # Chattering metric (control variation)
    control_variation = np.sum(np.abs(np.diff(controls)))

    # RMS error (after transient, last 2 seconds)
    steady_start = int((time[-1] - 2.0) / dt)
    rms_error = np.sqrt(np.mean(states[steady_start:, 1]**2 + states[steady_start:, 2]**2))

    return {
        'settling_time': t_settle,
        'ise': ise,
        'control_effort': control_effort,
        'chattering': control_variation,
        'rms_error': rms_error
    }


def main():
    """Main validation routine."""

    print("=" * 80)
    print("Terminal SMC Validation - MT-1.5")
    print("=" * 80)
    print()

    # Test conditions
    initial_state = np.array([0.0, 0.2, -0.15, 0.0, 0.0, 0.0])  # Significant disturbance
    duration = 5.0
    dt = 0.001

    print(f"Test Configuration:")
    print(f"  Initial state: theta1={initial_state[1]:.3f}, theta2={initial_state[2]:.3f}")
    print(f"  Duration: {duration}s")
    print(f"  Time step: {dt}s")
    print()

    # Run simulations
    print("[1/2] Running Classical SMC simulation...")
    t_classical, states_classical, controls_classical = run_comparison_simulation(
        'classical_smc', initial_state, duration, dt
    )
    metrics_classical = compute_performance_metrics(t_classical, states_classical, controls_classical)
    print("      [OK] Classical SMC complete")

    print("[2/2] Running Terminal SMC simulation...")
    t_tsmc, states_tsmc, controls_tsmc = run_comparison_simulation(
        'tsmc_smc', initial_state, duration, dt
    )
    metrics_tsmc = compute_performance_metrics(t_tsmc, states_tsmc, controls_tsmc)
    print("      [OK] Terminal SMC complete")
    print()

    # Display results
    print("=" * 80)
    print("Performance Comparison")
    print("=" * 80)
    print()

    print(f"{'Metric':<25} {'Classical SMC':>15} {'Terminal SMC':>15} {'Improvement':>15}")
    print("-" * 80)

    for metric_name in ['settling_time', 'ise', 'control_effort', 'chattering', 'rms_error']:
        classical_val = metrics_classical[metric_name]
        tsmc_val = metrics_tsmc[metric_name]
        improvement = (classical_val - tsmc_val) / classical_val * 100

        print(f"{metric_name.replace('_', ' ').title():<25} {classical_val:>15.4f} {tsmc_val:>15.4f} {improvement:>14.1f}%")

    print()

    # Validation checks
    print("=" * 80)
    print("Validation Checks")
    print("=" * 80)
    print()

    settling_improvement = (metrics_classical['settling_time'] - metrics_tsmc['settling_time']) / metrics_classical['settling_time'] * 100
    chattering_reduction = (metrics_classical['chattering'] - metrics_tsmc['chattering']) / metrics_classical['chattering'] * 100

    checks = [
        ("Finite-time convergence (30-50% faster)", settling_improvement >= 30.0, f"{settling_improvement:.1f}%"),
        ("Reduced chattering (any improvement)", chattering_reduction > 0.0, f"{chattering_reduction:.1f}%"),
        ("Lower ISE (better tracking)", metrics_tsmc['ise'] < metrics_classical['ise'], "Yes" if metrics_tsmc['ise'] < metrics_classical['ise'] else "No"),
        ("Bounded control effort", metrics_tsmc['control_effort'] < 1000.0, f"{metrics_tsmc['control_effort']:.1f}")
    ]

    all_passed = True
    for check_name, passed, value in checks:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {check_name}: {value}")
        all_passed = all_passed and passed

    print()

    # Generate plots
    print("=" * 80)
    print("Generating Comparison Plots")
    print("=" * 80)
    print()

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle('Terminal SMC vs Classical SMC Performance Comparison', fontsize=14, fontweight='bold')

    # Theta 1
    axes[0, 0].plot(t_classical, states_classical[:, 1], 'b-', label='Classical SMC', linewidth=1.5)
    axes[0, 0].plot(t_tsmc, states_tsmc[:, 1], 'r--', label='Terminal SMC', linewidth=1.5)
    axes[0, 0].axhline(0.02, color='k', linestyle=':', linewidth=0.8, label='2% threshold')
    axes[0, 0].axhline(-0.02, color='k', linestyle=':', linewidth=0.8)
    axes[0, 0].set_ylabel('Theta 1 (rad)')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Theta 2
    axes[0, 1].plot(t_classical, states_classical[:, 2], 'b-', label='Classical SMC', linewidth=1.5)
    axes[0, 1].plot(t_tsmc, states_tsmc[:, 2], 'r--', label='Terminal SMC', linewidth=1.5)
    axes[0, 1].axhline(0.02, color='k', linestyle=':', linewidth=0.8, label='2% threshold')
    axes[0, 1].axhline(-0.02, color='k', linestyle=':', linewidth=0.8)
    axes[0, 1].set_ylabel('Theta 2 (rad)')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Control signals
    axes[1, 0].plot(t_classical, controls_classical, 'b-', label='Classical SMC', linewidth=1.5)
    axes[1, 0].plot(t_tsmc, controls_tsmc, 'r--', label='Terminal SMC', linewidth=1.5)
    axes[1, 0].set_ylabel('Control (N)')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Control variation (chattering)
    window = 100
    classical_variation = np.abs(np.diff(controls_classical))
    tsmc_variation = np.abs(np.diff(controls_tsmc))
    classical_smooth = np.convolve(classical_variation, np.ones(window)/window, mode='same')
    tsmc_smooth = np.convolve(tsmc_variation, np.ones(window)/window, mode='same')

    axes[1, 1].plot(t_classical[:-1], classical_smooth, 'b-', label='Classical SMC', linewidth=1.5)
    axes[1, 1].plot(t_tsmc[:-1], tsmc_smooth, 'r--', label='Terminal SMC', linewidth=1.5)
    axes[1, 1].set_ylabel('Control Variation (N/step)')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_title('Chattering Comparison (100-sample moving avg)')

    # Phase portrait theta1
    axes[2, 0].plot(states_classical[:, 1], states_classical[:, 4], 'b-', label='Classical SMC', linewidth=1.5, alpha=0.7)
    axes[2, 0].plot(states_tsmc[:, 1], states_tsmc[:, 4], 'r--', label='Terminal SMC', linewidth=1.5, alpha=0.7)
    axes[2, 0].plot(states_classical[0, 1], states_classical[0, 4], 'go', markersize=8, label='Start')
    axes[2, 0].plot(0, 0, 'k*', markersize=12, label='Origin')
    axes[2, 0].set_xlabel('Theta 1 (rad)')
    axes[2, 0].set_ylabel('Theta 1 dot (rad/s)')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)
    axes[2, 0].set_title('Phase Portrait (Pendulum 1)')

    # Phase portrait theta2
    axes[2, 1].plot(states_classical[:, 2], states_classical[:, 5], 'b-', label='Classical SMC', linewidth=1.5, alpha=0.7)
    axes[2, 1].plot(states_tsmc[:, 2], states_tsmc[:, 5], 'r--', label='Terminal SMC', linewidth=1.5, alpha=0.7)
    axes[2, 1].plot(states_classical[0, 2], states_classical[0, 5], 'go', markersize=8, label='Start')
    axes[2, 1].plot(0, 0, 'k*', markersize=12, label='Origin')
    axes[2, 1].set_xlabel('Theta 2 (rad)')
    axes[2, 1].set_ylabel('Theta 2 dot (rad/s)')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    axes[2, 1].set_title('Phase Portrait (Pendulum 2)')

    plt.tight_layout()

    # Save plot
    output_path = project_root / '.ai' / 'planning' / 'research' / 'week2' / 'validation' / 'tsmc_comparison.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Plot saved: {output_path.relative_to(project_root)}")
    print()

    # Final summary
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)
    print()

    if all_passed:
        print("[SUCCESS] All validation checks passed!")
        print()
        print("Terminal SMC demonstrates:")
        print(f"  - {settling_improvement:.1f}% faster convergence than Classical SMC")
        print(f"  - {chattering_reduction:.1f}% reduction in chattering")
        print(f"  - Superior tracking performance (lower ISE)")
        print()
        return 0
    else:
        print("[WARNING] Some validation checks failed.")
        print("Review the detailed metrics above.")
        print()
        return 1


if __name__ == '__main__':
    exit(main())
