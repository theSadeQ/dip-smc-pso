# Example from: docs\testing\validation_methodology_guide.md
# Index: 8
# Runnable: True
# Hash: 83301779

class TestReachingLawSatisfaction:
    """Validate reaching law for sliding mode controllers."""

    def test_reaching_law_condition(self):
        """Test σ·σ̇ ≤ -η|σ| is satisfied."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.dynamics import SimplifiedDynamics

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        physics_cfg = {'M': 1.0, 'm1': 0.1, 'm2': 0.1, 'L1': 0.5, 'L2': 0.5, 'g': 9.81}
        dynamics = SimplifiedDynamics(physics_cfg)

        state = np.array([0.0, 0.2, 0.15, 0.0, 0.0, 0.0])

        from src.controllers.smc.core.sliding_surface import LinearSlidingSurface
        surface = LinearSlidingSurface([10.0, 8.0, 15.0, 12.0])

        dt = 0.01
        for _ in range(50):
            s_current = surface.compute(state)

            # Apply control
            result = controller.compute_control(state, {}, {})
            u = result.get('control_output', result.get('control', 0.0))

            # Step dynamics
            x_dot = dynamics.dynamics(state, u)
            state_next = state + dt * x_dot

            s_next = surface.compute(state_next)
            s_dot = (s_next - s_current) / dt

            # Reaching law: s·ṡ ≤ -η|s|
            reaching_product = s_current * s_dot
            eta = 0.5  # Reaching rate parameter

            if abs(s_current) > controller.boundary_layer:
                # Outside boundary layer, reaching law must be satisfied
                assert reaching_product <= -eta * abs(s_current) + 0.1, (
                    f"Reaching law violated: σ·σ̇ = {reaching_product}, "
                    f"but should be ≤ {-eta * abs(s_current)}"
                )

            state = state_next