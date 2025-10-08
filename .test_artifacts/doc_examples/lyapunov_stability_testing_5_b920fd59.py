# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 5
# Runnable: False
# Hash: b920fd59

@given(
    state=valid_states(),
    disturbance=st.floats(min_value=-0.5, max_value=0.5)
)
def test_ISS_property(state, disturbance):
    """Input-to-State Stability (ISS)"""
    # Simulate with disturbance
    u = controller.compute_control(state)
    u_disturbed = u + disturbance

    state_next = dynamics.step(state, u_disturbed, dt=0.01)

    # ISS condition: ||x(t)|| ≤ β(||x(0)||, t) + γ(||d||)
    x_norm = np.linalg.norm(state_next)
    d_norm = abs(disturbance)

    # Simplified check: state bounded by disturbance magnitude
    assert x_norm <= 10 * d_norm + 1.0, \
        f"Not ISS: ||x||={x_norm} vs ||d||={d_norm}"