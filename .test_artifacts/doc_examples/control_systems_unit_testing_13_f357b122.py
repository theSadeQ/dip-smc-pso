# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 13
# Runnable: False
# Hash: f357b122

def test_monte_carlo_robustness():
    """Test controller robustness with random state sampling."""
    controller = create_test_controller()

    np.random.seed(42)
    n_samples = 1000

    failures = 0

    for _ in range(n_samples):
        # Random state within physical bounds
        state = np.random.uniform(
            low=[-1.0, -np.pi/6, -np.pi/6, -1.0, -2.0, -2.0],
            high=[1.0, np.pi/6, np.pi/6, 1.0, 2.0, 2.0]
        )

        try:
            result = controller.compute_control(state, (), {})

            # Check for numerical issues
            if not np.isfinite(result.u):
                failures += 1
            elif abs(result.u) > controller.max_force:
                failures += 1
        except Exception:
            failures += 1

    success_rate = 1.0 - (failures / n_samples)

    # Require 99.9% success rate for production deployment
    assert success_rate >= 0.999, \
        f"Monte Carlo success rate too low: {success_rate:.2%} (target ≥99.9%)"