# Example from: docs\guides\how-to\testing-validation.md
# Index: 7
# Runnable: True
# Hash: 5f8bf522

# tests/test_benchmarks/test_controller_performance.py
import pytest
import numpy as np
from src.controllers import create_smc_for_pso, SMCType

def test_classical_smc_benchmark(benchmark):
    """Benchmark classical SMC control computation."""
    controller = create_smc_for_pso(
        SMCType.CLASSICAL,
        gains=[10, 8, 15, 12, 50, 5],
        max_force=100.0
    )

    state = np.array([0, 0, 0.1, 0, 0.15, 0])
    state_vars = {}
    history = controller.initialize_history()

    # Benchmark the control computation
    result = benchmark(
        controller.compute_control,
        state, state_vars, history
    )

    # Verify result is valid
    control, _, _ = result
    assert abs(control) <= 100.0

def test_full_simulation_benchmark(benchmark):
    """Benchmark full simulation."""
    from src.controllers.factory import create_controller
    from src.core.simulation_runner import SimulationRunner
    from src.config import load_config

    config = load_config('config.yaml')
    controller = create_controller(
        'classical_smc',
        config=config.controllers.classical_smc
    )
    runner = SimulationRunner(config)

    # Benchmark full simulation
    result = benchmark(runner.run, controller)

    # Verify completion
    assert 'metrics' in result