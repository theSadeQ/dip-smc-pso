# Example from: docs\testing\validation_methodology_guide.md
# Index: 14
# Runnable: True
# Hash: ceaae1cb

# tests/validation/test_scientific_properties.py

class TestControlTheoreticProperties:
    """Validate control-theoretic guarantees."""

    def test_exponential_stability(self):
        """Test closed-loop system exhibits exponential stability."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.dynamics import SimplifiedDynamics

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        physics_cfg = {'M': 1.0, 'm1': 0.1, 'm2': 0.1, 'L1': 0.5, 'L2': 0.5, 'g': 9.81}
        dynamics = SimplifiedDynamics(physics_cfg)

        # Initial state
        state = np.array([0.0, 0.2, 0.15, 0.0, 0.0, 0.0])
        initial_error = np.linalg.norm(state)

        # Simulate
        errors = [initial_error]
        for _ in range(500):
            result = controller.compute_control(state, {}, {})
            u = result.get('control_output', result.get('control', 0.0))
            x_dot = dynamics.dynamics(state, u)
            state = state + 0.01 * x_dot
            errors.append(np.linalg.norm(state))

        errors = np.array(errors)
        t = np.arange(len(errors)) * 0.01

        # Fit exponential decay: e(t) ≈ e(0)·exp(-λt)
        log_errors = np.log(errors + 1e-10)
        coeffs = np.polyfit(t, log_errors, 1)
        decay_rate = -coeffs[0]

        # Positive decay rate indicates exponential stability
        assert decay_rate > 0, (
            f"System not exponentially stable: decay rate = {decay_rate}"
        )

    def test_finite_time_convergence_to_sliding_surface(self):
        """Test reaching phase achieves sliding surface in finite time."""
        from src.controllers.smc.sta_smc import STASMC
        from src.core.dynamics import SimplifiedDynamics

        controller = STASMC(
            gains=[25.0, 10.0, 15.0, 12.0, 20.0, 15.0],
            max_force=100.0
        )

        physics_cfg = {'M': 1.0, 'm1': 0.1, 'm2': 0.1, 'L1': 0.5, 'L2': 0.5, 'g': 9.81}
        dynamics = SimplifiedDynamics(physics_cfg)

        state = np.array([0.0, 0.2, 0.15, 0.0, 0.0, 0.0])

        from src.controllers.smc.core.sliding_surface import LinearSlidingSurface
        surface = LinearSlidingSurface([25.0, 10.0, 15.0, 12.0])

        reached_surface = False
        for i in range(1000):
            s = surface.compute(state)

            if abs(s) < 0.01:  # Reached sliding surface
                reached_surface = True
                print(f"Reached sliding surface at iteration {i}")
                break

            result = controller.compute_control(state, {}, {})
            u = result.get('control_output', result.get('control', 0.0))
            x_dot = dynamics.dynamics(state, u)
            state = state + 0.01 * x_dot

        assert reached_surface, "Failed to reach sliding surface in finite time"