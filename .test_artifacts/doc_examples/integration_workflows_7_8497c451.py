# Example from: docs\testing\guides\integration_workflows.md
# Index: 7
# Runnable: False
# Hash: 8497c451

def test_disturbance_rejection_integration():
    """Integration test with external disturbances"""
    state = [0, 0, 0, 0]

    for t in np.arange(0, 5.0, 0.01):
        # Apply disturbance at t=2.5s
        disturbance = 0.5 if 2.5 <= t < 2.6 else 0

        u = controller.compute_control(state)
        u_total = u + disturbance

        state = dynamics.step(state, u_total, dt=0.01)

    # Should recover despite disturbance
    assert np.linalg.norm(state) < 0.1, "Failed to reject disturbance"