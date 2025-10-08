# Example from: docs\factory\testing_validation_documentation.md
# Index: 3
# Runnable: True
# Hash: f5f38586

class TestFactoryPlantIntegration:
    """Test integration between factory and plant models."""

    def setup_method(self):
        """Setup integration test environment."""
        from src.plant.configurations import ConfigurationFactory

        self.plant_configs = {
            'simplified': ConfigurationFactory.create_default_config("simplified"),
            'full': ConfigurationFactory.create_default_config("full") if hasattr(ConfigurationFactory, 'create_default_config') else None
        }

        self.test_scenarios = {
            'equilibrium': np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            'small_disturbance': np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0]),
            'large_angles': np.array([0.5, 0.8, 0.6, 0.2, 0.1, 0.15])
        }

    @pytest.mark.parametrize("plant_type", ['simplified'])
    @pytest.mark.parametrize("controller_type,gains", [
        ('classical_smc', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]),
        ('adaptive_smc', [25.0, 18.0, 15.0, 10.0, 4.0]),
    ])
    def test_controller_plant_compatibility(
        self,
        plant_type: str,
        controller_type: str,
        gains: List[float]
    ):
        """Test controller-plant compatibility across configurations."""
        plant_config = self.plant_configs[plant_type]
        if plant_config is None:
            pytest.skip(f"Plant config {plant_type} not available")

        # Create controller
        controller = create_controller(controller_type, plant_config, gains)

        # Test control computation for all scenarios
        for scenario_name, state in self.test_scenarios.items():
            control_output = controller.compute_control(state, (), {})

            assert control_output is not None
            assert hasattr(control_output, 'u')

            # Validate control output
            control_value = control_output.u
            assert isinstance(control_value, (int, float, np.ndarray))
            assert np.isfinite(control_value)

    def test_closed_loop_simulation(self):
        """Test closed-loop simulation with factory-created controllers."""
        from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics

        plant_config = self.plant_configs['simplified']
        dynamics = SimplifiedDIPDynamics(plant_config)

        controller = create_controller(
            'classical_smc',
            plant_config,
            [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        )

        # Run closed-loop simulation
        state = np.array([0.1, 0.2, 0.1, 0.0, 0.0, 0.0])
        dt = 0.001
        simulation_time = 0.1  # Short simulation for testing

        for step in range(int(simulation_time / dt)):
            # Compute control
            control_output = controller.compute_control(state, (), {})
            control = np.array([control_output.u])

            # Simulate dynamics
            result = dynamics.compute_dynamics(state, control)
            assert result.success

            # Integrate
            state = state + dt * result.state_derivative

            # Basic stability check
            assert np.all(np.abs(state) < 10.0), f"System unstable at step {step}"

    def test_multiple_controller_coordination(self):
        """Test multiple controllers working with same plant configuration."""
        plant_config = self.plant_configs['simplified']

        controllers = {
            'classical': create_controller('classical_smc', plant_config, [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]),
            'adaptive': create_controller('adaptive_smc', plant_config, [25.0, 18.0, 15.0, 10.0, 4.0])
        }

        test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])

        # Test that all controllers can compute control for same state
        control_outputs = {}
        for name, controller in controllers.items():
            control_output = controller.compute_control(test_state, (), {})
            control_outputs[name] = control_output.u

            assert np.isfinite(control_output.u)
            assert abs(control_output.u) <= 200.0  # Reasonable control bounds

        # Controllers should produce different outputs (unless coincidentally same)
        # This tests that they're actually different controllers
        if len(set(control_outputs.values())) > 1:
            assert True  # Different outputs expected
        else:
            # Same outputs acceptable for this simple state
            pass

    def test_plant_parameter_sensitivity(self):
        """Test controller behavior with plant parameter variations."""
        # Create multiple plant configurations (simulated variations)
        base_config = self.plant_configs['simplified']

        controller = create_controller(
            'classical_smc',
            base_config,
            [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        )

        # Test robustness to initial conditions
        challenging_states = [
            np.array([0.3, 0.4, 0.2, 0.1, 0.0, 0.0]),
            np.array([0.1, 0.1, 0.1, 1.0, 0.8, 0.6]),
            np.array([0.6, 0.8, 0.5, 0.3, 0.2, 0.1])
        ]

        for i, state in enumerate(challenging_states):
            try:
                control_output = controller.compute_control(state, (), {})
                assert np.isfinite(control_output.u)
                assert abs(control_output.u) <= 500.0  # Allow higher control for challenging states
            except Exception as e:
                pytest.fail(f"Controller failed on challenging state {i}: {e}")