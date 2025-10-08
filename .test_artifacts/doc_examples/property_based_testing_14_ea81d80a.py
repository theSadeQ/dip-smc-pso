# Example from: docs\testing\guides\property_based_testing.md
# Index: 14
# Runnable: False
# Hash: ea81d80a

@given(
    state=valid_states(),
    boundary_layer=st.floats(min_value=0.01, max_value=1.0)
)
def test_chattering_bounded_by_boundary_layer(state, boundary_layer):
    """Chattering frequency inversely related to boundary layer"""
    controller.set_boundary_layer(boundary_layer)

    control_sequence = []
    for _ in range(100):
        u = controller.compute_control(state)
        control_sequence.append(u)
        state = dynamics.step(state, u, dt=0.01)

    # Count sign changes (chattering indicator)
    sign_changes = count_sign_changes(control_sequence)

    # Larger boundary layer → fewer sign changes
    assert sign_changes < 50 / boundary_layer, \
        f"Excessive chattering: {sign_changes} switches with ϕ={boundary_layer}"