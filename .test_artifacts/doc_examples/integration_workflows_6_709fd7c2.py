# Example from: docs\testing\guides\integration_workflows.md
# Index: 6
# Runnable: False
# Hash: 709fd7c2

@pytest.mark.integration
def test_nominal_stabilization():
    """Baseline integration test"""
    initial_states = [
        [0.1, 0, 0, 0],
        [0, 0.1, 0, 0],
        [-0.1, -0.1, 0, 0]
    ]

    for state in initial_states:
        trajectory = simulate(controller, dynamics, state, duration=5.0)
        final_error = np.linalg.norm(trajectory[-1])
        assert final_error < 0.05, f"Failed for initial state {state}"