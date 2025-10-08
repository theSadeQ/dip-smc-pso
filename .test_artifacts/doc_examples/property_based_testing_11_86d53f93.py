# Example from: docs\testing\guides\property_based_testing.md
# Index: 11
# Runnable: True
# Hash: 86d53f93

@given(state=valid_states(), scale=st.floats(min_value=0.1, max_value=10))
def test_control_scaling_property(state, scale):
    """If error scales, control should scale proportionally"""
    u1 = controller.compute_control(state)
    scaled_state = state * scale
    u2 = controller.compute_control(scaled_state)

    # Check proportionality (for linear controllers)
    assert abs(u2 / u1 - scale) < 0.01, \
        "Control does not scale with state"