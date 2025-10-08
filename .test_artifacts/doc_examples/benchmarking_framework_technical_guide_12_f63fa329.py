# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 12
# Runnable: True
# Hash: f63fa329

# tests/test_benchmarks/performance/test_controller_benchmarks.py

import pytest
from src.controllers.smc.classic_smc import ClassicalSMC

class TestControllerPerformance:
    """Performance benchmarks for controller computations."""

    @pytest.mark.benchmark(group="control_computation")
    def test_classical_smc_performance(self, benchmark):
        """Benchmark classical SMC control computation speed."""
        controller = ClassicalSMC(
            gains=[10, 8, 15, 12, 50, 5],
            max_force=100,
            boundary_layer=0.01
        )

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

        result = benchmark(controller.compute_control, state, {}, {})

        # Performance criteria
        stats = benchmark.stats
        assert stats['mean'] < 1e-3  # <1ms average

    @pytest.mark.benchmark(group="simulation")
    def test_full_simulation_performance(self, benchmark):
        """Benchmark end-to-end simulation performance."""
        from src.core.simulation_runner import run_simulation

        controller = ClassicalSMC(
            gains=[10, 8, 15, 12, 50, 5],
            max_force=100,
            boundary_layer=0.01
        )

        def simulate():
            return run_simulation(
                controller=controller,
                duration=1.0,
                dt=0.01,
                initial_state=[0.1, 0.1, 0, 0, 0, 0]
            )

        result = benchmark(simulate)

        # Throughput criteria (100 steps in <100ms)
        assert benchmark.stats['mean'] < 0.1