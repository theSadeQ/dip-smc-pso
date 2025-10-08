# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 11
# Runnable: False
# Hash: 668d2ca6

@pytest.mark.benchmark
def test_compute_control_performance(benchmark):
    """Benchmark control computation for real-time requirements."""
    controller = create_test_controller()
    state = np.array([0.1, 0.2, -0.1, 0.0, 0.3, -0.2])

    def run_control():
        return controller.compute_control(state, (), {})

    result = benchmark(run_control)

    # Real-time requirement: <1ms computation time
    # For 100Hz control loop (dt=0.01s), we need ~10ms budget
    # Leave margin for other operations, target <1ms for controller
    mean_time = benchmark.stats['mean']
    assert mean_time < 0.001, \
        f"Control computation too slow: {mean_time*1000:.2f}ms (target <1ms)"