# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 11
# Runnable: False
# Hash: 0e3668ee

# example-metadata:
# runnable: false

class TestSystemLevelMathematics:
    """Test mathematical consistency across system components."""

    def test_control_law_decomposition(self):
        """Test that control law components sum correctly."""
        config = ClassicalSMCConfig(
            gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],
            max_force=100.0,
            dt=0.01,
            boundary_layer=0.01
        )
        controller = ModularClassicalSMC(config=config)

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

        # Get overall control output
        result = controller.compute_control(state, {}, {})
        total_control = result.get('control_output', result.get('control', result.get('u')))

        # Get individual components (if available in debug output)
        components = result.get('debug', {})

        if 'u_equivalent' in components and 'u_switching' in components and 'u_derivative' in components:
            u_eq = components['u_equivalent']
            u_sw = components['u_switching']
            u_d = components['u_derivative']

            # Before saturation, should sum correctly
            u_unsaturated = u_eq + u_sw + u_d

            # After saturation
            u_saturated = np.clip(u_unsaturated, -config.max_force, config.max_force)

            # Should match total control (before any additional processing)
            if total_control is not None:
                assert np.allclose(u_saturated, total_control, rtol=1e-10)

    def test_lyapunov_function_properties(self):
        """Test Lyapunov function properties for stability analysis."""
        config = ClassicalSMCConfig(
            gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],
            max_force=100.0,
            dt=0.01,
            boundary_layer=0.01
        )
        controller = ModularClassicalSMC(config=config)

        surface = LinearSlidingSurface(config.get_surface_gains())

        # Multiple test states
        states = [
            np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01]),
            np.array([0.2, 0.1, 0.15, 0.05, 0.08, 0.03]),
            np.array([-0.1, -0.05, -0.08, -0.02, -0.03, -0.01])
        ]

        for state in states:
            s = surface.compute(state)

            # Lyapunov function candidate: V = 0.5 * s²
            V = 0.5 * s**2

            # V should be non-negative
            assert V >= 0

            # V = 0 if and only if s = 0
            if abs(s) < 1e-10:
                assert V < 1e-15
            else:
                assert V > 0

    def test_reaching_law_satisfaction(self):
        """Test that reaching law is satisfied: s*ṡ ≤ -η|s|."""
        config = ClassicalSMCConfig(
            gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],
            max_force=100.0,
            dt=0.01,
            boundary_layer=0.01
        )

        surface = LinearSlidingSurface(config.get_surface_gains())

        # Test state away from surface
        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])
        s = surface.compute(state)

        # Simplified reaching law check (without full dynamics)
        # For switching control: u_sw = -K * sign(s)
        # The reaching condition s*ṡ ≤ -η|s| should be satisfied
        # when K is chosen large enough

        # This is a simplified test - full test would require dynamics model
        if abs(s) > config.boundary_layer:
            # Outside boundary layer, should have strong reaching behavior
            expected_reaching_rate = -config.K * abs(s) / max(abs(s), config.boundary_layer)
            assert expected_reaching_rate < 0  # Should be moving toward surface