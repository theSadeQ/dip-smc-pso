# Example from: docs\factory\testing_validation_documentation.md
# Index: 5
# Runnable: True
# Hash: b4966a6e

class TestRealTimePerformance:
    """Test real-time performance requirements."""

    def setup_method(self):
        """Setup performance testing environment."""
        from src.plant.configurations import ConfigurationFactory
        self.plant_config = ConfigurationFactory.create_default_config("simplified")

        # Performance thresholds
        self.max_control_computation_time = 0.001  # 1ms for 1kHz control
        self.max_factory_creation_time = 0.01      # 10ms for factory creation
        self.max_memory_per_controller = 1.0       # 1MB per controller

    def test_control_computation_performance(self):
        """Test control computation meets real-time constraints."""
        import time

        controller = create_controller(
            'classical_smc',
            self.plant_config,
            [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        )

        test_states = [
            np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0]),
            np.array([0.3, 0.4, 0.2, 0.1, 0.0, 0.0]),
            np.array([0.5, 0.6, 0.3, 0.2, 0.1, 0.0])
        ]

        computation_times = []

        for state in test_states:
            for _ in range(100):  # Multiple computations for statistical significance
                start_time = time.time()
                control_output = controller.compute_control(state, (), {})
                computation_time = time.time() - start_time

                computation_times.append(computation_time)
                assert control_output is not None

        # Performance validation
        avg_time = np.mean(computation_times)
        max_time = np.max(computation_times)

        assert avg_time < self.max_control_computation_time, f"Average computation time {avg_time:.6f}s exceeds limit"
        assert max_time < self.max_control_computation_time * 2, f"Max computation time {max_time:.6f}s too high"

    def test_factory_creation_performance(self):
        """Test factory creation performance."""
        import time

        creation_times = []

        for i in range(20):
            gains = [20.0 + i, 15.0, 12.0, 8.0, 35.0, 5.0]

            start_time = time.time()
            controller = create_controller('classical_smc', self.plant_config, gains)
            creation_time = time.time() - start_time

            creation_times.append(creation_time)
            assert controller is not None

        avg_creation_time = np.mean(creation_times)
        max_creation_time = np.max(creation_times)

        assert avg_creation_time < self.max_factory_creation_time, f"Average creation time {avg_creation_time:.6f}s exceeds limit"
        assert max_creation_time < self.max_factory_creation_time * 2, f"Max creation time {max_creation_time:.6f}s too high"

    def test_memory_efficiency(self):
        """Test memory efficiency during intensive usage."""
        import gc
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        controllers = []

        # Create many controllers
        for i in range(50):
            gains = [20.0 + i, 15.0, 12.0, 8.0, 35.0, 5.0]
            controller = create_controller('classical_smc', self.plant_config, gains)
            controllers.append(controller)

            # Use controller to ensure it's not optimized away
            test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
            _ = controller.compute_control(test_state, (), {})

        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_per_controller = (peak_memory - initial_memory) / len(controllers)

        # Clean up
        del controllers
        gc.collect()

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_leak = final_memory - initial_memory

        # Validate memory efficiency
        assert memory_per_controller < self.max_memory_per_controller, f"Memory per controller {memory_per_controller:.3f}MB exceeds limit"
        assert memory_leak < 10.0, f"Memory leak detected: {memory_leak:.3f}MB"

    @pytest.mark.benchmark
    def test_pso_evaluation_benchmark(self):
        """Benchmark PSO evaluation performance."""
        from src.controllers.factory.smc_factory import create_smc_for_pso, SMCType

        def benchmark_fitness_function(gains: List[float]) -> float:
            controller = create_smc_for_pso(SMCType.CLASSICAL, gains, self.plant_config)
            test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
            control = controller.compute_control(test_state)
            return abs(control[0])

        # Benchmark parameters
        n_evaluations = 100
        test_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]

        import time
        start_time = time.time()

        for _ in range(n_evaluations):
            fitness = benchmark_fitness_function(test_gains)
            assert np.isfinite(fitness)

        total_time = time.time() - start_time
        avg_time_per_evaluation = total_time / n_evaluations

        # PSO evaluation should be fast enough for optimization
        assert avg_time_per_evaluation < 0.01, f"PSO evaluation too slow: {avg_time_per_evaluation:.6f}s per evaluation"