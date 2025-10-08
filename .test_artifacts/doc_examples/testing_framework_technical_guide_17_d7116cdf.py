# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 17
# Runnable: True
# Hash: d7116cdf

class TestEndToEndSimulation:
    """Integration tests for complete simulation workflows."""

    def test_full_simulation_pipeline(self):
        """Test complete simulation from initialization to results."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.simulation_runner import run_simulation

        # Setup
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        initial_state = [0.0, 0.0, 0.1, 0.1, 0.0, 0.0]

        # Execute
        result = run_simulation(
            controller=controller,
            duration=5.0,
            dt=0.01,
            initial_state=initial_state
        )

        # Validate
        assert 'time' in result
        assert 'states' in result
        assert 'controls' in result
        assert len(result['time']) == len(result['states'])
        assert len(result['time']) == len(result['controls']) + 1

        # Performance validation
        final_state = result['states'][-1]
        assert np.linalg.norm(final_state) < 0.05  # Stabilized

    def test_simulation_with_disturbance(self):
        """Test simulation with external disturbance."""
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.simulation_runner import run_simulation

        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        # Define disturbance function
        def disturbance(t):
            if 1.0 <= t <= 2.0:
                return 20.0  # Impulse disturbance
            return 0.0

        result = run_simulation(
            controller=controller,
            duration=5.0,
            dt=0.01,
            initial_state=[0.0, 0.0, 0.1, 0.1, 0.0, 0.0],
            disturbance=disturbance
        )

        # Controller should recover from disturbance
        final_state = result['states'][-1]
        assert np.linalg.norm(final_state) < 0.1  # Recovered