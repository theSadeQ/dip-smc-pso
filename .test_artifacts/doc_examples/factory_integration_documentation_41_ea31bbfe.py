# Example from: docs\factory_integration_documentation.md
# Index: 41
# Runnable: False
# Hash: ea31bbfe

# Validate control theory properties
def test_controller_stability():
    controller = create_controller('classical_smc', gains=[10, 8, 15, 12, 50, 5])

    # Test Lyapunov stability
    state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    control_output = controller.compute_control(state, 0.0, {})

    # Verify control output bounds
    assert abs(control_output.u) <= controller.max_force

# Validate PSO optimization compatibility
def test_pso_optimization_compatibility():
    factory = create_pso_controller_factory(SMCType.CLASSICAL)

    # Test gain bounds
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
    assert len(lower_bounds) == factory.n_gains
    assert all(l < u for l, u in zip(lower_bounds, upper_bounds))

    # Test gain validation
    wrapper = factory([10, 8, 15, 12, 50, 5])
    test_gains = np.array([[10, 8, 15, 12, 50, 5], [0, 0, 0, 0, 0, 0]])
    validity = wrapper.validate_gains(test_gains)
    assert validity[0] == True   # Valid gains
    assert validity[1] == False  # Invalid gains (zeros)