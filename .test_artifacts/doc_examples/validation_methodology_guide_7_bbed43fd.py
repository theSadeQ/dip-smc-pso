# Example from: docs\testing\validation_methodology_guide.md
# Index: 7
# Runnable: True
# Hash: bbed43fd

# tests/validation/test_lyapunov_properties.py

class TestLyapunovFunctionProperties:
    """Validate Lyapunov function properties for stability analysis."""

    def test_positive_definiteness(self):
        """Test V(σ) > 0 for σ ≠ 0, V(0) = 0."""
        from src.controllers.smc.core.sliding_surface import LinearSlidingSurface

        gains = [5.0, 3.0, 4.0, 2.0]
        surface = LinearSlidingSurface(gains)

        # Test states
        states = [
            np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01]),  # Non-zero
            np.array([0.2, 0.1, 0.15, 0.05, 0.08, 0.03]),   # Non-zero
            np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])        # Zero (equilibrium)
        ]

        for state in states:
            s = surface.compute(state)
            V = 0.5 * s**2  # Lyapunov candidate: V = ½σ²

            if np.linalg.norm(state) < 1e-10:
                # At equilibrium, V should be zero
                assert V < 1e-15, f"V(0) should be zero, got {V}"
            else:
                # Away from equilibrium, V should be positive
                assert V > 0, f"V(σ) should be positive for σ ≠ 0, got {V}"

    def test_lyapunov_decrease_property(self):
        """Test V̇(σ) < 0 for σ ≠ 0 (Lyapunov decrease condition)."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.dynamics import SimplifiedDynamics

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        physics_cfg = {
            'M': 1.0, 'm1': 0.1, 'm2': 0.1,
            'L1': 0.5, 'L2': 0.5, 'g': 9.81
        }
        dynamics = SimplifiedDynamics(physics_cfg)

        # Initial state away from equilibrium
        state = np.array([0.0, 0.2, 0.15, 0.0, 0.0, 0.0])

        V_values = []
        for _ in range(100):
            # Compute sliding variable
            from src.controllers.smc.core.sliding_surface import LinearSlidingSurface
            surface = LinearSlidingSurface([10.0, 8.0, 15.0, 12.0])
            s = surface.compute(state)

            V = 0.5 * s**2
            V_values.append(V)

            # Apply control and step dynamics
            result = controller.compute_control(state, {}, {})
            u = result.get('control_output', result.get('control', 0.0))
            x_dot = dynamics.dynamics(state, u)
            state = state + 0.01 * x_dot

        # Verify Lyapunov decrease: V̇ < 0
        V_derivative = np.diff(V_values)
        positive_derivatives = np.sum(V_derivative > 0)

        # Allow small violations due to numerical errors
        violation_ratio = positive_derivatives / len(V_derivative)
        assert violation_ratio < 0.05, (
            f"Lyapunov function should decrease monotonically, "
            f"but increased {violation_ratio*100:.1f}% of the time"
        )