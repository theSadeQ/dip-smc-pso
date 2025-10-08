# Example from: docs\testing\validation_methodology_guide.md
# Index: 12
# Runnable: True
# Hash: 1feb4bfd

# tests/validation/test_numerical_precision.py

class TestNumericalPrecision:
    """Validate numerical precision and stability."""

    def test_floating_point_consistency(self):
        """Test that repeated computations yield identical results."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

        # Compute control 100 times
        results = []
        for _ in range(100):
            result = controller.compute_control(state, {}, {})
            control = result.get('control_output', result.get('control'))
            results.append(control)

        results = np.array(results)

        # All results should be identical (deterministic)
        std_dev = np.std(results)
        assert std_dev < 1e-15, f"Floating-point consistency violated: std = {std_dev}"

    def test_numerical_stability_small_values(self):
        """Test numerical stability with very small state values."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        # Very small state values (near machine precision)
        small_state = np.array([1e-15, 1e-15, 1e-15, 1e-15, 1e-15, 1e-15])

        result = controller.compute_control(small_state, {}, {})
        control = result.get('control_output', result.get('control'))

        # Control should be finite and small
        assert np.isfinite(control), f"Control is not finite for small state: {control}"
        assert abs(control) < 1.0, f"Control magnitude too large for small state: {control}"

    def test_numerical_stability_large_values(self):
        """Test numerical stability with large state values."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        # Large state values
        large_state = np.array([10.0, 5.0, 3.0, 2.0, 2.0, 1.0])

        result = controller.compute_control(large_state, {}, {})
        control = result.get('control_output', result.get('control'))

        # Control should be finite and saturated
        assert np.isfinite(control), f"Control is not finite for large state: {control}"
        assert abs(control) <= 100.0 * 1.01, f"Control exceeds saturation: {control}"