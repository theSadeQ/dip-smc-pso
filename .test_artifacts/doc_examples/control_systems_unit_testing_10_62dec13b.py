# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 10
# Runnable: False
# Hash: 62dec13b

# example-metadata:
# runnable: false

def test_history_telemetry():
    """Test that controller properly tracks telemetry in history."""
    controller = create_test_controller()

    state = np.array([0.1, 0.2, -0.1, 0.0, 0.3, -0.2])
    history = {}

    result = controller.compute_control(state, (), history)

    # Verify all required telemetry is tracked
    required_keys = ['sigma', 'epsilon_eff', 'u_eq', 'u_robust', 'u_total', 'u']
    for key in required_keys:
        assert key in history, f"Missing required history key: {key}"
        assert len(history[key]) == 1, f"History key {key} should have 1 entry"

    # Run multiple steps and verify accumulation
    for _ in range(5):
        controller.compute_control(state, (), history)

    for key in required_keys:
        assert len(history[key]) == 6, \
            f"History key {key} should accumulate (expected 6, got {len(history[key])})"