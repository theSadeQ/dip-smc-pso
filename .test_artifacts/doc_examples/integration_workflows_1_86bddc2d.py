# Example from: docs\testing\guides\integration_workflows.md
# Index: 1
# Runnable: False
# Hash: 86bddc2d

def test_closed_loop_integration():
    """Test full closed-loop system"""
    controller = ClassicalSMC(gains=[77.62, 44.45, 17.31, 14.25, 18.66, 9.76])
    dynamics = FullDynamics()
    initial_state = [0.2, -0.1, 0.0, 0.0]

    # Simulate closed loop
    trajectory = simulate(
        controller=controller,
        dynamics=dynamics,
        initial_state=initial_state,
        duration=5.0,
        dt=0.01
    )

    # Integration assertions
    final_state = trajectory[-1]
    assert np.linalg.norm(final_state) < 0.05, "Did not stabilize"

    # Check no integration errors
    assert len(trajectory) == 500, "Unexpected trajectory length"
    assert all(is_valid_state(s) for s in trajectory), "Invalid states generated"