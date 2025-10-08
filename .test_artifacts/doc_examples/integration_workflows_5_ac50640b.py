# Example from: docs\testing\guides\integration_workflows.md
# Index: 5
# Runnable: False
# Hash: ac50640b

def test_multi_stage_integration():
    """Progressive integration testing"""
    # Stage 1: Unit level
    controller = ClassicalSMC(gains=[10, 5, 8])
    assert controller.compute_control([0.1, 0, 0, 0]) is not None

    # Stage 2: Subsystem integration
    dynamics = SimplifiedDynamics()
    state = [0.1, 0, 0, 0]
    u = controller.compute_control(state)
    next_state = dynamics.step(state, u, 0.01)
    assert dynamics.is_valid_state(next_state)

    # Stage 3: Full system integration
    trajectory = simulate(controller, dynamics, state, duration=1.0)
    assert len(trajectory) > 0

    # Stage 4: Performance validation
    metrics = analyze_performance(trajectory)
    assert metrics['settling_time'] < 2.0