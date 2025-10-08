# Example from: docs\factory\testing_validation_documentation.md
# Index: 4
# Runnable: True
# Hash: 07751e0c

class TestPSOIntegration:
    """Test PSO optimization integration with factory system."""

    def setup_method(self):
        """Setup PSO integration test environment."""
        from src.plant.configurations import ConfigurationFactory
        self.plant_config = ConfigurationFactory.create_default_config("simplified")

        # Import PSO integration components
        from src.controllers.factory.smc_factory import (
            create_smc_for_pso, get_gain_bounds_for_pso, validate_smc_gains, SMCType
        )

        self.pso_functions = {
            'create_smc_for_pso': create_smc_for_pso,
            'get_gain_bounds_for_pso': get_gain_bounds_for_pso,
            'validate_smc_gains': validate_smc_gains
        }

    @pytest.mark.parametrize("controller_type", [
        SMCType.CLASSICAL,
        SMCType.ADAPTIVE,
    ])
    def test_pso_controller_creation(self, controller_type: SMCType):
        """Test PSO-compatible controller creation."""
        # Get appropriate gains for controller type
        if controller_type == SMCType.CLASSICAL:
            gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        elif controller_type == SMCType.ADAPTIVE:
            gains = [25.0, 18.0, 15.0, 10.0, 4.0]
        else:
            pytest.skip(f"Controller type {controller_type} not fully implemented")

        # Create PSO controller
        pso_controller = self.pso_functions['create_smc_for_pso'](
            controller_type, gains, self.plant_config
        )

        assert pso_controller is not None
        assert hasattr(pso_controller, 'compute_control')
        assert hasattr(pso_controller, 'n_gains')
        assert hasattr(pso_controller, 'controller_type')

        # Test PSO interface
        test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
        control = pso_controller.compute_control(test_state)

        assert isinstance(control, np.ndarray)
        assert control.shape == (1,)
        assert np.isfinite(control[0])

    def test_pso_gain_bounds(self):
        """Test PSO gain bounds generation."""
        for controller_type in [SMCType.CLASSICAL, SMCType.ADAPTIVE]:
            bounds = self.pso_functions['get_gain_bounds_for_pso'](controller_type)

            assert isinstance(bounds, tuple)
            assert len(bounds) == 2

            lower_bounds, upper_bounds = bounds
            assert len(lower_bounds) == len(upper_bounds)
            assert all(l < u for l, u in zip(lower_bounds, upper_bounds))
            assert all(l > 0 for l in lower_bounds)  # All gains must be positive

    def test_pso_gain_validation(self):
        """Test PSO gain validation functionality."""
        # Test valid gains
        valid_classical_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        assert self.pso_functions['validate_smc_gains'](SMCType.CLASSICAL, valid_classical_gains)

        valid_adaptive_gains = [25.0, 18.0, 15.0, 10.0, 4.0]
        assert self.pso_functions['validate_smc_gains'](SMCType.ADAPTIVE, valid_adaptive_gains)

        # Test invalid gains
        invalid_gains = [-1.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # Negative gain
        assert not self.pso_functions['validate_smc_gains'](SMCType.CLASSICAL, invalid_gains)

        wrong_length_gains = [20.0, 15.0, 12.0]  # Too few gains
        assert not self.pso_functions['validate_smc_gains'](SMCType.CLASSICAL, wrong_length_gains)

    def test_pso_optimization_simulation(self):
        """Test simulated PSO optimization workflow."""
        # Create PSO-compatible fitness function
        def simple_fitness_function(gains: List[float]) -> float:
            try:
                controller = self.pso_functions['create_smc_for_pso'](
                    SMCType.CLASSICAL, gains, self.plant_config
                )

                # Simple fitness: minimize control effort for small disturbance
                test_state = np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0])
                control = controller.compute_control(test_state)

                # Fitness function: minimize control effort
                return abs(control[0])

            except Exception:
                return 1000.0  # High penalty for failures

        # Test fitness function with valid gains
        test_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        fitness = simple_fitness_function(test_gains)

        assert isinstance(fitness, (int, float))
        assert np.isfinite(fitness)
        assert fitness >= 0

        # Test fitness function with invalid gains
        invalid_gains = []
        invalid_fitness = simple_fitness_function(invalid_gains)
        assert invalid_fitness == 1000.0  # Should return penalty value

    def test_pso_thread_safety(self):
        """Test PSO operations are thread-safe."""
        import threading
        import time

        results = []
        errors = []

        def pso_worker(worker_id: int):
            try:
                for i in range(3):
                    gains = [20.0 + worker_id, 15.0, 12.0, 8.0, 35.0, 5.0]
                    controller = self.pso_functions['create_smc_for_pso'](
                        SMCType.CLASSICAL, gains, self.plant_config
                    )

                    test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
                    control = controller.compute_control(test_state)
                    assert isinstance(control, np.ndarray)
                    time.sleep(0.001)

                results.append(True)
            except Exception as e:
                errors.append(f"Worker {worker_id}: {str(e)}")
                results.append(False)

        # Create multiple worker threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=pso_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify results
        assert not errors, f"Thread safety errors: {errors}"
        assert all(results), "Some PSO workers failed"