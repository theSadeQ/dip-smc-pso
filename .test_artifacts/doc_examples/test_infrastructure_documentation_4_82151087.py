# Example from: docs\test_infrastructure_documentation.md
# Index: 4
# Runnable: True
# Hash: 82151087

@pytest.mark.numerical_stability
def test_rk45_energy_conservation():
    """Test energy conservation in RK45 integration with zero friction."""
    dynamics = DIPDynamics(friction_params={"cart": 0.0, "joint1": 0.0, "joint2": 0.0})
    initial_energy = compute_total_energy(initial_state, dynamics)
    final_state = integrate_system(dynamics, initial_state, sim_time=10.0, method="RK45")
    final_energy = compute_total_energy(final_state, dynamics)
    assert abs(final_energy - initial_energy) / initial_energy < 1e-6