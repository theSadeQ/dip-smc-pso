# Example from: docs\guides\how-to\testing-validation.md
# Index: 6
# Runnable: True
# Hash: dbbc0f17

def test_robustness_to_mass_variation():
    """Test controller with ±30% mass variation."""
    from src.plant.models.dynamics import DoubleInvertedPendulum

    masses = [0.7, 0.85, 1.0, 1.15, 1.3]  # ±30% variation
    results = []

    for m0 in masses:
        # Create dynamics with varied mass
        dynamics = DoubleInvertedPendulum(
            m0=m0, m1=0.1, m2=0.1,
            l1=0.5, l2=0.5
        )

        # Create controller
        controller = create_smc_for_pso(
            SMCType.CLASSICAL,
            gains=[10, 8, 15, 12, 50, 5],
            max_force=100.0
        )

        # Run simulation
        result = simulate_with_dynamics(controller, dynamics)

        results.append({
            'm0': m0,
            'ise': result['metrics']['ise'],
            'settling_time': result['metrics']['settling_time']
        })

    # Check robustness
    ise_values = [r['ise'] for r in results]
    ise_variance = np.std(ise_values) / np.mean(ise_values)

    print(f"\nRobustness Analysis (Mass Variation):")
    for r in results:
        print(f"  m0={r['m0']:.2f}: ISE={r['ise']:.4f}, "
              f"Settling={r['settling_time']:.2f}s")

    print(f"\nISE Coefficient of Variation: {ise_variance:.3f}")

    # Robustness criterion: CV < 0.3
    assert ise_variance < 0.3, "Controller not robust to mass variation"