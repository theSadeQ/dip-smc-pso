# Example from: docs\testing\guides\property_based_testing.md
# Index: 3
# Runnable: True
# Hash: 6655c2f7

from hypothesis import given, strategies as st

@given(
    theta1=st.floats(min_value=-π, max_value=π),
    theta2=st.floats(min_value=-π, max_value=π),
    velocity=st.floats(min_value=-10, max_value=10)
)
def test_control_never_exceeds_limits(theta1, theta2, velocity):
    """Control output must NEVER exceed actuator limits"""
    state = construct_state(theta1, theta2, velocity)
    u = controller.compute_control(state)

    assert -MAX_TORQUE <= u <= MAX_TORQUE, \
        f"Control {u} exceeded limits for state {state}"