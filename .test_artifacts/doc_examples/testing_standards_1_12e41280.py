# Example from: docs\testing\standards\testing_standards.md
# Index: 1
# Runnable: False
# Hash: 12e41280

def test_classical_smc_control_computation_valid_input():
    """Test classical SMC control computation with valid state input."""
    # Setup
    controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5], max_force=100.0)
    state = np.array([0.1, 0.05, 0.02, 0.0, 0.0, 0.0])

    # Execute
    control = controller.compute_control(state, 0.0, {})

    # Verify
    assert isinstance(control, float)
    assert -100.0 <= control <= 100.0  # Within actuator limits
    assert not np.isnan(control) and not np.isinf(control)

def test_classical_smc_invalid_state_dimension():
    """Test classical SMC raises appropriate error for invalid state dimension."""
    controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])
    invalid_state = np.array([0.1, 0.05])  # Only 2 elements instead of 6

    with pytest.raises(ValueError, match="State vector must have 6 elements"):
        controller.compute_control(invalid_state, 0.0, {})