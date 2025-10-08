# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 12
# Runnable: False
# Hash: 9ac449c8

def test_numerical_stability():
    """Test controller numerical stability under edge cases."""
    controller = create_test_controller()

    # Test with very small values (underflow risk)
    tiny_state = np.array([1e-15, 1e-15, 1e-15, 1e-15, 1e-15, 1e-15])
    result = controller.compute_control(tiny_state, (), {})
    assert np.isfinite(result.u), "Should handle tiny values"

    # Test with zeros
    zero_state = np.zeros(6)
    result = controller.compute_control(zero_state, (), {})
    assert np.isfinite(result.u), "Should handle zero state"

    # Test with mixed magnitudes (conditioning risk)
    mixed_state = np.array([1e-6, 1e3, 1e-6, 1e3, 1e-6, 1e3])
    result = controller.compute_control(mixed_state, (), {})
    assert np.isfinite(result.u), "Should handle mixed magnitudes"