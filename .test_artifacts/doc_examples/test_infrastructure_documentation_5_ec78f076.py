# Example from: docs\test_infrastructure_documentation.md
# Index: 5
# Runnable: False
# Hash: ec78f076

# example-metadata:
# runnable: false

@pytest.mark.convergence
@pytest.mark.property_based
def test_sliding_mode_reachability(initial_state):
    """Test finite-time convergence to sliding surface."""
    controller = SuperTwistingSMC(gains=[15, 10])
    dynamics = DIPDynamics()

    t_reach = estimate_reaching_time(controller, dynamics, initial_state)
    trajectory = simulate_reaching_phase(controller, dynamics, initial_state, t_reach * 1.5)

    # Verify sliding surface is reached within predicted time
    surface_values = [controller.compute_sliding_surface(state) for state in trajectory]
    assert min(abs(s) for s in surface_values[-10:]) < 0.01  # Within ε-band