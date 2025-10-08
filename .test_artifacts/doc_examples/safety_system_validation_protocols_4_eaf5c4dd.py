# Example from: docs\safety_system_validation_protocols.md
# Index: 4
# Runnable: False
# Hash: eaf5c4dd

@hypothesis.given(
    theta1=st.floats(min_value=-π, max_value=π),
    theta2=st.floats(min_value=-π, max_value=π),
    control_gains=st.lists(st.floats(min_value=0.1, max_value=100), min_size=6, max_size=6)
)
def test_lyapunov_stability_property(theta1, theta2, control_gains):
    """Verify Lyapunov stability for all valid parameter combinations."""
    controller = ClassicalSMC(gains=control_gains)
    state = np.array([theta1, theta2, 0, 0, 0, 0])

    # Compute Lyapunov function
    V = controller.compute_lyapunov_function(state)

    # Property: V ≥ 0 for all states
    assert V >= 0

    # Property: V = 0 only at equilibrium
    if not np.allclose(state, 0):
        assert V > 0