# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 14
# Runnable: False
# Hash: f80c626c

class TestClassicalSMCControlComputation:
    """Test Classical SMC control computation."""

    def test_compute_control_valid_output(self):
        """Test that compute_control returns valid, bounded output."""
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])
        result = controller.compute_control(state, {}, {})

        control = result.get('control_output', result.get('control', result.get('u')))

        # Validate output properties
        assert control is not None
        assert isinstance(control, (float, np.ndarray))
        assert np.all(np.isfinite(control))
        assert np.all(np.abs(control) <= 100.0)  # Within saturation

    def test_compute_control_equilibrium(self):
        """Test control at equilibrium (should be near zero)."""
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        equilibrium = np.zeros(6)
        result = controller.compute_control(equilibrium, {}, {})

        control = result.get('control_output', result.get('control', result.get('u')))

        # At equilibrium, control should be minimal
        if control is not None:
            assert np.abs(control) < 1.0  # Small control near equilibrium

    def test_compute_control_large_deviation(self):
        """Test control with large state deviation (saturation)."""
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        large_state = np.array([1.0, 0.5, 0.8, 0.3, 0.5, 0.2])
        result = controller.compute_control(large_state, {}, {})

        control = result.get('control_output', result.get('control', result.get('u')))

        # Large deviation should saturate control
        if control is not None:
            assert np.abs(control) == pytest.approx(100.0, abs=0.1)

    def test_compute_control_deterministic(self):
        """Test that repeated calls produce identical results."""
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

        results = []
        for _ in range(100):
            result = controller.compute_control(state, {}, {})
            control = result.get('control_output', result.get('control', result.get('u')))
            if control is not None:
                results.append(control)

        results = np.array(results)

        # All results should be identical (deterministic)
        std_dev = np.std(results, axis=0)
        assert np.all(std_dev < 1e-15)  # Machine precision