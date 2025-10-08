# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 3
# Runnable: False
# Hash: bfc406f6

def test_state_vector_validation():
    """Test proper handling of state vectors with correct dimensions."""
    controller = create_test_controller()

    # Valid 6D state: [x, theta1, theta2, xdot, dtheta1, dtheta2]
    valid_state = np.array([0.1, 0.05, -0.03, 0.0, 0.1, -0.05])

    result = controller.compute_control(
        state=valid_state,
        state_vars=(),
        history={}
    )

    assert isinstance(result.u, (float, np.floating))
    assert np.isfinite(result.u)

    # Invalid state dimensions should be caught early
    invalid_states = [
        np.array([0.1, 0.05, 0.0]),  # Too short
        np.array([0.1, 0.05, -0.03, 0.0, 0.1, -0.05, 0.0]),  # Too long
    ]

    for invalid_state in invalid_states:
        with pytest.raises((ValueError, IndexError)):
            controller.compute_control(
                state=invalid_state,
                state_vars=(),
                history={}
            )