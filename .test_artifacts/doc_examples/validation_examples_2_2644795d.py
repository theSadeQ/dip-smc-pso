# Example from: docs\validation\validation_examples.md
# Index: 2
# Runnable: False
# Hash: 2644795d

"""
Monte Carlo Stability Validation for Sliding Mode Controller
============================================================

This script validates controller stability under parameter uncertainty
using Latin Hypercube Sampling for efficient coverage.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.analysis.validation.monte_carlo import MonteCarloConfig, MonteCarloAnalyzer
from src.controllers.smc_classical import ClassicalSMC  # Example controller
from src.simulation.double_inverted_pendulum import DoubleInvertedPendulum

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def simulate_stability_check(params: dict, **kwargs) -> dict:
    """
    Simulate controller for given parameter set.

    Parameters
    ----------
    params : dict
        System parameters: {'mass': float, 'length': float, 'friction': float}

    Returns
    -------
    dict
        Performance metrics: {'stable': bool, 'settling_time': float,
                              'max_angle': float, 'final_error': float}
    """
    # Extract parameters
    mass = params['mass']
    length = params['length']
    friction = params['friction']

    # Create system with perturbed parameters
    system = DoubleInvertedPendulum(
        m1=mass, m2=mass,  # Assume both pendulums have same mass uncertainty
        L1=length, L2=length,
        b=friction
    )

    # Create controller with nominal gains
    controller = ClassicalSMC(
        gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
        boundary_layer_width=0.1
    )

    # Simulation parameters
    dt = 0.01  # 10ms time step
    t_sim = 5.0  # 5 second simulation
    n_steps = int(t_sim / dt)

    # Initial condition: small perturbation
    state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])  # [θ1, θ2, x, θ̇1, θ̇2, ẋ]
    target = np.zeros(6)  # Upright equilibrium

    # Tracking arrays
    angles = []
    times = []

    # Simulate
    for step in range(n_steps):
        t = step * dt

        # Compute control
        u = controller.compute_control(state, target, dt)

        # Apply control and step system
        state = system.step(u, dt, state)

        # Record
        angles.append(max(abs(state[0]), abs(state[1])))  # Max angle deviation
        times.append(t)

        # Check for instability (angle > 30 degrees)
        if max(abs(state[0]), abs(state[1])) > np.radians(30):
            # System went unstable
            return {
                'stable': False,
                'settling_time': np.inf,
                'max_angle': max(abs(state[0]), abs(state[1])),
                'final_error': np.inf
            }

    # Analyze stability
    angles = np.array(angles)

    # Settling time: time to reach and stay within ±2 degrees
    settling_threshold = np.radians(2.0)
    settled = angles < settling_threshold

    if np.any(settled):
        # Find first time settled
        first_settled = np.where(settled)[0][0]
        # Check if stays settled for at least 0.5s
        if first_settled < n_steps - 50:  # 50 steps = 0.5s
            if np.all(angles[first_settled:] < settling_threshold):
                settling_time = times[first_settled]
            else:
                settling_time = np.inf  # Oscillatory, never truly settles
        else:
            settling_time = times[first_settled]
    else:
        settling_time = np.inf

    # Final error
    final_error = angles[-1]

    # Max angle reached
    max_angle = np.max(angles)

    # Stable if settles within simulation time
    stable = settling_time < t_sim

    return {
        'stable': stable,
        'settling_time': settling_time if stable else np.inf,
        'max_angle': float(max_angle),
        'final_error': float(final_error)
    }


def main():
    """Main validation script."""

    print("=" * 70)
    print("Monte Carlo Stability Validation")
    print("=" * 70)

    # Configure Monte Carlo analysis
    config = MonteCarloConfig(
        n_samples=500,  # 500 samples for good coverage
        sampling_method="latin_hypercube",  # LHS for efficient space coverage
        random_seed=RANDOM_SEED,
        confidence_level=0.95,
        convergence_tolerance=0.01,
        min_samples=100,
        max_samples=1000,
        parallel_processing=True,
        max_workers=4
    )

    # Define parameter uncertainty distributions
    parameter_distributions = {
        'mass': {
            'type': 'uniform',
            'low': 0.9,   # -10% nominal (assume nominal = 1.0 kg)
            'high': 1.1   # +10% nominal
        },
        'length': {
            'type': 'uniform',
            'low': 0.95,  # -5% nominal (assume nominal = 1.0 m)
            'high': 1.05  # +5% nominal
        },
        'friction': {
            'type': 'uniform',
            'low': 0.05,   # Low friction
            'high': 0.15   # High friction
        }
    }

    # Create analyzer
    analyzer = MonteCarloAnalyzer(config)

    print("\n1. Running Monte Carlo simulations...")
    print(f"   Sampling method: {config.sampling_method}")
    print(f"   Number of samples: {config.n_samples}")
    print(f"   Parameter ranges:")
    print(f"     - Mass: {parameter_distributions['mass']}")
    print(f"     - Length: {parameter_distributions['length']}")
    print(f"     - Friction: {parameter_distributions['friction']}")

    # Run validation
    result = analyzer.validate(
        data=[],  # No existing data
        simulation_function=simulate_stability_check,
        parameter_distributions=parameter_distributions
    )

    # Extract results
    if result.status.name == 'SUCCESS':
        mc_results = result.data['monte_carlo_simulation']
        stats = mc_results['statistical_summary']
        convergence = mc_results['convergence_analysis']

        print("\n2. Results:")
        print("-" * 70)

        # Stability success rate
        n_successful = mc_results['n_successful_simulations']
        print(f"\n   Successful simulations: {n_successful}/{config.n_samples}")

        # Stability rate
        if 'stable' in stats:
            stable_stats = stats['stable']
            stability_rate = stable_stats['mean']
            print(f"\n   ✓ STABILITY RATE: {stability_rate*100:.1f}%")

            if stability_rate < 0.95:
                print(f"     ⚠ WARNING: Stability rate below 95% threshold!")
                print(f"     Controller may not be robust enough.")
            else:
                print(f"     ✓ Controller meets 95% stability requirement")

        # Settling time statistics
        if 'settling_time' in stats:
            settling_stats = stats['settling_time']
            print(f"\n   Settling Time Statistics:")
            print(f"     Mean:   {settling_stats['mean']:.3f} s")
            print(f"     Std:    {settling_stats['std']:.3f} s")
            print(f"     Median: {settling_stats['median']:.3f} s")
            print(f"     Min:    {settling_stats['min']:.3f} s")
            print(f"     Max:    {settling_stats['max']:.3f} s")

            # Confidence interval
            if 'confidence_interval' in settling_stats:
                ci = settling_stats['confidence_interval']
                print(f"     95% CI: [{ci['lower']:.3f}, {ci['upper']:.3f}] s")

        # Max angle statistics
        if 'max_angle' in stats:
            angle_stats = stats['max_angle']
            print(f"\n   Maximum Angle Deviation:")
            print(f"     Mean:   {np.degrees(angle_stats['mean']):.2f}°")
            print(f"     95th percentile: {np.degrees(angle_stats.get('percentile_95', 0)):.2f}°")

            if np.degrees(angle_stats.get('percentile_95', 0)) > 25:
                print(f"     ⚠ WARNING: 95th percentile angle exceeds 25°")

        # Convergence analysis
        print(f"\n3. Convergence Analysis:")
        print(f"   Converged: {convergence['converged']}")
        if convergence['converged']:
            print(f"   Convergence point: {convergence['convergence_point']} samples")
        else:
            print(f"   ⚠ May need more samples for full convergence")

        # Distribution analysis
        if 'distribution_analysis' in result.data:
            dist_analysis = result.data['distribution_analysis']
            if 'best_fit' in dist_analysis and dist_analysis['best_fit']:
                print(f"\n4. Distribution Fitting:")
                print(f"   Best fit: {dist_analysis['best_fit']}")

                best_dist = dist_analysis['distribution_fits'][dist_analysis['best_fit']]
                print(f"   K-S statistic: {best_dist['ks_statistic']:.4f}")
                print(f"   p-value: {best_dist['p_value']:.4f}")

        # Risk analysis
        if 'risk_analysis' in result.data:
            risk = result.data['risk_analysis']
            print(f"\n5. Risk Analysis (Settling Time):")

            if 'value_at_risk' in risk:
                var = risk['value_at_risk']
                print(f"   VaR (5%):  {var.get('var_5', 'N/A')} s  (worst 5% scenarios)")
                print(f"   VaR (10%): {var.get('var_10', 'N/A')} s  (worst 10% scenarios)")

            if 'conditional_value_at_risk' in risk:
                cvar = risk['conditional_value_at_risk']
                print(f"   CVaR (5%): {cvar.get('cvar_5', 'N/A')} s  (avg of worst 5%)")

        print("\n" + "=" * 70)
        print("VALIDATION CONCLUSION:")

        # Overall assessment
        if 'stable' in stats and stats['stable']['mean'] >= 0.95:
            print("✓ Controller PASSES stability validation")
            print("  - Stability rate ≥ 95%")
            print("  - Ready for hardware-in-the-loop testing")
        else:
            print("✗ Controller FAILS stability validation")
            print("  - Stability rate < 95%")
            print("  - Recommendation: Increase control gains or add robustness")

        print("=" * 70)

    else:
        print(f"\n✗ Validation FAILED: {result.message}")
        if 'error_details' in result.data:
            print(f"   Error: {result.data['error_details']}")


if __name__ == "__main__":
    main()