# Example from: docs\test_infrastructure_documentation.md
# Index: 7
# Runnable: False
# Hash: 2e81df02

@pytest.mark.full_dynamics
@pytest.mark.benchmark
def test_full_vs_simplified_dynamics():
    """Compare full and simplified dynamics models."""
    full_dynamics = FullDIPDynamics()
    simplified_dynamics = DIPDynamics()

    controller = ClassicalSMC(gains=validated_gains)

    full_trajectory = simulate_system(controller, full_dynamics, sim_time=10.0)
    simplified_trajectory = simulate_system(controller, simplified_dynamics, sim_time=10.0)

    # Trajectories should be similar for small-angle approximation regime
    angle_error = compute_trajectory_difference(full_trajectory, simplified_trajectory)
    assert max(angle_error) < 0.05  # Within 3 degrees