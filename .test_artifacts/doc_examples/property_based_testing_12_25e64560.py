# Example from: docs\testing\guides\property_based_testing.md
# Index: 12
# Runnable: False
# Hash: 25e64560

# example-metadata:
# runnable: false

@given(state=valid_states())
def test_no_regression_from_baseline(state):
    """Current controller performs at least as well as baseline"""
    # Baseline controller (e.g., from v1.0)
    u_baseline = baseline_controller.compute_control(state)
    cost_baseline = evaluate_performance(state, u_baseline)

    # Current controller
    u_current = current_controller.compute_control(state)
    cost_current = evaluate_performance(state, u_current)

    assert cost_current <= cost_baseline * 1.05, \  # Allow 5% tolerance
        f"Performance regression detected: {cost_current} > {cost_baseline}"