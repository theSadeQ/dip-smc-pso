# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 4
# Runnable: True
# Hash: f1a969d0

# tests/test_benchmarks/performance/test_performance_benchmarks_deep.py
import pytest

class TestControllerPerformanceBenchmarks:
    """Performance benchmarks for controller computations."""

    @pytest.mark.benchmark
    def test_classical_smc_compute_speed(self, benchmark):
        """Benchmark classical SMC control computation."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)
        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

        result = benchmark(controller.compute_control, state, {}, {})

        # Performance criteria
        assert benchmark.stats['mean'] < 1e-4  # < 0.1 ms per control step
        assert benchmark.stats['stddev'] < 1e-5  # Low variance

    @pytest.mark.benchmark
    def test_simulation_throughput(self, benchmark):
        """Benchmark end-to-end simulation throughput."""
        controller = ClassicalSMC(
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        def run_short_simulation():
            return run_simulation(
                controller=controller,
                duration=1.0,
                dt=0.01,
                initial_state=[0.1, 0.1, 0.0, 0.0, 0.0, 0.0]
            )

        result = benchmark(run_short_simulation)

        # Throughput criteria (100 timesteps in <100ms)
        assert benchmark.stats['mean'] < 0.1