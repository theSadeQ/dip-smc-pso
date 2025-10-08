# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 1
# Runnable: False
# Hash: 943fe2c8

# example-metadata:
# runnable: false

# Step 1: RED - Write failing test
# tests/test_controllers/smc/algorithms/classical/test_new_feature.py

def test_chattering_reduction_effectiveness():
    """Test that chattering reduction algorithm reduces control rate."""
    controller = ClassicalSMC(
        gains=[10, 8, 15, 12, 50, 5],
        max_force=100,
        boundary_layer=0.01,
        chattering_reduction=True  # New feature
    )

    state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

    control_history = []
    for _ in range(100):
        result = controller.compute_control(state, {}, {})
        control = result['control']
        control_history.append(control)

    # Calculate control rate
    control_rate = np.std(np.diff(control_history))

    # Should be significantly lower than baseline
    assert control_rate < 5.0, f"Chattering reduction ineffective: rate={control_rate}"

# Run test → FAILS (feature not implemented)
# pytest tests/test_controllers/smc/algorithms/classical/test_new_feature.py -v