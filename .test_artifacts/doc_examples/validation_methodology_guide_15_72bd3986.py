# Example from: docs\testing\validation_methodology_guide.md
# Index: 15
# Runnable: True
# Hash: 72bd3986

class TestMonteCarloValidation:
    """Validate controller robustness via Monte Carlo simulation."""

    def test_robustness_to_initial_conditions(self):
        """Test controller stabilizes system from diverse initial conditions."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.dynamics import SimplifiedDynamics

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        physics_cfg = {'M': 1.0, 'm1': 0.1, 'm2': 0.1, 'L1': 0.5, 'L2': 0.5, 'g': 9.81}
        dynamics = SimplifiedDynamics(physics_cfg)

        # Monte Carlo: 100 random initial conditions
        n_trials = 100
        successes = 0

        for _ in range(n_trials):
            # Random initial state within bounds
            state = np.random.uniform(-0.2, 0.2, size=6)

            # Simulate
            for _ in range(500):
                result = controller.compute_control(state, {}, {})
                u = result.get('control_output', result.get('control', 0.0))
                x_dot = dynamics.dynamics(state, u)
                state = state + 0.01 * x_dot

            # Check stabilization
            if np.linalg.norm(state) < 0.05:
                successes += 1

        success_rate = successes / n_trials
        assert success_rate > 0.90, (
            f"Controller stabilized only {success_rate*100:.1f}% of initial conditions"
        )